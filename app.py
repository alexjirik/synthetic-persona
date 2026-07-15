import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Roundpeg | Growth Target Engine", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .rp-header { color: #F26A21; font-weight: 800; font-size: 2rem; }
    .truth-box { background-color: #f8f9fa; padding: 15px; border-left: 5px solid #F26A21; margin-bottom: 20px; border-radius: 4px; }
    .truth-title { font-weight: bold; color: #343a40; text-transform: uppercase; font-size: 0.85rem;}
    </style>
""", unsafe_allow_html=True)

# --- STRATEGIC FRAMEWORK ---
def render_strategic_framework():
    st.markdown("<div class='rp-header'>Growth Target Engine</div>", unsafe_allow_html=True)
    st.markdown("*Translating survey data into the Five Fundamental Truths.*")
    
    cols = st.columns(5)
    truths = [
        ("1. Create Advocates", "Purchase intent is fleeting, predisposition is forever."),
        ("2. Ensure Differentiation", "Growth targets aren't created in a vacuum, they're created in the real world."),
        ("3. Expand Size-of-Prize", "A Growth Target gets you where you want to go."),
        ("4. Focus Activation", "A master brand Growth Target is key to where you want a brand to go."),
        ("5. Generate Empathy", "Game-changing growth requires both clarity & conviction.")
    ]
    
    for col, (title, desc) in zip(cols, truths):
        with col:
            st.markdown(f"""
            <div class="truth-box">
                <div class="truth-title">{title}</div>
                <div style="font-size: 0.8rem; margin-top: 5px; color: #6c757d;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

render_strategic_framework()

# --- 1. DATA INGESTION LAYER ---
st.sidebar.markdown("### 📥 1. Ingest Data")
# UPGRADE: Now accepts both CSV and Excel (.xlsx) files
uploaded_file = st.sidebar.file_uploader("Upload Survey Data (CSV or Excel)", type=['csv', 'xlsx'])

# Helper function to generate mock survey data including the new mindset
@st.cache_data
def generate_mock_survey_data():
    np.random.seed(42)
    n_respondents = 5000
    # UPGRADE: Added "Eating is Pure" to the segmentation
    segments = ['Moment Makers', 'Expressive Escapists', 'Blue Mindset', 'Eating is Pure']
    data = {
        'Respondent_ID': range(1, n_respondents + 1),
        'Mindset_Segment': np.random.choice(segments, n_respondents, p=[0.20, 0.15, 0.45, 0.20]),
        'Trait: Life should be fun': np.random.choice(['Agree', 'Disagree'], n_respondents, p=[0.6, 0.4]),
        'Trait: Skeptical of ads': np.random.choice(['Agree', 'Disagree'], n_respondents, p=[0.5, 0.5]),
        # Psychographic statements relevant to the new mindset
        'Psychographic: I check ingredient labels': np.random.choice(['Agree', 'Disagree'], n_respondents, p=[0.4, 0.6]),
        'Psychographic: I prefer organic foods': np.random.choice(['Agree', 'Disagree'], n_respondents, p=[0.3, 0.7]),
        'Behavior: Active on TikTok': np.random.choice(['Yes', 'No'], n_respondents, p=[0.35, 0.65])
    }
    
    df = pd.DataFrame(data)
    
    # Bias Moment makers
    df.loc[df['Mindset_Segment'] == 'Moment Makers', 'Trait: Life should be fun'] = np.random.choice(['Agree', 'Disagree'], len(df[df['Mindset_Segment'] == 'Moment Makers']), p=[0.85, 0.15])
    # Bias Escapists
    df.loc[df['Mindset_Segment'] == 'Expressive Escapists', 'Behavior: Active on TikTok'] = np.random.choice(['Yes', 'No'], len(df[df['Mindset_Segment'] == 'Expressive Escapists']), p=[0.85, 0.15])
    
    # BIAS "Eating is Pure" so the Index pops in the Math Engine
    df.loc[df['Mindset_Segment'] == 'Eating is Pure', 'Psychographic: I check ingredient labels'] = np.random.choice(['Agree', 'Disagree'], len(df[df['Mindset_Segment'] == 'Eating is Pure']), p=[0.90, 0.10])
    df.loc[df['Mindset_Segment'] == 'Eating is Pure', 'Psychographic: I prefer organic foods'] = np.random.choice(['Agree', 'Disagree'], len(df[df['Mindset_Segment'] == 'Eating is Pure']), p=[0.88, 0.12])
    
    return df

if uploaded_file is not None:
    # UPGRADE: Logic to route to the correct Pandas reader
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    st.sidebar.success(f"Data from '{uploaded_file.name}' loaded successfully!")
else:
    st.sidebar.info("Using Mock Survey Data for Demonstration.")
    df = generate_mock_survey_data()

# --- 2. QUERY BUILDER ---
st.sidebar.markdown("### ⚙️ 2. Cross-Tab Settings")
target_col = st.sidebar.selectbox("Select Target Variable (Columns)", df.columns, index=1)
behavior_cols = st.sidebar.multiselect("Select Behaviors/Traits (Rows)", [c for c in df.columns if c not in ['Respondent_ID', target_col]], default=[c for c in df.columns if c not in ['Respondent_ID', target_col]])

# --- 3. THE MATH ENGINE ---
if st.sidebar.button("Run Simmons Math Engine"):
    with st.spinner("Crunching vertical, horizontal, and index metrics..."):
        
        results = []
        total_population = len(df)
        target_sizes = df[target_col].value_counts()
        
        for behavior in behavior_cols:
            positive_responses = df[behavior].unique()
            target_response = positive_responses[0] if 'Agree' in positive_responses or 'Yes' in positive_responses else positive_responses[0]
            
            total_behavior_count = len(df[df[behavior] == target_response])
            total_vertical_pct = total_behavior_count / total_population if total_population > 0 else 0
            
            for target_segment in target_sizes.index:
                segment_size = target_sizes[target_segment]
                target_in_base = len(df[(df[target_col] == target_segment) & (df[behavior] == target_response)])
                
                vertical_pct = target_in_base / segment_size if segment_size > 0 else 0
                horizontal_pct = target_in_base / total_behavior_count if total_behavior_count > 0 else 0
                index_score = (vertical_pct / total_vertical_pct) * 100 if total_vertical_pct > 0 else 0
                
                results.append({
                    "Behavior/Trait": f"{behavior} ({target_response})",
                    "Segment": target_segment,
                    "Sample (000)": target_in_base,
                    "Vertical %": vertical_pct,
                    "Horizontal %": horizontal_pct,
                    "Index": index_score
                })
        
        results_df = pd.DataFrame(results)
        
        # --- DISPLAY RESULTS ---
        st.markdown("### 📊 Audience Predispositions")
        
        pivot_df = results_df.pivot(index="Behavior/Trait", columns="Segment", values=["Vertical %", "Index"])
        # Flatten the MultiIndex to prevent Streamlit rendering errors
        pivot_df.columns = [f"{col[1]} | {col[0]}" for col in pivot_df.columns]
        
        def style_simmons_table(styler):
            format_dict = {}
            for col in pivot_df.columns:
                if 'Vertical' in col:
                    format_dict[col] = "{:.1%}"
                elif 'Index' in col:
                    format_dict[col] = "{:.0f}"
            styler.format(format_dict)
            
            def color_index(val):
                if pd.isna(val): return ''
                if val > 115: return 'color: #155724; background-color: #d4edda; font-weight: bold;'
                elif val < 85: return 'color: #721c24; background-color: #f8d7da;'
                return ''
            
            # Apply styling strictly to the flattened Index columns
            index_cols = [c for c in pivot_df.columns if 'Index' in c]
            styler.map(color_index, subset=index_cols)
            return styler
        
        st.dataframe(pivot_df.style.pipe(style_simmons_table), use_container_width=True, height=400)
        
        st.info("💡 **How to read this:** Notice how the **Eating is Pure** mindset drastically over-indexes on organic preferences and label checking, validating the psychographic profile.")
        
        # Save the flat results DataFrame for the Query Engine
        st.session_state['crosstab_results_flat'] = results_df

# --- 4. QUICK DATA QUERIES (NO AI) ---
st.markdown("---")
st.markdown("### 🔍 Quick Data Queries")
st.markdown("Ask exact, mathematically accurate questions about your run. **100% secure, offline, and math-based.**")

if 'crosstab_results_flat' in st.session_state:
    query_df = st.session_state['crosstab_results_flat']
    
    # Pre-built questions that researchers ask most often
    query_type = st.selectbox("Select a quick question to ask the data:", [
        "What are the highest indexing traits for a specific segment?",
        "Which segment indexes highest for a specific trait?",
        "What is the total sample size for a specific segment?"
    ])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if query_type == "What are the highest indexing traits for a specific segment?":
        selected_segment = st.selectbox("Select Segment:", query_df['Segment'].unique())
        top_traits = query_df[query_df['Segment'] == selected_segment].sort_values(by="Index", ascending=False)
        st.dataframe(top_traits[['Behavior/Trait', 'Index', 'Vertical %', 'Horizontal %']].head(10), use_container_width=True)
        
    elif query_type == "Which segment indexes highest for a specific trait?":
        selected_trait = st.selectbox("Select Trait:", query_df['Behavior/Trait'].unique())
        top_segments = query_df[query_df['Behavior/Trait'] == selected_trait].sort_values(by="Index", ascending=False)
        st.dataframe(top_segments[['Segment', 'Index', 'Vertical %', 'Sample (000)']].head(5), use_container_width=True)
        
    elif query_type == "What is the total sample size for a specific segment?":
        selected_segment = st.selectbox("Select Segment:", query_df['Segment'].unique())
        base_size = len(df[df[target_col] == selected_segment])
        st.metric(label=f"Total Respondents in '{selected_segment}'", value=f"{base_size:,}")

else:
    st.info("👆 Run the Simmons Math Engine above to unlock quick queries!")
