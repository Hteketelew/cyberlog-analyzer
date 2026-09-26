import re
from collections import Counter


FAILED_LOGIN_PATTERNS = [
    "Failed password",
    "authentication failure",
    "Failed login",
    "Invalid user"
]


def analyze_events(events):
    results = []

    failed_ips = []

    for event in events:
        message = event.get("message", "")

        if any(pattern.lower() in message.lower()
               for pattern in FAILED_LOGIN_PATTERNS):

            ip_match = re.search(
                r"(?:from|rhost=)\s*(\d+\.\d+\.\d+\.\d+)",
                message
            )

            ip = ip_match.group(1) if ip_match else "unknown"

            failed_ips.append(ip)

            results.append({
                "type": "failed_login",
                "severity": "medium",
                "ip": ip,
                "message": message
            })

    counts = Counter(failed_ips)

    for ip, count in counts.items():
        if ip != "unknown" and count >= 5:
            results.append({
                "type": "possible_bruteforce",
                "severity": "high",
                "ip": ip,
                "count": count,
                "message": f"{count} failed login attempts detected"
            })

    return results
