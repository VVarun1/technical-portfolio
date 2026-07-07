import streamlit as st
import pandas as pd
import random

st.title("AI Bias Audit Dashboard")
st.write("Test model outputs across demographics to detect skew.")

demographics = ["Age", "Gender", "Ethnicity", "Region"]
selected_demo = st.selectbox("Select Demographic to Audit", demographics)

# Simulated data
data = pd.DataFrame({
    "Group": ["Group A", "Group B", "Group C", "Group D"],
    "Sentiment_Score": [random.uniform(0.4, 0.6) for _ in range(4)],
    "Toxicity_Score": [random.uniform(0.01, 0.1) for _ in range(4)]
})

st.bar_chart(data.set_index("Group")["Sentiment_Score"])
st.table(data)
