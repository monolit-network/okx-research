"""Deep research in the background: launch, poll, print.

Usage:  X_API_KEY=...  python3 background_job.py "your deep question"
"""
import json, os, sys, time, urllib.request

BASE = "https://mcp.monolit.network/okx"
KEY = os.environ["X_API_KEY"]
HDRS = {"x-api-key": KEY, "content-type": "application/json"}

def call(method: str, path: str, body: dict | None = None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, headers=HDRS, method=method)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

question = sys.argv[1] if len(sys.argv) > 1 else \
    'Who are the most profitable traders of "OKB" pairs on X Layer this month? Deep dive.'

job = call("POST", "/v1/messages", {
    "model": "okx-research",
    "background": True,
    "max_cost_usd": 1.0,
    "messages": [{"role": "user", "content": question}],
})
job_id = job["id"]
print("job:", job_id)

while True:
    time.sleep(15)
    res = call("GET", f"/v1/jobs/{job_id}")
    status = res.get("status")
    print("status:", status)
    if status == "completed":
        print("\n" + res["content"][0]["text"])
        u = res.get("usage", {})
        print("\ncost_usd:", u.get("cost_usd"), "| charged credits:", u.get("charged_credits"))
        break
    if status in ("failed", "cancelled"):
        print(res)
        break
