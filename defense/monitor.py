import time
from defense.anomaly_detector import AnomalyDetector
from defense.response import DefenseResponse

class DefenseMonitor:
    """
    The orchestrator for the Defense Layer. Tracks behavior,
    logs history, and trips alarms if an attack is underway.
    """
    def __init__(self):
        self.call_history = []
        self.detector = AnomalyDetector()
        self.responder = DefenseResponse()
        
    def log_and_inspect(self, tool_name: str, args: dict) -> bool:
        """
        Logs the call and inspects for anomalies.
        Returns True if safe, False if an anomaly was detected and blocked.
        """
        timestamp = time.time()
        call_record = {
            "timestamp": timestamp,
            "tool": tool_name,
            "args": args
        }
        self.call_history.append(call_record)
        
        # Check for anomalies
        anomaly = self.detector.detect(self.call_history, call_record)
        
        if anomaly:
            print(f"[DefenseMonitor] BLOCKING: Anomaly detected prior to execution.")
            self.responder.trigger_alert(anomaly, call_record)
            return False
            
        return True
