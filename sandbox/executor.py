from tools.base_tool import BaseTool
from sandbox.guard import SecurityGuard
from defense.monitor import DefenseMonitor
from evaluation.metrics import MetricsManager

class SecureToolExecutor:
    """
    The Sandbox Executor Phase.
    Securely wraps all BaseTool executions, completely abstracting away
    raw access to the underlying APIs and local systems.
    """
    def __init__(self, guard: SecurityGuard = None, monitor: DefenseMonitor = None, metrics: MetricsManager = None):
        self.guard = guard or SecurityGuard()
        self.monitor = monitor or DefenseMonitor()
        self.metrics = metrics or MetricsManager()

    def execute_safely(self, tool: BaseTool, **kwargs):
        """
        Intercepts the execute call, validates it through the Guard, 
        and only then executes it if permitted.
        """
        print(f"\n[Sandbox] Intercepting execution request for tool '{tool.name}'...")
        
        # 1. Defense Monitor Inspection
        is_safe = self.monitor.log_and_inspect(tool.name, kwargs)
        if not is_safe:
            self.metrics.record_blocked_defense()
            return {"error": "SECURITY BLOCK: Intrusion Detected by Defense Monitor."}
        
        # 2. Strict Policy Enforcement
        is_allowed = self.guard.check_permissions(tool.name, kwargs)
        
        if not is_allowed:
            self.metrics.record_blocked_policy()
            return {"error": "SECURITY BLOCK: Action denied by Sandbox Policy Engine."}
            
        print(f"[Sandbox] Authorization granted. Executing '{tool.name}'.")
        self.metrics.record_allowed()
        return tool.execute(**kwargs)
