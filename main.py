import streamlit as st
from evaluator import load_gemini, evaluate_idea
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Idea Evaluator", layout="wide")

st.title("🔍 AI-Powered Idea Evaluator")
st.write("Enter your idea(s) and get a full feasibility analysis in seconds.")

# Load API key and model
api_key = os.getenv("GEMINI_API_KEY")
model = load_gemini(api_key)

mode = st.radio("Choose Evaluation Mode", ["Single Idea", "Compare Two Ideas"])

st.subheader("Additional Parameters")
col1, col2 = st.columns(2)

with col1:
    market_size = st.select_slider("Market Size", ["small", "medium", "large"])
    budget = st.select_slider("Budget", ["low", "medium", "high"])

with col2:
    team_skill = st.select_slider("Team Skill Level", ["junior", "mid", "senior"])
    timeline = st.select_slider("Timeline Urgency", ["flexible", "moderate", "urgent"])

if mode == "Single Idea":
    idea = st.text_area("💡 Enter your idea:", height=150)

    if st.button("✨ Evaluate Idea"):
        if not idea.strip():
            st.warning("Please enter an idea first.")
        else:
            with st.spinner("Analyzing..."):
                result = evaluate_idea(model, idea, market_size, team_skill, budget, timeline)

            if "error" in result:
                st.error("Model returned invalid JSON")
                st.code(result["raw"])
            else:
                st.success("Analysis complete!")
                st.subheader("📊 Evaluation Results")
                st.metric("Feasibility Score", result["feasibility_score"])
                st.metric("Difficulty Score", result["difficulty_score"])
                st.metric("Success Probability", f"{result['success_probability']}")
                st.write("### Estimated Time"); st.info(result["estimated_time"])
                st.write("### Estimated Cost"); st.info(result["estimated_cost"])
                st.write("### Potential ROI"); st.info(result["potential_roi"])
                st.write("### Key Risks"); st.write(result["key_risks"])
                st.write("### Bottlenecks"); st.write(result["major_bottlenecks"])
                st.write("### Summary"); st.write(result["viability_summary"])
                st.download_button("⬇️ Export JSON", data=str(result), file_name="analysis.json", mime="application/json")

else:  
    idea1 = st.text_area("💡 Enter Idea 1:", height=150)
    idea2 = st.text_area("💡 Enter Idea 2:", height=150)

    if st.button("✨ Compare Ideas"):
        if not idea1.strip() or not idea2.strip():
            st.warning("Please enter both ideas to compare.")
        else:
            with st.spinner("Analyzing both ideas..."):
                result1 = evaluate_idea(model, idea1, market_size, team_skill, budget, timeline)
                result2 = evaluate_idea(model, idea2, market_size, team_skill, budget, timeline)

            if "error" in result1 or "error" in result2:
                st.error("One or both evaluations returned invalid JSON")
                if "error" in result1: st.code(result1["raw"])
                if "error" in result2: st.code(result2["raw"])
            else:
                st.success("Comparative analysis complete!")
                st.subheader("📊 Comparative Evaluation Results")

                cols = st.columns(2)
                with cols[0]:
                    st.write("### Idea 1")
                    st.write(idea1)
                    st.metric("Feasibility Score", result1["feasibility_score"])
                    st.metric("Difficulty Score", result1["difficulty_score"])
                    st.metric("Success Probability", f"{result1['success_probability']}")
                    st.write("Estimated Time"); st.info(result1["estimated_time"])
                    st.write("Estimated Cost"); st.info(result1["estimated_cost"])
                    st.write("Potential ROI"); st.info(result1["potential_roi"])

                with cols[1]:
                    st.write("### Idea 2")
                    st.write(idea2)
                    st.metric("Feasibility Score", result2["feasibility_score"])
                    st.metric("Difficulty Score", result2["difficulty_score"])
                    st.metric("Success Probability", f"{result2['success_probability']}")
                    st.write("Estimated Time"); st.info(result2["estimated_time"])
                    st.write("Estimated Cost"); st.info(result2["estimated_cost"])
                    st.write("Potential ROI"); st.info(result2["potential_roi"])

                st.write("### Summary Comparison")
                st.write("**Idea 1:**", result1["viability_summary"])
                st.write("**Idea 2:**", result2["viability_summary"])

                st.download_button(
                    "⬇️ Export Both JSONs",
                    data=str({"idea1": result1, "idea2": result2}),
                    file_name="comparison_analysis.json",
                    mime="application/json"
                )
