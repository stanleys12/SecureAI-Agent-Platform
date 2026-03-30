import json
import logging
from urllib.parse import urlparse

class PolicyEngine:
    """
    The Core Policy Engine.
    Loads JSON-based policies and validates every tool execution attempt
    against strict constraints.
    """
    def __init__(self, policy_file: str = None):
        import os
        if policy_file is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.policy_file = os.path.join(base_dir, "policy", "policies.json")
        else:
            self.policy_file = policy_file
        self.policies = self._load_policies()

    def _load_policies(self) -> dict:
        try:
            with open(self.policy_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to load policies: {e}")
            return {}

    def validate(self, tool_name: str, tool_args: dict) -> bool:
        """
        Validates if the current tool execution is allowed under the loaded policies.
        Returns True if allowed, False if blocked.
        """
        tool_policy = self.policies.get(tool_name)
        
        # Default Deny: If tool isn't in policy or is explicitly denied, block it.
        if not tool_policy or tool_policy.get("action", "deny") == "deny":
            print(f"[PolicyEngine] BLOCKED: Tool '{tool_name}' is not allowed or missing from policy.")
            return False

        # Specific Tool Constraints
        if tool_name == "http_request":
            return self._validate_http(tool_args, tool_policy)
            
        elif tool_name == "db_query":
            return self._validate_db(tool_args, tool_policy)

        elif tool_name == "file_reader":
            # If action was allow, it's allowed. We don't have constraints yet.
            return True

        # If we reach here and it was action=allow, it passes
        return True

    def _validate_http(self, args: dict, policy: dict) -> bool:
        url = args.get("url", "")
        method = args.get("method", "").upper()
        
        # 1. Check Allowed Methods
        allowed_methods = [m.upper() for m in policy.get("methods", [])]
        if method not in allowed_methods:
            print(f"[PolicyEngine] BLOCKED: HTTP Method '{method}' is not allowed.")
            return False
            
        # 2. Check Allowed Domains
        try:
            parsed_domain = urlparse(url).netloc
            allowed_domains = policy.get("allowed_domains", [])
            # Support exact matches for now
            if parsed_domain not in allowed_domains:
                print(f"[PolicyEngine] BLOCKED: Domain '{parsed_domain}' is not allowed.")
                return False
        except Exception:
            return False
            
        return True

    def _validate_db(self, args: dict, policy: dict) -> bool:
        query = args.get("query", "").strip().upper()
        
        # Check Read-Only Constraint
        if policy.get("read_only", False):
            # Extremely basic SQL validation - real implementations would parse the AST
            if not query.startswith("SELECT"):
                print(f"[PolicyEngine] BLOCKED: Write operations are forbidden. Rule triggered for query type.")
                return False
                
        return True
