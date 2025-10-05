# Starlink Enterprise MCP Server
<img src="https://github.com/ry-ops/starlink-mcp-server/blob/main/starlink-mcp-server.png" width="100%">

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/badge/uv-latest-green.svg)](https://github.com/astral-sh/uv)
[![MCP](https://img.shields.io/badge/MCP-1.0-purple.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

Manage your Starlink terminal fleet through Claude AI using the Starlink Enterprise API.

## Perfect For

- **Enterprise customers** with multiple Starlink terminals deployed
- **Fleet operators** needing centralized terminal management
- **IT teams** monitoring terminal health and performance
- **Operations managers** tracking data usage and costs

## Features

✅ **Terminal Management**
- List all your user terminals
- Get real-time telemetry (uptime, signal, obstructions)
- View terminal details and configuration
- Historical performance data

✅ **Service Line Management**
- List all service lines (subscriptions)
- Track data usage by date range
- View subscription details and status
- Monitor billing and plans

✅ **Address Management**
- List all service addresses
- Check service availability at new locations
- View address details

✅ **Account Overview**
- Complete fleet status at a glance
- Summary statistics across all terminals
- Quick health checks

## Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Claude Desktop App
- **Starlink Business/Enterprise Account** with API access
- **Client ID and Client Secret** from your Starlink account manager

## Quick Start

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create and setup project
mkdir starlink-mcp-server && cd starlink-mcp-server
mkdir src

# Save starlink_mcp_server.py to src/
# Save pyproject.toml to root
# Save .env.example to root

# Install
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# Configure credentials
cp .env.example .env
# Edit .env and add your STARLINK_CLIENT_ID and STARLINK_CLIENT_SECRET
```

## Getting API Access

API access is available by request to Starlink Enterprise and Business customers. Contact your Starlink account manager or email `business-support@starlink.com` to request access.

### Step 1: Create Service Account

1. Log into https://www.starlink.com/account
2. Navigate to **Settings** tab
3. Find **"Service Accounts"** section
4. Click **"+ Add Service Account"**
5. Note your Client ID and Client Secret

### Step 2: Configure Environment

Add credentials to `.env`:

```bash
STARLINK_CLIENT_ID=your_actual_client_id_here
STARLINK_CLIENT_SECRET=your_actual_client_secret_here
```

## Connect to Claude Desktop

### Configuration File Location

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

### Add Server Configuration

```json
{
  "mcpServers": {
    "starlink": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/starlink-mcp-server",
        "run",
        "python",
        "src/starlink_mcp_server.py"
      ],
      "env": {
        "STARLINK_CLIENT_ID": "your_client_id",
        "STARLINK_CLIENT_SECRET": "your_client_secret"
      }
    }
  }
}
```

**Important:** Replace `/absolute/path/to/starlink-mcp-server` with your actual path!

### Restart Claude

1. Quit Claude Desktop completely
2. Reopen Claude Desktop
3. Look for 🔌 icon - you should see "starlink" connected

## Available Tools

### list_user_terminals
List all your Starlink terminals with status.

**Example:**
```
Show me all my Starlink terminals
```

### get_terminal_details
Get detailed information about a specific terminal.

**Example:**
```
Get details for terminal abc-123-def-456
```

### get_terminal_telemetry
Get real-time performance data (uptime, signal quality, obstructions, throughput).

**Example:**
```
Show me telemetry for terminal abc-123-def-456
```

### list_service_lines
List all your service lines (subscriptions).

**Example:**
```
List all my service lines
```

### get_service_line_details
Get details about a specific service line.

**Example:**
```
Get details for service line xyz-789
```

### get_data_usage
Get data usage over a date range.

**Example:**
```
Show me data usage from 2024-01-01 to 2024-01-31 for service line xyz-789
```

### list_addresses
List all service addresses.

**Example:**
```
Show me all my Starlink addresses
```

### get_address_details
Get details about a specific address.

**Example:**
```
Get details for address addr-123
```

### check_service_availability
Check if Starlink is available at coordinates.

**Example:**
```
Is Starlink available at latitude 45.5, longitude -93.2?
```

### get_account_overview
Get complete overview of your fleet.

**Example:**
```
Give me an overview of my entire Starlink account
```

### list_subscription_products
List available Starlink plans and products.

**Example:**
```
What subscription products are available?
```

### get_terminal_history
Get historical data for a terminal.

**Example:**
```
Show me history for terminal abc-123 from 2024-01-01T00:00:00Z to 2024-01-02T00:00:00Z
```

## Common Use Cases

### Daily Fleet Check
```
Good morning! Show me all my terminals and highlight any with issues
```

### Troubleshooting
```
Terminal ABC123 in Denver is slow. Show me its telemetry data
```

### Usage Monitoring
```
Show me data usage for all service lines this month
```

### Expansion Planning
```
We want to add terminals at these locations: [coordinates]. Check service availability
```

### Performance Review
```
Show me terminals with lowest uptime over the past 30 days
```

### Cost Analysis
```
Which service lines had the highest data usage last month?
```

## Example Workflows

### Morning Status Report
```
Claude, give me a morning report:
1. List all terminals
2. Show which ones are offline or have issues
3. Total data usage yesterday across all service lines
```

### Terminal Troubleshooting
```
1. Get telemetry for terminal [id]
2. Show 24-hour history
3. Compare to other terminals at same location
```

### Monthly Review
```
1. Get account overview
2. Data usage for January across all service lines
3. List terminals by uptime percentage
4. Identify any performance trends
```

## Project Structure

```
starlink-mcp-server/
├── src/
│   └── starlink_mcp_server.py    # Main server code
├── pyproject.toml                 # Dependencies
├── .env                           # Your credentials (DO NOT COMMIT)
├── .env.example                   # Template
├── .gitignore                     # Git exclusions
└── README.md                      # This file
```

## API Rate Limits

| Endpoint | Limit |
|----------|-------|
| Authentication | 10 requests/minute |
| Terminal queries | 100 requests/minute |
| Telemetry | 1000 requests/minute |
| Data usage | 100 requests/minute |

**Tips:**
- Cache terminal lists (they change rarely)
- Batch related requests
- Implement retry logic with exponential backoff

## Troubleshooting

### "credentials not configured"
- Check `.env` file exists and has correct values
- Ensure no extra spaces in credential values
- Verify credentials with your account manager

### "Authentication failed"
- Confirm Client ID and Client Secret are correct
- Check that your service account is active
- Contact account manager if credentials expired

### Server won't connect to Claude
- Verify absolute path in `claude_desktop_config.json`
- Check Python and dependencies installed
- Test server manually: `python src/starlink_mcp_server.py`
- Restart Claude Desktop

### Rate limit errors
- You've exceeded API limits
- Wait for limit reset (usually 1 minute)
- Reduce request frequency
- Consider caching results

## Security Best Practices

✅ **Do:**
- Keep `.env` in `.gitignore`
- Use strong, unique credentials
- Rotate credentials periodically
- Use environment variables, not hardcoded values
- Separate dev/prod credentials

❌ **Don't:**
- Commit credentials to git
- Share credentials publicly
- Hardcode credentials in code
- Use same credentials across environments

## Support

### Starlink Support
- **Email**: business-support@starlink.com
- **Account Manager**: Contact your assigned manager
- **Support Portal**: https://www.starlink.com/support

### Documentation
- **API Docs**: https://starlink.readme.io/docs (requires access)
- **Enterprise Guide**: https://starlink-enterprise-guide.readme.io
- **Swagger UI**: https://web-api.starlink.com/enterprise/swagger/index.html

## Contributing

Found a bug or have a feature request? Please open an issue on GitHub.

## License

MIT

---

**Manage your Starlink fleet effortlessly with Claude AI!** 🛰️✨
