#!/usr/bin/env python
import os
import sys
import logging
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Literal

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mcp_polygon import server


def transport() -> Literal["stdio", "sse", "streamable-http"]:
    """
    Determine the transport type for the MCP server.
    Defaults to 'stdio' if not set in environment variables.
    """
    mcp_transport_str = os.environ.get("MCP_TRANSPORT", "stdio")

    # These are currently the only supported transports
    supported_transports: dict[str, Literal["stdio", "sse", "streamable-http"]] = {
        "stdio": "stdio",
        "sse": "sse",
        "streamable-http": "streamable-http",
    }

    return supported_transports.get(mcp_transport_str, "stdio")


def heartbeat_logger():
    """Background thread to log heartbeat messages every 30 seconds"""
    while True:
        time.sleep(30)
        logger.info(f"Server heartbeat - MCP Polygon server is running [PID: {os.getpid()}]")


# Ensure the server process doesn't exit immediately when run as an MCP server
def start_server():
    logger.info("=" * 60)
    logger.info("MCP Polygon Server Starting")
    logger.info("=" * 60)

    # Log environment information
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Process ID: {os.getpid()}")

    # Check transport mode
    transport_mode = transport()
    logger.info(f"Transport mode: {transport_mode}")

    # Check API key
    polygon_api_key = os.environ.get("POLYGON_API_KEY", "")
    if not polygon_api_key:
        logger.warning("POLYGON_API_KEY environment variable not set - server will run but API calls will fail")
    else:
        logger.info(f"POLYGON_API_KEY configured (length: {len(polygon_api_key)} chars)")

    # Log deployment environment
    if os.environ.get("RAILWAY_ENVIRONMENT"):
        logger.info(f"Running on Railway - Environment: {os.environ.get('RAILWAY_ENVIRONMENT')}")
        logger.info(f"Railway Service: {os.environ.get('RAILWAY_SERVICE_NAME', 'unknown')}")

    # Start heartbeat logger in background
    heartbeat_thread = threading.Thread(target=heartbeat_logger, daemon=True)
    heartbeat_thread.start()
    logger.info("Heartbeat monitoring started (will log every 30 seconds)")

    logger.info("-" * 60)
    logger.info(f"Server initialized at {datetime.now().isoformat()}")
    logger.info(f"Ready to accept {transport_mode} connections")
    logger.info("-" * 60)

    # Start the server
    server.run(transport=transport())


if __name__ == "__main__":
    start_server()
