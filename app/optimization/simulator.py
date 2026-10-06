def what_if(
    current_cost,
    idle_hours_per_day=4,
    idle_threshold=10,
    archive_old_data=True
):
    # Demonstration simulator. In a production implementation, the
    # current_cost would be derived from verified provider pricing.
    shutdown_saving = min(current_cost * 0.35, idle_hours_per_day * 30 * 0.05)

    archive_saving = current_cost * 0.05 if archive_old_data else 0
    optimized = max(0, current_cost - shutdown_saving - archive_saving)
    saving = current_cost - optimized

    return {
        "current_cost": round(current_cost, 2),
        "optimized_cost": round(optimized, 2),
        "saving": round(saving, 2),
        "saving_percent": round((saving / current_cost * 100), 2) if current_cost else 0,
        "parameters": {
            "idle_hours_per_day": idle_hours_per_day,
            "idle_threshold": idle_threshold,
            "archive_old_data": archive_old_data,
        }
    }
