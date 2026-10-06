from app.database.database import init_db
from app.collectors.collector import save_collection
from app.analytics.usage_analysis import analyze_usage
from app.optimization.recommendation_engine import (
    generate_recommendations,
    save_recommendations,
)

def main():
    init_db()
    save_collection()

    summary = analyze_usage()

    if summary.empty:
        print("No historical usage data yet.")
        print("Run: python app/seed_demo.py")
        return

    recommendations = generate_recommendations(summary)
    save_recommendations(recommendations)

    print("\n========== PIPELINE SUMMARY ==========")
    print(summary.to_string(index=False))
    print(f"\nRecommendations generated: {len(recommendations)}")

if __name__ == "__main__":
    main()
