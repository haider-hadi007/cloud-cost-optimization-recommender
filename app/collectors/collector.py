import sqlite3
from app.database.database import init_db, get_connection
from app.collectors.docker_collector import collect_container_metrics
from app.collectors.s3_collector import collect_s3_objects

def save_collection():
    init_db()
    containers = collect_container_metrics()
    objects = collect_s3_objects()

    with get_connection() as conn:
        for r in containers:
            conn.execute(
                """INSERT INTO resources(resource_id, resource_type, name)
                   VALUES (?, ?, ?)
                   ON CONFLICT(resource_id) DO NOTHING""",
                (r["resource_id"], r["resource_type"], r["name"])
            )
            conn.execute(
                """INSERT INTO usage_metrics
                   (resource_id,timestamp,cpu_usage,memory_usage,network_rx_mb,
                    network_tx_mb,runtime_hours,status)
                   VALUES (?,?,?,?,?,?,?,?)""",
                (r["resource_id"], r["timestamp"], r["cpu_usage"], r["memory_usage"],
                 r["network_rx_mb"], r["network_tx_mb"], r["runtime_hours"], r["status"])
            )

        for o in objects:
            conn.execute(
                """INSERT INTO s3_objects
                   (bucket,object_key,size_bytes,last_modified,storage_class,access_count,last_checked)
                   VALUES (?,?,?,?,?,?,?)
                   ON CONFLICT(bucket,object_key) DO UPDATE SET
                     size_bytes=excluded.size_bytes,
                     last_modified=excluded.last_modified,
                     storage_class=excluded.storage_class,
                     last_checked=excluded.last_checked""",
                (o["bucket"], o["object_key"], o["size_bytes"], o["last_modified"],
                 o["storage_class"], o["access_count"], o["last_checked"])
            )
        conn.commit()

    print(f"Collected {len(containers)} containers and {len(objects)} S3 objects.")

if __name__ == "__main__":
    save_collection()
