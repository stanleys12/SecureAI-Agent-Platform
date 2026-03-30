from policy.policy_engine import PolicyEngine

class SecurityGuard:
    """
    The enforcement logic component of the Sandbox Phase.
    Acts as the strict gatekeeper that consults the Policy Engine 
    before any action occurs.
    """
    def __init__(self, policy_engine: PolicyEngine = None):
        self.policy_engine = policy_engine or PolicyEngine()
        
    def check_permissions(self, tool_name: str, args: dict) -> bool:
        """Consults the policy engine for validation."""
        return self.policy_engine.validate(tool_name, args)
