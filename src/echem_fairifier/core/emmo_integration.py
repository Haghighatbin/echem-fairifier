"""
EMMO (Elementary Multiperspective Material Ontology) integration for electrochemistry.
Provides controlled vocabularies and term validation.
"""

import streamlit as st
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class EMMOTerm:
    """Represents an EMMO ontology term."""

    iri: str
    label: str
    definition: str
    synonyms: List[str] = None
    parent_classes: List[str] = None

    def __post_init__(self):
        if self.synonyms is None:
            self.synonyms = []
        if self.parent_classes is None:
            self.parent_classes = []


class EMMOElectrochemistryIntegration:
    """Integration with EMMO Electrochemistry Domain Ontology."""

    def __init__(self):
        self.ontology_url = "https://w3id.org/emmo/domain/electrochemistry"
        self.local_terms = self._load_local_terms()
        self.validation_cache = {}

        # Set up logging
        self.logger = logging.getLogger(__name__)

    def _load_local_terms(self) -> Dict[str, EMMOTerm]:
        """Load pre-defined EMMO electrochemistry terms for offline validation."""

        # Key electrochemical technique terms from EMMO electrochemistry domain
        terms = {
            "cyclic_voltammetry": EMMOTerm(
                iri="https://w3id.org/emmo/domain/electrochemistry#electrochemistry_25aae0e9_a17c_4eb6_ac69_dd4264fad3d5",
                label="CyclicVoltammetry",
                definition="A voltammetry technique where the potential swept linearly between two limits at a constant rate.",
                synonyms=["CV", "cyclic voltammetry"],
            ),
            "differential_pulse_voltammetry": EMMOTerm(
                iri="https://w3id.org/emmo/domain/electrochemistry#electrochemistry_f49b84d4_e1f9_424c_bb22_8cea23c0a7d4",
                label="DifferentialPulseVoltammetry",
                definition="A voltammetry technique where pulses of potential are applied on top of a linear sweep.",
                synonyms=["DPV", "differential pulse voltammetry"],
            ),
            "square_wave_voltammetry": EMMOTerm(
                iri="https://w3id.org/emmo/domain/electrochemistry#electrochemistry_979e24bc_a0d6_4a94_ad99_46739c887dc1",
                label="SquareWaveVoltammetry",
                definition="A voltammetry technique where a square wave potential is superimposed on a staircase waveform.",
                synonyms=["SWV", "square wave voltammetry"],
            ),
            "electrochemical_impedance_spectroscopy": EMMOTerm(
                iri="https://w3id.org/emmo/domain/electrochemistry#electrochemistry_c7c8cda4_b8a4_4b1a_b0eb_58cbb1516945",
                label="ElectrochemicalImpedanceSpectroscopy",
                definition="A technique that applies a small amplitude sinusoidal voltage perturbation to measure impedance.",
                synonyms=["EIS", "impedance spectroscopy"],
            ),
            "chronoamperometry": EMMOTerm(
                iri="https://w3id.org/emmo/domain/electrochemistry#electrochemistry_f57e2b9c_bc4c_4245_b154_7ee83e688464",
                label="Chronoamperometry",
                definition="A technique where potential steps are applied and current response is measured vs time.",
                synonyms=["CA", "chronoamperometry"],
            ),
            # Electrode terms
            "working_electrode": EMMOTerm(
                iri="https://w3id.org/emmo/domain/electrochemistry#electrochemistry_fb0d9eef_92af_4628_8814_e065ca255d59",
                label="WorkingElectrode",
                definition="The electrode at which the electrochemical reaction of interest occurs.",
                synonyms=["WE", "working electrode"],
            ),
            "reference_electrode": EMMOTerm(
                iri="https://w3id.org/emmo/domain/electrochemistry#electrochemistry_8e3bd7c7_681b_4f50_8ac5_f3dad6312ff4",
                label="ReferenceElectrode",
                definition="An electrode with a stable and well-known electrode potential.",
                synonyms=["RE", "reference electrode"],
            ),
            "counter_electrode": EMMOTerm(
                iri="https://w3id.org/emmo/domain/electrochemistry#electrochemistry_4bd89acc_d5ee_4dae_8bb0_bf9e5de43fbd",
                label="CounterElectrode",
                definition="An electrode used to complete the electrical circuit in an electrochemical cell.",
                synonyms=["CE", "auxiliary electrode", "counter electrode"],
            ),
            # Material terms
            "glassy_carbon": EMMOTerm(
                iri="https://w3id.org/emmo/domain/electrochemistry#electrochemistry_3f70e5de_fa27_46a4_b201_92d0e6b5ab7a",
                label="GlassyCarbon",
                definition="A non-graphitising carbon with a glass-like structure.",
                synonyms=["GC", "vitreous carbon"],
            ),
            "platinum": EMMOTerm(
                iri="https://w3id.org/emmo/domain/electrochemistry#electrochemistry_1b827d8b_47e4_4f5a_a49e_4ad3fb28d559",
                label="Platinum",
                definition="A precious metal electrode material with high chemical stability.",
                synonyms=["Pt", "platinum"],
            ),
            # Electrolyte components
            "potassium_nitrate": EMMOTerm(
                iri="https://w3id.org/emmo/domain/electrochemistry#electrochemistry_5e8b6d8c_3d60_4186_8b47_0c80b154b0a9",
                label="PotassiumNitrate",
                definition="An ionic compound with formula KNO3, commonly used as supporting electrolyte.",
                synonyms=["KNO3", "potassium nitrate"],
            ),
        }

        return terms

    def validate_technique(self, technique: str) -> Optional[EMMOTerm]:
        """
        Validate if a technique name matches EMMO vocabulary.

        Args:
            technique: Technique name to validate

        Returns:
            EMMOTerm if valid, None otherwise
        """
        technique_lower = technique.lower().replace(" ", "_")

        # Direct lookup
        if technique_lower in self.local_terms:
            return self.local_terms[technique_lower]

        # Synonym lookup
        for term in self.local_terms.values():
            if technique.upper() in [syn.upper() for syn in term.synonyms]:
                return term

        # Fuzzy matching for common variations
        technique_mappings = {
            "cv": "cyclic_voltammetry",
            "dpv": "differential_pulse_voltammetry",
            "swv": "square_wave_voltammetry",
            "eis": "electrochemical_impedance_spectroscopy",
            "ca": "chronoamperometry",
        }

        if technique.lower() in technique_mappings:
            return self.local_terms[technique_mappings[technique.lower()]]

        return None

    def get_controlled_vocabulary(self, category: str) -> Dict[str, EMMOTerm]:
        """
        Get controlled vocabulary terms for a specific category.

        Args:
            category: Category like 'techniques', 'electrodes', 'materials'

        Returns:
            Dictionary of relevant terms
        """
        category_filters = {
            "techniques": ["voltammetry", "spectroscopy", "chronoamperometry"],
            "electrodes": ["electrode"],
            "materials": ["carbon", "platinum", "gold", "silver"],
            "electrolytes": ["nitrate", "chloride", "sulfate"],
        }

        if category not in category_filters:
            return {}

        keywords = category_filters[category]
        filtered_terms = {}

        for key, term in self.local_terms.items():
            if any(
                keyword in term.label.lower() or keyword in term.definition.lower()
                for keyword in keywords
            ):
                filtered_terms[key] = term

        return filtered_terms

    def suggest_terms(self, user_input: str, category: str = None) -> List[EMMOTerm]:
        """
        Suggest EMMO terms based on user input.

        Args:
            user_input: User's input text
            category: Optional category to filter suggestions

        Returns:
            List of suggested EMMOTerm objects
        """
        suggestions = []
        user_lower = user_input.lower()

        search_terms = self.local_terms
        if category:
            search_terms = self.get_controlled_vocabulary(category)

        for term in search_terms.values():
            # Check label similarity
            if user_lower in term.label.lower():
                suggestions.append(term)
                continue

            # Check synonym similarity
            if any(user_lower in syn.lower() for syn in term.synonyms):
                suggestions.append(term)
                continue

            # Check definition keywords
            if user_lower in term.definition.lower():
                suggestions.append(term)

        return suggestions[:5]  # Return top 5 suggestions

    def validate_metadata_terms(self, metadata: Dict) -> Dict[str, List[str]]:
        """
        Validate metadata terms against EMMO vocabulary.

        Args:
            metadata: Metadata dictionary to validate

        Returns:
            Dictionary with validation results
        """
        results = {"valid_terms": [], "suggestions": [], "warnings": []}

        # Validate technique
        technique_name = metadata.get("technique", {}).get("name", "")
        if technique_name:
            emmo_term = self.validate_technique(technique_name)
            if emmo_term:
                results["valid_terms"].append(
                    f"Technique '{technique_name}' matches EMMO term: {emmo_term.label}"
                )
            else:
                suggestions = self.suggest_terms(technique_name, "techniques")
                if suggestions:
                    results["suggestions"].append(
                        f"Consider using EMMO-compliant term for '{technique_name}': {suggestions[0].label}"
                    )

        # Validate electrodes
        exp_setup = metadata.get("experimental_setup", {})
        for electrode_type in [
            "working_electrode",
            "reference_electrode",
            "counter_electrode",
        ]:
            electrode_desc = exp_setup.get(electrode_type, "")
            if electrode_desc:
                suggestions = self.suggest_terms(electrode_desc, "electrodes")
                if suggestions:
                    results["suggestions"].append(
                        f"EMMO term available for {electrode_type}: {suggestions[0].label}"
                    )

        # Check for general EMMO compliance
        if not results["valid_terms"] and not results["suggestions"]:
            results["warnings"].append(
                "No EMMO vocabulary matches found. Consider using controlled terms for better interoperability."
            )

        return results

    def enrich_metadata_with_emmo(self, metadata: Dict) -> Dict:
        """
        Enrich metadata with EMMO IRIs and controlled vocabulary.

        Args:
            metadata: Original metadata dictionary

        Returns:
            Enriched metadata with EMMO terms
        """
        enriched = metadata.copy()

        # Add EMMO section
        enriched["emmo_compliance"] = {
            "ontology_version": "https://w3id.org/emmo/domain/electrochemistry",
            "terms_used": [],
            "vocabulary_mapping": {},
        }

        # Enrich technique information
        technique_name = metadata.get("technique", {}).get("name", "")
        if technique_name:
            emmo_term = self.validate_technique(technique_name)
            if emmo_term:
                enriched["technique"]["emmo_iri"] = emmo_term.iri
                enriched["technique"]["emmo_label"] = emmo_term.label
                enriched["technique"]["emmo_definition"] = emmo_term.definition

                enriched["emmo_compliance"]["terms_used"].append(
                    {
                        "iri": emmo_term.iri,
                        "label": emmo_term.label,
                        "used_for": "technique",
                    }
                )

        # Add controlled vocabulary suggestions
        exp_setup = metadata.get("experimental_setup", {})
        vocabulary_suggestions = {}

        for field, value in exp_setup.items():
            if value and isinstance(value, str):
                suggestions = self.suggest_terms(value)
                if suggestions:
                    vocabulary_suggestions[field] = {
                        "input_value": value,
                        "emmo_suggestion": suggestions[0].label,
                        "emmo_iri": suggestions[0].iri,
                    }

        if vocabulary_suggestions:
            enriched["emmo_compliance"]["vocabulary_mapping"] = vocabulary_suggestions

        return enriched

    def generate_emmo_report(self, metadata: Dict) -> str:
        """
        Generate a report on EMMO compliance.

        Args:
            metadata: Metadata dictionary

        Returns:
            Human-readable compliance report
        """
        validation_results = self.validate_metadata_terms(metadata)

        report = "# EMMO Compliance Report\n\n"

        if validation_results["valid_terms"]:
            report += "## ✅ Validated Terms\n"
            for term in validation_results["valid_terms"]:
                report += f"- {term}\n"
            report += "\n"

        if validation_results["suggestions"]:
            report += "## 💡 Vocabulary Suggestions\n"
            for suggestion in validation_results["suggestions"]:
                report += f"- {suggestion}\n"
            report += "\n"

        if validation_results["warnings"]:
            report += "## ⚠️ Recommendations\n"
            for warning in validation_results["warnings"]:
                report += f"- {warning}\n"
            report += "\n"

        report += "## 📚 About EMMO\n"
        report += "The Elementary Multiperspective Material Ontology (EMMO) provides "
        report += "standardised vocabulary for materials science and electrochemistry. "
        report += (
            "Using EMMO terms improves data interoperability and FAIR compliance.\n\n"
        )
        report += f"Ontology URL: {self.ontology_url}\n"

        return report


# Convenience functions for Streamlit integration
def get_emmo_integration() -> EMMOElectrochemistryIntegration:
    """Get EMMO integration instance (cached)."""
    if "emmo_integration" not in st.session_state:
        st.session_state.emmo_integration = EMMOElectrochemistryIntegration()
    return st.session_state.emmo_integration


def validate_with_emmo(metadata: Dict) -> Dict[str, List[str]]:
    """Validate metadata against EMMO vocabulary."""
    emmo = get_emmo_integration()
    return emmo.validate_metadata_terms(metadata)


def enrich_with_emmo(metadata: Dict) -> Dict:
    """Enrich metadata with EMMO terms."""
    emmo = get_emmo_integration()
    return emmo.enrich_metadata_with_emmo(metadata)
