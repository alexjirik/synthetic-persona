import streamlit as st
import pandas as pd
import numpy as np
import json
import io
from PIL import Image
import docx
import PyPDF2
import google.generativeai as genai

st.set_page_config(page_title="Roundpeg: Synthetic Mindset Engine", layout="wide")

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

# ---------------------------------------------------------
# CACHED DATA LOADERS (Speed Optimization)
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
    n = 4000
    return pd.DataFrame({
        'Respondent_ID': range(1, n + 1),
        'Mindset_Segment': np.random.choice(['Moment Makers', 'Expressive Escapists', 'Green Mindset', 'Yellow Mindset', 'Blue Mindset'], n, p=[0.25, 0.15, 0.20, 0.10, 0.30]),
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

# ---------------------------------------------------------
# UI & INGESTION
# ---------------------------------------------------------

st.title("Roundpeg: Synthetic Mindset Engine 🎯")
st.markdown("<p class='big-font'>Fusing quantitative predispositions with qualitative human truths.</p>", unsafe_allow_html=True)

df = None
doc_texts = {}
uploaded_images = []

with st.sidebar:
    st.header("1. Ingest Data Streams")
    
    api_key = st.text_input("🔑 Gemini API Key (Required for Synthesis)", type="password")
    if api_key:
        genai.configure(api_key=api_key)
        
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
        doc_texts[doc.name] = parse_document(doc)

if image_files:
    for img_file in image_files:
        try:
            img = Image.open(img_file)
            uploaded_images.append((img_file.name, img))
        except Exception as e:
            st.sidebar.error(f"Error loading image {img_file.name}: {e}")

# ---------------------------------------------------------
# STRATEGY EXECUTION
# ---------------------------------------------------------

if df is not None:
    columns = df.columns.tolist()

    st.sidebar.header("2. Strategy Configuration")
    target_var = st.sidebar.selectbox("Select Target (e.g., Mindset)", columns, index=columns.index('Mindset_Segment') if 'Mindset_Segment' in columns else 0)
    explore_var = st.sidebar.selectbox("Select Variable to Explore", columns, index=columns.index('Generation') if 'Generation' in columns else min(1, len(columns)-1))
    weight_var = st.sidebar.selectbox("Select Survey Weight", ['None (Unweighted)'] + columns, index=columns.index('_Weight')+1 if '_Weight' in columns else 0)

    if st.sidebar.button("Run Synthetic Analysis", type="primary"):
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "🧠 Roundpeg Mindset Synthesis", 
            "📊 Quant Crosstab Engine", 
            "📓 Raw Ethnography",
            "📸 Visual Evidence"
        ])
        
        # --- TAB 1: THE ROUNDPEG LLM SYNTHESIS ENGINE ---
        with tab1:
            st.subheader("Generate Roundpeg Mindset Profile")
            
            available_targets = df[target_var].dropna().unique()
            selected_segment = st.selectbox("Select a Segment to Synthesize:", available_targets)
            
            if st.button("✨ Auto-Synthesize Mindset via Gemini"):
                if not api_key:
                    st.warning("⚠️ Please enter your Gemini API Key in the sidebar to run the Synthesis Engine.")
                else:
                    with st.spinner(f"Synthesizing Roundpeg Profile for '{selected_segment}'..."):
                        
                        # 1. Grab Quant Data Context (Top indexing traits for this specific segment)
                        segment_df = df[df[target_var] == selected_segment]
                        total_n = len(segment_df)
                        
                        # We calculate the top indexing elements from the explore_var to feed the AI
                        weight_col = weight_var if weight_var != 'None (Unweighted)' else '__dummy_weight'
                        if weight_col == '__dummy_weight':
                            df['__dummy_weight'] = 1
                        
                        math_context = compute_simmons_crosstab(df, target_var, explore_var, weight_col)
                        try:
                            # Safely extract the 'Index' column for the selected segment
                            if selected_segment in math_context.columns.get_level_values(0):
                                segment_indices = math_context.xs('Index', axis=1, level=1)[selected_segment]
                                top_indices = segment_indices.sort_values(ascending=False).head(5).to_dict()
                                quant_context_string = f"Top Indexing '{explore_var}' Traits: {top_indices}"
                            else:
                                quant_context_string = "Quant data available, but index calculation failed for this specific slice."
                        except Exception as e:
                            quant_context_string = f"Could not compute top indices automatically. ({e})"

                        # 2. Grab Qual Data Context (Raw ethnography)
                        raw_context = "\n".join(doc_texts.values())
                        if not raw_context:
                            raw_context = "No raw ethnographic text provided. Rely purely on quantitative inferences."
                        
                        # 3. THE ROUNDPEG SYSTEM PROMPT
                        prompt = f"""
                        You are a senior brand strategist at Roundpeg, a boutique insights consultancy. 
                        Your job is to synthesize raw data into a 'Roundpeg Growth Target Mindset'.
                        
                        We are building a profile for a consumer segment named: '{selected_segment}'.
                        Sample Size in data: {total_n}.
                        
                        Here is the Quantitative Data (Index scores where 100 is average):
                        {quant_context_string}
                        
                        Here are the Qualitative Field Notes/Ethnographies:
                        {raw_context[:10000]}
                        
                        INSTRUCTIONS:
                        You must generate a strategic profile that strictly adheres to the 'Roundpeg 5 Fundamental Truths':
                        1. Predisposition is forever (Focus on motivations, attitudes, beliefs).
                        2. Created in the real world (Holistic human point-of-view).
                        3. Gets you where you want to go (Identify the 20% who drive 80% of business).
                        4. Master brand alignment (Category opportunities).
                        5. Clarity & conviction (Uncover the defining human truth/tension).
                        
                        OUTPUT FORMAT (You must use exactly these headers):
                        
                        ### 🧠 {selected_segment.upper()} MINDSET
                        *(Provide a 1-2 sentence tagline summarizing who they are as people)*
                        
                        #### 1. What they value in a brand
                        *   **Conscious Interest:** (What do they actively look for?)
                        *   **Top Motivations:** (What drives their purchase behavior?)
                        
                        #### 2. The Human Truth (Clarity & Conviction)
                        *   **Tension/Barrier:** (What is holding them back in the real world?)
                        *   **The Ultimate Truth:** (The strategic narrative the brand must adopt to win them over)
                        
                        #### 3. How they consume media & the world
                        *(A short paragraph on their online anthropology—how they use social media, what they read, who they trust based on the provided data)*
                        
                        Do not use generic marketing jargon. Speak with empathy, clarity, and precision.
                        """
                        
                        try:
                            # Using Gemini 1.5 Pro
                            model = genai.GenerativeModel('gemini-1.5-pro')
                            response = model.generate_content(prompt)
                            
                            st.success("Roundpeg Synthesis Complete!")
                            st.markdown(f"<div style='padding: 20px; background-color: #fcfcfc; border-left: 6px solid #FF6B6B; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>{response.text}</div>", unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"AI Generation Error: {e}")

        # --- TAB 2: QUANT CROSSTAB ENGINE ---
        with tab2:
            st.subheader(f"Profiling '{target_var}' against '{explore_var}'")
            
            weight_col = weight_var if weight_var != 'None (Unweighted)' else '__dummy_weight'
            if weight_col == '__dummy_weight':
                df['__dummy_weight'] = 1
                
            final_table = compute_simmons_crosstab(df, target_var, explore_var, weight_col)
            
            # Flatten MultiIndex for Streamlit display
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
            
            index_cols = [col for col in final_table.columns if 'Index' in col]
            styled_table = final_table.style.map(color_index, subset=index_cols)
            
            st.dataframe(styled_table, use_container_width=True, height=500)

        # --- TAB 3: RAW ETHNOGRAPHY ---
        with tab3:
            st.subheader("Raw Ethnographic Transcripts & Journals")
            if doc_texts:
                for doc_name, text in doc_texts.items():
                    with st.expander(f"📄 {doc_name}", expanded=False):
                        st.text_area("Content", value=text, height=300, disabled=True, key=f"text_{doc_name}")
            else:
                st.info("No documents uploaded. Use the sidebar to upload TXT, DOCX, PDF, or MD files.")

        # --- TAB 4: VISUAL EVIDENCE ---
        with tab4:
            st.subheader("Visual Anthropology & Field Photos")
            if uploaded_images:
                cols = st.columns(3)
                for i, (img_name, img) in enumerate(uploaded_images):
                    with cols[i % 3]:
                        st.image(img, caption=img_name, use_column_width=True)
            else:
                st.info("No images uploaded. Use the sidebar to upload PNG or JPG files.")

else:
    st.info("Awaiting Data Upload in the Sidebar. (Or click 'Use Mock Audience Data')")
