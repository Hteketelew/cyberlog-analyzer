def analyze_events(events):
    alerts = []

    suspicious_keywords = [
        "failed",
        "failure",
        "unauthorized",
        "invalid",
        "denied",
        "attack",
        "malware",
        "error",
        "brute force",
        "login failed"
    ]

    for event in events:
        message = event.get("message", "").lower()

        for keyword in suspicious_keywords:
            if keyword in message:
                alerts.append({
                    "type": "Suspicious Activity",
                    "severity": "Medium",
                    "keyword": keyword,
                    "message": event.get("message", ""),
                    "timestamp": event.get("timestamp"),
                    "host": event.get("host"),
                    "process": event.get("process")
                })
                break

    return alerts
