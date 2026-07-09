import streamlit as st
import pandas as pd
import numpy as np
import json
import io

# NEW LIBRARIES FOR UNIVERSAL INGESTION
from PIL import Image
import docx
import PyPDF2

st.set_page_config(page_title="Synthetic Mindset Engine", layout="wide")

st.markdown("""
    <style>
    .big-font { font-size:18px !important; font-weight: 400; color: #555;}
    .mindset-card { background-color: #f8f9fa; padding: 20px; border-radius: 12px; border-left: 6px solid #FF6B6B; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px;}
    .truth-header { color: #FF6B6B; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-size: 12px; margin-bottom: 5px; }
    .metric-container { background-color: #ffffff; border: 1px solid #e0e0e0; padding: 15px; border-radius: 8px; text-align: center; }
    .status-dot { height: 10px; width: 10px; background-color: #27ae60; border-radius: 50%; display: inline-block; }
    .glass-panel { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1); backdrop-filter: blur(5px); }
    .editorial-hero-sub { font-size: 12px; font-weight: 600; text-transform: uppercase; color: #888; margin-top: 8px; margin-bottom: 2px; letter-spacing: 1px; }
    </style>
    """, unsafe_allow_html=True)

# Base qualitative database. This will be updated if a user uploads a custom JSON.
DEFAULT_MINDSET_DATABASE = {
    "The Harmonizer": {
        "tagline": "Approach betterment fluidly - enriching their mind, body and connection with others.",
        "anthropology": "Online behavior shows a shift away from 'hustle culture' toward holistic wellness. They follow micro-influencers focused on mental health, outdoor recreation, and balanced living.",
        "attitudes": ["I'm an optimist (Index: 153)", "Like to pursue a life of challenge & change (Index: 171)", "I exercise at least once per week (Index: 156)"],
        "brands": ["REI", "J.Crew", "Banana Republic", "Costco"],
        "truth": "TENSION: They want to grow and evolve, but feel overwhelmed by fragmented wellness trends. TRUTH: They seek brands that act as unifying partners in their holistic journey, not just purveyors of singular products."
    },
    "The Satisfier": {
        "tagline": "Lifestyle is carefree, exciting & focused on the road less traveled.",
        "anthropology": "Social listening reveals high engagement with travel, extreme sports, and spontaneous event content. They value experiences over physical accumulation.",
        "attitudes": ["Enjoy taking risks (Index: 144)", "Travel the unbeaten path (Index: 136)", "Spur of the moment (Index: 182)"],
        "brands": ["Puma", "Crocs", "Nike"],
        "truth": "TENSION: They crave spontaneous joy in a highly regimented, scheduled world. TRUTH: They gravitate toward brands that remove friction and act as enablers of immediate, carefree experiences."
    },
    "The Calculator": {
        "tagline": "Disciplined & feel a greater sense of duty to those around them.",
        "anthropology": "Digital footprints index highly on financial planning, consumer reports, and family-oriented logistics. They research heavily before committing.",
        "attitudes": ["Duty is more important than personal enjoyment (Index: 162)", "I don't like responsibility (Index: 75 - Low)", "Swayed by other people's views (Index: 186)"],
        "brands": ["Express", "Ann Taylor", "Nordstrom Rack"],
        "truth": "TENSION: They carry the mental load for their families and fear making the 'wrong' choice. TRUTH: They need brands to provide absolute transparency, validating their choices so they can finally relax."
    }
}

# ---------------------------------------------------------
# PERFORMANCE OPTIMIZATION: @st.cache_data decorators
# These ensure that heavy file reads and math calculations 
# are stored in memory and only run once.
# ---------------------------------------------------------

@st.cache_data
def load_quant_data(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

@st.cache_data
def load_qual_json(file):
    return json.load(file)

@st.cache_data
def load_raw_text(file):
    return file.getvalue().decode("utf-8")

# --- NEW UNIVERSAL DOCUMENT PARSER ---
@st.cache_data
def parse_document(file):
    """Extracts text from TXT, DOCX, and PDF files."""
    text = ""
    try:
        if file.name.endswith('.txt') or file.name.endswith('.md'):
            text = file.getvalue().decode("utf-8")
        elif file.name.endswith('.docx'):
            doc = docx.Document(io.BytesIO(file.getvalue()))
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        elif file.name.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.getvalue()))
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
    except Exception as e:
        return f"Error parsing document {file.name}: {e}"
    return text

@st.cache_data
def generate_mock_data():
    np.random.seed(42)
    n = 2000
    return pd.DataFrame({
        'Respondent_ID': range(1, n + 1),
        'Mindset_Segment': np.random.choice(['The Harmonizer', 'The Satisfier', 'The Calculator', 'Unclassified'], n, p=[0.25, 0.30, 0.20, 0.25]),
        'Generation': np.random.choice(['Gen Z', 'Millennial', 'Gen X', 'Boomer+'], n, p=[0.15, 0.40, 0.25, 0.20]),
        'Income_Bracket': np.random.choice(['Under $50k', '$50k-$99k', '$100k-$149k', '$150k+'], n),
        'Region': np.random.choice(['Northeast', 'Midwest', 'South', 'West'], n),
        '_Weight': np.random.uniform(0.7, 1.3, n)
    })

@st.cache_data
def compute_simmons_crosstab(df, target_var, explore_var, weight_col):
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
    return final_table.drop('Total', errors='ignore')

st.title("Synthetic Mindset Engine 🎯")
st.markdown("<p class='big-font'>Fusing quantitative predispositions with qualitative human truths.</p>", unsafe_allow_html=True)

# Application State
df = None
active_mindset_db = DEFAULT_MINDSET_DATABASE.copy()

with st.sidebar:
    st.header("1. Ingest Data Streams")
    
    with st.expander("📊 Tabular Data (Quant)", expanded=True):
        st.caption("Upload Survey Data to power the Crosstab Engine.")
        quant_file = st.file_uploader("Upload Data", type=['csv', 'xlsx', 'tsv', 'parquet'])
        use_mock = st.button("Use Mock Audience Data")
        
    with st.expander("🧠 Structured Data (Qual Profiles)"):
        st.caption("Upload JSON to update Mindset definitions.")
        qual_json_file = st.file_uploader("Upload JSON", type=['json'])
        
    with st.expander("📓 Unstructured Text (Ethnography)"):
        st.caption("Upload raw transcripts, journals, or field notes.")
        raw_docs = st.file_uploader("Upload Documents", type=['txt', 'docx', 'pdf', 'md'], accept_multiple_files=True)

    with st.expander("📸 Visual Evidence (Anthropology)"):
        st.caption("Upload photos from the field or social listening screenshots.")
        image_files = st.file_uploader("Upload Images", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

# Process Data
if use_mock:
    df = generate_mock_data()
    st.sidebar.success("Loaded 2,000 Mock Respondents.")
elif quant_file is not None:
    try:
        df = load_quant_data(quant_file)
        st.sidebar.success(f"Loaded {len(df)} rows.")
    except Exception as e:
        st.sidebar.error(f"Quant Error: {e}")

if qual_json_file is not None:
    try:
        uploaded_profiles = load_qual_json(qual_json_file)
        active_mindset_db.update(uploaded_profiles)
        st.sidebar.success("Updated Qualitative Profiles.")
    except Exception as e:
        st.sidebar.error(f"JSON Error: {e}")

# Process New Document Types
doc_texts = {}
if raw_docs:
    for doc in raw_docs:
        doc_texts[doc.name] = parse_document(doc)

# Process Images
uploaded_images = []
if image_files:
    for img_file in image_files:
        try:
            img = Image.open(img_file)
            uploaded_images.append((img_file.name, img))
        except Exception as e:
            st.sidebar.error(f"Error loading image {img_file.name}: {e}")

if df is not None:
    columns = df.columns.tolist()

    st.sidebar.header("2. Strategy Configuration")
    target_var = st.sidebar.selectbox("Select Target (e.g., Mindset)", columns, index=columns.index('Mindset_Segment') if 'Mindset_Segment' in columns else 0)
    explore_var = st.sidebar.selectbox("Select Variable to Explore", columns, index=columns.index('Generation') if 'Generation' in columns else min(1, len(columns)-1))
    weight_var = st.sidebar.selectbox("Select Survey Weight", ['None (Unweighted)'] + columns, index=columns.index('_Weight')+1 if '_Weight' in columns else 0)

    if st.sidebar.button("Run Synthetic Analysis", type="primary"):
        
        # We now have 4 tabs to accommodate the multi-format data
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Quant Crosstab (Simmons)", 
            "🧠 The Synthetic Mindset (Qual)", 
            "📓 Raw Ethnography",
            "📸 Visual Evidence"
        ])
        
        with tab1:
            st.subheader(f"Profiling '{target_var}' against '{explore_var}'")
            
            weight_col = weight_var if weight_var != 'None (Unweighted)' else '__dummy_weight'
            if weight_col == '__dummy_weight':
                df['__dummy_weight'] = 1
                
            # Utilize the cached math function
            final_table = compute_simmons_crosstab(df, target_var, explore_var, weight_col)
            
            # Flatten MultiIndex columns to avoid Streamlit Styler exceptions
            final_table.columns = [f"{col[0]} | {col[1]}" for col in final_table.columns]
            
            def color_index(val):
                try:
                    v = float(val)
                    if pd.isna(v): return ''
                    color = '#27ae60' if v > 115 else '#c0392b' if v < 85 else 'inherit'
                    weight = 'bold' if v > 115 or v < 85 else 'normal'
                    return f'color: {color}; font-weight: {weight}'
                except (ValueError, TypeError):
                    return ''
            
            # Target only the newly flattened 'Index' columns
            index_cols = [col for col in final_table.columns if 'Index' in col]
            styled_table = final_table.style.map(color_index, subset=index_cols)
            
            st.dataframe(styled_table, use_container_width=True, height=400)
            st.caption("*Index > 115 indicates strong predisposition. Index < 85 indicates barrier.*")

        with tab2:
            st.subheader("The Growth Target Truths")
            
            available_targets = df[target_var].dropna().unique()
            selected_segment = st.selectbox("Select a Segment to Profile:", available_targets)
            
            # Look up the qualitative data from the active database
            qual_data = active_mindset_db.get(selected_segment)
            
            if qual_data:
                st.markdown(f"### {selected_segment}")
                st.markdown(f"*{qual_data.get('tagline', '')}*")
                
                segment_df = df[df[target_var] == selected_segment]
                total_n = len(segment_df)
                total_pop = len(df)
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(f"<div class='metric-container'><p class='status-dot' style='display:inline-block; margin-right:5px;'></p><b>Sample Size:</b> {total_n}</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"<div class='metric-container'><b>% of Population:</b> {round((total_n/total_pop)*100, 1)}%</div>", unsafe_allow_html=True)
                with c3:
                    st.markdown(f"<div class='metric-container'><b>Status:</b> Active Segment</div>", unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)

                col_left, col_right = st.columns([1.5, 1])
                
                with col_left:
                    st.markdown(f"""
                    <div style='padding: 20px; background-color: #f9f9f9; border-radius: 8px;'>
                        <p class='editorial-hero-sub'>1. Predisposition (Attitudes)</p>
                        <ul style='font-size: 14px; color: #333;'>
                            {"".join([f"<li>{item}</li>" for item in qual_data.get('attitudes', [])])}
                        </ul>
                        <br>
                        <p class='editorial-hero-sub'>2. Real World (Online Anthropology)</p>
                        <p style='font-size: 14px; color: #333;'>{qual_data.get('anthropology', 'No anthropology data available.')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_right:
                    st.markdown(f"""
                    <div style='padding: 20px; background-color: #f9f9f9; border-radius: 8px;'>
                        <p class='editorial-hero-sub'>3. Brand Alignment (Affinity)</p>
                        <p style='font-size: 14px; color: #333;'><i>Brands they index highly with:</i><br> <b>{', '.join(qual_data.get('brands', []))}</b></p>
                        <br>
                        <p class='editorial-hero-sub' style='color: #ff5500;'>4. THE HUMAN TRUTH</p>
                        <p style='font-size: 15px; font-weight: 500; color: #111; border-left: 3px solid #ff5500; padding-left: 10px;'>
                            {qual_data.get('truth', 'No truth defined.')}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning(f"No qualitative profile exists yet for '{selected_segment}'. Upload a JSON file in the sidebar to define this segment's qualitative traits.")

        with tab3:
            st.subheader("Raw Ethnographic Transcripts & Journals")
            if doc_texts:
                for doc_name, text in doc_texts.items():
                    with st.expander(f"📄 {doc_name}", expanded=False):
                        st.text_area("Content", value=text, height=300, disabled=True, key=f"text_{doc_name}")
            else:
                st.info("No documents uploaded. Use the sidebar to upload TXT, DOCX, PDF, or MD files.")

        with tab4:
            st.subheader("Visual Anthropology & Field Photos")
            if uploaded_images:
                cols = st.columns(3) # Display in a 3-column grid
                for i, (img_name, img) in enumerate(uploaded_images):
                    with cols[i % 3]:
                        st.image(img, caption=img_name, use_column_width=True)
            else:
                st.info("No images uploaded. Use the sidebar to upload PNG or JPG files.")

else:
    st.info("Awaiting Data Upload in the Sidebar. (Or click 'Use Mock Audience Data')")
