from datetime import datetime, timezone
import docker

def _cpu_percent(stats):
    cpu = stats.get("cpu_stats", {})
    precpu = stats.get("precpu_stats", {})
    cpu_delta = cpu.get("cpu_usage", {}).get("total_usage", 0) - precpu.get("cpu_usage", {}).get("total_usage", 0)
    system_delta = cpu.get("system_cpu_usage", 0) - precpu.get("system_cpu_usage", 0)
    online = cpu.get("online_cpus") or 1
    if system_delta > 0 and cpu_delta >= 0:
        return round((cpu_delta / system_delta) * online * 100, 2)
    return 0.0

def _memory_percent(stats):
    mem = stats.get("memory_stats", {})
    usage = mem.get("usage", 0)
    limit = mem.get("limit", 0)
    return round((usage / limit) * 100, 2) if limit else 0.0

def _network_mb(stats):
    networks = stats.get("networks") or {}
    rx = sum(v.get("rx_bytes", 0) for v in networks.values()) / (1024**2)
    tx = sum(v.get("tx_bytes", 0) for v in networks.values()) / (1024**2)
    return round(rx, 4), round(tx, 4)

def collect_container_metrics():
    client = docker.from_env()
    rows = []
    now = datetime.now(timezone.utc).isoformat()

    for container in client.containers.list():
        stats = container.stats(stream=False)
        rx, tx = _network_mb(stats)
        started = container.attrs.get("State", {}).get("StartedAt")
        runtime_hours = 0.0
        if started:
            try:
                started_dt = datetime.fromisoformat(started.replace("Z", "+00:00"))
                runtime_hours = max(0, (datetime.now(timezone.utc) - started_dt).total_seconds() / 3600)
            except ValueError:
                pass

        rows.append({
            "resource_id": container.name,
            "resource_type": "docker_container",
            "name": container.name,
            "timestamp": now,
            "cpu_usage": _cpu_percent(stats),
            "memory_usage": _memory_percent(stats),
            "network_rx_mb": rx,
            "network_tx_mb": tx,
            "runtime_hours": round(runtime_hours, 4),
            "status": container.status,
        })

    return rows

if __name__ == "__main__":
    for row in collect_container_metrics():
        print(row)
