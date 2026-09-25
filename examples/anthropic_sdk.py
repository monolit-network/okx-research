"""Drop-in via the official Anthropic SDK (wire format is Messages-compatible).

Usage:  X_API_KEY=...  python3 anthropic_sdk.py
Requires:  pip install anthropic
"""
import os
from anthropic import Anthropic

client = Anthropic(
    base_url="https://mcp.monolit.network/okx",
    api_key=os.environ["X_API_KEY"],
)

msg = client.messages.create(
    model="okx-research",
    max_tokens=4096,
    extra_body={"max_cost_usd": 0.5},
    messages=[{
        "role": "user",
        "content": 'Top traded tokens on X Layer this week - anything unusual?',
    }],
)
print(msg.content[0].text)
