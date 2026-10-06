from app.agent.tools import (
    get_metrics,
    analyze_idle,
    detect_usage_anomalies,
    simulate_cost,
    list_recommendations,
)

class CloudOptimizationAgent:
    """
    Lightweight tool-using agent.
    It selects analysis tools based on the user's goal and combines
    their observations into an explainable response.

    This is intentionally deterministic and works without an external
    LLM. An LLM adapter can be added later for natural-language planning.
    """

    def run(self, goal="find opportunities to reduce cloud cost"):
        observations = {}

        # Tool selection / planning
        observations["metrics"] = get_metrics()
        observations["usage"] = analyze_idle()

        if "anomal" in goal.lower() or "all" in goal.lower():
            observations["anomalies"] = detect_usage_anomalies()

        observations["simulation"] = simulate_cost()
        observations["recommendations"] = list_recommendations()

        actions = []
        for rec in observations["recommendations"]:
            actions.append({
                "resource": rec["resource_id"],
                "action": rec["recommendation"],
                "evidence": rec["reason"],
                "confidence": rec["confidence"],
                "estimated_saving": rec["estimated_saving"],
                "approval_required": True,
            })

        return {
            "goal": goal,
            "plan": [
                "inspect resources",
                "analyze historical utilization",
                "inspect anomalies when requested",
                "simulate optimization",
                "produce explainable recommendations",
            ],
            "observations": observations,
            "actions": actions,
        }

if __name__ == "__main__":
    import json
    result = CloudOptimizationAgent().run(
        "Find opportunities to reduce cloud cost and check anomalies"
    )
    print(json.dumps(result, indent=2, default=str))
