import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command=r"C:\Users\window\Desktop\projects\my-first-app\.venv\Scripts\python.exe",
    args=[
        r"C:\Users\window\Desktop\projects\my-first-app\mcp_server.py"
    ]
)

async def call_mcp_tool(tool_name, arguments):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                tool_name,
                arguments
            )

            return result