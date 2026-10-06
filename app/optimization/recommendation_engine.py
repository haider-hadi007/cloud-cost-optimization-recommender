from app.database.database import get_connection
from app.optimization.cost_engine import simulate_shutdown

def generate_recommendations(summary):
    recommendations = []

    for _, row in summary.iterrows():
        idle = float(row["idle_percent"])
        avg_cpu = float(row["avg_cpu"])
        resource = row["resource_id"]

        if idle >= 70 and avg_cpu < 10:
            confidence = min(0.99, 0.65 + idle / 300)
            estimate = simulate_shutdown(18.0, 4.0)

            recommendations.append({
                "resource_id": resource,
                "recommendation": "Schedule shutdown during low-usage periods",
                "reason": (
                    f"Idle utilization is {idle:.1f}% and average CPU is "
                    f"{avg_cpu:.1f}%. Historical data indicates sustained low demand."
                ),
                "confidence": round(confidence, 2),
                "estimated_saving": estimate["saving"],
            })

        elif avg_cpu < 20:
            recommendations.append({
                "resource_id": resource,
                "recommendation": "Review resource sizing",
                "reason": f"Average CPU utilization is only {avg_cpu:.1f}%.",
                "confidence": 0.72,
                "estimated_saving": 5.0,
            })

    return recommendations

def save_recommendations(recommendations):
    with get_connection() as conn:
        for r in recommendations:
            conn.execute(
                """INSERT INTO recommendations
                (resource_id,recommendation,reason,confidence,estimated_saving)
                VALUES (?,?,?,?,?)""",
                (
                    r["resource_id"], r["recommendation"], r["reason"],
                    r["confidence"], r["estimated_saving"]
                )
            )
        conn.commit()
