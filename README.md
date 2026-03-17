# moltbook-sentiment MCP Server

> Real-time crypto market sentiment from 2M+ AI agent discussions — powered by Llama 3.1 8B

[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-blue)](https://modelcontextprotocol.io)
[![Free Tier](https://img.shields.io/badge/Free-Tier-green)](http://187.124.93.57:8080)

## What it does

Provides your AI assistant with live crypto market signals sourced from **Moltbook** — a platform where 2M+ AI agents discuss, analyze, and debate crypto markets.

**Why agent data?** Unlike human social media sentiment, AI agents post structured analysis with defined objectives. The signal is cleaner.

## Tools

| Tool | Description |
|------|-------------|
| `get_crypto_sentiment` | Overall market signal: bullish/bearish/neutral, score (-1 to +1), post breakdown |
| `get_top_signals` | Top 5 bullish and top 5 bearish posts by upvotes right now |

## Live Example

```bash
curl -X POST http://187.124.93.57:8081/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_crypto_sentiment","arguments":{}}}'
```

**Response:**
```json
{
  "signal": "neutral",
  "score": 0.13,
  "bullish": 14,
  "bearish": 10,
  "neutral": 6,
  "total_posts": 30,
  "source": "Moltbook AI agent community (2M+ agents)"
}
```

## Setup

### Claude Desktop / Cursor (HTTP mode)

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "crypto-sentiment": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "http://187.124.93.57:8081/mcp"]
    }
  }
}
```

### Direct HTTP

**MCP endpoint:** `http://187.124.93.57:8081/mcp`  
**REST API:** `http://187.124.93.57:8080`  
**Demo key:** `demo_key_12345`

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/sentiment?key=YOUR_KEY` | Current sentiment summary |
| `GET /api/v1/signals?key=YOUR_KEY` | Top bullish + bearish posts |
| `GET /api/v1/latest?key=YOUR_KEY` | Most recent analyzed posts |
| `POST /mcp` | MCP JSON-RPC endpoint |

## Pricing

| Tier | Price | Rate Limit |
|------|-------|------------|
| Free | $0 | 100 req/hour |
| Paid | $10/mo USDC on Base | 10,000 req/hour |

**Payment:** Send $10 USDC on Base network to:  
`0xAd24409F212c92a5c0Ad83AeBB47551827f164F8`  
API key auto-issued within 5 minutes.

## Architecture

- **Data source:** Moltbook AI agent community posts (hourly refresh)
- **Inference:** Llama 3.1 8B via Ollama (self-hosted, no external API costs)
- **Infrastructure:** Hostinger VPS (Ubuntu 24.04, 15GB RAM)
- **Stack:** Python 3, Flask, MCP JSON-RPC 2.0

## License

MIT
