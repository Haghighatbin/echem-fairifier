"""
Reusable UI components for the EChem FAIRifier Streamlit app.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List, Optional, Tuple
from ..config.techniques import ElectrochemicalTechniques, TechniqueParameter


class UIComponents:
    """Collection of reusable UI components."""
    
    @staticmethod
    def render_header():
        """Render the application header."""
        st.markdown("""
        <style>
        .main-header {
            text-align: center;
            padding: 1rem 0;
            margin-bottom: 2rem;
            background: linear-gradient(90deg, #1f77b4, #2ca02c);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .subtitle {
            text-align: center;
            color: #666;
            font-size: 1.2em;
            margin-bottom: 2rem;
        }
        .info-box {
            background-color: #e7f3ff;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #1f77b4;
            margin: 1rem 0;
        }
        .warning-box {
            background-color: #fff3cd;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #ffc107;
            margin: 1rem 0;
        }
        .success-box {
            background-color: #d4edda;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #28a745;
            margin: 1rem 0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="main-header">', unsafe_allow_html=True)
        st.title("⚡ EChem FAIRifier")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Making electrochemical data FAIR-compliant</div>', 
                   unsafe_allow_html=True)
    
    @staticmethod
    def render_fair_info():
        """Render FAIR principles information."""
        with st.expander("ℹ️ What is FAIR data?", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **FAIR Principles:**
                - **F**indable: Easy to locate and identify
                - **A**ccessible: Retrievable using standard protocols  
                - **I**nteroperable: Can integrate with other data
                - **R**eusable: Well-described for replication
                """)
            
            with col2:
                st.markdown("""
                **This tool helps by:**
                - Adding standardised metadata
                - Using controlled vocabularies (EMMO)
                - Generating unique identifiers
                - Ensuring proper attribution
                """)
    
    @staticmethod
    def render_file_upload() -> Optional[object]:
        """Render file upload widget with validation."""
        st.subheader("📁 Upload Data")
        
        uploaded_file = st.file_uploader(
            "Choose your electrochemical data file",
            type=["csv"],
            help="Upload a CSV file containing your electrochemical measurement data"
        )
        
        if uploaded_file:
            # Show file info
            file_details = {
                "Filename": uploaded_file.name,
                "File size": f"{uploaded_file.size / 1024:.1f} KB",
                "File type": uploaded_file.type
            }
            
            with st.expander("📋 File Information"):
                for key, value in file_details.items():
                    st.write(f"**{key}:** {value}")
        
        return uploaded_file
    
    @staticmethod
    def render_technique_selector() -> Tuple[str, str]:
        """Render technique selection with description."""
        st.subheader("🔬 Experimental Technique")
        
        technique_list = ElectrochemicalTechniques.get_technique_list()
        
        technique = st.selectbox(
            "Select Electrochemical Technique",
            technique_list,
            help="Choose the electrochemical method used for your measurement"
        )
        
        # Show technique description
        description = ElectrochemicalTechniques.get_technique_description(technique)
        st.info(f"**{technique}:** {description}")
        
        return technique, description
    
    @staticmethod
    def render_technique_parameters(technique: str) -> Dict[str, Any]:
        """Render technique-specific parameter inputs."""
        st.subheader("⚙️ Technique Parameters")
        
        parameters = ElectrochemicalTechniques.get_technique_parameters(technique)
        custom_params = {}
        
        if not parameters:
            st.warning(f"No parameters defined for {technique}")
            return {}
        
        # Create parameter inputs
        cols = st.columns(2)
        col_idx = 0
        
        for param_name, param_def in parameters.items():
            with cols[col_idx % 2]:
                custom_params[param_name] = UIComponents._render_parameter_input(
                    param_name, param_def
                )
            col_idx += 1
        
        return custom_params
    
    @staticmethod
    def _render_parameter_input(param_name: str, param_def: TechniqueParameter) -> Any:
        """Render individual parameter input."""
        label = f"{param_def.name.replace('_', ' ').title()}"
        if param_def.unit:
            label += f" ({param_def.unit})"
        
        if param_def.parameter_type == "list":
            # Handle list parameters
            val_str = st.text_input(
                label,
                value=", ".join(map(str, param_def.default_value)),
                help=param_def.description
            )
            try:
                return [float(x.strip()) for x in val_str.split(",") if x.strip()]
            except ValueError:
                st.error(f"Invalid format for {param_name}. Use comma-separated numbers.")
                return param_def.default_value
        else:
            # Handle numeric parameters
            return st.number_input(
                label,
                value=float(param_def.default_value),
                min_value=param_def.min_value,
                max_value=param_def.max_value,
                help=param_def.description,
                format="%.6f" if param_def.default_value < 0.1 else "%.3f"
            )
    
    @staticmethod
    def render_experimental_details() -> Dict[str, str]:
        """Render experimental setup inputs."""
        st.subheader("🧪 Experimental Setup")
        
        col1, col2 = st.columns(2)
        
        with col1:
            working_electrode = st.text_input(
                "Working Electrode",
                value="Glassy carbon, 3 mm",
                help="Material and dimensions of working electrode"
            )
            
            reference_electrode = st.text_input(
                "Reference Electrode",
                value="Ag/AgCl",
                help="Type of reference electrode used"
            )
            
            electrolyte = st.text_input(
                "Electrolyte",
                value="3 mM [Fe(CN)6]³⁻/⁴⁻ in 0.1 M KNO₃",
                help="Electrolyte composition and concentration"
            )
        
        with col2:
            counter_electrode = st.text_input(
                "Counter Electrode",
                value="Platinum wire",
                help="Material of counter electrode"
            )
            
            temperature = st.text_input(
                "Temperature",
                value="Room temperature (20±2°C)",
                help="Experimental temperature"
            )
            
            atmosphere = st.selectbox(
                "Atmosphere",
                ["Air", "Nitrogen", "Argon", "Other"],
                help="Atmospheric conditions during measurement"
            )
        
        return {
            "working_electrode": working_electrode,
            "reference_electrode": reference_electrode,
            "counter_electrode": counter_electrode,
            "electrolyte": electrolyte,
            "temperature": temperature,
            "atmosphere": atmosphere
        }
    
    @staticmethod
    def render_attribution_fields() -> Dict[str, str]:
        """Render attribution and contact information fields."""
        with st.expander("👤 Attribution & Contact (Optional but Recommended)", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                creator = st.text_input(
                    "Creator/Researcher Name",
                    help="Primary researcher or data creator"
                )
                
                institution = st.text_input(
                    "Institution/Organization",
                    help="Research institution or organization"
                )
                
                orcid = st.text_input(
                    "ORCID ID",
                    placeholder="0000-0000-0000-0000",
                    help="ORCID identifier for researcher attribution"
                )
            
            with col2:
                contact_email = st.text_input(
                    "Contact Email",
                    help="Email for data inquiries"
                )
                
                publication_doi = st.text_input(
                    "Related Publication DOI",
                    placeholder="10.1000/xyz123",
                    help="DOI of related publication"
                )
                
                license_choice = st.selectbox(
                    "Data License",
                    ["CC-BY-4.0", "CC0-1.0", "MIT", "Other"],
                    help="License for data reuse"
                )
        
        return {
            "creator": creator,
            "institution": institution,
            "contact_email": contact_email,
            "orcid": orcid,
            "publication_doi": publication_doi,
            "license": license_choice
        }
    
    @staticmethod
    def render_data_preview(df: pd.DataFrame, technique: str) -> None:
        """Render data preview with appropriate plotting."""
        st.subheader("📊 Data Preview")
        
        # Show basic data info
        with st.expander("📋 Dataset Information"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Rows", len(df))
            with col2:
                st.metric("Columns", len(df.columns))
            with col3:
                st.metric("File Size", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
            
            st.write("**Columns found:**", list(df.columns))
        
        # Generate appropriate plot
        fig = UIComponents._create_technique_plot(df, technique)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Unable to generate plot. Please check column names match expected format.")
            
        # Show data sample
        with st.expander("🔍 Data Sample (First 10 rows)"):
            st.dataframe(df.head(10))
    
    @staticmethod
    def _create_technique_plot(df: pd.DataFrame, technique: str) -> Optional[go.Figure]:
        """Create appropriate plot for the technique."""
        try:
            if technique == "CV" and all(col in df.columns for col in ["Potential (V)", "Current (A)"]):
                fig = px.line(
                    df, x="Potential (V)", y="Current (A)",
                    title="Cyclic Voltammogram",
                    labels={"Potential (V)": "Potential / V", "Current (A)": "Current / A"}
                )
                
            elif technique == "EIS" and all(col in df.columns for col in ["Z_real (Ohm)", "Z_imag (Ohm)"]):
                fig = px.scatter(
                    df, x="Z_real (Ohm)", y="Z_imag (Ohm)",
                    title="Nyquist Plot",
                    labels={"Z_real (Ohm)": "Z' / Ω", "Z_imag (Ohm)": "-Z'' / Ω"}
                )
                fig.update_yaxis(autorange="reversed")
                
            elif technique == "CA" and all(col in df.columns for col in ["Time (s)", "Current (A)"]):
                fig = px.line(
                    df, x="Time (s)", y="Current (A)",
                    title="Chronoamperogram",
                    labels={"Time (s)": "Time / s", "Current (A)": "Current / A"}
                )
                
            elif all(col in df.columns for col in ["Potential (V)", "Current (A)"]):
                # Generic electrochemical plot
                fig = px.line(
                    df, x="Potential (V)", y="Current (A)",
                    title=f"{technique} Measurement",
                    labels={"Potential (V)": "Potential / V", "Current (A)": "Current / A"}
                )
            else:
                return None
            
            fig.update_layout(
                template="plotly_white",
                showlegend=False,
                font=dict(size=12)
            )
            return fig
            
        except Exception as e:
            st.error(f"Error creating plot: {str(e)}")
            return None
    
    @staticmethod
    def render_validation_results(validation_results: Dict[str, List[str]]) -> None:
        """Render metadata validation results."""
        errors = validation_results.get("errors", [])
        warnings = validation_results.get("warnings", [])
        
        if errors:
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.error("❌ **Validation Errors:**")
            for error in errors:
                st.write(f"• {error}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        if warnings:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.warning("⚠️ **Recommendations:**")
            for warning in warnings:
                st.write(f"• {warning}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        if not errors and not warnings:
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.success("✅ **Metadata validation passed!** Your data meets FAIR standards.")
            st.markdown('</div>', unsafe_allow_html=True)