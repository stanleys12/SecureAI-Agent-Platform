import time

class AnomalyDetector:
    """
    Detects suspicious behavior patterns such as rapid-fire requests,
    SQL injections, or potential data exfiltration.
    """
    def __init__(self):
        self.rate_limit_window = 10 # seconds
        self.max_calls_per_window = 5
        self.suspicious_keywords = [
            "/etc/passwd", 
            "DROP TABLE", 
            "UNION SELECT", 
            "aws_access_key", 
            "secret",
            "1=1"
        ]

    def detect(self, call_history: list, current_call: dict) -> str:
        """
        Returns the name/reason of the anomaly if detected, else None.
        """
        # 1. Rate Limiting (Velocity Check)
        recent_calls = [
            c for c in call_history 
            if current_call["timestamp"] - c["timestamp"] < self.rate_limit_window
        ]
        if len(recent_calls) > self.max_calls_per_window:
            return "HIGH_FREQUENCY_CALLS"

        # 2. Payload Inspection (Suspicious Keywords)
        args_str = str(current_call["args"]).upper()
        for keyword in self.suspicious_keywords:
            if keyword.upper() in args_str:
                return f"SUSPICIOUS_PAYLOAD_KEYWORD_MATCH: '{keyword}'"

        # 3. Exfiltration Patterns (Data in URL)
        if current_call["tool"] == "http_request":
            url = current_call["args"].get("url", "")
            if len(url) > 200: # Unusually long URL might contain exfiltrated data
                return "POTENTIAL_DATA_EXFILTRATION_IN_URL"

        return None
