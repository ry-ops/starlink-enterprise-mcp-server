# Starlink MCP Server
<img src="https://github.com/ry-ops/starlink-mcp-server/blob/main/starlink-mcp-server.png" width="100%">
A Model Context Protocol (MCP) server written in Python that provides Claude AI with access to Starlink satellite data and services.

## Features

- **Satellite Information**: Query real-time Starlink satellite positions and status
- **Coverage Maps**: Check Starlink service availability by location
- **Service Status**: Monitor Starlink network health and outages
- **Satellite Passes**: Get upcoming satellite pass predictions for any location

## Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- Claude Desktop App (for integration)

## Installation

### 1. Install uv (if you haven't already)

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone and Setup Project

```bash
# Clone the repository
git clone https://github.com/yourusername/starlink-mcp-server.git
cd starlink-mcp-server

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
uv pip install -e .
```

## Usage

### Running the Server Standalone

```bash
python src/starlink_mcp_server.py
```

### Connecting to Claude Desktop

1. Open your Claude Desktop configuration file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. Add the Starlink MCP server configuration:

```json
{
  "mcpServers": {
    "starlink": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/starlink-mcp-server",
        "run",
        "starlink-mcp-server"
      ]
    }
  }
}
```

Alternatively, if you've activated your virtual environment:

```json
{
  "mcpServers": {
    "starlink": {
      "command": "/absolute/path/to/starlink-mcp-server/.venv/bin/python",
      "args": [
        "/absolute/path/to/starlink-mcp-server/src/starlink_mcp_server.py"
      ]
    }
  }
}
```

3. Restart Claude Desktop

4. Look for the 🔌 icon in Claude to see connected MCP servers

## Available Tools

### get_satellite_info
Get information about Starlink satellites including their positions and status.

**Parameters:**
- `satellite_id` (optional): Specific satellite ID to query

**Example:**
```
Can you get info on Starlink satellites?
```

### get_coverage_map
Get information about Starlink coverage availability in different regions.

**Parameters:**
- `latitude` (required): Latitude coordinate
- `longitude` (required): Longitude coordinate

**Example:**
```
Check Starlink coverage at latitude 45.5, longitude -122.6
```

### get_service_status
Check Starlink service status and outages.

**Parameters:** None

**Example:**
```
What's the current Starlink service status?
```

### get_satellite_passes
Get upcoming satellite passes for a specific location.

**Parameters:**
- `latitude` (required): Latitude coordinate
- `longitude` (required): Longitude coordinate
- `days` (optional): Number of days to forecast (default: 7)

**Example:**
```
Show me Starlink satellite passes for my location at 40.7°N, 74.0°W for the next 3 days
```

## Development

### Project Structure

```
starlink-mcp-server/
├── src/
│   └── starlink_mcp_server.py    # Main server implementation
├── pyproject.toml                 # Project configuration
├── README.md
└── .venv/                         # Virtual environment (created by uv)
```

### Running in Development Mode

```bash
# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run the server
python src/starlink_mcp_server.py
```

### Code Formatting

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Format code
black src/

# Lint code
ruff check src/
```

### Testing

```bash
# Run tests (when implemented)
pytest
```

## API Configuration

**Important Note:** This server currently uses placeholder implementations. You'll need to:

1. **Find Starlink API Access**
   - Check for official Starlink developer APIs
   - Consider using satellite tracking APIs like:
     - [N2YO.com API](https://www.n2yo.com/api/) - Satellite tracking
     - [Space-Track.org](https://www.space-track.org/) - Satellite catalog
     - Community APIs for Starlink data

2. **Update API Endpoints**
   - Replace mock data in `src/starlink_mcp_server.py`
   - Add authentication if required
   - Implement proper error handling

3. **Add Environment Variables**
   - Create a `.env` file for API keys:
   ```bash
   STARLINK_API_KEY=your_api_key_here
   SATELLITE_TRACKING_API_KEY=your_key_here
   ```

### Example API Integration

```python
import os
from dotenv import load_dotenv

load_dotenv()

async def get_satellite_info(self, satellite_id: Optional[str] = None) -> dict:
    api_key = os.getenv("STARLINK_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}
    
    url = f"https://api.starlink.com/v1/satellites"
    if satellite_id:
        url += f"/{satellite_id}"
    
    response = await self.client.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
```

## Useful Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [uv Documentation](https://github.com/astral-sh/uv)
- [Starlink Community APIs](https://github.com/r-spacex/SpaceX-API)

## Troubleshooting

### Server not connecting to Claude

- Verify the absolute paths in `claude_desktop_config.json`
- Ensure virtual environment is activated
- Check that all dependencies are installed: `uv pip list`
- Restart Claude Desktop after configuration changes
- Check Claude Desktop logs for errors

### Import Errors

```bash
# Reinstall dependencies
uv pip install --force-reinstall -e .
```

### API Errors

- Verify API endpoints are correct
- Check if authentication is required
- Review rate limits and quotas
- Enable debug logging to see raw responses

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT

## Future Enhancements

- [ ] Real Starlink API integration
- [ ] Authentication support with environment variables
- [ ] Caching for satellite data
- [ ] WebSocket support for real-time updates
- [ ] Speed test functionality
- [ ] Account management tools
- [ ] Historical data analysis
- [ ] Coverage map visualization

## Support

For issues and questions, please open an issue on GitHub.

## Acknowledgments

- Built with [Model Context Protocol](https://modelcontextprotocol.io/)
- Powered by [uv](https://github.com/astral-sh/uv) for fast Python package management
