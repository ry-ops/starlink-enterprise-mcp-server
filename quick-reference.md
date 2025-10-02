# Starlink MCP Server - Quick Reference

## Environment Variables

```bash
# Required for satellite tracking
N2YO_API_KEY=your_key_here

# Required for enterprise features  
STARLINK_CLIENT_ID=your_client_id
STARLINK_CLIENT_SECRET=your_secret
```

## Quick Commands

### Installation
```bash
# One-time setup
curl -LsSf https://astral.sh/uv/install.sh | sh
mkdir starlink-mcp-server && cd starlink-mcp-server
uv venv && source .venv/bin/activate
uv pip install -e .
cp .env.example .env
# Edit .env with your credentials
```

### Testing
```bash
# Test the server
python src/starlink_mcp_server.py

# Test specific API
python test_starlink_api.py
```

## Claude Queries Cheat Sheet

### 🆓 Free Features (Satellite Tracking)

| What You Want | Ask Claude |
|---------------|------------|
| List satellites | `Show me 10 Starlink satellites` |
| Track satellite | `Track satellite 44713 from Seattle` |
| Pass predictions | `When can I see satellites from NYC?` |
| Overhead now | `What satellites are above me at 45°N, 122°W?` |
| Statistics | `Show Starlink constellation stats` |

### 🏢 Enterprise Features (Terminal Management)

| What You Want | Ask Claude |
|---------------|------------|
| List terminals | `Show all my terminals` |
| Terminal health | `Get telemetry for terminal [id]` |
| Data usage | `Show data usage for Jan 2024` |
| Fleet overview | `Give me my account overview` |
| Check coverage | `Is service available at 45.5°N, 93.2°W?` |
| Terminal history | `Show 24h history for terminal [id]` |

### 🔄 Combined Queries

```
Show terminals with poor signal + satellites overhead at those locations

List my top 5 data users + their service line details  

Check all terminals + show which need attention

Overview of fleet + constellation statistics
```

## API Endpoints Quick Reference

### Authentication
```
POST /enterprise/v1/auth/token
```

### Terminals
```
GET  /enterprise/v1/user-terminals
GET  /enterprise/v1/user-terminals/{id}
GET  /enterprise/v1/user-terminals/{id}/telemetry
```

### Service Lines
```
GET  /enterprise/v1/service-lines
GET  /enterprise/v1/service-lines/{id}/data-usage
```

### Availability
```
GET  /enterprise/v1/availability?lat={lat}&lon={lon}
```

## Common NORAD IDs

```
ISS: 25544
Starlink-1007: 44713
Starlink-1008: 44714
Starlink-1020: 44238
```

## Rate Limits

| API | Limit |
|-----|-------|
| N2YO | 1000/hour |
| Starlink Auth | 10/minute |
| Starlink Terminals | 100/minute |
| Starlink Telemetry | 1000/minute |

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| "API key not configured" | Add key to `.env` file |
| "Invalid credentials" | Check CLIENT_ID and CLIENT_SECRET |
| Server won't start | `uv pip install --force-reinstall -e .` |
| Token expired | Restart MCP server |
| Rate limited | Wait or reduce request frequency |

## File Structure

```
starlink-mcp-server/
├── src/
│   └── starlink_mcp_server.py    # Main server
├── .env                            # Your credentials (DO NOT COMMIT)
├── .env.example                    # Template
├── pyproject.toml                  # Dependencies
├── README.md                       # Full documentation
├── ENTERPRISE_SETUP.md             # API setup guide
├── QUICK_REFERENCE.md              # This file
└── .gitignore                      # Git exclusions
```

## Configuration File Location

### Claude Desktop Config

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### Basic Config
```json
{
  "mcpServers": {
    "starlink": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/starlink-mcp-server",
        "run",
        "python",
        "src/starlink_mcp_server.py"
      ]
    }
  }
}
```

## Status Indicators

| Icon | Meaning |
|------|---------|
| 🔌 | Server connected |
| 🆓 | Free tier feature |
| 🏢 | Enterprise feature |
| ✅ | Working correctly |
| ❌ | Error/Not configured |
| ⚠️ | Warning/Attention needed |

## Important Links

| Resource | URL |
|----------|-----|
| N2YO API | https://www.n2yo.com/api/ |
| CelesTrak | https://celestrak.org |
| Starlink API Docs | https://starlink.readme.io/docs |
| Starlink Support | business-support@starlink.com |
| MCP Docs | https://modelcontextprotocol.io/ |

## Support Contacts

| Issue Type | Contact |
|------------|---------|
| API Access | Your account manager |
| Technical Issues | business-support@starlink.com |
| Billing | Your account manager |
| General Support | https://www.starlink.com/support |

## Example Workflows

### Morning Check
```bash
1. "Show my account overview"
2. "Which terminals need attention?"
3. "Data usage yesterday across all service lines"
```

### Troubleshooting
```bash
1. "Terminal [id] telemetry"
2. "Satellites overhead at terminal location"
3. "24h history for terminal [id]"
4. "Compare to other terminals"
```

### Monthly Review
```bash
1. "Data usage Jan 1-31 for all service lines"
2. "Terminal uptime statistics"  
3. "Terminals with degraded performance"
4. "Cost analysis by service line"
```

## Quick Tips

✅ **Do:**
- Cache terminal IDs locally
- Batch related requests
- Monitor rate limits
- Keep credentials secure
- Test changes in staging

❌ **Don't:**
- Commit `.env` to git
- Hardcode credentials
- Poll telemetry too frequently
- Ignore rate limit errors
- Share API credentials

## Getting Help

1. Check this quick reference
2. Read ENTERPRISE_SETUP.md
3. Search README.md
4. Contact Starlink support
5. Open GitHub issue

---

**Quick Start:** `uv venv && source .venv/bin/activate && uv pip install -e . && python src/starlink_mcp_server.py`
