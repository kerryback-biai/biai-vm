"""Generate nginx config that routes /<username>/ to each student's code-server.

Each code-server instance binds to 127.0.0.1:0 (random port).
We read the actual port from code-server's config after it starts.
"""
import subprocess
import json
import os
import re

def get_code_server_port(username):
    """Get the port code-server is listening on for a given user."""
    try:
        # Get the main PID of the code-server service
        result = subprocess.run(
            ["systemctl", "show", f"code-server@{username}", "--property=MainPID"],
            capture_output=True, text=True
        )
        pid = result.stdout.strip().split("=")[1]
        if pid == "0":
            return None
        # Search all listening sockets for any process in this service's cgroup
        result = subprocess.run(
            ["ss", "-tlnp"],
            capture_output=True, text=True
        )
        # Look for the main pid or any child pid
        cgroup_pids = subprocess.run(
            ["bash", "-c", f"cat /proc/{pid}/task/*/children 2>/dev/null; echo {pid}"],
            capture_output=True, text=True
        ).stdout.split()
        for line in result.stdout.splitlines():
            for cpid in cgroup_pids:
                if f"pid={cpid}" in line:
                    match = re.search(r"127\.0\.0\.1:(\d+)", line)
                    if match:
                        return int(match.group(1))
    except Exception:
        pass
    return None


def get_students():
    """Get list of students from the database."""
    result = subprocess.run(
        ["python3", "/opt/biai-vm/fetch-students.py"],
        capture_output=True, text=True,
        env={**os.environ}
    )
    students = []
    for line in result.stdout.strip().splitlines():
        if ":" in line:
            username = line.split(":")[0]
            students.append(username)
    return students


def generate_config(students):
    """Generate nginx site config."""
    locations = []
    for username in students:
        port = get_code_server_port(username)
        if not port:
            print(f"  WARNING: no port found for {username}, skipping")
            continue
        print(f"  {username} -> 127.0.0.1:{port}")
        locations.append(f"""
    # {username}
    location /{username}/ {{
        proxy_pass http://127.0.0.1:{port}/;
        proxy_set_header Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection upgrade;
        proxy_set_header Accept-Encoding gzip;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_http_version 1.1;
    }}""")

    config = f"""server {{
    listen 80;
    server_name vm.kerryback.com;

    # Landing page
    location = / {{
        default_type text/html;
        return 200 '<html><head><title>BI to AI Workshop</title></head><body>
<h1>BI to AI: Claude Code with Python Lab</h1>
<p>Access your workspace at <code>https://vm.kerryback.com/your-username/</code></p>
</body></html>';
    }}
{"".join(locations)}
}}
"""
    return config


if __name__ == "__main__":
    # Source environment
    env_file = "/etc/biai.env"
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, _, value = line.partition("=")
                    os.environ[key] = value

    students = get_students()
    print(f"Generating nginx config for {len(students)} students...")
    config = generate_config(students)

    with open("/etc/nginx/sites-available/biai-vm", "w") as f:
        f.write(config)

    # Enable site
    os.makedirs("/etc/nginx/sites-enabled", exist_ok=True)
    try:
        os.symlink("/etc/nginx/sites-available/biai-vm",
                    "/etc/nginx/sites-enabled/biai-vm")
    except FileExistsError:
        pass

    # Remove default site
    try:
        os.remove("/etc/nginx/sites-enabled/default")
    except FileNotFoundError:
        pass

    print("Nginx config written to /etc/nginx/sites-available/biai-vm")
