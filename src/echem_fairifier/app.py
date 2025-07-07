"""
EChem FAIRifier - Main Streamlit Application
Making electrochemical data FAIR-compliant

EChem FAIRifier transforms raw electrochemical data
into FAIR-compliant datasets with comprehensive metadata,
automated validation, and  documentation.
Built for the electrochemistry community to improve data
sharing, reproducibility, and collaboration.

Developer: Amin Haghighatbin
Date: 210.6.2025
"""

import sys
from pathlib import Path

current_dir = Path(__file__).parent
src_dir = current_dir.parent.parent
sys.path.insert(0, str(src_dir))

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from io import BytesIO
import zipfile
from typing import Dict, Any

from src.echem_fairifier.core.metadata_generator import FAIRMetadataGenerator
from src.echem_fairifier.core.validator import ECDataValidator
from src.echem_fairifier.core.emmo_integration import EMMOElectrochemistryIntegration
from src.echem_fairifier.ui.components import UIComponents
from src.echem_fairifier._version import __version__, get_version_info

# Serve Google verification file if accessed
query_params = st.query_params
if query_params.get("gv") == '1':
    st.markdown("google-site-verification: google814ae2d9326e9a51.html")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="EChem FAIRifier",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/haghighatbin/echem-fairifier",
        "Report a bug": "https://github.com/haghighatbin/echem-fairifier/issues",
        "About": f"EChem FAIRifier v{__version__} - Making electrochemical data FAIR-compliant",
    },
)


def show_post_download_help():
    with st.expander("📦 What to do with your FAIR bundle"):
        st.markdown(
            """
        Your download contains everything for data sharing:
        
        **🚀 Quick Actions:**
        - **Upload to Zenodo** → Get a DOI for citations
        - **Share with collaborators** → Include entire ZIP
        - **Submit to journals** → Use generated citations
        
        **📁 Bundle Contents:**
        - `data/` → Your processed datasets
        - `metadata/` → FAIR-compliant descriptions  
        - `documentation/` → README and methodology
        - `visualisations/` → **💡 Tip:** Add your own publication-ready plots before submitting to repositories
        
        **Need help?** Check our [User Guide](https://github.com/haghighatbin/echem-fairifier/blob/main/docs/USER_GUIDE.md)
        """
        )


def main():
    """Main application function."""

    # Initialise components
    ui = UIComponents()
    metadata_gen = FAIRMetadataGenerator()
    validator = ECDataValidator()
    emmo_integration = EMMOElectrochemistryIntegration()

    # Render header
    ui.render_header()

    st.markdown(
        f"""
    <div style="text-align: center; color: #666; font-size: 0.8em; margin-bottom: 1.5rem;">
        A project by <strong>Amin Haghighatbin</strong> | Making electrochemical research more reproducible<br>
        <span style="font-size: 0.7em; color: #888;">v{__version__}</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    ui.render_fair_info()

    # Sidebar for progress tracking
    with st.sidebar:
        st.header("📋 Progress")
        progress_container = st.container()

        st.markdown("---")
        with st.expander("ℹ️ About", expanded=False):
            version_info = get_version_info()
            st.write(f"**Version:** {version_info['version']}")
            st.write(f"**Release:** {version_info['release_name']}")
            st.write(f"**Date:** {version_info['release_date']}")
            st.write(f"**Developer:** {version_info['author']}")
            st.markdown("[📖 User Guide](https://github.com/haghighatbin/echem-fairifier)")
            st.markdown("[🐛 Report Issue](https://github.com/haghighatbin/echem-fairifier/issues)")

    # Main content area
    tab1, tab2, tab3 = st.tabs(["📁 Data Upload", "📝 Metadata", "📦 Export"])

    # Initialise session state
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
    if "metadata" not in st.session_state:
        st.session_state.metadata = None
    if "validation_results" not in st.session_state:
        st.session_state.validation_results = None

    # Tab 1: Data Upload
    with tab1:
        uploaded_file = ui.render_file_upload()

        if uploaded_file:
            st.session_state.uploaded_file = uploaded_file

            try:
                # Validate file type
                if not uploaded_file.name.lower().endswith(".csv"):
                    st.error("❌ Please upload a CSV file.")
                    st.info("💡 Tip: Save your data as CSV format from Excel or other software.")
                    return

                # Try to read the file with different encodings if needed
                df = None
                encodings_to_try = ["utf-8", "latin1", "cp1252", "iso-8859-1"]

                for encoding in encodings_to_try:
                    try:
                        uploaded_file.seek(0)  # Reset file pointer
                        df = pd.read_csv(uploaded_file, encoding=encoding)
                        st.success(f"✅ File loaded successfully (encoding: {encoding})")
                        break
                    except UnicodeDecodeError:
                        continue
                    except Exception as e:
                        if encoding == encodings_to_try[-1]:  # Last encoding attempt
                            raise e
                        continue

                if df is None:
                    st.error("❌ Could not read the file. Please check the file format.")
                    return

                # Basic data validation
                if df.empty:
                    st.warning("⚠️ The uploaded file appears to be empty.")
                    st.info("Please upload a file with data.")
                    return

                # Check for at least some numeric data
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) == 0:
                    st.warning("⚠️ No numeric columns detected in your data.")
                    st.info("Make sure your measurement data (potential, current, etc.) are in numeric format.")
                    st.write("**Detected columns:**", list(df.columns))
                else:
                    st.success(f"✅ Found {len(numeric_cols)} numeric columns for analysis")

                # Store dataframe in session state
                st.session_state.df = df

                # Show data preview with error handling
                try:
                    ui.render_data_preview(df, "CV")  # Default to CV for preview
                except Exception as plot_error:
                    st.warning(f"⚠️ Preview generation issue: {str(plot_error)}")
                    st.info("Don't worry - you can still proceed with metadata generation!")

                    # Show basic data info as fallback
                    with st.expander("📋 Basic Data Information"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Rows:** {len(df)}")
                            st.write(f"**Columns:** {len(df.columns)}")
                        with col2:
                            st.write(f"**Numeric columns:** {len(numeric_cols)}")
                            st.write(f"**File size:** {uploaded_file.size / 1024:.1f} KB")

                        st.write("**Column names:**", list(df.columns))
                        st.dataframe(df.head())

            except pd.errors.EmptyDataError:
                st.error("❌ The file is empty or contains no data.")
                st.info("Please upload a file with actual measurement data.")

            except pd.errors.ParserError as e:
                st.error(f"❌ File parsing error: {str(e)}")
                st.info("Please check that your file is properly formatted CSV.")
                st.markdown(
                    """
                **Common solutions:**
                - Ensure data is separated by commas
                - Check for extra commas or special characters
                - Make sure column headers are in the first row
                """
                )

            except Exception as e:
                st.error(f"❌ Unexpected error processing file: {str(e)}")
                st.info("Please try again or contact support if the problem persists.")

                # Debug information for development
                if st.checkbox("Show debug information"):
                    st.write("**Error details:**", str(e))
                    st.write(
                        "**File info:**",
                        {
                            "name": uploaded_file.name,
                            "size": uploaded_file.size,
                            "type": uploaded_file.type,
                        },
                    )

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
        if "df" in st.session_state:
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
                # Validate required inputs
                if not technique:
                    st.error("❌ Please select a technique.")
                    return

                if not all(
                    [
                        experimental_details.get("working_electrode"),
                        experimental_details.get("reference_electrode"),
                        experimental_details.get("electrolyte"),
                    ]
                ):
                    st.error("❌ Please fill in all required experimental details.")
                    return

                dataset_info = {
                    "filename": st.session_state.uploaded_file.name,
                    "size_bytes": st.session_state.uploaded_file.size,
                }

                # Generate base metadata
                with st.spinner("Generating FAIR metadata..."):
                    metadata = metadata_gen.generate_metadata(
                        technique=technique,
                        technique_parameters=technique_parameters,
                        experimental_details=all_experimental_details,
                        dataset_info=dataset_info,
                    )

                # Enrich with EMMO terms (with error handling)
                try:
                    with st.spinner("Enriching with EMMO vocabulary..."):
                        metadata = emmo_integration.enrich_metadata_with_emmo(metadata)
                except Exception as emmo_error:
                    st.warning(f"⚠️ EMMO enrichment had issues: {str(emmo_error)}")
                    st.info("Proceeding with basic metadata (EMMO features may be limited)")

                st.session_state.metadata = metadata

                # Comprehensive validation
                try:
                    validation_results = validator.validate_metadata(metadata)

                    # Add EMMO validation if available
                    try:
                        emmo_validation = emmo_integration.validate_metadata_terms(metadata)
                        if emmo_validation.get("suggestions"):
                            validation_results["info"].extend(emmo_validation["suggestions"])
                    except Exception as emmo_val_error:
                        st.warning(f"⚠️ EMMO validation issue: {str(emmo_val_error)}")

                    st.session_state.validation_results = validation_results

                except Exception as val_error:
                    st.warning(f"⚠️ Validation had issues: {str(val_error)}")
                    # Continue with basic validation results
                    st.session_state.validation_results = {
                        "errors": [],
                        "warnings": ["Validation system had issues - please review metadata manually"],
                        "info": [],
                        "fair_score": 0.5,
                        "completeness_score": 0.5,
                    }

                st.success("✅ Metadata generated successfully!")
                st.balloons()

            except Exception as e:
                st.error(f"❌ Error generating metadata: {str(e)}")
                st.info("Please check your inputs and try again.")

                # Debug information for development
                if st.checkbox("Show debug information", key="debug_metadata"):
                    st.write("**Error details:**", str(e))
                    st.write("**Technique:**", technique)
                    st.write("**Parameters:**", technique_parameters)
                    import traceback

                    st.code(traceback.format_exc())

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
                mime="text/yaml",
            )

        with col2:
            st.subheader("🔍 Metadata Summary")

            # Display key information
            metadata = st.session_state.metadata

            st.write("**Experiment Overview:**")
            st.write(f"• Technique: {metadata.get('technique', {}).get('name', 'N/A')}")
            st.write(f"• Created: {metadata.get('created_date', 'N/A')[:10]}")
            st.write(f"• ID: {metadata.get('experiment_id', 'N/A')[:8]}...")

            exp_setup = metadata.get("experimental_setup", {})
            st.write("**Experimental Setup:**")
            st.write(f"• Working Electrode: {exp_setup.get('working_electrode', 'N/A')}")
            st.write(f"• Electrolyte: {exp_setup.get('electrolyte', 'N/A')}")

            attribution = metadata.get("attribution", {})
            if attribution.get("creator"):
                st.write("**Attribution:**")
                st.write(f"• Creator: {attribution.get('creator', 'N/A')}")
                st.write(f"• Institution: {attribution.get('institution', 'N/A')}")

        # FAIR Bundle Export
        st.markdown("---")
        st.subheader("📦 FAIR Data Bundle")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.write("**Bundle Contents:**")
            st.write("• `data/` - Original data file (CSV)")
            st.write("• `metadata/` - FAIR metadata (YAML) and citation file")
            st.write("• `documentation/` - README with usage instructions")

        with col2:
            if st.button("📦 Create FAIR Bundle", type="primary"):
                try:
                    with st.spinner("Creating FAIR bundle..."):
                        # Create ZIP bundle
                        zip_buffer = create_fair_bundle(
                            st.session_state.uploaded_file,
                            yaml_str,
                            st.session_state.metadata,
                        )

                        st.success("✅ FAIR bundle created successfully!")

                    # Generate filename with technique and experiment ID
                    technique_name = st.session_state.metadata.get("technique", {}).get("name", "unknown")
                    exp_id = st.session_state.metadata.get("experiment_id", "unknown")[:8]
                    filename = f"fair_bundle_{technique_name.lower()}_{exp_id}.zip"

                    st.download_button(
                        label="⬇️ Download FAIR Bundle (.zip)",
                        data=zip_buffer,
                        file_name=filename,
                        mime="application/zip",
                        help="Download your complete FAIR data package",
                    )
                    show_post_download_help()

                except Exception as e:
                    st.error(f"❌ Error creating bundle: {str(e)}")
                    st.info("You can still download the metadata separately using the button above.")

                    # Debug information
                    if st.checkbox("Show bundle debug info", key="debug_bundle"):
                        st.write("**Error details:**", str(e))
                        import traceback

                        st.code(traceback.format_exc())

    # Update progress sidebar
    update_progress_sidebar(progress_container)


def create_fair_bundle(uploaded_file, yaml_str: str, metadata: Dict[str, Any]) -> BytesIO:
    """Create a ZIP bundle with data and metadata."""

    zip_buffer = BytesIO()
    try:
        # Create README content
        readme_content = generate_readme(metadata)

        # Create citation content
        citation_content = generate_citation(metadata)

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            # Add original data file to data/ folder
            try:
                uploaded_file.seek(0)  # Reset file pointer
                zip_file.writestr(f"data/{uploaded_file.name}", uploaded_file.getvalue())
            except Exception as e:
                st.warning(f"Issue adding data file to bundle: {str(e)}")
                zip_file.writestr("data/data_file_error.txt", f"Original file could not be added: {str(e)}")

            # Add metadata to metadata/ folder
            try:
                zip_file.writestr("metadata/metadata.yaml", yaml_str)
            except Exception as e:
                st.warning(f"Issue adding metadata: {str(e)}")
                basic_metadata = f"# Metadata generation error\nError: {str(e)}\nTechnique: {metadata.get('technique', {}).get('name', 'Unknown')}"
                zip_file.writestr("metadata/metadata_error.txt", basic_metadata)

            # Add citation to metadata/ folder
            try:
                zip_file.writestr("metadata/CITATION.cff", citation_content)
            except Exception as e:
                st.warning(f"Issue adding citation: {str(e)}")
                basic_citation = f"# Citation information could not be generated\n# Error: {str(e)}"
                zip_file.writestr("metadata/CITATION_error.txt", basic_citation)

            # Add README to documentation/ folder
            try:
                zip_file.writestr("documentation/README.md", readme_content)
            except Exception as e:
                st.warning(f"Issue adding README: {str(e)}")
                basic_readme = "# EChem FAIR Bundle\n\nThis bundle was generated by EChem FAIRifier.\nSome documentation could not be generated due to errors."
                zip_file.writestr("documentation/README.md", basic_readme)

    except Exception as e:
        st.error(f"Critical error creating ZIP file: {str(e)}")
        # Create minimal ZIP with error information
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            error_info = f"Bundle creation failed: {str(e)}\nPlease contact support or try again."
            zip_file.writestr("ERROR.txt", error_info)

    zip_buffer.seek(0)
    return zip_buffer


def generate_readme(metadata: Dict[str, Any]) -> str:
    """Generate README content for the FAIR bundle."""

    try:
        technique_name = metadata.get("technique", {}).get("name", "Unknown")
        created_date = metadata.get("created_date", "Unknown")[:10]
        exp_id = metadata.get("experiment_id", "N/A")

        readme = f"""# Electrochemical Data Bundle

## Overview
This bundle contains FAIR-compliant electrochemical data generated using EChem FAIRifier.

**Technique:** {technique_name}
**Created:** {created_date}
**ID:** {exp_id}

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
    except Exception as e:
        readme = f"""# Electrochemical Data Bundle

This bundle was generated by EChem FAIRifier, but some information could not be included due to errors.

Error details: {str(e)}

Please check the metadata.yaml file for experiment details.

---
Generated by EChem FAIRifier v1.0
"""

    return readme


def generate_citation(metadata: Dict[str, Any]) -> str:
    """Generate Citation File Format content."""

    try:
        attribution = metadata.get("attribution", {})
        technique_name = metadata.get("technique", {}).get("name", "Electrochemical")

        # Handle name splitting safely
        creator_name = attribution.get("creator", "Unknown")
        if creator_name and creator_name != "Unknown":
            name_parts = creator_name.strip().split()
            if len(name_parts) >= 2:
                family_name = name_parts[-1]
                given_names = " ".join(name_parts[:-1])
            else:
                family_name = creator_name
                given_names = ""
        else:
            family_name = "Unknown"
            given_names = ""

        cff_content = f"""cff-version: 1.2.0
message: "If you use this dataset, please cite it as below."
type: dataset
title: "{technique_name} measurement data"
authors:
- family-names: "{family_name}"
  given-names: "{given_names}"
  orcid: "{attribution.get('orcid', '')}"
  affiliation: "{attribution.get('institution', '')}"
date-released: "{metadata.get('created_date', '')[:10]}"
license: "{metadata.get('fair_compliance', {}).get('reusable', {}).get('license', 'Unknown')}"
repository-code: "https://github.com/haghighatbin/echem-fairifier"
"""
    except Exception as e:
        cff_content = f"""cff-version: 1.2.0
message: "Citation information could not be generated properly."
type: dataset
title: "Electrochemical measurement data"
# Error in citation generation: {str(e)}
# Please update this file manually with proper attribution
"""

    return cff_content


def update_progress_sidebar(container):
    """Update the progress tracking in sidebar."""

    with container:
        steps = [
            ("📁 Upload Data", st.session_state.uploaded_file is not None),
            ("📝 Generate Metadata", st.session_state.metadata is not None),
            ("✅ Validation", st.session_state.validation_results is not None),
            ("📦 Export Bundle", False),  # This is always the final step
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
