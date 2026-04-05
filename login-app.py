"""Login page with admin panel for user management."""
import grp
import subprocess
from fastapi import FastAPI, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional
import secrets
import time

app = FastAPI()

# Simple session store: token -> (username, expiry)
sessions: dict[str, tuple[str, float]] = {}
SESSION_HOURS = 12
DEFAULT_PASSWORD = "execed@rice"

BANNER_STYLE = """
body { font-family: system-ui, sans-serif; margin: 0; padding: 0; background: #1e1e2e; color: #cdd6f4; }
.banner { text-align: center; padding: 24px 0 8px; position: relative; }
.banner h1 { font-size: 1.5em; margin: 0; color: #89b4fa; }
.banner p { margin: 4px 0; font-size: 0.95em; color: #a6adc8; }
.card { max-width: 420px; margin: 40px auto; background: #313244; border-radius: 12px; padding: 32px; box-shadow: 0 4px 24px rgba(0,0,0,0.3); }
.card h2 { margin: 0 0 20px; font-size: 1.1em; text-align: center; color: #cdd6f4; font-weight: normal; }
label { display: block; margin-bottom: 4px; font-size: 0.85em; color: #a6adc8; }
input { width: 100%; padding: 10px; margin-bottom: 16px; border: 1px solid #45475a; border-radius: 6px; background: #1e1e2e; color: #cdd6f4; font-size: 1em; box-sizing: border-box; }
input:focus { outline: none; border-color: #89b4fa; }
button, .btn { padding: 10px; border: none; border-radius: 6px; background: #89b4fa; color: #1e1e2e; font-size: 1em; font-weight: 600; cursor: pointer; }
button:hover, .btn:hover { background: #74c7ec; }
.btn-full { width: 100%; }
.error { color: #f38ba8; text-align: center; margin-bottom: 12px; font-size: 0.9em; }
.success { color: #a6e3a1; text-align: center; margin-bottom: 12px; font-size: 0.9em; }
.instructions { font-size: 0.9em; color: #a6adc8; line-height: 1.6; margin-top: 16px; }
.about-btn { position: absolute; bottom: 5px; right: 20px; background: rgba(255,255,255,0.1); border: none; color: #a6adc8; width: 28px; height: 28px; border-radius: 50%; cursor: pointer; font-size: 14px; display: flex; align-items: center; justify-content: center; transition: all 0.2s; }
.about-btn:hover { background: rgba(255,255,255,0.2); color: #cdd6f4; transform: scale(1.1); }
.about-tooltip { position: absolute; bottom: 40px; right: 0; background: #45475a; color: #cdd6f4; padding: 10px 14px; border-radius: 8px; font-size: 0.8em; line-height: 1.5; white-space: nowrap; opacity: 0; visibility: hidden; transition: opacity 0.2s, visibility 0.2s; pointer-events: none; box-shadow: 0 2px 12px rgba(0,0,0,0.3); }
.about-btn:hover .about-tooltip { opacity: 1; visibility: visible; pointer-events: auto; }
.about-tooltip::before { content: ''; position: absolute; bottom: -4px; right: 12px; width: 8px; height: 8px; background: #45475a; transform: rotate(45deg); }
.admin-link { position: absolute; bottom: 5px; left: 20px; background: rgba(255,255,255,0.1); border: none; color: #a6adc8; width: 28px; height: 28px; border-radius: 50%; cursor: pointer; font-size: 16px; display: flex; align-items: center; justify-content: center; transition: all 0.2s; text-decoration: none; }
.admin-link:hover { background: rgba(255,255,255,0.2); color: #cdd6f4; transform: scale(1.1); }
table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 0.9em; }
th, td { padding: 8px 12px; text-align: left; border-bottom: 1px solid #45475a; }
th { color: #a6adc8; font-weight: normal; font-size: 0.85em; }
td { color: #cdd6f4; }
.btn-sm { padding: 4px 10px; font-size: 0.8em; border-radius: 4px; }
.btn-danger { background: #f38ba8; }
.btn-danger:hover { background: #eba0ac; }
.admin-card { max-width: 560px; }
.add-form { display: flex; gap: 8px; align-items: end; }
.add-form input { margin-bottom: 0; flex: 1; }
.add-form button { white-space: nowrap; }
"""

ABOUT_WIDGET = """<div class="about-btn">&#9432;<div class="about-tooltip">Developed by Kerry Back,<br>J. Howard Creekmore Professor of Finance<br>and Professor of Economics,<br>Rice University</div></div>"""

LOGIN_PAGE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI+Code Lab</title><style>{style}</style></head>
<body>
<div class="banner">
  <h1>AI+Code Lab</h1>
  <p>Rice Business Executive Education</p>
  {about}
</div>
<div class="card">
  <h2>Log in to your workspace</h2>
  <div class="instructions">
    <p>After logging in, two new tabs will open: one with a File Explorer
    view and one with a terminal in which you can open Claude Code.</p>
  </div>
  {error}
  <form method="post" action="/login" style="margin-top:20px">
    <label for="username">Username</label>
    <input type="text" id="username" name="username" autofocus required>
    <label for="password">Password</label>
    <input type="password" id="password" name="password" required>
    <button type="submit" class="btn-full">Log In</button>
  </form>
</div>
</body></html>"""

LAUNCH_PAGE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>AI+Code Lab</title>
<style>{style}
.card {{ text-align: center; max-width: 480px; }}
.card a {{ color: #89b4fa; text-decoration: none; display: inline-block; margin: 8px 12px; font-size: 1em; }}
.card a:hover {{ text-decoration: underline; }}
</style>
<script>
window.onload = function() {{
    window.open("/{username}/", "_blank");
    window.open("/{username}/files/", "_blank");
}};
</script>
</head>
<body>
<div class="banner">
  <h1>AI+Code Lab</h1>
  <p>Rice Business Executive Education</p>
  {admin_icon}
  {about}
</div>
<div class="card">
  <h2>Welcome, {username}</h2>
  <p>Two tabs should have opened:</p>
  <p>
    <a href="/{username}/" target="_blank">Terminal</a>
    <a href="/{username}/files/" target="_blank">File Explorer</a>
  </p>
  <p style="font-size:0.85em;color:#a6adc8;margin-top:16px">
    If tabs were blocked by your browser, click the links above.
  </p>
</div>
</body></html>"""

ADMIN_PAGE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI+Code Lab — Admin</title><style>{style}</style></head>
<body>
<div class="banner">
  <h1>AI+Code Lab</h1>
  <p>Rice Business Executive Education</p>
  {about}
</div>
<div class="card admin-card">
  <h2>&#9881; User Management</h2>
  {message}
  <form method="post" action="/admin/add" style="margin-bottom: 20px;">
    <label>Add user (password will be set to <code style="color:#89b4fa">{default_password}</code>)</label>
    <div class="add-form">
      <input type="text" name="new_username" placeholder="firstname_lastname" required>
      <button type="submit" class="btn">Add</button>
    </div>
  </form>
  <table>
    <tr><th>Username</th><th>Admin</th><th></th></tr>
    {user_rows}
  </table>
  <p style="text-align:center;margin-top:20px">
    <a href="/" style="color:#89b4fa;text-decoration:none">&larr; Back to login</a>
  </p>
</div>
</body></html>"""


def check_credentials(username: str, password: str) -> bool:
    """Verify credentials against Linux PAM via su."""
    try:
        result = subprocess.run(
            ["su", "-c", "true", username],
            input=password + "\n",
            capture_output=True, text=True, timeout=5,
        )
        return result.returncode == 0
    except Exception:
        return False


def is_admin(username: str) -> bool:
    """Check if user is in the sudo group."""
    try:
        sudo_group = grp.getgrnam("sudo")
        return username in sudo_group.gr_mem
    except KeyError:
        return False


def get_session_user(session: Optional[str]) -> Optional[str]:
    """Return username if session is valid, else None."""
    if not session or session not in sessions:
        return None
    username, expiry = sessions[session]
    if time.time() > expiry:
        del sessions[session]
        return None
    return username


def list_workshop_users() -> list[dict]:
    """List users that have a ttyd service (workshop users)."""
    result = subprocess.run(
        ["bash", "-c", "cat /etc/biai-ports 2>/dev/null"],
        capture_output=True, text=True,
    )
    users = []
    for line in result.stdout.strip().splitlines():
        if ":" in line:
            username = line.split(":")[0]
            users.append({"username": username, "is_admin": is_admin(username)})
    return users


def add_user(username: str) -> tuple[bool, str]:
    """Create a Linux user and set up their workspace."""
    result = subprocess.run(
        ["bash", "-c", f"""
            useradd -m -s /bin/bash -N '{username}' 2>&1 && \
            echo '{username}:{DEFAULT_PASSWORD}' | chpasswd 2>&1 && \
            bash /opt/biai-vm/setup-user.sh '{username}' 2>&1
        """],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode == 0:
        return True, f"User '{username}' created."
    return False, f"Failed to create '{username}': {result.stdout} {result.stderr}"


def delete_user(username: str) -> tuple[bool, str]:
    """Delete a Linux user and their services."""
    result = subprocess.run(
        ["bash", "-c", f"""
            systemctl stop ttyd-{username} filebrowser-{username} 2>/dev/null
            systemctl disable ttyd-{username} filebrowser-{username} 2>/dev/null
            rm -f /etc/systemd/system/ttyd-{username}.service /etc/systemd/system/filebrowser-{username}.service
            systemctl daemon-reload
            userdel -r '{username}' 2>&1
            sed -i '/^{username}:/d' /etc/biai-ports
            bash /opt/biai-vm/generate-nginx.sh 2>&1
        """],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode == 0:
        return True, f"User '{username}' deleted."
    return False, f"Failed to delete '{username}': {result.stdout} {result.stderr}"


def render_admin(message: str = "") -> str:
    users = list_workshop_users()
    rows = ""
    for u in users:
        admin_badge = "&#9989;" if u["is_admin"] else ""
        delete_btn = f"""<form method="post" action="/admin/delete" style="display:inline;margin:0">
            <input type="hidden" name="del_username" value="{u['username']}">
            <button type="submit" class="btn-sm btn-danger"
                onclick="return confirm('Delete {u['username']}?')">Delete</button>
        </form>"""
        rows += f"<tr><td>{u['username']}</td><td>{admin_badge}</td><td>{delete_btn}</td></tr>\n"
    return ADMIN_PAGE.format(
        style=BANNER_STYLE, about=ABOUT_WIDGET, message=message,
        user_rows=rows, default_password=DEFAULT_PASSWORD,
    )


@app.get("/", response_class=HTMLResponse)
def login_form():
    return LOGIN_PAGE.format(style=BANNER_STYLE, about=ABOUT_WIDGET, error="")


@app.post("/login", response_class=HTMLResponse)
def login(username: str = Form(...), password: str = Form(...)):
    if check_credentials(username, password):
        token = secrets.token_urlsafe(32)
        sessions[token] = (username, time.time() + SESSION_HOURS * 3600)
        admin_icon = ""
        if is_admin(username):
            admin_icon = '<a href="/admin" class="admin-link" title="Admin">&#9881;</a>'
        response = HTMLResponse(
            LAUNCH_PAGE.format(
                style=BANNER_STYLE, about=ABOUT_WIDGET,
                username=username, admin_icon=admin_icon,
            )
        )
        response.set_cookie("session", token, max_age=SESSION_HOURS * 3600)
        return response
    return LOGIN_PAGE.format(
        style=BANNER_STYLE, about=ABOUT_WIDGET,
        error='<p class="error">Invalid username or password.</p>',
    )


@app.get("/admin", response_class=HTMLResponse)
def admin_page(session: Optional[str] = Cookie(None)):
    username = get_session_user(session)
    if not username or not is_admin(username):
        return RedirectResponse("/", status_code=303)
    return render_admin()


@app.post("/admin/add", response_class=HTMLResponse)
def admin_add_user(new_username: str = Form(...), session: Optional[str] = Cookie(None)):
    username = get_session_user(session)
    if not username or not is_admin(username):
        return RedirectResponse("/", status_code=303)
    new_username = new_username.strip().lower().replace(" ", "_")
    if not new_username:
        return render_admin('<p class="error">Username cannot be empty.</p>')
    ok, msg = add_user(new_username)
    cls = "success" if ok else "error"
    return render_admin(f'<p class="{cls}">{msg}</p>')


@app.post("/admin/delete", response_class=HTMLResponse)
def admin_delete_user(del_username: str = Form(...), session: Optional[str] = Cookie(None)):
    username = get_session_user(session)
    if not username or not is_admin(username):
        return RedirectResponse("/", status_code=303)
    if del_username == username:
        return render_admin('<p class="error">You cannot delete yourself.</p>')
    ok, msg = delete_user(del_username)
    cls = "success" if ok else "error"
    return render_admin(f'<p class="{cls}">{msg}</p>')
