#!/usr/bin/env python3
"""
Moltbook Sentiment MCP Server (stdio mode)
Compatible with Claude Desktop, Cursor, and any MCP client.

Usage in claude_desktop_config.json:
{
  "mcpServers": {
    "crypto-sentiment": {
      "command": "python3",
      "args": ["/path/to/server.py"],
      "env": {"API_KEY": "your_api_key_here"}
    }
  }
}
"""
import json, sys, os, requests
from datetime import datetime

API_BASE = os.environ.get("API_BASE", "http://187.124.93.57:8080")
API_KEY  = os.environ.get("API_KEY", "demo_key_12345")

TOOLS = [
    {
        "name": "get_crypto_sentiment",
        "description": "Get current crypto market sentiment from 2M+ AI agent discussions on Moltbook. Returns signal (bullish/bearish/neutral), score (-1 to +1), and post breakdown.",
        "inputSchema": {"type": "object", "properties": {"hours": {"type": "integer", "description": "Lookback hours (default 24)", "default": 24}}}
    },
    {
        "name": "get_top_signals",
        "description": "Get the top bullish and bearish crypto posts from AI agents right now, ranked by upvotes.",
        "inputSchema": {"type": "object", "properties": {}}
    }
]

def call_tool(name, args):
    try:
        if name == "get_crypto_sentiment":
            r = requests.get(f"{API_BASE}/api/v1/sentiment?key={API_KEY}", timeout=10)
            return r.json()
        elif name == "get_top_signals":
            r = requests.get(f"{API_BASE}/api/v1/signals?key={API_KEY}", timeout=10)
            return r.json()
        return {"error": f"Unknown tool: {name}"}
    except Exception as e:
        return {"error": str(e)}

def handle(req):
    method = req.get("method", "")
    rid = req.get("id")
    if method == "initialize":
        return {"jsonrpc":"2.0","id":rid,"result":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"serverInfo":{"name":"moltbook-sentiment","version":"1.0.0"}}}
    elif method == "tools/list":
        return {"jsonrpc":"2.0","id":rid,"result":{"tools":TOOLS}}
    elif method == "tools/call":
        name = req.get("params",{}).get("name")
        args = req.get("params",{}).get("arguments",{})
        result = call_tool(name, args)
        return {"jsonrpc":"2.0","id":rid,"result":{"content":[{"type":"text","text":json.dumps(result,indent=2)}]}}
    elif method in ("notifications/initialized", "ping"):
        return None
    return {"jsonrpc":"2.0","id":rid,"error":{"code":-32601,"message":"Method not found"}}

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    try:
        resp = handle(json.loads(line))
        if resp: print(json.dumps(resp), flush=True)
    except Exception as e:
        print(json.dumps({"jsonrpc":"2.0","id":None,"error":{"code":-32700,"message":str(e)}}), flush=True)
