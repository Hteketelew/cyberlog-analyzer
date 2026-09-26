from backend.analyzer import analyze_events


def test_failed_login_detection():

    events = [
        {
            "message":
            "Failed password for admin from 10.0.0.5"
        }
    ]

    alerts = analyze_events(events)

    assert len(alerts) == 1
    assert alerts[0]["type"] == "failed_login"


def test_bruteforce_detection():

    events = []

    for _ in range(5):
        events.append({
            "message":
            "Failed password for admin from 10.0.0.5"
        })

    alerts = analyze_events(events)

    assert any(
        alert["type"] == "possible_bruteforce"
        for alert in alerts
    )
