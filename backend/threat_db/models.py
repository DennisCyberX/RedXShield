from typing import TypedDict, Optional
from datetime import datetime

class AnalysisResult(TypedDict):
    domain: str
    risk_score: float
    indicators: dict
    timestamp: str
    virustotal: Optional[dict]
    whois_analysis: Optional[dict]

class ThreatIntel(TypedDict):
    source: str
    data: dict
    timestamp: str
