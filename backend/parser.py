import re
from datetime import datetime


LOG_PATTERN = re.compile(
    r"(?P<timestamp>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}) "
    r"(?P<host>\S+) "
    r"(?P<process>[\w\-]+)(?:\[\d+\])?: "
    r"(?P<message>.*)"
)


def parse_line(line):
    match = LOG_PATTERN.match(line.strip())

    if not match:
        return {
            "raw": line.strip(),
            "parsed": False
        }

    data = match.groupdict()
    data["parsed"] = True
    data["raw"] = line.strip()

    return data


def parse_file(path):
    events = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                events.append(parse_line(line))

    return events
