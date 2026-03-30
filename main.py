import sys
import os

# Ensure Python can find our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.http_tool import HTTPTool
from tools.db_tool import DBTool
from tools.file_tool import FileTool
from agent.agent import DummyLLMAgent

def main():
    print("=== Secure AI Agent Platform ===")
    print("--- Phase 1: Basic Agent + Tools Demo ---\n")
    
    # Initialize Tools
    tools = [
        HTTPTool(),
        DBTool(),
        FileTool()
    ]
    
    # Initialize Agent
    agent = DummyLLMAgent(tools)
    
    print("Available Tools Registered by Agent:")
    print(agent.get_tool_descriptions())
    print("\n-------------------------------------------")
    
    # 1. Test HTTP Tool
    agent.run("Agent, can you fetch some data from a website using HTTP?")
    
    # 2. Test DB Tool
    agent.run("Agent, query the database and select all users.")
    
    # 3. Test File Tool
    agent.run("Agent, read the python file tools/base_tool.py from the local filesystem.")

if __name__ == "__main__":
    main()
