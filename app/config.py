from pathlib import Path
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

DB_PATH = ROOT / "cloud_optimizer.db"
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
MODEL_DIR = ROOT / "models"

LOCALSTACK_ENDPOINT = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "test")

# Demonstration pricing model. Replace these with verified provider pricing
# before claiming real-world billing accuracy.
COMPUTE_PER_HOUR = float(os.getenv("COMPUTE_PER_HOUR", "0.05"))
STORAGE_HOT_PER_GB_MONTH = float(os.getenv("STORAGE_HOT_PER_GB_MONTH", "0.023"))
STORAGE_COLD_PER_GB_MONTH = float(os.getenv("STORAGE_COLD_PER_GB_MONTH", "0.01"))

for p in [RAW_DIR, PROCESSED_DIR, MODEL_DIR]:
    p.mkdir(parents=True, exist_ok=True)
