import sqlite3
from app.config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_id TEXT UNIQUE NOT NULL,
    resource_type TEXT NOT NULL,
    name TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS usage_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    cpu_usage REAL DEFAULT 0,
    memory_usage REAL DEFAULT 0,
    network_rx_mb REAL DEFAULT 0,
    network_tx_mb REAL DEFAULT 0,
    runtime_hours REAL DEFAULT 0,
    status TEXT,
    FOREIGN KEY(resource_id) REFERENCES resources(resource_id)
);

CREATE TABLE IF NOT EXISTS s3_objects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bucket TEXT NOT NULL,
    object_key TEXT NOT NULL,
    size_bytes INTEGER DEFAULT 0,
    last_modified TEXT,
    storage_class TEXT DEFAULT 'STANDARD',
    access_count INTEGER DEFAULT 0,
    last_checked TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(bucket, object_key)
);

CREATE TABLE IF NOT EXISTS cost_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    estimated_cost REAL NOT NULL,
    currency TEXT DEFAULT 'USD'
);

CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_id TEXT NOT NULL,
    recommendation TEXT NOT NULL,
    reason TEXT NOT NULL,
    confidence REAL NOT NULL,
    estimated_saving REAL DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS optimization_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recommendation_id INTEGER,
    resource_id TEXT NOT NULL,
    action_type TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    executed_at TEXT,
    result TEXT
);
"""

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.executescript(SCHEMA)
        conn.commit()

if __name__ == "__main__":
    init_db()
    print(f"Database initialized: {DB_PATH}")
