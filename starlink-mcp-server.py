#!/usr/bin/env python3
"""
Starlink Enterprise MCP Server
Manage your Starlink terminals through Claude AI using the Starlink Enterprise API
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Any, Optional, Dict, List
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


class StarlinkEnterpriseMCPServer:
    def __init__(self):
        self.server = Server("starlink-enterprise-mcp-server")
        self.client = httpx.AsyncClient(timeout=30.0)
        
        # Starlink Enterprise API credentials
        self.starlink_client_id = os.getenv("STARLINK_CLIENT_ID", "")
        self.starlink_client_secret = os.getenv("STARLINK_CLIENT_SECRET", "")
        self.starlink_access_token = None
        self.starlink_token_expiry = None
        
        # API Base URL
        self.starlink_api_base = "https://web-api.starlink.com/enterprise/v1"
        
        self.setup_handlers()

    async def get_starlink_access_token(self) -> str:
        """Get or refresh Starlink Enterprise API access token"""
        # Check if we have a valid token
        if self.starlink_access_token and self.starlink_token_expiry:
            if datetime.utcnow() < self.starlink_token_expiry:
                return self.starlink_access_token
        
        # Request new token
        auth_url = f"{self.starlink_api_base}/auth/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.starlink_client_id,
            "client_secret": self.starlink_client_secret
        }
        
        try:
            response = await self.client.post(auth_url, data=data)
            response.raise_for_status()
            
            token_data = response.json()
            self.starlink_access_token = token_data["access_token"]
            # Set expiry 5 minutes before actual expiry for safety
            expires_in = token_data.get("expires_in", 3600)
            self.starlink_token_expiry = datetime.utcnow() + timedelta(seconds=expires_in - 300)
            
            return self.starlink_access_token
        except Exception as e:
            raise Exception(f"Failed to authenticate with Starlink API: {str(e)}")

    async def starlink_api_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make authenticated request to Starlink Enterprise API"""
        if not self.starlink_client_id or not self.starlink_client_secret:
            raise ValueError(
                "Starlink Enterprise API credentials not configured. "
                "Please set STARLINK_CLIENT_ID and STARLINK_CLIENT_SECRET environment variables."
            )
        
        token = await self.get_starlink_access_token()
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        headers["Content-Type"] = "application/json"
        
        url = f"{self.starlink_api_base}{endpoint}"
        
        try:
            response = await self.client.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            
            # Handle empty responses
            if response.status_code == 204 or not response.text:
                return {"status": "success", "message": "Operation completed"}
            
            return response.json()
        except httpx.HTTPStatusError as e:
            error_detail = e.response.text if e.response else str(e)
            raise Exception(f"Starlink API error ({e.response.status_code}): {error_detail}")
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")

    def setup_handlers(self):
        """Register MCP tool handlers"""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available Starlink Enterprise tools"""
            return [
                Tool(
                    name="list_user_terminals",
                    description="List all your Starlink user terminals with their current status",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page": {
                                "type": "number",
                                "description": "Page number for pagination (default: 1)",
                                "default": 1
                            },
                            "page_size": {
                                "type": "number",
                                "description": "Number of results per page (default: 50, max: 100)",
                                "default": 50
                            }
                        }
                    }
                ),
                Tool(
                    name="get_terminal_details",
                    description="Get detailed information about a specific user terminal including hardware info and configuration",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_terminal_id": {
                                "type": "string",
                                "description": "User terminal ID (UUID format)"
                            }
                        },
                        "required": ["user_terminal_id"]
                    }
                ),
                Tool(
                    name="get_terminal_telemetry",
                    description="Get real-time telemetry data for a terminal (uptime, signal quality, obstructions, throughput)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_terminal_id": {
                                "type": "string",
                                "description": "User terminal ID"
                            }
                        },
                        "required": ["user_terminal_id"]
                    }
                ),
                Tool(
                    name="list_service_lines",
                    description="List all your Starlink service lines (subscriptions/accounts)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page": {
                                "type": "number",
                                "description": "Page number",
                                "default": 1
                            },
                            "page_size": {
                                "type": "number",
                                "description": "Results per page",
                                "default": 50
                            }
                        }
                    }
                ),
                Tool(
                    name="get_service_line_details",
                    description="Get details about a specific service line including subscription status and plan",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "service_line_id": {
                                "type": "string",
                                "description": "Service line ID (UUID format)"
                            }
                        },
                        "required": ["service_line_id"]
                    }
                ),
                Tool(
                    name="get_data_usage",
                    description="Get data usage statistics for a service line over a date range",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "service_line_id": {
                                "type": "string",
                                "description": "Service line ID"
                            },
                            "start_date": {
                                "type": "string",
                                "description": "Start date in YYYY-MM-DD format"
                            },
                            "end_date": {
                                "type": "string",
                                "description": "End date in YYYY-MM-DD format"
                            }
                        },
                        "required": ["service_line_id", "start_date", "end_date"]
                    }
                ),
                Tool(
                    name="list_addresses",
                    description="List all service addresses associated with your account",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page": {
                                "type": "number",
                                "description": "Page number",
                                "default": 1
                            }
                        }
                    }
                ),
                Tool(
                    name="get_address_details",
                    description="Get details about a specific service address",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "address_id": {
                                "type": "string",
                                "description": "Address ID (UUID format)"
                            }
                        },
                        "required": ["address_id"]
                    }
                ),
                Tool(
                    name="check_service_availability",
                    description="Check if Starlink service is available at a specific location",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "latitude": {
                                "type": "number",
                                "description": "Latitude coordinate"
                            },
                            "longitude": {
                                "type": "number",
                                "description": "Longitude coordinate"
                            }
                        },
                        "required": ["latitude", "longitude"]
                    }
                ),
                Tool(
                    name="get_account_overview",
                    description="Get a complete overview of your Starlink account including all terminals, service lines, and summary statistics",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="list_subscription_products",
                    description="List available Starlink subscription products and service plans",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="get_terminal_history",
                    description="Get historical telemetry data for a terminal over a specified time period",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "user_terminal_id": {
                                "type": "string",
                                "description": "User terminal ID"
                            },
                            "start_time": {
                                "type": "string",
                                "description": "Start time in ISO format (e.g., 2024-01-01T00:00:00Z)"
                            },
                            "end_time": {
                                "type": "string",
                                "description": "End time in ISO format"
                            }
                        },
                        "required": ["user_terminal_id", "start_time", "end_time"]
                    }
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Handle tool calls"""
            try:
                if name == "list_user_terminals":
                    result = await self.list_user_terminals(
                        arguments.get("page", 1),
                        arguments.get("page_size", 50)
                    )
                elif name == "get_terminal_details":
                    result = await self.get_terminal_details(arguments["user_terminal_id"])
                elif name == "get_terminal_telemetry":
                    result = await self.get_terminal_telemetry(arguments["user_terminal_id"])
                elif name == "list_service_lines":
                    result = await self.list_service_lines(
                        arguments.get("page", 1),
                        arguments.get("page_size", 50)
                    )
                elif name == "get_service_line_details":
                    result = await self.get_service_line_details(arguments["service_line_id"])
                elif name == "get_data_usage":
                    result = await self.get_data_usage(
                        arguments["service_line_id"],
                        arguments["start_date"],
                        arguments["end_date"]
                    )
                elif name == "list_addresses":
                    result = await self.list_addresses(arguments.get("page", 1))
                elif name == "get_address_details":
                    result = await self.get_address_details(arguments["address_id"])
                elif name == "check_service_availability":
                    result = await self.check_service_availability(
                        arguments["latitude"],
                        arguments["longitude"]
                    )
                elif name == "get_account_overview":
                    result = await self.get_account_overview()
                elif name == "list_subscription_products":
                    result = await self.list_subscription_products()
                elif name == "get_terminal_history":
                    result = await self.get_terminal_history(
                        arguments["user_terminal_id"],
                        arguments["start_time"],
                        arguments["end_time"]
                    )
                else:
                    raise ValueError(f"Unknown tool: {name}")

                return [TextContent(type="text", text=json.dumps(result, indent=2))]
                
            except Exception as e:
                error_msg = f"Error: {str(e)}\n\n"
                
                if "credentials not configured" in str(e):
                    error_msg += "Please set the following environment variables:\n"
                    error_msg += "  - STARLINK_CLIENT_ID\n"
                    error_msg += "  - STARLINK_CLIENT_SECRET\n\n"
                    error_msg += "Contact your Starlink account manager to request API access."
                
                return [TextContent(type="text", text=error_msg)]

    # === TERMINAL MANAGEMENT ===
    
    async def list_user_terminals(self, page: int = 1, page_size: int = 50) -> dict:
        """List all user terminals"""
        return await self.starlink_api_request(
            "GET",
            "/user-terminals",
            params={"page": page, "pageSize": page_size}
        )

    async def get_terminal_details(self, user_terminal_id: str) -> dict:
        """Get detailed terminal information"""
        return await self.starlink_api_request(
            "GET",
            f"/user-terminals/{user_terminal_id}"
        )

    async def get_terminal_telemetry(self, user_terminal_id: str) -> dict:
        """Get real-time terminal telemetry"""
        return await self.starlink_api_request(
            "GET",
            f"/user-terminals/{user_terminal_id}/telemetry"
        )

    async def get_terminal_history(self, user_terminal_id: str, start_time: str, end_time: str) -> dict:
        """Get historical terminal data"""
        return await self.starlink_api_request(
            "GET",
            f"/user-terminals/{user_terminal_id}/history",
            params={"startTime": start_time, "endTime": end_time}
        )

    # === SERVICE LINE MANAGEMENT ===
    
    async def list_service_lines(self, page: int = 1, page_size: int = 50) -> dict:
        """List all service lines"""
        return await self.starlink_api_request(
            "GET",
            "/service-lines",
            params={"page": page, "pageSize": page_size}
        )

    async def get_service_line_details(self, service_line_id: str) -> dict:
        """Get service line details"""
        return await self.starlink_api_request(
            "GET",
            f"/service-lines/{service_line_id}"
        )

    async def get_data_usage(self, service_line_id: str, start_date: str, end_date: str) -> dict:
        """Get data usage for a service line"""
        return await self.starlink_api_request(
            "GET",
            f"/service-lines/{service_line_id}/data-usage",
            params={"startDate": start_date, "endDate": end_date}
        )

    # === ADDRESS MANAGEMENT ===
    
    async def list_addresses(self, page: int = 1) -> dict:
        """List all addresses"""
        return await self.starlink_api_request(
            "GET",
            "/addresses",
            params={"page": page}
        )

    async def get_address_details(self, address_id: str) -> dict:
        """Get address details"""
        return await self.starlink_api_request(
            "GET",
            f"/addresses/{address_id}"
        )

    async def check_service_availability(self, latitude: float, longitude: float) -> dict:
        """Check service availability at coordinates"""
        return await self.starlink_api_request(
            "GET",
            "/availability",
            params={"latitude": latitude, "longitude": longitude}
        )

    # === ACCOUNT OVERVIEW ===
    
    async def get_account_overview(self) -> dict:
        """Get complete account overview"""
        try:
            # Fetch all data in parallel
            terminals_task = self.list_user_terminals(page_size=100)
            service_lines_task = self.list_service_lines(page_size=100)
            addresses_task = self.list_addresses()
            
            terminals, service_lines, addresses = await asyncio.gather(
                terminals_task,
                service_lines_task,
                addresses_task,
                return_exceptions=True
            )
            
            # Build overview
            overview = {
                "account_summary": {
                    "generated_at": datetime.utcnow().isoformat(),
                    "total_terminals": len(terminals.get("results", [])) if isinstance(terminals, dict) else 0,
                    "total_service_lines": len(service_lines.get("results", [])) if isinstance(service_lines, dict) else 0,
                    "total_addresses": len(addresses.get("results", [])) if isinstance(addresses, dict) else 0,
                },
                "terminals": terminals if isinstance(terminals, dict) else {"error": str(terminals)},
                "service_lines": service_lines if isinstance(service_lines, dict) else {"error": str(service_lines)},
                "addresses": addresses if isinstance(addresses, dict) else {"error": str(addresses)}
            }
            
            return overview
            
        except Exception as e:
            raise Exception(f"Failed to generate account overview: {str(e)}")

    async def list_subscription_products(self) -> dict:
        """List available subscription products"""
        return await self.starlink_api_request(
            "GET",
            "/subscription-products"
        )

    async def cleanup(self):
        """Cleanup resources"""
        await self.client.aclose()

    async def run(self):
        """Run the MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point"""
    server = StarlinkEnterpriseMCPServer()
    try:
        await server.run()
    finally:
        await server.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
