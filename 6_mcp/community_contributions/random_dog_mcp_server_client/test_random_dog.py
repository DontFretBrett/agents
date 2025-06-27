#!/usr/bin/env python3

import asyncio
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
from IPython.display import display, Markdown

async def test_random_dog_mcp():
    """Test the random dog MCP server"""
    
    # MCP Server parameters
    params = {"command": "uv", "args": ["run", "random_dog_server.py"]}
    
    print("🐕 Testing Random Dog MCP Server...")
    
    # Test the MCP server directly
    async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as server:
        # List available tools
        mcp_tools = await server.list_tools()
        print(f"\n📋 Available tools: {[tool.name for tool in mcp_tools]}")
        
        # Test getting a random dog
        print("\n🎲 Testing get_random_dog tool...")
        result = await server.call_tool("get_random_dog", {})
        print(f"Result: {result}")
        
        # Test getting just the URL
        print("\n🔗 Testing get_dog_image_url tool...")
        url_result = await server.call_tool("get_dog_image_url", {})
        print(f"Dog image URL: {url_result}")

async def test_with_agent():
    """Test the MCP server with an AI agent"""
    
    params = {"command": "uv", "args": ["run", "random_dog_server.py"]}
    
    instructions = """You are a helpful assistant that can fetch random dog images. 
    When asked for a dog image, use the available tools to get one and provide the user with the URL and file size information."""
    
    request = "Can you get me a random dog image?"
    model = "gpt-4o-mini"
    
    print("\n🤖 Testing with AI Agent...")
    
    async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as mcp_server:
        agent = Agent(name="dog_fetcher", instructions=instructions, model=model, mcp_servers=[mcp_server])
        
        with trace("random_dog_test"):
            result = await Runner.run(agent, request)
            print(f"\n🐕 Agent Response: {result.final_output}")

if __name__ == "__main__":
    print("🐕 Random Dog MCP Server Test")
    print("=" * 40)
    
    # Run the tests
    asyncio.run(test_random_dog_mcp())
    print("\n" + "=" * 40)
    asyncio.run(test_with_agent()) 