import streamlit as st
import pandas as pd
import numpy as np
import json
import io
from PIL import Image
import docx
import PyPDF2
import google.generativeai as genai

st.set_page_config(page_title="Roundpeg: Synthetic Mindset Engine", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    .big-font { font-size:18px !important; font-weight: 400; color: #555;}
    .mindset-card { background-color: #f8f9fa; padding: 20px; border-radius: 12px; border-left: 6px solid #FF6B6B; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px;}
    .truth-header { color: #FF6B6B; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-size: 14px; margin-bottom: 8px; }
    .metric-container { background-color: #ffffff; border: 1px solid #e0e0e0; padding: 15px; border-radius: 8px; text-align: center; }
    .status-dot { height: 10px; width: 10px; background-color: #27ae60; border-radius: 50%; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_quant_data(file):
    """Loads Survey Data from CSV or Excel safely."""
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

@st.cache_data(show_spinner=False)
def parse_document(file_bytes, file_name):
    """Universal parser for Ethnography and Interview transcripts."""
    text = ""
    try:
        if file_name.endswith('.txt') or file_name.endswith('.md'):
            text = file_bytes.decode("utf-8")
        elif file_name.endswith('.docx'):
            doc = docx.Document(io.BytesIO(file_bytes))
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        elif file_name.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        return f"[Error parsing {file_name}: {e}]"
    return text

@st.cache_data(show_spinner=False)
def generate_mock_data():
    """Generates 4,000 mock respondents for testing the engine without data."""
    np.random.seed(42)
    n = 4000
    return pd.DataFrame({
        'Respondent_ID': range(1, n + 1),
        'Mindset_Segment': np.random.choice(
            ['Moment Makers', 'Expressive Escapists', 'Green Mindset', 'Yellow Mindset', 'Blue Mindset'], 
            n, p=[0.25, 0.15, 0.20, 0.10, 0.30]
        ),
        'Generation': np.random.choice(['Gen Z', 'Millennial', 'Gen X', 'Boomer+'], n, p=[0.15, 0.40, 0.25, 0.20]),
        'Income_Bracket': np.random.choice(['Under $50k', '$50k-$99k', '$100k-$149k', '$150k+'], n),
        'Region': np.random.choice(['Northeast', 'Midwest', 'South', 'West'], n),
        '_Weight': np.random.uniform(0.7, 1.3, n)
    })

@st.cache_data(show_spinner=False)
def compute_simmons_crosstab(df, target_var, explore_var, weight_col):
    """The core MRI Simmons math engine for calculating Universe, Reach, Comp, and Index."""
    # Build the base cross-tabulation
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
    
    # Concat the results into a single multi-index dataframe
    final_table = pd.concat(results.values(), axis=1, keys=results.keys())
    final_table = final_table.drop('Total', errors='ignore')
    
    # Flatten the multi-index columns to prevent Streamlit Arrow errors
    final_table.columns = [f"{col[0]} | {col[1]}" for col in final_table.columns]
    
    return final_table

st.title("Roundpeg: Synthetic Mindset Engine 🎯")
st.markdown("<p class='big-font'>Fusing quantitative predispositions with qualitative human truths.</p>", unsafe_allow_html=True)

df = None
doc_texts = {}
uploaded_images = []

with st.sidebar:
    st.header("1. System Configuration")
    api_key = st.text_input("🔑 Gemini API Key", type="password", help="Required to synthesize qualitative truths.")
    if api_key:
        genai.configure(api_key=api_key)
        
    st.header("2. Ingest Data Streams")
    
    with st.expander("📊 Tabular Data (Quant)", expanded=True):
        st.caption("Upload Survey Data to power the Crosstab Engine.")
        quant_file = st.file_uploader("Upload Data", type=['csv', 'xlsx', 'tsv', 'parquet'])
        use_mock = st.button("Use Mock Audience Data")
        
    with st.expander("📓 Unstructured Text (Ethnography)"):
        st.caption("Upload raw transcripts, journals, or field notes.")
        raw_docs = st.file_uploader("Upload Documents", type=['txt', 'docx', 'pdf', 'md'], accept_multiple_files=True)

    with st.expander("📸 Visual Evidence (Anthropology)"):
        st.caption("Upload photos from the field or social listening screenshots.")
        image_files = st.file_uploader("Upload Images", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if use_mock:
    df = generate_mock_data()
    st.sidebar.success("Loaded 4,000 Mock Respondents.")
elif quant_file is not None:
    try:
        df = load_quant_data(quant_file)
        st.sidebar.success(f"Loaded {len(df)} rows.")
    except Exception as e:
        st.sidebar.error(f"Quant Error: {e}")

if raw_docs:
    for doc in raw_docs:
        doc_texts[doc.name] = parse_document(doc.getvalue(), doc.name)

if image_files:
    for img_file in image_files:
        try:
            img = Image.open(img_file)
            uploaded_images.append((img_file.name, img))
        except Exception as e:
            st.sidebar.error(f"Error loading image {img_file.name}: {e}")

if df is not None:
    columns = df.columns.tolist()

    st.sidebar.header("3. Strategy Configuration")
    target_var = st.sidebar.selectbox("Select Target Segment", columns, index=columns.index('Mindset_Segment') if 'Mindset_Segment' in columns else 0)
    explore_var = st.sidebar.selectbox("Select Variable to Explore", columns, index=columns.index('Generation') if 'Generation' in columns else min(1, len(columns)-1))
    weight_var = st.sidebar.selectbox("Select Survey Weight", ['None (Unweighted)'] + columns, index=columns.index('_Weight')+1 if '_Weight' in columns else 0)
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🧠 Roundpeg Mindset Synthesis", 
        "📊 Quant Crosstab Engine", 
        "📓 Raw Ethnography",
        "📸 Visual Evidence"
    ])
    
    with tab1:
        available_targets = [x for x in df[target_var].dropna().unique() if str(x).strip() != '']
        selected_segment = st.selectbox("Select a Segment to Profile & Synthesize:", available_targets)
        
        segment_df = df[df[target_var] == selected_segment]
        total_n = len(segment_df)
        total_pop = len(df)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='metric-container'><p class='status-dot'></p><br><b>Raw Sample Size:</b><br><span style='font-size: 24px;'>{total_n}</span></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='metric-container'><b>% of Total Audience:</b><br><span style='font-size: 24px;'>{round((total_n/total_pop)*100, 1)}%</span></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='metric-container'><b>Data Streams:</b><br><span style='font-size: 16px;'>{len(doc_texts)} Qual Docs | {len(columns)} Quant Vars</span></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("🔢 MRI Simmons Anchor")
        simmons_count_code = st.text_area(
            "Segment Count Code / Definition", 
            placeholder="e.g., Must agree with 5 of 8:\n- I enjoy taking risks\n- I like to stand out...", 
            help="Paste the Simmons count code logic here. The AI will use this as the anchor for the mindset's psychological profile."
        )
        
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("✨ Auto-Synthesize Mindset via Gemini", type="primary"):
            if not api_key:
                st.error("⚠️ Please enter your Gemini API Key in the sidebar to run the Strategy Engine.")
            else:
                with st.spinner(f"Synthesizing Roundpeg Profile for '{selected_segment}'..."):
                    
                    weight_col = weight_var if weight_var != 'None (Unweighted)' else '__dummy_weight'
                    if weight_col == '__dummy_weight':
                        df['__dummy_weight'] = 1
                    
                    math_context = compute_simmons_crosstab(df, target_var, explore_var, weight_col)
                    
                    quant_context_string = ""
                    try:
                        target_col = f"{selected_segment} | Index"
                        if target_col in math_context.columns:
                            segment_indices = math_context[target_col].dropna()
                            top_indices = segment_indices.sort_values(ascending=False).head(5).to_dict()
                            bottom_indices = segment_indices.sort_values(ascending=True).head(3).to_dict()
                            quant_context_string = f"Top Over-Indexing Traits in '{explore_var}': {top_indices}\nTop Under-Indexing Traits (Barriers): {bottom_indices}"
                        else:
                            quant_context_string = "Could not isolate index data for this specific segment."
                    except Exception as e:
                        quant_context_string = f"Failed to compute indices: {e}"

                    raw_context = "\n\n--- DOCUMENT BREAK ---\n\n".join(doc_texts.values())
                    if not raw_context.strip():
                        raw_context = "No raw qualitative/ethnographic text provided. You must rely purely on the quantitative inferences provided."
                    
                    prompt = f"""
                    You are a Senior Brand Strategist at Roundpeg, a highly respected boutique insights consultancy.
                    Your task is to synthesize raw quantitative and qualitative data into a strategic 'Roundpeg Growth Target Mindset'.
                    
                    We are building a profile for the consumer segment named: '{selected_segment}'.
                    
                    === DATA INPUTS ===
                    MRI SIMMONS COUNT CODE (Segment Definition):
                    {simmons_count_code if simmons_count_code else "No explicit count code provided. Rely on index scores."}

                    QUANTITATIVE CONTEXT (Index scores where 100 is average, >120 is high propensity):
                    {quant_context_string}
                    
                    QUALITATIVE ETHNOGRAPHY / FIELD NOTES:
                    {raw_context[:15000]}
                    
                    === ROUNDPEG METHODOLOGY ===
                    Adhere strictly to the Roundpeg 5 Fundamental Truths:
                    1. Purchase intent is fleeting, predisposition is forever (Focus on deep motivations, attitudes, beliefs).
                    2. Created in the real world (Reframe from a holistic human point-of-view).
                    3. Gets you where you want to go (Identify the vital drivers).
                    4. Master brand alignment (Complementary category opportunities).
                    5. Game-changing growth requires clarity & conviction (Uncover the defining human tension and barrier).
                    
                    === REQUIRED OUTPUT FORMAT ===
                    You MUST format your response EXACTLY using the following Markdown structure. Do not deviate.
                    
                    ### 🧠 THE {selected_segment.upper()} MINDSET
                    *(Write a punchy, insightful 1-2 sentence tagline summarizing who they are as people)*

                    <div class="mindset-card">
                    <p class="truth-header">The Human Truth (Clarity & Conviction)</p>
                    <ul>
                        <li><b>The Core Tension:</b> (What is holding them back in the real world? What is their struggle?)</li>
                        <li><b>The Ultimate Truth:</b> (The strategic narrative or emotional hook a brand must adopt to win them over.)</li>
                    </ul>
                    </div>

                    #### 1. What they value in a Product/Brand
                    *   **Conscious Interest:** (What do they actively look for? e.g., innovative design, safety, status)
                    *   **Top Motivations:** (What drives their underlying behavior? e.g., feeling alive, protecting family)
                    *   **Willingness to Spend:** (How do they view money/purchasing in this context?)

                    #### 2. How they consume media & the world
                    *(Write a tight, strategic paragraph on their online anthropology—how they use social media, what they read, who they trust. Base this on the provided data, or infer deeply based on their generational/index profile).*
                    """
                    
                    try:
                        model = genai.GenerativeModel('gemini-1.5-pro')
                        response = model.generate_content(prompt)
                        st.success("Roundpeg Synthesis Complete!")
                        st.markdown(response.text, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"AI Generation Error. Please check your API Key and network. Details: {e}")

    with tab2:
        st.subheader("Simmons-Style Crosstab")
        st.caption("Metrics calculated: Universe (000), Vertical % (Composition), Horizontal % (Reach), and Index (Propensity).")
        
        weight_col = weight_var if weight_var != 'None (Unweighted)' else '__dummy_weight'
        if weight_col == '__dummy_weight':
            df['__dummy_weight'] = 1
            
        final_table = compute_simmons_crosstab(df, target_var, explore_var, weight_col)
        
        def color_index(val):
            try:
                v = float(val)
                if pd.isna(v): return ''
                color = '#27ae60' if v > 115 else '#c0392b' if v < 85 else 'inherit'
                weight = 'bold' if v > 115 or v < 85 else 'normal'
                return f'color: {color}; font-weight: {weight}'
            except (ValueError, TypeError):
                return ''
        
        index_cols = [col for col in final_table.columns if 'Index' in col]
        styled_table = final_table.style.map(color_index, subset=index_cols)
        
        st.dataframe(styled_table, use_container_width=True, height=600)

    with tab3:
        st.subheader("Raw Ethnographic Transcripts & Journals")
        if doc_texts:
            for doc_name, text in doc_texts.items():
                with st.expander(f"📄 {doc_name}", expanded=False):
                    st.text_area(f"Contents of {doc_name}", value=text, height=300, disabled=True)
        else:
            st.info("No qualitative documents uploaded. Use the sidebar to upload TXT, DOCX, PDF, or MD files.")

    with tab4:
        st.subheader("Visual Anthropology & Field Photos")
        if uploaded_images:
            cols = st.columns(3)
            for i, (img_name, img) in enumerate(uploaded_images):
                with cols[i % 3]:
                    st.image(img, caption=img_name, use_container_width=True)
        else:
            st.info("No images uploaded. Use the sidebar to upload PNG or JPG files.")

else:
    st.info("Awaiting Data Upload in the Sidebar. (Click 'Use Mock Audience Data' to demo the system).")
