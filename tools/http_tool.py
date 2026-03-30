import requests
from tools.base_tool import BaseTool

class HTTPTool(BaseTool):
    """
    A basic tool to make HTTP requests. Very useful for an agent,
    but highly dangerous if unconstrained (e.g. CSRF, internal SSRF).
    """
    @property
    def name(self) -> str:
        return "http_request"

    @property
    def description(self) -> str:
        return "Makes an HTTP request to a given URL. Provide 'method' (GET, POST), 'url', and optional 'headers' and 'json_data'."

    def execute(self, method: str, url: str, headers: dict = None, json_data: dict = None, **kwargs):
        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=headers or {},
                json=json_data,
                timeout=5
            )
            return {
                "status_code": response.status_code,
                "content": response.text[:1000] # Truncate to avoid massive payloads
            }
        except Exception as e:
            return {"error": str(e)}
