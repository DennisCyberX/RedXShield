import re
import json
from datetime import datetime
from typing import Dict, Any, Optional
import hashlib
from pathlib import Path

# Domain Validation Utilities
def is_valid_domain(domain: str) -> bool:
    """Validate domain format using RFC 1035 rules"""
    if not domain or len(domain) > 253:
        return False
        
    pattern = (
        r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63})*\.?$'
    )
    return bool(re.fullmatch(pattern, domain))

def normalize_domain(domain: str) -> Optional[str]:
    """Normalize domain to lowercase and strip whitespace"""
    if not domain:
        return None
    return domain.lower().strip()

# Data Serialization
class DateTimeEncoder(json.JSONEncoder):
    """Extended JSON encoder that handles datetime objects"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def safe_json_dumps(data: Dict) -> str:
    """Safely serialize dictionary to JSON with datetime support"""
    return json.dumps(data, cls=DateTimeEncoder)

def safe_json_loads(json_str: str) -> Dict:
    """Safely deserialize JSON with datetime parsing"""
    def datetime_parser(dct):
        for k, v in dct.items():
            if isinstance(v, str):
                try:
                    dct[k] = datetime.fromisoformat(v)
                except (ValueError, TypeError):
                    pass
        return dct
    return json.loads(json_str, object_hook=datetime_parser)

# Database Utilities
def generate_db_checksum(db_path: str) -> str:
    """Generate SHA256 checksum of database file"""
    hash_sha256 = hashlib.sha256()
    with open(db_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def backup_database(source_path: str, backup_dir: str = "backups") -> str:
    """Create timestamped database backup"""
    Path(backup_dir).mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{backup_dir}/storage_{timestamp}.sqlite3"
    
    with open(source_path, 'rb') as src, open(backup_path, 'wb') as dst:
        dst.write(src.read())
    
    return backup_path

# Threat Intelligence Utilities
def calculate_threat_level(indicators: Dict) -> float:
    """Calculate composite threat score (0-1) from indicators"""
    malicious = indicators.get('malicious', 0)
    suspicious = indicators.get('suspicious', 0)
    total = indicators.get('total_engines', 1)  # Prevent division by zero
    
    # Weighted score calculation
    return min(1.0, (malicious * 0.7 + suspicious * 0.3) / total)

def merge_threat_intel(existing: Dict, new: Dict) -> Dict:
    """Merge two threat intelligence reports"""
    merged = existing.copy()
    
    # Merge indicators
    for key in ['malicious', 'suspicious']:
        merged[key] = max(existing.get(key, 0), new.get(key, 0))
    
    # Merge additional data
    if 'sources' in existing or 'sources' in new:
        merged['sources'] = list(set(
            existing.get('sources', []) + new.get('sources', [])
        ))
    
    merged['last_updated'] = datetime.now()
    return merged
