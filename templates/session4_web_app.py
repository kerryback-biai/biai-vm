"""
Exercise 3: Add a Web Interface
================================
Turn your agent into a web app using FastAPI.

This starter gives you the web framework. Your job:
  1. Copy your working agent loop from Exercise 2 into the chat() function
  2. Make it stream responses back to the browser

When done, run with:
  python session4_web_app.py

Then open http://localhost:8000 in your browser.

Hint: Ask Claude Code to help you! Say:
  "Help me turn my ex2 agent into a FastAPI web app with streaming"
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
import uvicorn

app = FastAPI()

# --- The chat page (already done for you) ---
HTML = """
<!DOCTYPE html>
<html>
<head><title>My Data Agent</title>
<style>
  body { font-family: sans-serif; max-width: 700px; margin: 2rem auto; }
  #messages { border: 1px solid #ddd; padding: 1rem; height: 400px; overflow-y: auto; margin-bottom: 1rem; }
  .user { color: #2c3e50; font-weight: bold; }
  .agent { color: #27ae60; }
  form { display: flex; gap: 0.5rem; }
  input { flex: 1; padding: 0.5rem; }
  button { padding: 0.5rem 1rem; }
</style>
</head>
<body>
  <h2>XYZ Corp Data Agent</h2>
  <div id="messages"></div>
  <form onsubmit="send(event)">
    <input id="input" placeholder="Ask a question..." autofocus>
    <button>Send</button>
  </form>
  <script>
    async function send(e) {
      e.preventDefault();
      const input = document.getElementById('input');
      const msg = input.value.trim();
      if (!msg) return;
      input.value = '';
      const messages = document.getElementById('messages');
      messages.innerHTML += `<p class="user">You: ${msg}</p>`;
      messages.innerHTML += `<p class="agent" id="current">Agent: </p>`;
      const res = await fetch('/chat?q=' + encodeURIComponent(msg));
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      while (true) {
        const {done, value} = await reader.read();
        if (done) break;
        document.getElementById('current').textContent += decoder.decode(value);
      }
      document.getElementById('current').removeAttribute('id');
      messages.scrollTop = messages.scrollHeight;
    }
  </script>
</body>
</html>
"""

@app.get("/")
def home():
    return HTMLResponse(HTML)


@app.get("/chat")
def chat(q: str):
    """
    TODO: Implement streaming chat endpoint.

    This should:
      1. Take the question from the 'q' parameter
      2. Run your agent loop (from Exercise 2)
      3. Stream the text response back

    Hint: Use StreamingResponse with a generator function.
    The generator should yield text chunks as Claude produces them.

    Simple version (no streaming — just return the full answer):
      return {"answer": "your answer here"}

    Streaming version:
      def generate():
          yield "chunk 1"
          yield "chunk 2"
      return StreamingResponse(generate(), media_type="text/plain")
    """
    # TODO: Replace this placeholder
    def placeholder():
        yield "This endpoint isn't implemented yet. "
        yield "Copy your agent loop from Exercise 2 and make it stream!"

    return StreamingResponse(placeholder(), media_type="text/plain")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
