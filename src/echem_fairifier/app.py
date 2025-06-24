"""
EChem FAIRifier - Main Streamlit Application
Making electrochemical data FAIR-compliant
"""

import streamlit as st
import pandas as pd
import yaml
from io import BytesIO
import zipfile
from typing import Dict, Any

from .config.techniques import ElectrochemicalTechniques
from .core.metadata_generator import FAIRMetadataGenerator
from .ui.components import UIComponents

# Page configuration
st.set_page_config(
    page_title="EChem FAIRifier",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/haghighatbin/echem-fairifier',
        'Report a bug': 'https://github.com/haghighatbin/echem-fairifier/issues',
        'About': "EChem FAIRifier v1.0 - Making electrochemical data FAIR-compliant"
    }
)


def main():
    """Main application function."""
    
    ui = UIComponents()
    metadata_gen = FAIRMetadataGenerator()
    
    ui.render_header()
    ui.render_fair_info()
    
    with st.sidebar:
        st.header("📋 Progress")
        progress_container = st.container()
    
    tab1, tab2, tab3 = st.tabs(["📁 Data Upload", "📝 Metadata", "📦 Export"])
    
    # Initialise session state
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'metadata' not in st.session_state:
        st.session_state.metadata = None
    if 'validation_results' not in st.session_state:
        st.session_state.validation_results = None
    
    # Tab 1: Data Upload
    with tab1:
        uploaded_file = ui.render_file_upload()
        
        if uploaded_file:
            st.session_state.uploaded_file = uploaded_file
            
            try:
                # Validate and load data
                if not uploaded_file.name.endswith('.csv'):
                    st.error("❌ Please upload a CSV file.")
                    return
                
                df = pd.read_csv(uploaded_file)
                
                if df.empty:
                    st.warning("⚠️ The uploaded file appears to be empty/incomplete.")
                    return
                
                # Store dataframe in session state
                st.session_state.df = df
                
                # Show data preview
                # [TODO: Needs more clever algo to ignore the headers and handle different column-headers]
                ui.render_data_preview(df, "CV")  # Default to CV for preview 
                
                st.success("✅ File uploaded successfully!")
                
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
                st.info("Please ensure your file is a valid CSV with proper formatting.")
                return
    
    # Tab 2: Metadata Configuration
    with tab2:
        if not st.session_state.uploaded_file:
            st.info("👈 Please upload a data file first.")
            return
        
        st.header("🔬 Experimental Configuration")
        
        # Technique selection
        technique, description = ui.render_technique_selector()
        
        # Update data preview with correct technique
        if 'df' in st.session_state:
            with st.expander("📊 Updated Data Preview"):
                ui.render_data_preview(st.session_state.df, technique)
        
        # Technique parameters
        technique_parameters = ui.render_technique_parameters(technique)
        
        # Experimental details
        experimental_details = ui.render_experimental_details()
        
        # Attribution fields
        attribution_details = ui.render_attribution_fields()
        
        # Combine all details
        all_experimental_details = {**experimental_details, **attribution_details}
        
        # Generate metadata
        if st.button("🔄 Generate Metadata", type="primary"):
            try:
                dataset_info = {
                    "filename": st.session_state.uploaded_file.name
                }
                
                metadata = metadata_gen.generate_metadata(
                    technique=technique,
                    technique_parameters=technique_parameters,
                    experimental_details=all_experimental_details,
                    dataset_info=dataset_info
                )
                
                st.session_state.metadata = metadata
                
                # Validate metadata
                validation_results = metadata_gen.validate_metadata(metadata)
                st.session_state.validation_results = validation_results
                
                st.success("✅ Metadata generated successfully!")
                
            except Exception as e:
                st.error(f"❌ Error generating metadata: {str(e)}")
    
    # Tab 3: Export and Preview
    with tab3:
        if not st.session_state.metadata:
            st.info("👈 Please generate metadata first.")
            return
        
        st.header("📋 Metadata Preview & Export")
        
        # Show validation results
        if st.session_state.validation_results:
            ui.render_validation_results(st.session_state.validation_results)
        
        # Metadata preview
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📄 YAML Metadata")
            yaml_str = metadata_gen.generate_yaml(st.session_state.metadata)
            st.code(yaml_str, language="yaml")
            
            # Download YAML button
            st.download_button(
                label="📄 Download Metadata (YAML)",
                data=yaml_str,
                file_name=f"metadata_{technique.lower()}.yaml",
                mime="text/yaml"
            )
        
        with col2:
            st.subheader("🔍 Metadata Summary")
            
            # Display key information
            metadata = st.session_state.metadata
            
            st.write("**Experiment Overview:**")
            st.write(f"• Technique: {metadata.get('technique', {}).get('name', 'N/A')}")
            st.write(f"• Created: {metadata.get('created_date', 'N/A')[:10]}")
            st.write(f"• ID: {metadata.get('experiment_id', 'N/A')[:8]}...")
            
            exp_setup = metadata.get('experimental_setup', {})
            st.write("**Experimental Setup:**")
            st.write(f"• Working Electrode: {exp_setup.get('working_electrode', 'N/A')}")
            st.write(f"• Electrolyte: {exp_setup.get('electrolyte', 'N/A')}")
            
            attribution = metadata.get('attribution', {})
            if attribution.get('creator'):
                st.write("**Attribution:**")
                st.write(f"• Creator: {attribution.get('creator', 'N/A')}")
                st.write(f"• Institution: {attribution.get('institution', 'N/A')}")
        
        # FAIR Bundle Export
        st.markdown("---")
        st.subheader("📦 FAIR Data Bundle")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("**Bundle Contents:**")
            st.write("• Original data file (CSV)")
            st.write("• FAIR metadata (YAML)")
            st.write("• README with usage instructions")
        
        with col2:
            if st.button("📦 Create FAIR Bundle", type="primary"):
                try:
                    # Create ZIP bundle
                    zip_buffer = create_fair_bundle(
                        st.session_state.uploaded_file,
                        yaml_str,
                        st.session_state.metadata
                    )
                    
                    st.download_button(
                        label="⬇️ Download FAIR Bundle (.zip)",
                        data=zip_buffer,
                        file_name=f"fair_bundle_{technique.lower()}_{metadata.get('experiment_id', 'unknown')[:8]}.zip",
                        mime="application/zip"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Error creating bundle: {str(e)}")
    
    # Update progress sidebar
    update_progress_sidebar(progress_container)


def create_fair_bundle(uploaded_file, yaml_str: str, metadata: Dict[str, Any]) -> BytesIO:
    """Create a ZIP bundle with data and metadata."""
    
    zip_buffer = BytesIO()
    
    # Create README content
    readme_content = generate_readme(metadata)
    
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Add original data file
        zip_file.writestr(uploaded_file.name, uploaded_file.getvalue())
        
        # Add metadata
        zip_file.writestr("metadata.yaml", yaml_str)
        
        # Add README
        zip_file.writestr("README.md", readme_content)
        
        # Add citation file
        citation_content = generate_citation(metadata)
        zip_file.writestr("CITATION.cff", citation_content)
    
    zip_buffer.seek(0)
    return zip_buffer


def generate_readme(metadata: Dict[str, Any]) -> str:
    """Generate README content for the FAIR bundle."""
    
    technique_name = metadata.get('technique', {}).get('name', 'Unknown')
    created_date = metadata.get('created_date', 'Unknown')[:10]
    
    readme = f"""# Electrochemical Data Bundle

## Overview
This bundle contains FAIR-compliant electrochemical data generated using EChem FAIRifier.

**Technique:** {technique_name}
**Created:** {created_date}
**ID:** {metadata.get('experiment_id', 'N/A')}

## Files Included
- `{metadata.get('dataset', {}).get('filename', 'data.csv')}` - Raw experimental data
- `metadata.yaml` - FAIR metadata following EChem-FAIR schema
- `CITATION.cff` - Citation information in Citation File Format

## Usage
This data follows FAIR principles:
- **Findable:** Unique identifier and rich metadata
- **Accessible:** Open formats (CSV, YAML)
- **Interoperable:** Standardised vocabulary and structure
- **Reusable:** Clear licensing and attribution

## Citation
Please see CITATION.cff for proper attribution.

## License
{metadata.get('fair_compliance', {}).get('reusable', {}).get('license', 'Please check metadata for licensing information')}

---
Generated by EChem FAIRifier v1.0
"""
    return readme


def generate_citation(metadata: Dict[str, Any]) -> str:
    """Generate Citation File Format content."""
    
    attribution = metadata.get('attribution', {})
    
    cff_content = f"""cff-version: 1.2.0
message: "If you use this dataset, please cite it as below."
type: dataset
title: "{metadata.get('technique', {}).get('name', 'Electrochemical')} measurement data"
authors:
- family-names: "{attribution.get('creator', 'Unknown').split()[-1] if attribution.get('creator') else 'Unknown'}"
  given-names: "{' '.join(attribution.get('creator', 'Unknown').split()[:-1]) if attribution.get('creator') else 'Unknown'}"
  orcid: "{attribution.get('orcid', '')}"
  affiliation: "{attribution.get('institution', '')}"
date-released: "{metadata.get('created_date', '')[:10]}"
license: "{metadata.get('fair_compliance', {}).get('reusable', {}).get('license', 'Unknown')}"
repository-code: "https://github.com/your-org/echem-fairifier"
"""
    return cff_content


def update_progress_sidebar(container):
    """Update the progress tracking in sidebar."""
    
    with container:
        steps = [
            ("📁 Upload Data", st.session_state.uploaded_file is not None),
            ("📝 Generate Metadata", st.session_state.metadata is not None),
            ("✅ Validation", st.session_state.validation_results is not None),
            ("📦 Export Bundle", False)  # This is always the final step
        ]
        
        for step_name, completed in steps:
            if completed:
                st.success(f"✅ {step_name}")
            else:
                st.info(f"⏳ {step_name}")
        
        # Show completion percentage
        completed_steps = sum(1 for _, completed in steps[:-1] if completed)
        total_steps = len(steps) - 1
        progress = completed_steps / total_steps if total_steps > 0 else 0
        
        st.progress(progress)
        st.write(f"Progress: {completed_steps}/{total_steps} steps completed")


if __name__ == "__main__":
    main()