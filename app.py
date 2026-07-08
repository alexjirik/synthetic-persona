import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="Synthetic Mindset Engine", layout="wide")
st.title("Synthetic Mindset Engine 🧠")
st.markdown("Upload raw survey data to dynamically generate Simmons-style strategic crosstabs.")

# 1. File Uploader in Sidebar
st.sidebar.header("1. Data Ingestion")
uploaded_file = st.sidebar.file_uploader("Upload Survey Data (CSV or Excel)", type=['csv', 'xlsx'])

# 2. Main Logic Execution
if uploaded_file is not None:
    # Read file based on extension
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.sidebar.success("Data loaded successfully!")
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

    # 3. Dynamic Column Selection
    st.sidebar.header("2. Crosstab Configuration")
    columns = df.columns.tolist()
    
    row_var = st.sidebar.selectbox("Select Row (e.g., Target Demographic)", columns)
    col_var = st.sidebar.selectbox("Select Column (e.g., Mindset Segment)", columns)
    
    weight_options = ['None (Unweighted)'] + columns
    weight_var = st.sidebar.selectbox("Select Survey Weight (Optional)", weight_options)

    # 4. The Simmons Math Engine
    if st.button("Generate Strategic Crosstab"):
        # Apply weighting logic
        if weight_var == 'None (Unweighted)':
            df['_Weight'] = 1
            weight_col = '_Weight'
        else:
            weight_col = weight_var
            
        # Base Crosstab Calculation
        crosstab = pd.crosstab(
            df[row_var], 
            df[col_var], 
            values=df[weight_col], 
            aggfunc='sum', 
            margins=True, 
            margins_name='Total'
        )
        
        # Calculate Simmons Core Metrics
        results = {}
        for column in crosstab.columns:
            if column != 'Total':
                count = crosstab[column]
                # Vertical % (Of the column, how many are in this row?)
                vert_pct = (count / crosstab.loc['Total', column]) * 100
                # Horizontal % (Of the row, how many are in this column?)
                horz_pct = (count / crosstab['Total']) * 100
                # Population % for Index baseline
                pop_pct = (crosstab['Total'] / crosstab.loc['Total', 'Total']) * 100
                # Index (Propensity)
                index = (vert_pct / pop_pct) * 100
                
                results[column] = pd.DataFrame({
                    'Size': count.round(0),
                    'Vert %': vert_pct.round(1),
                    'Horz %': horz_pct.round(1),
                    'Index': index.round(0)
                })
        
        # Format and display the final table
        final_table = pd.concat(results.values(), axis=1, keys=results.keys())
        # Drop the aggregate 'Total' row to keep the strategic view clean
        final_table = final_table.drop('Total', errors='ignore')
        
        st.subheader(f"Analyzing: {row_var} by {col_var}")
        
        # Use st.dataframe for an interactive, scrollable, and sortable table
        st.dataframe(final_table, use_container_width=True)

else:
    # Empty State
    st.info("Awaiting data. Please upload a CSV or Excel file in the sidebar to begin.")
    st.write("### Expected Data Format")
    st.write("Your file should be raw respondent-level data, where each row is a person and each column is a survey question, demographic marker, or assigned mindset.")
