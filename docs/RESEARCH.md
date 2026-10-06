# Research Design

## Research Question

Can historical resource utilization patterns be used to identify inefficiencies and generate explainable cloud cost optimization recommendations?

## Baselines

1. Rule-based recommendations
2. ML-assisted analysis
3. Agentic tool-using workflow

## Metrics

- Idle detection rate
- Anomaly count
- Prediction MAE
- Estimated cost reduction
- False recommendation rate
- Recommendation confidence

## Limitations

LocalStack is a simulation environment. S3 access counts are not real user-access telemetry. Pricing is a demonstration model until replaced by verified provider pricing.

## Safety

The system recommends actions and requests human approval. Automatic destructive remediation is not enabled by default.
