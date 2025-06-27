#!/usr/bin/env python3

import asyncio
import json
from typing import List, Dict, Any
from agents.mcp import MCPServerStdio
from agents.tools import FunctionTool

class RandomDogMCPClient:
    """MCP Client for the Random Dog server"""
    
    def __init__(self):
        self.server_params = {"command": "uv", "args": ["run", "random_dog_server.py"]}
        self.server = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.server = MCPServerStdio(params=self.server_params, client_session_timeout_seconds=30)
        await self.server.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.server:
            await self.server.__aexit__(exc_type, exc_val, exc_tb)
    
    async def list_tools(self) -> List:
        """List available tools from the MCP server"""
        if not self.server:
            raise RuntimeError("Client not initialized. Use 'async with' context manager.")
        return await self.server.list_tools()
    
    async def get_random_dog(self) -> Dict[str, Any]:
        """Get a random dog image data"""
        if not self.server:
            raise RuntimeError("Client not initialized. Use 'async with' context manager.")
        return await self.server.call_tool("get_random_dog", {})
    
    async def get_dog_image_url(self) -> str:
        """Get just the URL of a random dog image"""
        if not self.server:
            raise RuntimeError("Client not initialized. Use 'async with' context manager.")
        return await self.server.call_tool("get_dog_image_url", {})
    
    async def get_openai_function_tools(self) -> List[FunctionTool]:
        """Convert MCP tools to OpenAI function tools format"""
        if not self.server:
            raise RuntimeError("Client not initialized. Use 'async with' context manager.")
        
        mcp_tools = await self.list_tools()
        openai_tools = []
        
        for tool in mcp_tools:
            # Create a lambda that captures the current tool name
            async def tool_handler(tool_name=tool.name, **kwargs):
                return await self.server.call_tool(tool_name, kwargs)
            
            function_tool = FunctionTool(
                name=tool.name,
                description=tool.description,
                params_json_schema=tool.inputSchema,
                on_invoke_tool=tool_handler
            )
            openai_tools.append(function_tool)
        
        return openai_tools

# Example usage functions
async def test_client():
    """Test the MCP client directly"""
    print("🐕 Testing Random Dog MCP Client...")
    
    async with RandomDogMCPClient() as client:
        # List tools
        tools = await client.list_tools()
        print(f"\n📋 Available tools: {[tool.name for tool in tools]}")
        
        # Get random dog data
        dog_data = await client.get_random_dog()
        print(f"\n🐕 Random dog data: {dog_data}")
        
        # Get just the URL
        dog_url = await client.get_dog_image_url()
        print(f"\n🔗 Dog image URL: {dog_url}")

async def test_with_openai_tools():
    """Test using the client to create OpenAI-compatible function tools"""
    print("\n🤖 Testing OpenAI Function Tools Integration...")
    
    async with RandomDogMCPClient() as client:
        # Get OpenAI-compatible tools
        openai_tools = await client.get_openai_function_tools()
        print(f"\n🔧 OpenAI Function Tools: {[tool.name for tool in openai_tools]}")
        
        # Test calling one of the tools
        if openai_tools:
            tool = openai_tools[0]  # get_random_dog
            result = await tool.on_invoke_tool()
            print(f"\n🎲 Tool result: {result}")

# Utility function to get a simple random dog
async def get_random_dog_simple() -> Dict[str, Any]:
    """Simple utility function to get a random dog"""
    async with RandomDogMCPClient() as client:
        return await client.get_random_dog()

if __name__ == "__main__":
    print("🐕 Random Dog MCP Client Test")
    print("=" * 50)
    
    # Run tests
    asyncio.run(test_client())
    asyncio.run(test_with_openai_tools())
    
    print("\n" + "=" * 50)
    print("✅ Random Dog MCP Client tests completed!") 