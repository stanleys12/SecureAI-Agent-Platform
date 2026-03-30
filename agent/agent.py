from typing import List, Dict, Any
from tools.base_tool import BaseTool

class DummyLLMAgent:
    """
    A foundational wrapper representing the LLM Agent that can route intent to tools.
    For Phase 1 (and keeping it local), we implement a mock decision engine.
    In a real app, 'run' would send a prompt + tool JSON array to OpenAI/Anthropic
    and parse the tool_calls property.
    """
    def __init__(self, tools: List[BaseTool]):
        # Store tools mapped by their name so the agent can look them up
        self.tools = {tool.name: tool for tool in tools}

    def get_tool_descriptions(self) -> str:
        """Returns what the LLM typically sees when considering tools."""
        descriptions = []
        for name, tool in self.tools.items():
            descriptions.append(f"- {name}: {tool.description}")
        return "\n".join(descriptions)

    def run(self, user_input: str) -> str:
        """
        Takes user input, uses the prompt/LLM to decide which tool to call, 
        and executes it.
        """
        print(f"\\n[Agent] Receiving task: '{user_input}'")
        
        # In a real environment, this goes out to the LLM. 
        # We're keeping it deterministic for foundational testing right now.
        tool_call = self._mock_llm_decision(user_input)
        
        if not tool_call:
            return "[Agent] I decided not to use any tools for this input."

        tool_name = tool_call.get("tool")
        tool_args = tool_call.get("args", {})
        
        print(f"[Agent] Decided to execute: {tool_name}({tool_args})")
        
        # Enforce Tool Existence
        if tool_name not in self.tools:
            return f"[Agent Error] Attempted to use non-existent tool '{tool_name}'."

        # Execute Tool
        tool = self.tools[tool_name]
        try:
            result = tool.execute(**tool_args)
            print(f"[Agent] Tool returned: {result}")
            return f"Success! Tool Result: {result}"
        except Exception as e:
            return f"[Agent Error] Tool crashed: {str(e)}"

    def _mock_llm_decision(self, user_input: str) -> Dict[str, Any]:
        """
        Simulates an LLM identifying the right tool based on keywords.
        """
        prompt = user_input.lower()
        if "fetch" in prompt or "http" in prompt or "website" in prompt:
            return {
                "tool": "http_request", 
                "args": {"method": "GET", "url": "https://jsonplaceholder.typicode.com/todos/1"}
            }
        elif "database" in prompt or "select" in prompt or "query" in prompt:
            return {
                "tool": "db_query", 
                "args": {"query": "SELECT * FROM users"}
            }
        elif "read" in prompt and "file" in prompt:
            return {
                "tool": "file_reader", 
                "args": {"filepath": "secure-ai-agent/tools/base_tool.py"}
            }
        return None
