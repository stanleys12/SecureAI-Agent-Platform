class MetricsManager:
    """
    Tracks and reports execution statistics, specifically
    how many attacks were stopped by our defense layers vs allowed.
    """
    def __init__(self):
        self.stats = {
            "total_calls": 0,
            "allowed_calls": 0,
            "blocked_by_policy": 0,
            "blocked_by_defense": 0
        }

    def record_allowed(self):
        self.stats["total_calls"] += 1
        self.stats["allowed_calls"] += 1

    def record_blocked_policy(self):
        self.stats["total_calls"] += 1
        self.stats["blocked_by_policy"] += 1

    def record_blocked_defense(self):
        self.stats["total_calls"] += 1
        self.stats["blocked_by_defense"] += 1
        
    def generate_report(self):
        return f"""
📊 === SECURITY METRICS REPORT === 📊
Total Tool Executions Attempted : {self.stats['total_calls']}
Calls Safely Authorized         : {self.stats['allowed_calls']}
Blocked by Policy Engine        : {self.stats['blocked_by_policy']} (Rules/Domain constraints)
Blocked by Defense Layer        : {self.stats['blocked_by_defense']} (Anomalies/Attacks)
=====================================
"""
