from datetime import datetime, timezone

def recommend_s3_archival(objects, old_days=180):
    """
    LocalStack does not provide real historical object access counts.
    access_count can therefore be populated from application logs later.
    """
    now = datetime.now(timezone.utc)
    results = []

    for obj in objects:
        last = obj.get("last_modified")
        if not last:
            continue

        dt = datetime.fromisoformat(last.replace("Z", "+00:00"))
        age_days = (now - dt).days

        if age_days >= old_days and obj.get("access_count", 0) < 5:
            size_gb = obj.get("size_bytes", 0) / (1024 ** 3)
            results.append({
                "bucket": obj["bucket"],
                "object_key": obj["object_key"],
                "age_days": age_days,
                "size_gb": round(size_gb, 4),
                "recommendation": "Move to lower-cost/cold storage",
                "reason": f"Object age is {age_days} days and access count is low.",
            })

    return results
