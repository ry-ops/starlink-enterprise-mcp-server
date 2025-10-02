# Starlink MCP Server

A Model Context Protocol (MCP) server that provides Claude AI with access to Starlink satellite data and services.

## Features

- **Satellite Information**: Query real-time Starlink satellite positions and status
- **Coverage Maps**: Check Starlink service availability by location
- **Service Status**: Monitor Starlink network health and outages

## Prerequisites

- Node.js 18 or higher
- npm or yarn
- Claude Desktop App (for integration)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/starlink-mcp-server.git
cd starlink-mcp-server
```

2. Install dependencies:
```bash
npm install
```

3. Build the project:
```bash
npm run build
```

## Usage

### Running the Server

```bash
npm start
```

### Connecting to Claude Desktop

1. Open your Claude Desktop configuration file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the Starlink MCP server configuration:

```json
{
  "mcpServers": {
    "starlink": {
      "command": "node",
      "args": ["/absolute/path/to/starlink-mcp-server/build/index.js"]
    }
  }
}
```

3. Restart Claude Desktop

## Available Tools

### get_satellite_info
Get information about Starlink satellites including their positions and status.

**Parameters:**
- `satellite_id` (optional): Specific satellite ID to query

### get_coverage_map
Get information about Starlink coverage availability in different regions.

**Parameters:**
- `latitude` (required): Latitude coordinate
- `longitude` (required): Longitude coordinate

### get_service_status
Check Starlink service status and outages.

**Parameters:** None

## API Configuration

**Important Note:** This server currently uses placeholder implementations. You'll need to:

1. Sign up for Starlink API access (if available)
2. Update the API endpoints in `src/index.ts`
3. Add authentication if required
4. Implement proper error handling for API responses

### Starlink API Resources

- Official Starlink API documentation may be limited
- Consider using community APIs like:
  - SpaceX API: https://github.com/r-spacex/SpaceX-API
  - Satellite tracking APIs
  - Starlink community endpoints

## Development

Run in development mode with auto-rebuild:

```bash
npm run watch
```

Then in another terminal:
```bash
npm start
```

## Project Structure

```
starlink-mcp-server/
├── src/
│   └── index.ts          # Main server implementation
├── build/                # Compiled JavaScript (generated)
├── package.json
├── tsconfig.json
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT

## Troubleshooting

### Server not connecting to Claude
- Verify the absolute path in `claude_desktop_config.json`
- Check that the build directory exists and contains compiled files
- Restart Claude Desktop after configuration changes

### API errors
- Verify API endpoints are correct
- Check if authentication is required
- Review rate limits and quotas

## Future Enhancements

- [ ] Real Starlink API integration
- [ ] Authentication support
- [ ] Caching for satellite data
- [ ] WebSocket support for real-time updates
- [ ] Additional tools (speed tests, account management)
- [ ] Error logging and monitoring

## Support

For issues and questions, please open an issue on GitHub.
