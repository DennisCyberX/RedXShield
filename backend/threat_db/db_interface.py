import sqlite3
import json
from datetime import datetime

DB_PATH = "./backend/threat_db/storage.sqlite3"

def connect():
    return sqlite3.connect(DB_PATH)

def insert_threat_record(domain, risk_score, tags, shap_values):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO threats (domain, risk_score, tags, shap_values, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (domain, risk_score, json.dumps(tags), json.dumps(shap_values), datetime.utcnow()))
    conn.commit()
    conn.close()

def get_threat_record(domain):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT domain, risk_score, tags, shap_values, created_at FROM threats WHERE domain = ?", (domain,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {
            "domain": row[0],
            "risk_score": row[1],
            "tags": json.loads(row[2]),
            "shap_values": json.loads(row[3]),
            "created_at": row[4]
        }
    return None
