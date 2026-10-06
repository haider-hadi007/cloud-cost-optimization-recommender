from app.config import (
    COMPUTE_PER_HOUR,
    STORAGE_HOT_PER_GB_MONTH,
    STORAGE_COLD_PER_GB_MONTH,
)

def compute_container_monthly_cost(active_hours=720):
    return active_hours * COMPUTE_PER_HOUR

def compute_storage_monthly_cost(size_gb, tier="hot"):
    rate = STORAGE_COLD_PER_GB_MONTH if tier == "cold" else STORAGE_HOT_PER_GB_MONTH
    return size_gb * rate

def calculate_savings(current_cost, optimized_cost):
    saving = max(0.0, current_cost - optimized_cost)
    pct = (saving / current_cost * 100) if current_cost else 0.0
    return {
        "current_cost": round(current_cost, 2),
        "optimized_cost": round(optimized_cost, 2),
        "saving": round(saving, 2),
        "saving_percent": round(pct, 2),
        "annual_saving": round(saving * 12, 2),
    }

def simulate_shutdown(current_monthly_cost, idle_hours_per_day):
    idle_hours_per_month = idle_hours_per_day * 30
    saving = min(current_monthly_cost, idle_hours_per_month * COMPUTE_PER_HOUR)
    return calculate_savings(current_monthly_cost, current_monthly_cost - saving)
