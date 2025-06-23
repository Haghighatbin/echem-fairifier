import streamlit as st
import yaml
import pandas as pd
from io import BytesIO
import zipfile

st.markdown("""
<style>
.main-header {
    text-align: center;
    padding: 1rem 0;
    margin-bottom: 2rem;
}
.info-box {
    background-color: #e7f3ff;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #1f77b4;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)
st.subheader('A Project by Amin Haghighatbin', divider=True, width=400)
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.title("⚡ EChem FAIRifier")
st.markdown("**Making electrochemical data FAIR-compliant**")
st.markdown('</div>', unsafe_allow_html=True)

with st.expander("ℹ️ What is FAIR data?"):
    st.markdown("""
    **FAIR** stands for:
    - **F**indable: Easy to locate and identify
    - **A**ccessible: Retrievable by identifier using standard protocols  
    - **I**nteroperable: Data can be integrated with other data
    - **R**eusable: Well-described so that it can be replicated/combined
    
    This tool helps make your electrochemical data FAIR by adding standardised metadata.
    """)

st.set_page_config(page_title="EChem FAIRifier", layout="wide")

TECHNIQUE_PARAMETERS = {
    "CV": {
        "scan_rate": 0.1,
        "start_potential": -0.2,
        "end_potential": 0.6,
        "step_size": 0.002,
        "cycles": 1
    },
    "DPV": {
        "pulse_amplitude": 0.05,
        "pulse_width": 0.05,
        "step_potential": 0.005,
        "scan_rate": 0.01
    },
    "SWV": {
        "frequency": 25,
        "amplitude": 0.025,
        "step_height": 0.004
    },
    "EIS": {
        "frequency_range": [1e5, 0.01],
        "ac_amplitude": 0.01,
        "bias_potential": 0.0,
        "equilibration_time": 10
    },
    "CA": {
        "step_potentials": [0.0, 0.5],
        "step_times": [5, 60],
        "total_duration": 65
    }
}


col1, col2 = st.columns([1, 1])
with col1:
    # --- File upload ---
    uploaded_file = st.file_uploader("Upload CV/EIS data (.csv)", type="csv")
    # --- Shared Metadata Fields ---
    technique = st.selectbox("Select Technique", list(TECHNIQUE_PARAMETERS.keys()))
    electrolyte = st.text_input("Electrolyte", "3 mM [FeCN6] in 0.1 M KNO3")
    working_electrode = st.text_input("Working Electrode", "Glassy carbon, 3 mm")
    reference_electrode = st.text_input("Reference Electrode", "Ag/AgCl")
    counter_electrode = st.text_input("Counter Electrode", "Platinum wire")


with col2:
    st.subheader("Technique Parameters")
    custom_params = {}
    for param, default in TECHNIQUE_PARAMETERS[technique].items():
        if isinstance(default, list):
            val = st.text_input(f"{param.replace('_', ' ').title()} (comma-separated)", 
                                ", ".join(map(str, default)))
            custom_params[param] = [float(x.strip()) for x in val.split(",") if x.strip()]
        else:
            custom_params[param] = st.number_input(f"{param.replace('_', ' ').title()}", value=default)
st.markdown("---")
col3, col4 = st.columns([1, 1])
if uploaded_file:
    metadata = {
        "technique": technique,
        "technique_parameters": custom_params,
        "electrolyte": electrolyte,
        "working_electrode": working_electrode,
        "reference_electrode": reference_electrode,
        "counter_electrode": counter_electrode,
        "dataset_link": uploaded_file.name
    }

    metadata_yaml_str = yaml.dump(metadata)

    with col3:
        st.subheader("Metadata Preview (YAML)")
        st.code(metadata_yaml_str, language="yaml")

    try:
        df = pd.read_csv(uploaded_file)
        if {'Potential (V)', 'Current (A)'}.issubset(df.columns):
            st.subheader("Voltammogram Preview")
            with col4:
                st.scatter_chart(df.set_index('Potential (V)')['Current (A)'], x_label='Potential / V', y_label='Current / A')
        else:
            st.info("CSV does not contain 'Potential (V)' and 'Current (A)' headers. Skipping plot.")
    except Exception as e:
        st.error(f"Error reading CSV for plotting: {e}")


    zip_buffer = BytesIO()
    try:
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("metadata.yaml", metadata_yaml_str)
            zip_file.writestr(uploaded_file.name, uploaded_file.getvalue())
        zip_buffer.seek(0)
    except Exception as e:
        st.error(f"Error creating the zip file: {e}")

    st.download_button(
            label="Download FAIR Bundle (.zip)",
            data=zip_buffer,
            file_name="fair_bundle.zip",
            mime="application/zip"
        )

else:
    st.warning("Please upload your electrochemical data file to continue.")

