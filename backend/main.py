from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from parser import parse_line
from analyzer import analyze_events


app = FastAPI(
    title="CyberLog Analyzer",
    description="A cybersecurity log analysis platform",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "name": "CyberLog Analyzer",
        "status": "running"
    }


@app.post("/analyze")
async def analyze_log(file: UploadFile = File(...)):
    content = await file.read()

    text = content.decode("utf-8", errors="ignore")

    events = [
        parse_line(line)
        for line in text.splitlines()
        if line.strip()
    ]

    alerts = analyze_events(events)

    return {
        "filename": file.filename,
        "total_lines": len(events),
        "alerts": alerts
    }
