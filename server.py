import os
import httpx
import yaml
from fastmcp import FastMCP
from fastmcp.server.providers.openapi import RouteMap, MCPType

base_url = os.getenv("BASE_URL")
if not base_url:
    raise ValueError("BASE_URL environment variable is required")

session_cookie = os.getenv("OVERLORD_TOKEN")
client_cookies = {}

if session_cookie:
    client_cookies["token"] = session_cookie
else:
    username = os.getenv("OVERLORD_USER")
    password = os.getenv("OVERLORD_PASS")

    if not username or not password:
        raise ValueError(
            "Neither OVERLORD_TOKEN nor OVERLORD_USER and OVERLORD_PASS were provided."
        )

    # Perform login request
    with httpx.Client(base_url=base_url) as auth_client:
        response = auth_client.post(
            "/api/login",
            json={"user": username, "pass": password},
        )
        response.raise_for_status()

        # Check if the server set a cookie in the response headers
        if response.cookies:
            client_cookies = dict(response.cookies)
        else:
            # Fallback to the token from the response JSON body
            data = response.json()
            token = data.get("token")
            if not token:
                raise ValueError("Login succeeded but no token or cookie was returned.")
            # Set under the expected cookie name (e.g., 'token' or 'session')
            client_cookies = {"token": token}

# Load and parse the YAML spec
with open("overlord_openapi.yml", "r") as f:
    openapi_spec = yaml.safe_load(f)

# 1. Separate profile endpoints from semantic spec
semantic_spec = dict(openapi_spec)
paths = semantic_spec.get("paths", {})

filtered_paths = {}
profile_paths = {}

for path, operations in paths.items():
    if path.rstrip("/").endswith("profile"):
        profile_paths[path] = operations
    else:
        filtered_paths[path] = operations

semantic_spec["paths"] = filtered_paths

# 2. Create an HTTP client for your API
client = httpx.AsyncClient(
    base_url=base_url,
    cookies=client_cookies,
    )

# 3. Restore pre-2.8.0 semantic mapping
# Create the MCP server
mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
    name="Overlord MCP"
    route_maps=[
       
        # Add different tags to detail view endpoints
        RouteMap(
            methods=["GET"],
            pattern=r"\profile",
            mcp_type=MCPType.TOOL,
            mcp_tags={"profile-performance"}
        ),

        
    ],
)

# 4. Explicitly register profile routes as regular tools
for path, operations in profile_paths.items():
    for method, op_data in operations.items():
        if method.lower() not in {"get", "post", "put", "patch", "delete"}:
            continue

        tool_name = op_data.get("operationId") or f"{method.lower()}_{path.strip('/').replace('/', '_')}"
        tool_desc = op_data.get("description") or op_data.get("summary") or f"{method.upper()} {path}"

        def make_tool(target_path=path, target_method=method.upper()):
            async def profile_tool(**kwargs):
                response = await client.request(target_method, target_path, params=kwargs)
                response.raise_for_status()
                return response.json()
            return profile_tool

        mcp.add_tool(
            make_tool(),
            name=tool_name,
            description=tool_desc,
        )

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=PORT)
