import streamlit as st
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="SafeSync",
    page_icon="logo.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for a Professional & Theme-Aware Look ---
st.markdown("""
<style>
    /* Base Styling */
    .stApp {
        background-color: var(--background-color);
    }
    :root{--bg:#0b1220;--card:#262730;--text:#e0e4f4;--muted:#a3acc2;--accent:#6ee7b7;--warn:#ffe08a;--error:#ff9aa2;--line:#1f2943}
    /* Card Styling using Streamlit Theme Variables */
    .card {
        background:var(--card);
        color: var(--text);
        /* background-color: var(--secondary-background-color); */
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid var(--gray-200);
    }
    /* Main title card header */
    .card h2 {
        color: var(--primary-color);
        font-size: 1.75rem;
        margin-top: 0;
        margin-bottom: 0.5rem;
        border-bottom: none; /* No line under this specific header */
    }
    /* Sub-headers inside other cards */
    .card h3 {
        color: var(--primary-color);
        margin-top: 0; /* Removes extra space above the title */
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--gray-300);
    }
    .card p, .card li {
        color: var(--text-color);
    }
    .muted {
        color: var(--gray-600);
        font-size: 0.9rem;
    }
    
    /* Specific styles for Drug Interaction List */
    .ddi-list ul {
        list-style-type: none;
        padding-left: 0;
    }
    .ddi-list li {
        padding: 0.75rem;
        border-left-width: 5px;
        border-left-style: solid;
        margin-bottom: 0.5rem;
        border-radius: 5px;
        background-color: var(--background-color);
    }
    .ddi-major {
        border-left-color: var(--red-80);
    }
    .ddi-moderate {
        border-left-color: var(--orange-80);
    }
    .ddi-minor {
        border-left-color: var(--blue-60);
    }
    .ddi-none {
        border-left-color: var(--gray-60);
    }

</style>
""", unsafe_allow_html=True)


# --- Sidebar ---
with st.sidebar:
    st.image("logo.jpg", width=120)
    st.title("SafeSync")
    st.markdown("##### *Smarter Choice, Safer Outcomes*")
    st.markdown("---")
    st.info("This tool provides drug formulation and interaction information based on the uploaded datasets. It is intended for informational purposes by medical professionals.")

# --- Data Loading and Caching ---
@st.cache_data
def load_data():
    try:
        df_drugs = pd.read_csv('data/merged.csv')
        df_interactions = pd.read_csv('data/Interaction.csv')
        df_drugs.columns = df_drugs.columns.str.strip()
        df_interactions.columns = df_interactions.columns.str.strip()
        if 'Mechansim' in df_interactions.columns:
            df_interactions.rename(columns={'Mechansim': 'Mechanism'}, inplace=True)
        return df_drugs, df_interactions
    except FileNotFoundError:
        st.error("Error: Dataset files not found. Please ensure `merged.csv` and `Interaction.csv` are in the 'data' directory.")
        return None, None

df_drugs, df_interactions = load_data()

# --- Main Page ---
st.title("SafeSync Drug Reference")
st.markdown("Select a drug and its dosage form to retrieve detailed formulation and safety information.")

if df_drugs is not None and df_interactions is not None:
    # --- User Input Section ---
    col1, col2 = st.columns([2, 2])
    api_list = sorted(df_drugs['Active pharmaceutical Ingredient (API)'].dropna().unique())
    
    with col1:
        selected_api = st.selectbox("Search for a Drug Name (API)", api_list, index=None, placeholder="Type or select a drug...")

    with col2:
        if selected_api:
            dosage_forms = sorted(df_drugs[df_drugs['Active pharmaceutical Ingredient (API)'] == selected_api]['Dosage_Form'].dropna().unique())
            selected_dosage = st.selectbox("Select Dosage Form", dosage_forms, index=None, placeholder="Select dosage...")
        else:
            st.selectbox("Select Dosage Form", [], disabled=True, placeholder="Select a drug first...")

    st.write("") # Spacer

    if st.button("Get Drug Information", type="primary", use_container_width=True):
        if selected_api and 'selected_dosage' in locals() and selected_dosage:
            drug_info = df_drugs[(df_drugs['Active pharmaceutical Ingredient (API)'] == selected_api) & (df_drugs['Dosage_Form'] == selected_dosage)]

            if not drug_info.empty:
                drug_info_row = drug_info.iloc[0]

                st.markdown("---")
                
                # --- Main Summary Card ---
                st.markdown(f"""
                <div class="card">
                    <h2>{drug_info_row['Active pharmaceutical Ingredient (API)']} — {drug_info_row['Dosage_Form']}</h2>
                    <strong>Overall excipient compatibility:</strong> Compatible<br>
                    <span class="muted">Therapeutic Class: {drug_info_row.get('Therapeutic_Class', 'N/A')}</span>
                </div>
                """, unsafe_allow_html=True)

                # --- Full Formulation Card ---
                st.markdown('<div class="card"><h3>💊 Full Formulation</h3>', unsafe_allow_html=True)
                excipients = [e.strip() for e in str(drug_info_row.get('Excipient_List', '')).split(';')]
                roles = [r.strip() for r in str(drug_info_row.get('Excipient_Roles', '')).split(';')]

                # FIX 1: Check if the first excipient is 'API' and remove it if so.
                if excipients and excipients[0].upper() == 'API':
                    excipients = excipients[1:]
                    roles = roles[1:]

                min_len = min(len(excipients), len(roles))
                formulation_df = pd.DataFrame({'Excipient Name': excipients[:min_len], 'Role': roles[:min_len]})
                st.table(formulation_df)
                st.markdown('</div>', unsafe_allow_html=True)

                # --- Storage & Compatibility Cards ---
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('<div class="card"><h3>🌡️ Recommended Storage</h3>', unsafe_allow_html=True)
                    st.info(f"**{drug_info_row.get('Recommended_Storage', 'Not specified.')}**")
                    st.markdown('</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown('<div class="card"><h3>🧪 Excipient Compatibility Notes</h3>', unsafe_allow_html=True)
                    notes = drug_info_row.get('Regulatory_Notes')
                    if pd.isna(notes) or str(notes).strip().lower() == 'nan':
                        st.warning('No specific compatibility notes available.')
                    else:
                        st.warning(str(notes))
                    st.markdown('</div>', unsafe_allow_html=True)

                # --- Drug-Drug Interactions (DDI) Card ---
                st.markdown('<div class="card ddi-list"><h3>🔄 Drug–Drug Interaction Summary</h3>', unsafe_allow_html=True)
                interactions = df_interactions[df_interactions['Drug A'] == selected_api]
                if not interactions.empty:
                    interaction_list_html = "<ul>"
                    has_valid_interaction = False
                    
                    for _, row in interactions.iterrows():
                        severity_text = str(row['Severity'])
                        severity_class = severity_text.strip().lower()
                        
                        # FIX 2: Skip rows where severity is 'nan', 'none', or empty.
                        if severity_class in ['nan', 'none', '']:
                            continue
                        
                        has_valid_interaction = True
                        interaction_list_html += (
                            f'<li class="ddi-{severity_class}">'
                            f"<strong>{row['Drug B']} ({severity_text}):</strong> "
                            f"{row.get('Mechanism', 'No mechanism described.')}</li>"
                        )
                    interaction_list_html += "</ul>"
                    
                    if has_valid_interaction:
                        st.markdown(interaction_list_html, unsafe_allow_html=True)
                    else:
                        st.success("No significant drug-drug interactions found in the dataset.")
                else:
                    st.success("No significant drug-drug interactions found in the dataset.")
                st.markdown('</div>', unsafe_allow_html=True)

                # --- References Card ---
                st.markdown(f"""<div class="card"><h3>📚 References</h3>
                <ul>
                    <li>_{drug_info_row.get('ReferenceSource', 'No references listed.')}_</li>
                </ul>
                </div>""", unsafe_allow_html=True)

            else:
                st.error("No data found for the selected drug and dosage form combination.")
        else:
            st.warning("Please select both a drug and a dosage form before proceeding.")