#!/usr/bin/env python3
"""
Demo script for Random Dog MCP Server
Add these cells to your Jupyter notebook to test the random dog MCP server
"""

# Cell 1: Setup and imports
"""
from dotenv import load_dotenv
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
from IPython.display import display, Markdown, Image
import requests

load_dotenv(override=True)
"""

# Cell 2: Test the MCP server directly
"""
# Test our random dog MCP server
params = {"command": "uv", "args": ["run", "random_dog_server.py"]}

async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as server:
    mcp_tools = await server.list_tools()
    print("Available tools:", [tool.name for tool in mcp_tools])
    
    # Get a random dog
    result = await server.call_tool("get_random_dog", {})
    print("Random dog result:", result)
"""

# Cell 3: Use with an AI Agent
"""
instructions = "You are a helpful assistant that can fetch random dog images. When asked for a dog image, use the available tools to get one and provide the user with the URL and file size information. Always be enthusiastic about dogs!"

request = "Can you get me a cute random dog image? I love dogs!"
model = "gpt-4o-mini"

async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as mcp_server:
    agent = Agent(name="dog_fetcher", instructions=instructions, model=model, mcp_servers=[mcp_server])
    with trace("random_dog_demo"):
        result = await Runner.run(agent, request)
    display(Markdown(result.final_output))
"""

# Cell 4: Display the dog image in notebook
"""
# Get a dog image and display it
async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as server:
    dog_data = await server.call_tool("get_random_dog", {})
    
if 'url' in dog_data and dog_data['url']:
    print(f"File size: {dog_data.get('fileSizeBytes', 'Unknown')} bytes")
    print(f"Image URL: {dog_data['url']}")
    
    # Display the image in Jupyter notebook
    try:
        display(Image(url=dog_data['url'], width=400))
    except:
        print("Could not display image, but here's the URL:", dog_data['url'])
else:
    print("Error getting dog image:", dog_data)
"""

# Cell 5: Test the client we created
"""
from random_dog_client import RandomDogMCPClient

# Test our custom client
async with RandomDogMCPClient() as client:
    # Get dog data
    dog_info = await client.get_random_dog()
    print("Dog info from client:", dog_info)
    
    # Get just URL
    dog_url = await client.get_dog_image_url()
    print("Dog URL from client:", dog_url)
    
    # Show OpenAI compatible tools
    openai_tools = await client.get_openai_function_tools()
    print("OpenAI tools:", [tool.name for tool in openai_tools])
"""

if __name__ == "__main__":
    print("🐕 Random Dog MCP Demo")
    print("=" * 40)
    print("Copy the code blocks above into Jupyter notebook cells to test the random dog MCP server!")
    print("\nFiles created:")
    print("- random_dog_server.py: The MCP server")
    print("- random_dog_client.py: The MCP client")
    print("- test_random_dog.py: Test script")
    print("- random_dog_demo.py: This demo file")
    print("\nTo run in Jupyter, copy the code from the triple quotes into separate cells.") 