from datetime import datetime, timezone
import boto3
from app.config import LOCALSTACK_ENDPOINT, AWS_REGION, AWS_ACCESS_KEY, AWS_SECRET_KEY

def s3_client():
    return boto3.client(
        "s3",
        endpoint_url=LOCALSTACK_ENDPOINT,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION,
    )

def collect_s3_objects():
    s3 = s3_client()
    rows = []
    checked = datetime.now(timezone.utc).isoformat()

    buckets = s3.list_buckets().get("Buckets", [])
    for b in buckets:
        bucket = b["Name"]
        response = s3.list_objects_v2(Bucket=bucket)
        for obj in response.get("Contents", []):
            rows.append({
                "bucket": bucket,
                "object_key": obj["Key"],
                "size_bytes": obj.get("Size", 0),
                "last_modified": obj["LastModified"].isoformat(),
                "storage_class": obj.get("StorageClass", "STANDARD"),
                "access_count": 0,
                "last_checked": checked,
            })
    return rows

if __name__ == "__main__":
    for row in collect_s3_objects():
        print(row)
