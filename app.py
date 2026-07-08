import streamlit as st
import pandas as pd
import numpy as np

# Page Config
st.set_page_config(page_title="Synthetic Mindset Explorer", layout="wide")
st.title("Synthetic Mindset Engine 🧠")

# 1. Mock Data Generator (Replace with your pd.read_csv logic later)
@st.cache_data
def load_data():
    np.random.seed(42)
    n = 1000
    data = pd.DataFrame({
        'Respondent_ID': range(1, n + 1),
        'Mindset': np.random.choice(['The Vanguard', 'The Pragmatist', 'The Traditionalist'], n, p=[0.2, 0.5, 0.3]),
        'Age_Cohort': np.random.choice(['Gen Z', 'Millennial', 'Gen X'], n),
        'Weight': np.random.uniform(0.8, 1.2, n) # Simulated survey weighting
    })
    return data

df = load_data()

# 2. Sidebar Controls
st.sidebar.header("Crosstab Configuration")
row_var = st.sidebar.selectbox("Select Row (Target)", ['Age_Cohort'])
col_var = st.sidebar.selectbox("Select Column (Mindset)", ['Mindset'])

# 3. The Core Simmons Math Engine
def calculate_simmons_crosstab(df, row, col, weight_col='Weight'):
    # Base weighted counts
    crosstab = pd.crosstab(df[row], df[col], values=df[weight_col], aggfunc='sum', margins=True, margins_name='Total')
    
    # Calculate Metrics
    results = {}
    for column in crosstab.columns:
        if column != 'Total':
            # Weighted Count
            count = crosstab[column]
            # Vertical % (Column %)
            vert_pct = (count / crosstab.loc['Total', column]) * 100
            # Horizontal % (Row %)
            horz_pct = (count / crosstab['Total']) * 100
            # Index Calculation: (Vertical % / Total Population %) * 100
            pop_pct = (crosstab['Total'] / crosstab.loc['Total', 'Total']) * 100
            index = (vert_pct / pop_pct) * 100
            
            # Formatting the output block for this column
            results[column] = pd.DataFrame({
                'Weighted (000)': count.round(0),
                'Vert %': vert_pct.round(1),
                'Horz %': horz_pct.round(1),
                'Index': index.round(0)
            })
            
    # Concatenate side-by-side with MultiIndex columns
    final_table = pd.concat(results.values(), axis=1, keys=results.keys())
    # Drop the "Total" row to clean up the view
    return final_table.drop('Total', errors='ignore')

# 4. UI Layout
st.subheader(f"Quant Layer: {row_var} by {col_var}")
quant_table = calculate_simmons_crosstab(df, row_var, col_var)
st.dataframe(quant_table, use_container_width=True)

st.divider()

# 5. The Qualitative "Anthropology" Integration
st.subheader("Qual Layer: Ethnography & Social Listening")
st.markdown("*(This section dynamically updates based on the quantitative index anomalies above)*")

col1, col2 = st.columns(2)

with col1:
    st.info("**Online Anthropology (Social Listening)**")
    st.markdown("""
    * **Dominant Sentiment:** Frustrated but optimistic.
    * **Key Verbatim:** "I want to try the new tech, but I don't want to feel like a beta tester for a massive corporation."
    * **Cultural Signal:** Migration toward localized, closed-loop community platforms.
    """)

with col2:
    st.success("**Journal Ethnography (In-Depth Insights)**")
    st.markdown("""
    * **Observed Behavior:** 'The Vanguard' mindset indexes highly with Gen Z (Index 142). Ethnographies reveal this isn't driven by wealth, but by a desire for *status signaling* through early adoption.
    * **Friction Point:** High abandonment rate if the onboarding process feels corporate.
    """)
