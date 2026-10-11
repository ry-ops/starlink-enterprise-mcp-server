import importlib.util
from pathlib import Path

SERVER = Path(__file__).resolve().parent.parent / "starlink-mcp-server.py"


def load_server():
    spec = importlib.util.spec_from_file_location("starlink_mcp_server", SERVER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_server_module_loads():
    module = load_server()
    assert hasattr(module, "main")
