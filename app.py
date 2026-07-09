import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Synthetic Mindset Engine", layout="wide")

# Custom CSS for premium agency aesthetic
st.markdown("""
    <style>
    .big-font { font-size:18px !important; font-weight: 400; color: #555;}
    .mindset-card { background-color: #f8f9fa; padding: 20px; border-radius: 12px; border-left: 6px solid #FF6B6B; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px;}
    .truth-header { color: #FF6B6B; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-size: 12px; margin-bottom: 5px; }
    .stat-box { background-color: #ffffff; border: 1px solid #e0e0e0; padding: 15px; border-radius: 8px; text-align: center; }
    .stat-value { font-size: 24px; font-weight: 700; color: #2C3E50; }
    .stat-label { font-size: 12px; color: #7F8C8D; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- THE QUALITATIVE REPOSITORY (ONLINE ANTHROPOLOGY & ETHNOGRAPHY) ---
# In the future, this could be connected to an external database or CMS.
MINDSET_DATABASE = {
    "The Harmonizer": {
        "tagline": "Approach betterment fluidly - enriching their mind, body and connection with others.",
        "anthropology": "Online behavior shows a shift away from 'hustle culture' toward holistic wellness. They follow micro-influencers focused on mental health, outdoor recreation, and balanced living.",
        "attitudes": ["I'm an optimist (Index: 153)", "Like to pursue a life of challenge & change (Index: 171)", "I exercise at least once per week (Index: 156)"],
        "brands": ["REI", "J.Crew", "Banana Republic", "Costco"],
        "human_truth": "TENSION: They want to grow and evolve, but feel overwhelmed by fragmented wellness trends. TRUTH: They seek brands that act as unifying partners in their holistic journey, not just purveyors of singular products."
    },
    "The Satisfier": {
        "tagline": "Lifestyle is carefree, exciting & focused on the road less traveled.",
        "anthropology": "Social listening reveals high engagement with travel, extreme sports, and spontaneous event content. They value experiences over physical accumulation.",
        "attitudes": ["Enjoy taking risks (Index: 144)", "Travel the unbeaten path (Index: 136)", "Spur of the moment (Index: 182)"],
        "brands": ["Puma", "Crocs", "Nike"],
        "human_truth": "TENSION: They crave spontaneous joy in a highly regimented, scheduled world. TRUTH: They gravitate toward brands that remove friction and act as enablers of immediate, carefree experiences."
    },
    "The Calculator": {
        "tagline": "Disciplined & feel a greater sense of duty to those around them.",
        "anthropology": "Digital footprints index highly on financial planning, consumer reports, and family-oriented logistics. They research heavily before committing.",
        "attitudes": ["Duty is more important than personal enjoyment (Index: 162)", "I don't like responsibility (Index: 75 - Low)", "Swayed by other people's views (Index: 186)"],
        "brands": ["Express", "Ann Taylor", "Nordstrom Rack"],
        "human_truth": "TENSION: They carry the mental load for their families and fear making the 'wrong' choice. TRUTH: They need brands to provide absolute transparency, validating their choices so they can finally relax."
    }
}

st.title("Synthetic Mindset Engine 🎯")
st.markdown("<p class='big-font'>Fusing quantitative predispositions with qualitative human truths.</p>", unsafe_allow_html=True)

with st.sidebar:
    st.header("1. Ingest Data")
    uploaded_file = st.file_uploader("Upload Raw Survey (CSV/Excel)", type=['csv', 'xlsx'])
    
    st.divider()
    st.markdown("### Or Test the Engine")
    use_mock = st.button("Generate Mock Audience Data")

df = None

if use_mock:
    np.random.seed(42)
    n = 2000
    df = pd.DataFrame({
        'Respondent_ID': range(1, n + 1),
        'Mindset_Segment': np.random.choice(['The Harmonizer', 'The Satisfier', 'The Calculator', 'Unclassified'], n, p=[0.25, 0.30, 0.20, 0.25]),
        'Generation': np.random.choice(['Gen Z', 'Millennial', 'Gen X', 'Boomer+'], n, p=[0.15, 0.40, 0.25, 0.20]),
        'Income_Bracket': np.random.choice(['Under $50k', '$50k-$99k', '$100k-$149k', '$150k+'], n),
        'Region': np.random.choice(['Northeast', 'Midwest', 'South', 'West'], n),
        '_Weight': np.random.uniform(0.7, 1.3, n)
    })
    st.sidebar.success("Loaded 2,000 Mock Respondents.")

elif uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

if df is not None:
    columns = df.columns.tolist()

    st.sidebar.header("2. Strategy Configuration")
    target_var = st.sidebar.selectbox("Select Target (e.g., Mindset)", columns, index=columns.index('Mindset_Segment') if 'Mindset_Segment' in columns else 0)
    explore_var = st.sidebar.selectbox("Select Variable to Explore", columns, index=columns.index('Generation') if 'Generation' in columns else min(1, len(columns)-1))
    weight_var = st.sidebar.selectbox("Select Survey Weight", ['None (Unweighted)'] + columns, index=columns.index('_Weight')+1 if '_Weight' in columns else 0)

    if st.sidebar.button("Run Synthetic Analysis", type="primary"):
        
        tab1, tab2 = st.tabs(["📊 Quant Crosstab (Simmons)", "🧠 The Synthetic Mindset (Qual)"])
        
        with tab1:
            st.subheader(f"Profiling '{target_var}' against '{explore_var}'")
            
            weight_col = weight_var if weight_var != 'None (Unweighted)' else '__dummy_weight'
            if weight_col == '__dummy_weight':
                df['__dummy_weight'] = 1
                
            crosstab = pd.crosstab(df[explore_var], df[target_var], values=df[weight_col], aggfunc='sum', margins=True, margins_name='Total')
            
            results = {}
            for column in crosstab.columns:
                if column != 'Total':
                    count = crosstab[column]
                    vert_pct = (count / crosstab.loc['Total', column]) * 100
                    horz_pct = (count / crosstab['Total']) * 100
                    pop_pct = (crosstab['Total'] / crosstab.loc['Total', 'Total']) * 100
                    index = (vert_pct / pop_pct) * 100
                    
                    results[column] = pd.DataFrame({
                        'Universe (000)': count.round(0),
                        'Vert % (Comp)': vert_pct.round(1),
                        'Horz % (Reach)': horz_pct.round(1),
                        'Index': index.round(0)
                    })
            
            final_table = pd.concat(results.values(), axis=1, keys=results.keys())
            final_table = final_table.drop('Total', errors='ignore')
            
            def color_index(val):
                if pd.isna(val): return ''
                color = '#27ae60' if val > 115 else '#c0392b' if val < 85 else 'inherit'
                weight = 'bold' if val > 115 or val < 85 else 'normal'
                return f'color: {color}; font-weight: {weight}'
            
            idx = pd.IndexSlice
            styled_table = final_table.style.applymap(color_index, subset=idx[:, idx[:, 'Index']])
            st.dataframe(styled_table, use_container_width=True, height=400)
            st.caption("*Index > 115 indicates strong predisposition. Index < 85 indicates barrier.*")

        with tab2:
            st.subheader("The Growth Target Truths")
            
            # Get unique mindsets from the selected target variable
            available_targets = df[target_var].dropna().unique()
            selected_segment = st.selectbox("Select a Segment to Profile:", available_targets)
            
            # Look up the qualitative data
            qual_data = MINDSET_DATABASE.get(selected_segment)
            
            if qual_data:
                st.markdown(f"### {selected_segment}")
                st.markdown(f"*{qual_data['tagline']}*")
                
                # Top metrics pulled dynamically from the dataframe
                segment_df = df[df[target_var] == selected_segment]
                total_n = len(segment_df)
                total_pop = len(df)
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(f"<div class='metric-container'><p class='status-dot' style='display:inline-block; margin-right:5px;'></p><b>Sample Size:</b> {total_N}</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"<div class='metric-container'><b>% of Population:</b> {round((total_n/total_pop)*100, 1)}%</div>", unsafe_allow_html=True)
                with c3:
                    st.markdown(f"<div class='metric-container'><b>Status:</b> Active Segment</div>", unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)

                # The 5 Truths Layout
                col_left, col_right = st.columns([1.5, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class='glass-panel' style='padding: 20px;'>
                        <p class='editorial-hero-sub'>1. Predisposition (Attitudes)</p>
                        <ul style='font-size: 14px; color: #D3D3D3;'>
                            {"".join([f"<li>{item}</li>" for item in qual_data['attitudes']])}
                        </ul>
                        <br>
                        <p class='editorial-hero-sub'>2. Real World (Online Anthropology)</p>
                        <p style='font-size: 14px; color: #D3D3D3;'>{qual_data['anthropology']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class='glass-panel' style='padding: 20px;'>
                        <p class='editorial-hero-sub'>4. Brand Alignment (Affinity)</p>
                        <p style='font-size: 14px; color: #D3D3D3;'><i>Brands they index highly with:</i><br> <b>{', '.join(qual_data['brands'])}</b></p>
                        <br>
                        <p class='editorial-hero-sub' style='color: #ff5500;'>5. THE HUMAN TRUTH</p>
                        <p style='font-size: 15px; font-weight: 500; color: #ffffff; border-left: 3px solid #ff5500; padding-left: 10px;'>
                            {qual_data['truth']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning(f"No qualitative profile exists yet for '{selected_segment}'. Update the `MINDSET_DATABASE` in the source code to map this segment.")

else:
    # Empty State with Methodology Reminder
    st.info("Awaiting Data Upload in the Sidebar. (Or click 'Generate Strategic Crosstab' with the Mock Data)")
