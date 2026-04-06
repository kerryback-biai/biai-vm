"""Lightweight Anthropic API proxy that logs per-user usage.

Sits between Claude Code and the Anthropic API on the AI+Code Lab VM.
Each user's ANTHROPIC_BASE_URL points to http://localhost:8080/proxy/{username},
so the proxy can attribute API calls to individual users and log token/cost data
to the shared meridian_usage_log table.
"""
import json
import logging
import os
import time
from contextlib import asynccontextmanager

import httpx
import psycopg2
import psycopg2.extras
from fastapi import FastAPI, Request
from fastapi.responses import Response, StreamingResponse

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("biai-proxy")

ANTHROPIC_BASE = "https://api.anthropic.com"
DATABASE_URL = os.environ.get("DATABASE_URL", "")

# Per-million-token pricing (USD)
MODEL_PRICING = {
    "claude-sonnet-4":   {"input": 3.0,  "output": 15.0, "cache_read": 0.30},
    "claude-opus-4":     {"input": 15.0, "output": 75.0, "cache_read": 1.50},
    "claude-haiku-3.5":  {"input": 0.80, "output": 4.0,  "cache_read": 0.08},
}
DEFAULT_PRICING = {"input": 3.0, "output": 15.0, "cache_read": 0.30}

# User ID cache: username -> (user_id, timestamp)
_user_cache: dict[str, tuple[int | None, float]] = {}
CACHE_TTL = 300


def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    return conn


def resolve_user_id(username: str) -> int | None:
    now = time.time()
    cached = _user_cache.get(username)
    if cached and now - cached[1] < CACHE_TTL:
        return cached[0]
    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id FROM users WHERE username = %s AND is_active = TRUE",
                (username,),
            )
            row = cur.fetchone()
            user_id = row[0] if row else None
        conn.close()
    except Exception as e:
        log.error("DB lookup failed for %s: %s", username, e)
        user_id = None
    _user_cache[username] = (user_id, now)
    return user_id


def get_pricing(model: str) -> dict:
    for prefix, pricing in MODEL_PRICING.items():
        if model.startswith(prefix):
            return pricing
    return DEFAULT_PRICING


def calc_cost_cents(model: str, input_tok: int, output_tok: int, cache_tok: int) -> float:
    p = get_pricing(model)
    return (
        input_tok * p["input"]
        + output_tok * p["output"]
        + cache_tok * p["cache_read"]
    ) / 10_000  # $/MTok -> cents/tok: divide by 1M, multiply by 100 = /10_000


def log_usage(user_id: int, model: str, input_tok: int, output_tok: int,
              cache_tok: int, tool_calls: int) -> None:
    cost = calc_cost_cents(model, input_tok, output_tok, cache_tok)
    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO meridian_usage_log
                   (user_id, input_tokens, output_tokens, cache_read_tokens,
                    model, cost_cents, tool_calls, request_type)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (user_id, input_tok, output_tok, cache_tok,
                 model, cost, tool_calls, "ai-lab"),
            )
        conn.close()
        log.info("Logged: user=%s model=%s in=%d out=%d cache=%d cost=%.4f¢",
                 user_id, model, input_tok, output_tok, cache_tok, cost)
    except Exception as e:
        log.error("Failed to log usage: %s", e)


http_client: httpx.AsyncClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global http_client
    http_client = httpx.AsyncClient(timeout=httpx.Timeout(300, connect=10))
    yield
    await http_client.aclose()


app = FastAPI(title="BIAI API Proxy", lifespan=lifespan)


@app.api_route("/proxy/{username}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(username: str, path: str, request: Request):
    user_id = resolve_user_id(username)
    if user_id is None:
        return Response(
            content=json.dumps({
                "type": "error",
                "error": {"type": "authentication_error",
                          "message": f"Unknown user: {username}"}
            }),
            status_code=401,
            media_type="application/json",
        )

    # Read request body
    body = await request.body()

    # Detect streaming and model from request body
    is_streaming = False
    model = "unknown"
    if body:
        try:
            req_json = json.loads(body)
            is_streaming = req_json.get("stream", False)
            model = req_json.get("model", "unknown")
        except (json.JSONDecodeError, AttributeError):
            pass

    # Build upstream headers (forward everything relevant)
    fwd_headers = {}
    for key in ("x-api-key", "anthropic-version", "content-type",
                "anthropic-beta", "anthropic-dangerous-direct-browser-access"):
        val = request.headers.get(key)
        if val:
            fwd_headers[key] = val

    target_url = f"{ANTHROPIC_BASE}/{path}"

    if is_streaming:
        return await handle_streaming(user_id, model, target_url, fwd_headers, body)
    else:
        return await handle_non_streaming(user_id, model, target_url, fwd_headers, body,
                                          request.method)


async def handle_streaming(user_id: int, model: str, url: str,
                           headers: dict, body: bytes) -> StreamingResponse:
    upstream = await http_client.send(
        http_client.build_request("POST", url, headers=headers, content=body),
        stream=True,
    )

    # State for accumulating usage from SSE events
    state = {"input": 0, "output": 0, "cache": 0, "tools": 0, "buffer": ""}

    async def stream_with_logging():
        try:
            async for chunk in upstream.aiter_bytes():
                yield chunk
                # Accumulate and parse SSE events
                state["buffer"] += chunk.decode("utf-8", errors="replace")
                while "\n\n" in state["buffer"]:
                    event_str, state["buffer"] = state["buffer"].split("\n\n", 1)
                    parse_sse_event(event_str, state)
        except Exception as e:
            log.error("Stream error: %s", e)
        finally:
            await upstream.aclose()
            # Log accumulated usage
            if state["input"] or state["output"]:
                log_usage(user_id, model, state["input"], state["output"],
                          state["cache"], state["tools"])

    resp_headers = dict(upstream.headers)
    return StreamingResponse(
        stream_with_logging(),
        status_code=upstream.status_code,
        media_type=resp_headers.get("content-type", "text/event-stream"),
        headers={k: v for k, v in resp_headers.items()
                 if k.lower() not in ("content-length", "transfer-encoding",
                                      "content-encoding", "connection")},
    )


async def handle_non_streaming(user_id: int, model: str, url: str,
                                headers: dict, body: bytes, method: str) -> Response:
    resp = await http_client.request(method, url, headers=headers, content=body)

    # Extract usage from response body
    if resp.status_code == 200 and body:
        try:
            resp_json = resp.json()
            usage = resp_json.get("usage", {})
            input_tok = usage.get("input_tokens", 0)
            output_tok = usage.get("output_tokens", 0)
            cache_tok = usage.get("cache_read_input_tokens", 0)
            # Count tool use blocks
            tool_calls = sum(
                1 for c in resp_json.get("content", [])
                if c.get("type") == "tool_use"
            )
            if input_tok or output_tok:
                log_usage(user_id, model, input_tok, output_tok, cache_tok, tool_calls)
        except Exception as e:
            log.error("Failed to parse response: %s", e)

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        media_type=resp.headers.get("content-type"),
    )


def parse_sse_event(event_str: str, state: dict) -> None:
    """Parse a single SSE event and update usage state."""
    event_type = ""
    data_str = ""
    for line in event_str.split("\n"):
        if line.startswith("event: "):
            event_type = line[7:].strip()
        elif line.startswith("data: "):
            data_str = line[6:]

    if not data_str:
        return

    try:
        data = json.loads(data_str)
    except json.JSONDecodeError:
        return

    if event_type == "message_start":
        usage = data.get("message", {}).get("usage", {})
        state["input"] += usage.get("input_tokens", 0)
        state["cache"] += usage.get("cache_read_input_tokens", 0)
    elif event_type == "message_delta":
        usage = data.get("usage", {})
        state["output"] += usage.get("output_tokens", 0)
    elif event_type == "content_block_start":
        if data.get("content_block", {}).get("type") == "tool_use":
            state["tools"] += 1
