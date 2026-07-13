import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Roundpeg: Synthetic Mindset Sandbox", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    .big-font { font-size:18px !important; font-weight: 400; color: #555;}
    .mindset-card { background-color: #f8f9fa; padding: 20px; border-radius: 12px; border-left: 6px solid #FF6B6B; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px;}
    .truth-header { color: #FF6B6B; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-size: 14px; margin-bottom: 8px; }
    .metric-container { background-color: #ffffff; border: 1px solid #e0e0e0; padding: 15px; border-radius: 8px; text-align: center; }
    .status-dot { height: 10px; width: 10px; background-color: #27ae60; border-radius: 50%; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

# This acts as our "offline" ethnographic repository, replacing the LLM for this sandbox.
ROUNDPEG_MINDSET_DB = {
    "Moment Makers": {
        "tagline": "Capable, competent and charismatic. Driven, confident, and fueled by purpose and pride.",
        "tension": "They crave raw, unfiltered experiences but feel increasingly boxed in by a digitized, hands-off world.",
        "truth": "They need brands that deliver tangible power and performance, enabling them to assert their presence and mastery.",
        "interest": "Power, Performance, Passion. They want to know what goes on 'under the hood'.",
        "motivations": "Excitement, connection, and letting loose. They consider themselves enthusiasts and born leaders.",
        "anthropology": "Leisure means sports and getting outdoors (Freshwater fishing, weight lifting). They consume media that is informative & practical, and index highly against live, high-adrenaline sports like UFC and NFL."
    },
    "Expressive Escapists": {
        "tagline": "Determined, discerning, and developing. They use standout choices as a personal canvas.",
        "tension": "They want to assert their unique identity but struggle to find platforms that feel truly authentic rather than mass-produced.",
        "truth": "They gravitate toward brands that act as amplifiers for their personality, offering bold, innovative designs that stand apart.",
        "interest": "Fun, Freedom, and Fashionable aesthetics. Exterior styling is their first consideration.",
        "motivations": "They want to be seen, celebrated, and set apart. They seek spirited performance that matches their energy.",
        "anthropology": "Their media diet is about connection and entertainment. They are disproportionately engaged with pop culture, hip-hop concerts, and use media to maintain a high-visibility social status."
    },
    "Blue Mindset": {
        "tagline": "Grounded, practical, and content. They find fulfillment in routine and close connections.",
        "tension": "They are overwhelmed by the constant noise, flash, and anxiety of modern social expectations.",
        "truth": "They require brands that are dependable, liberating, and simplify their lives without demanding excessive attention.",
        "interest": "Dependability, practicality, and a well-ordered life. They avoid unnecessary risks.",
        "motivations": "Quiet enjoyment, protecting their family, and maintaining a comfortable standard of living.",
        "anthropology": "They consume media carefully, favoring substance over flash. They are skeptical of advertising and prefer thoughtful content (e.g., PBS, Consumer Reports) that informs rather than distracts."
    },
    "Yellow Mindset": {
        "tagline": "Bold, competitive, and driven by recognition. They are savvy improvisers.",
        "anthropology": "Social media is a stage for identity and daily recognition. Influencers and friends guide their choices. They consume content to blend their online presence with their real-life ambitions.",
        "interest": "Innovation, luxury, and standing out. They eagerly adopt new technologies.",
        "motivations": "Achieving high social status and ensuring their lifestyle impresses others.",
        "truth": "They need brands that confer immediate status and serve as a shortcut to being perceived as successful and avant-garde.",
        "tension": "They are fiercely ambitious but fear falling behind the curve or blending into the background."
    },
    "Green Mindset": {
        "tagline": "Mindful, community-oriented, and purpose-driven.",
        "anthropology": "They spend their time reading deep-dive articles, listening to educational podcasts, and engaging with community-centric platforms.",
        "interest": "Eco-friendly options, sustainability, and ethical business practices.",
        "motivations": "Leaving a positive impact on the world and making responsible choices for future generations.",
        "truth": "They demand absolute transparency and alignment of values; a brand must prove its worth to the world, not just the consumer.",
        "tension": "They want to enjoy life's pleasures but carry a heavy sense of guilt regarding their environmental and social footprint."
    }
}

@st.cache_data(show_spinner=False)
def generate_mock_data():
    """Generates 4,000 mock respondents for testing the engine offline."""
    np.random.seed(42)
    n = 4000
    return pd.DataFrame({
        'Respondent_ID': range(1, n + 1),
        'Mindset_Segment': np.random.choice(
            ['Moment Makers', 'Expressive Escapists', 'Green Mindset', 'Yellow Mindset', 'Blue Mindset'], 
            n, p=[0.25, 0.15, 0.20, 0.10, 0.30]
        ),
        'Generation': np.random.choice(['Gen Z', 'Millennial', 'Gen X', 'Boomer+'], n, p=[0.15, 0.40, 0.25, 0.20]),
        'Income_Bracket': np.random.choice(['Under $50k', '$50k-$99k', '$100k-$149k', '$150k+'], n, p=[0.2, 0.3, 0.3, 0.2]),
        'Region': np.random.choice(['Northeast', 'Midwest', 'South', 'West'], n),
        '_Weight': np.random.uniform(0.7, 1.3, n)
    })

@st.cache_data(show_spinner=False)
def compute_simmons_crosstab(df, target_var, explore_var, weight_col):
    """The core MRI Simmons math engine for calculating Universe, Reach, Comp, and Index."""
    crosstab = pd.crosstab(
        df[explore_var], 
        df[target_var], 
        values=df[weight_col], 
        aggfunc='sum', 
        margins=True, 
        margins_name='Total'
    )
    
    results = {}
    for column in crosstab.columns:
        if column != 'Total':
            count = crosstab[column]
            vert_pct = (count / crosstab.loc['Total', column]) * 100
            horz_pct = (count / crosstab['Total']) * 100
            pop_pct = (crosstab['Total'] / crosstab.loc['Total', 'Total']) * 100
            
            # Avoid division by zero for index calculation
            index = np.where(pop_pct > 0, (vert_pct / pop_pct) * 100, 0)
            
            results[column] = pd.DataFrame({
                'Universe (000)': count.round(0),
                'Vert % (Comp)': vert_pct.round(1),
                'Horz % (Reach)': horz_pct.round(1),
                'Index': np.round(index, 0)
            })
    
    final_table = pd.concat(results.values(), axis=1, keys=results.keys())
    final_table = final_table.drop('Total', errors='ignore')
    
    # Flatten the multi-index columns to prevent Streamlit Arrow errors
    final_table.columns = [f"{col[0]} | {col[1]}" for col in final_table.columns]
    
    return final_table

st.title("Roundpeg: Synthetic Mindset Engine 🎯")
st.markdown("<p class='big-font'>Offline Sandbox: Fusing quantitative predispositions with qualitative human truths.</p>", unsafe_allow_html=True)

# Generate the mock data automatically for the sandbox
df = generate_mock_data()
columns = df.columns.tolist()

with st.sidebar:
    st.header("⚙️ Sandbox Configuration")
    st.success("Loaded 4,000 Mock Respondents.")
    st.info("This is a secure, offline prototype. No external APIs are used.")
    
    st.markdown("---")
    st.header("Strategy Configuration")
    target_var = st.selectbox("Select Target Segment", columns, index=columns.index('Mindset_Segment'))
    explore_var = st.selectbox("Select Variable to Explore", columns, index=columns.index('Generation'))
    weight_var = st.selectbox("Select Survey Weight", ['None (Unweighted)'] + columns, index=columns.index('_Weight')+1)

st.markdown("---")

tab1, tab2 = st.tabs([
    "🧠 Roundpeg Mindset Synthesis", 
    "📊 Quant Crosstab Engine"
])

with tab1:
    available_targets = [x for x in df[target_var].dropna().unique() if str(x).strip() != '']
    selected_segment = st.selectbox("Select a Segment to Profile:", available_targets)
    
    # Isolate data for the selected segment
    segment_df = df[df[target_var] == selected_segment]
    total_n = len(segment_df)
    total_pop = len(df)
    
    # Display high-level metrics
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='metric-container'><p class='status-dot'></p><br><b>Raw Sample Size:</b><br><span style='font-size: 24px;'>{total_n}</span></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-container'><b>% of Total Audience:</b><br><span style='font-size: 24px;'>{round((total_n/total_pop)*100, 1)}%</span></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric-container'><b>Data Streams:</b><br><span style='font-size: 16px;'>Roundpeg Qual Repo | MRI Simmons Mock</span></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Pull the qualitative profile from our hardcoded database
    profile = ROUNDPEG_MINDSET_DB.get(selected_segment, None)
    
    if profile:
        st.markdown(f"### 🧠 THE {str(selected_segment).upper()} MINDSET")
        st.markdown(f"*{profile['tagline']}*")
        
        st.markdown(f"""
        <div class="mindset-card">
        <p class="truth-header">The Human Truth (Clarity & Conviction)</p>
        <ul>
            <li><b>The Core Tension:</b> {profile['tension']}</li>
            <li><b>The Ultimate Truth:</b> {profile['truth']}</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("#### 1. What they value in a Product/Brand")
            st.markdown(f"*   **Conscious Interest:** {profile['interest']}")
            st.markdown(f"*   **Top Motivations:** {profile['motivations']}")
            
        with col_b:
            st.markdown("#### 2. How they consume media & the world")
            st.write(profile['anthropology'])
            
    else:
        st.warning(f"No qualitative profile exists in the database for '{selected_segment}'.")

with tab2:
    st.subheader("Simmons-Style Crosstab")
    st.caption("Metrics calculated: Universe (000), Vertical % (Composition), Horizontal % (Reach), and Index (Propensity).")
    
    weight_col = weight_var if weight_var != 'None (Unweighted)' else '__dummy_weight'
    if weight_col == '__dummy_weight':
        df['__dummy_weight'] = 1
        
    final_table = compute_simmons_crosstab(df, target_var, explore_var, weight_col)
    
    def color_index(val):
        """Highlights High indexing traits in green, Low in red."""
        try:
            v = float(val)
            if pd.isna(v): return ''
            color = '#27ae60' if v > 115 else '#c0392b' if v < 85 else 'inherit'
            weight = 'bold' if v > 115 or v < 85 else 'normal'
            return f'color: {color}; font-weight: {weight}'
        except (ValueError, TypeError):
            return ''
    
    # Apply styling only to columns that contain the word 'Index'
    index_cols = [col for col in final_table.columns if col.endswith('Index')]
    styled_table = final_table.style.map(color_index, subset=index_cols)
    
    st.dataframe(styled_table, use_container_width=True, height=600)
