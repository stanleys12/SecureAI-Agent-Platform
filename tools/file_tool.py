import os
from tools.base_tool import BaseTool

class FileTool(BaseTool):
    """
    A utility tool for the agent to read local files. This is a vector
    for Local File Inclusion (LFI) attacks if a prompt instructs it
    to read /etc/passwd or application code.
    """
    @property
    def name(self) -> str:
        return "file_reader"

    @property
    def description(self) -> str:
        return "Reads the contents of a file on the local filesystem. Provide 'filepath' as a string."

    def execute(self, filepath: str, **kwargs):
        try:
            if not os.path.exists(filepath):
                return {"error": f"File '{filepath}' does not exist."}
                
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return {"content": content[:2000]} # Truncate huge files
        except Exception as e:
            return {"error": str(e)}
