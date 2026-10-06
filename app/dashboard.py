import pandas as pd
import streamlit as st
import plotly.express as px

from app.database.database import init_db, get_connection
from app.analytics.usage_analysis import analyze_usage
from app.agent.agent import CloudOptimizationAgent
from app.optimization.simulator import what_if

st.set_page_config(
    page_title="Cloud Cost Optimizer",
    page_icon="☁️",
    layout="wide"
)

init_db()

st.title("☁️ Cloud Cost Optimization Dashboard")
st.caption("Monitor • Analyze • Predict • Recommend • Optimize")

with get_connection() as conn:
    usage = pd.read_sql_query(
        "SELECT * FROM usage_metrics ORDER BY timestamp", conn
    )
    recs = pd.read_sql_query(
        """SELECT resource_id,recommendation,confidence,estimated_saving,status
           FROM recommendations ORDER BY estimated_saving DESC""",
        conn
    )

summary = analyze_usage()

total_resources = int(summary["resource_id"].nunique()) if not summary.empty else 0
avg_idle = float(summary["idle_percent"].mean()) if not summary.empty else 0
current_cost = 142.80
potential_saving = float(recs["estimated_saving"].sum()) if not recs.empty else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Resources", total_resources)
c2.metric("Estimated Monthly Cost", f"${current_cost:.2f}")
c3.metric("Potential Saving", f"${potential_saving:.2f}")
c4.metric("Average Idle", f"{avg_idle:.1f}%")

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Overview", "Resources", "Recommendations", "Agent", "What-if Simulator"]
)

with tab1:
    if not usage.empty:
        usage["timestamp"] = pd.to_datetime(usage["timestamp"], utc=True)
        fig = px.line(
            usage,
            x="timestamp",
            y="cpu_usage",
            color="resource_id",
            title="CPU Utilization"
        )
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.line(
            usage,
            x="timestamp",
            y="memory_usage",
            color="resource_id",
            title="Memory Utilization"
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Run the collector or demo seed first.")

with tab2:
    st.subheader("Resource Analytics")
    st.dataframe(summary, use_container_width=True)

with tab3:
    st.subheader("Explainable Recommendations")
    if recs.empty:
        st.info("No recommendations yet. Run the pipeline.")
    else:
        st.dataframe(recs, use_container_width=True)

with tab4:
    st.subheader("Agentic AI")
    goal = st.text_input(
        "Agent goal",
        "Find opportunities to reduce cloud cost and check anomalies"
    )

    if st.button("Run Optimization Agent"):
        result = CloudOptimizationAgent().run(goal)

        st.write("### Agent Plan")
        st.write(result["plan"])

        st.write("### Agent Actions")
        st.json(result["actions"])

        st.warning(
            "Actions are recommendations only. Human approval is required "
            "before any real remediation."
        )

with tab5:
    st.subheader("What-if Cost Simulator")

    idle_hours = st.slider("Idle hours/day", 0, 12, 4)
    idle_threshold = st.slider("Idle CPU threshold (%)", 1, 50, 10)
    archive = st.checkbox("Archive old S3 data", True)

    result = what_if(
        current_cost,
        idle_hours_per_day=idle_hours,
        idle_threshold=idle_threshold,
        archive_old_data=archive
    )

    a, b, c = st.columns(3)
    a.metric("Current", f"${result['current_cost']:.2f}")
    b.metric("Optimized", f"${result['optimized_cost']:.2f}")
    c.metric("Saving", f"${result['saving']:.2f} ({result['saving_percent']:.1f}%)")

    st.json(result)
