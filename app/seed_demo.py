import random
from datetime import datetime, timedelta, timezone
from app.database.database import init_db, get_connection

def seed():
    init_db()
    now = datetime.now(timezone.utc)

    resources = [
        ("demo-api", "docker_container", "demo-api"),
        ("demo-worker", "docker_container", "demo-worker"),
        ("demo-batch", "docker_container", "demo-batch"),
    ]

    with get_connection() as conn:
        for rid, rtype, name in resources:
            conn.execute(
                """INSERT INTO resources(resource_id,resource_type,name)
                   VALUES(?,?,?)
                   ON CONFLICT(resource_id) DO NOTHING""",
                (rid, rtype, name)
            )

        for i in range(144):
            ts = now - timedelta(minutes=10 * (143 - i))
            hour = ts.hour

            # Different behavior patterns for research/testing
            api_cpu = max(2, 15 + 45 * (1 if 9 <= hour <= 18 else 0) + random.gauss(0, 5))
            worker_cpu = max(1, 8 + random.gauss(0, 3))
            batch_cpu = max(1, 5 + (70 if 13 <= hour <= 15 else 0) + random.gauss(0, 5))

            for rid, cpu in [
                ("demo-api", api_cpu),
                ("demo-worker", worker_cpu),
                ("demo-batch", batch_cpu),
            ]:
                mem = max(2, cpu * 0.6 + random.gauss(8, 2))
                conn.execute(
                    """INSERT INTO usage_metrics
                    (resource_id,timestamp,cpu_usage,memory_usage,
                     network_rx_mb,network_tx_mb,runtime_hours,status)
                    VALUES (?,?,?,?,?,?,?,?)""",
                    (
                        rid, ts.isoformat(), round(cpu, 2), round(mem, 2),
                        round(random.uniform(0.1, 5), 3),
                        round(random.uniform(0.1, 3), 3),
                        round(i / 6, 2), "running"
                    )
                )

        conn.commit()

    print("Demo historical data created: 432 usage records.")

if __name__ == "__main__":
    seed()
