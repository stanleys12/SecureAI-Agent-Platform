class DefenseResponse:
    """
    Handles actions taken when an anomaly or attack is detected.
    """
    def trigger_alert(self, reason: str, context: dict):
        """
        In a real system, this might page incident response, disable the agent,
        or log the event to a SIEM.
        """
        print(f"\n🚨 [DEFENSE ALERT] Intrusion Detection System Tripped!")
        print(f"🚨 Reason: {reason}")
        print(f"🚨 Context Tool: {context.get('tool')}")
        print(f"🚨 Context Args: {context.get('args')}\n")
