# Complete Project Flow

1. Docker and LocalStack provide a local cloud-like environment.
2. Python collectors inspect Docker containers and LocalStack S3.
3. Metrics are persisted in SQLite.
4. Historical analytics calculate average utilization, idle percentage and peak hours.
5. The cost engine estimates current and optimized costs using configurable demonstration prices.
6. Optimization rules create explainable recommendations.
7. Isolation Forest detects unusual utilization.
8. Random Forest predicts utilization from historical features.
9. A tool-using optimization agent calls metrics, analytics, anomaly and simulation tools.
10. Streamlit visualizes the system.
11. What-if simulation estimates savings under different policies.
12. Evaluation measures anomaly counts and prediction MAE.
13. Human approval is required before any real remediation.
