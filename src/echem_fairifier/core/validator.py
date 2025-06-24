"""
Enhanced validation for electrochemical data and metadata.
Includes JSON schema validation, FAIR compliance checking, and data quality assessment.
"""

import json
import pandas as pd
from typing import Dict, List, Any, Optional
from pathlib import Path
from jsonschema import validate, ValidationError
import re
from datetime import datetime
import hashlib


class ECDataValidator:
    """Comprehensive validator for electrochemical data and metadata."""

    def __init__(self, schema_path: Optional[str] = None):
        """
        Initialize validator with metadata schema.

        Args:
            schema_path: Path to JSON schema file. If None, uses default.
        """
        if schema_path is None:
            # Use default schema path relative to this file
            current_dir = Path(__file__).parent
            schema_path = current_dir.parent / "schemas" / "fair_metadata.json"

        self.schema_path = Path(schema_path)
        self.schema = self._load_schema()

        # Expected column patterns for different techniques
        self.column_patterns = {
            "CV": [r"[Pp]otential.*[Vv]", r"[Cc]urrent.*[Aa]", r"[Cc]ycle"],
            "DPV": [r"[Pp]otential.*[Vv]", r"[Cc]urrent.*[Aa]"],
            "SWV": [
                r"[Pp]otential.*[Vv]",
                r"[Cc]urrent.*[Aa]",
                r"[Ff]orward.*[Cc]urrent",
                r"[Rr]everse.*[Cc]urrent",
            ],
            "EIS": [
                r"[Ff]requency.*[Hh]z",
                r"[Zz].*[Rr]eal",
                r"[Zz].*[Ii]mag",
                r"[Pp]hase",
            ],
            "CA": [r"[Tt]ime.*[Ss]", r"[Cc]urrent.*[Aa]", r"[Pp]otential.*[Vv]"],
        }

    def _load_schema(self) -> Dict:
        """Load JSON schema for metadata validation."""
        try:
            if self.schema_path.exists():
                with open(self.schema_path, "r") as f:
                    return json.load(f)
            else:
                # Return minimal schema if file not found
                return self._get_minimal_schema()
        except Exception as e:
            print(f"Warning: Could not load schema from {self.schema_path}: {e}")
            return self._get_minimal_schema()

    def _get_minimal_schema(self) -> Dict:
        """Return minimal validation schema as fallback."""
        return {
            "type": "object",
            "required": ["experiment_id", "technique", "experimental_setup"],
            "properties": {
                "experiment_id": {"type": "string"},
                "technique": {
                    "type": "object",
                    "required": ["name"],
                    "properties": {"name": {"type": "string"}},
                },
                "experimental_setup": {
                    "type": "object",
                    "required": [
                        "working_electrode",
                        "reference_electrode",
                        "electrolyte",
                    ],
                    "properties": {
                        "working_electrode": {"type": "string"},
                        "reference_electrode": {"type": "string"},
                        "electrolyte": {"type": "string"},
                    },
                },
            },
        }

    def validate_metadata(self, metadata: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Comprehensive metadata validation.

        Args:
            metadata: Metadata dictionary to validate

        Returns:
            Dictionary with validation results
        """
        results = {
            "errors": [],
            "warnings": [],
            "info": [],
            "fair_score": 0.0,
            "completeness_score": 0.0,
        }

        # JSON Schema validation
        schema_results = self._validate_against_schema(metadata)
        results["errors"].extend(schema_results["errors"])
        results["warnings"].extend(schema_results["warnings"])

        # FAIR compliance check
        fair_results = self._check_fair_compliance(metadata)
        results["warnings"].extend(fair_results["warnings"])
        results["info"].extend(fair_results["recommendations"])
        results["fair_score"] = fair_results["score"]

        # Completeness assessment
        completeness_results = self._assess_completeness(metadata)
        results["warnings"].extend(completeness_results["warnings"])
        results["completeness_score"] = completeness_results["score"]

        # Technique-specific validation
        technique_results = self._validate_technique_parameters(metadata)
        results["warnings"].extend(technique_results["warnings"])
        results["errors"].extend(technique_results["errors"])

        return results

    def _validate_against_schema(
        self, metadata: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Validate metadata against JSON schema."""
        results = {"errors": [], "warnings": []}

        try:
            validate(instance=metadata, schema=self.schema)
            results["warnings"].append(
                "✅ Metadata structure is valid according to schema"
            )
        except ValidationError as e:
            results["errors"].append(f"Schema validation error: {e.message}")
        except Exception as e:
            results["warnings"].append(
                f"Schema validation could not be performed: {str(e)}"
            )

        return results

    def _check_fair_compliance(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Check FAIR (Findable, Accessible, Interoperable, Reusable) compliance."""
        results = {"warnings": [], "recommendations": [], "score": 0.0}
        score = 0
        max_score = 0

        # Findable (F)
        max_score += 4
        if metadata.get("experiment_id"):
            score += 1
            results["recommendations"].append("✅ F1: Unique identifier present")
        else:
            results["warnings"].append("❌ F1: Missing unique identifier")

        if metadata.get("attribution", {}).get("creator"):
            score += 1
            results["recommendations"].append("✅ F2: Creator information provided")
        else:
            results["warnings"].append("⚠️ F2: Consider adding creator information")

        technique = metadata.get("technique", {})
        if technique.get("name") and technique.get("description"):
            score += 1
            results["recommendations"].append(
                "✅ F3: Rich metadata with technique details"
            )
        else:
            results["warnings"].append("⚠️ F3: Add more descriptive metadata")

        if metadata.get("emmo_compliance", {}).get("terms_used"):
            score += 1
            results["recommendations"].append(
                "✅ F4: Uses controlled vocabulary (EMMO)"
            )
        else:
            results["warnings"].append(
                "💡 F4: Consider using EMMO vocabulary for better findability"
            )

        # Accessible (A)
        max_score += 2
        dataset = metadata.get("dataset", {})
        if dataset.get("format") in ["CSV", "JSON", "TSV"]:
            score += 1
            results["recommendations"].append("✅ A1: Data in open format")
        else:
            results["warnings"].append("⚠️ A1: Consider using open data formats")

        fair_comp = metadata.get("fair_compliance", {})
        if fair_comp.get("accessible", {}).get("access_protocol"):
            score += 1
            results["recommendations"].append("✅ A2: Access protocol specified")
        else:
            results["warnings"].append("💡 A2: Specify how data can be accessed")

        # Interoperable (I)
        max_score += 2
        if metadata.get("schema_version"):
            score += 1
            results["recommendations"].append("✅ I1: Uses standard metadata schema")

        if fair_comp.get("interoperable", {}).get("metadata_vocabulary"):
            score += 1
            results["recommendations"].append("✅ I2: Metadata vocabulary specified")
        else:
            results["warnings"].append("💡 I2: Specify metadata vocabulary used")

        # Reusable (R)
        max_score += 3
        license_info = fair_comp.get("reusable", {}).get("license")
        if license_info and license_info != "":
            score += 1
            results["recommendations"].append(
                f"✅ R1: License specified ({license_info})"
            )
        else:
            results["warnings"].append("⚠️ R1: Specify data license for reusability")

        if metadata.get("attribution", {}).get("institution"):
            score += 1
            results["recommendations"].append(
                "✅ R2: Institutional provenance provided"
            )
        else:
            results["warnings"].append("💡 R2: Add institutional information")

        if metadata.get("related_work", {}).get("publication_doi"):
            score += 1
            results["recommendations"].append("✅ R3: Linked to publication")
        else:
            results["warnings"].append(
                "💡 R3: Link to related publications if available"
            )

        results["score"] = score / max_score if max_score > 0 else 0
        return results

    def _assess_completeness(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Assess metadata completeness."""
        results = {"warnings": [], "score": 0.0}

        required_fields = [
            ("technique.name", "Technique name"),
            ("experimental_setup.working_electrode", "Working electrode"),
            ("experimental_setup.reference_electrode", "Reference electrode"),
            ("experimental_setup.electrolyte", "Electrolyte"),
            ("dataset.filename", "Dataset filename"),
        ]

        optional_but_recommended = [
            ("attribution.creator", "Creator name"),
            ("attribution.institution", "Institution"),
            ("experimental_setup.temperature", "Temperature"),
            ("technique.parameters", "Technique parameters"),
            ("fair_compliance.reusable.license", "License"),
            ("related_work.publication_doi", "Related publication"),
        ]

        # Check required fields
        present_required = 0
        for field_path, field_name in required_fields:
            if self._get_nested_value(metadata, field_path):
                present_required += 1
            else:
                results["warnings"].append(f"Missing required field: {field_name}")

        # Check recommended fields
        present_recommended = 0
        for field_path, field_name in optional_but_recommended:
            if self._get_nested_value(metadata, field_path):
                present_recommended += 1

        total_fields = len(required_fields) + len(optional_but_recommended)
        total_present = present_required + present_recommended
        results["score"] = total_present / total_fields

        if results["score"] >= 0.8:
            results["warnings"].append(
                f"✅ High completeness score: {results['score']:.1%}"
            )
        elif results["score"] >= 0.6:
            results["warnings"].append(
                f"⚠️ Moderate completeness: {results['score']:.1%} - consider adding more details"
            )
        else:
            results["warnings"].append(
                f"❌ Low completeness: {results['score']:.1%} - important information missing"
            )

        return results

    def _validate_technique_parameters(
        self, metadata: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Validate technique-specific parameters."""
        results = {"errors": [], "warnings": []}

        technique_name = metadata.get("technique", {}).get("name", "")
        parameters = metadata.get("technique", {}).get("parameters", {})

        if not technique_name:
            results["errors"].append("Technique name is required")
            return results

        # Validate based on technique type
        if technique_name == "CV":
            results.update(self._validate_cv_parameters(parameters))
        elif technique_name == "EIS":
            results.update(self._validate_eis_parameters(parameters))
        elif technique_name in ["DPV", "SWV"]:
            results.update(self._validate_pulse_parameters(parameters, technique_name))
        elif technique_name == "CA":
            results.update(self._validate_ca_parameters(parameters))

        return results

    def _validate_cv_parameters(self, params: Dict) -> Dict[str, List[str]]:
        """Validate CV-specific parameters."""
        results = {"errors": [], "warnings": []}

        scan_rate = params.get("scan_rate")
        if scan_rate is not None:
            if not isinstance(scan_rate, (int, float)) or scan_rate <= 0:
                results["errors"].append("CV scan rate must be positive number")
            elif scan_rate > 10:
                results["warnings"].append(
                    "CV scan rate seems high (>10 V/s) - please verify"
                )

        start_pot = params.get("start_potential")
        end_pot = params.get("end_potential")
        if start_pot is not None and end_pot is not None:
            if abs(end_pot - start_pot) < 0.1:
                results["warnings"].append("CV potential window seems narrow (<0.1 V)")

        return results

    def _validate_eis_parameters(self, params: Dict) -> Dict[str, List[str]]:
        """Validate EIS-specific parameters."""
        results = {"errors": [], "warnings": []}

        freq_range = params.get("frequency_range")
        if freq_range and isinstance(freq_range, list) and len(freq_range) >= 2:
            if freq_range[0] <= freq_range[1]:
                results["warnings"].append("EIS frequency range should be [high, low]")

        ac_amplitude = params.get("ac_amplitude")
        if ac_amplitude is not None:
            if ac_amplitude > 0.1:
                results["warnings"].append(
                    "EIS AC amplitude >0.1V may cause non-linear response"
                )

        return results

    def _validate_pulse_parameters(
        self, params: Dict, technique: str
    ) -> Dict[str, List[str]]:
        """Validate pulse technique parameters (DPV, SWV)."""
        results = {"errors": [], "warnings": []}

        if technique == "DPV":
            pulse_width = params.get("pulse_width")
            if pulse_width is not None and pulse_width < 0.01:
                results["warnings"].append("DPV pulse width <10ms may be too short")

        elif technique == "SWV":
            frequency = params.get("frequency")
            if frequency is not None and frequency > 1000:
                results["warnings"].append("SWV frequency >1000Hz may be too high")

        return results

    def _validate_ca_parameters(self, params: Dict) -> Dict[str, List[str]]:
        """Validate CA-specific parameters."""
        results = {"errors": [], "warnings": []}

        step_times = params.get("step_times")
        if step_times and isinstance(step_times, list):
            if any(t < 0.1 for t in step_times):
                results["warnings"].append(
                    "CA step times <0.1s may be too short for steady-state"
                )

        return results

    def validate_data_file(
        self, df: pd.DataFrame, technique: str
    ) -> Dict[str, List[str]]:
        """
        Validate uploaded data file structure and content.

        Args:
            df: DataFrame containing the data
            technique: Electrochemical technique used

        Returns:
            Dictionary with validation results
        """
        results = {"errors": [], "warnings": [], "info": []}

        # Basic structure checks
        if df.empty:
            results["errors"].append("Data file is empty")
            return results

        results["info"].append(
            f"Data file contains {len(df)} rows and {len(df.columns)} columns"
        )

        # Check for expected columns
        expected_patterns = self.column_patterns.get(technique, [])
        if expected_patterns:
            matched_columns = []
            for pattern in expected_patterns:
                matching_cols = [
                    col for col in df.columns if re.search(pattern, col, re.IGNORECASE)
                ]
                if matching_cols:
                    matched_columns.extend(matching_cols)
                else:
                    results["warnings"].append(
                        f"No column matching pattern '{pattern}' for {technique}"
                    )

            if matched_columns:
                results["info"].append(f"Found expected columns: {matched_columns}")
            else:
                results["warnings"].append(
                    f"No expected column patterns found for {technique}"
                )

        # Data quality checks
        numeric_cols = df.select_dtypes(include=["number"]).columns

        if len(numeric_cols) < 2:
            results["warnings"].append(
                "Expected at least 2 numeric columns for electrochemical data"
            )

        # Check for missing values
        missing_data = df.isnull().sum()
        if missing_data.any():
            results["warnings"].append(
                f"Missing values found in columns: {missing_data[missing_data > 0].to_dict()}"
            )

        # Check for duplicate rows
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            results["warnings"].append(f"Found {duplicates} duplicate rows")

        # Basic statistical checks
        for col in numeric_cols:
            if df[col].std() == 0:
                results["warnings"].append(f"Column '{col}' has constant values")

        return results

    def generate_validation_report(
        self, metadata: Dict, data_validation: Dict = None
    ) -> str:
        """Generate comprehensive validation report."""

        validation_results = self.validate_metadata(metadata)

        report = "# Validation Report\n\n"
        report += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        # Summary scores
        report += "## 📊 Summary Scores\n\n"
        report += f"- **FAIR Compliance:** {validation_results['fair_score']:.1%}\n"
        report += f"- **Metadata Completeness:** {validation_results['completeness_score']:.1%}\n\n"

        # Errors
        if validation_results["errors"]:
            report += "## ❌ Errors (Must Fix)\n\n"
            for error in validation_results["errors"]:
                report += f"- {error}\n"
            report += "\n"

        # Warnings
        if validation_results["warnings"]:
            report += "## ⚠️ Warnings & Recommendations\n\n"
            for warning in validation_results["warnings"]:
                report += f"- {warning}\n"
            report += "\n"

        # Information
        if validation_results["info"]:
            report += "## ℹ️ Information\n\n"
            for info in validation_results["info"]:
                report += f"- {info}\n"
            report += "\n"

        # Data validation if provided
        if data_validation:
            report += "## 📁 Data File Validation\n\n"
            for category in ["errors", "warnings", "info"]:
                items = data_validation.get(category, [])
                if items:
                    icon = {"errors": "❌", "warnings": "⚠️", "info": "ℹ️"}[category]
                    report += f"### {icon} {category.title()}\n\n"
                    for item in items:
                        report += f"- {item}\n"
                    report += "\n"

        return report

    def _get_nested_value(self, data: Dict, path: str) -> Any:
        """Get value from nested dictionary using dot notation."""
        keys = path.split(".")
        value = data

        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return None

    def calculate_data_checksum(self, file_content: bytes) -> str:
        """Calculate SHA-256 checksum for data integrity."""
        return hashlib.sha256(file_content).hexdigest()

    def validate_orcid(self, orcid: str) -> bool:
        """Validate ORCID format."""
        pattern = r"^\d{4}-\d{4}-\d{4}-\d{3}[0-9X]$"
        return bool(re.fullmatch(pattern, orcid))

    def validate_doi(self, doi: str) -> bool:
        """Validate DOI format."""
        pattern = r"^10\.\d{4,9}/[\S]+$"
        return bool(re.fullmatch(pattern, doi))

    def suggest_improvements(self, metadata: Dict) -> List[str]:
        """Suggest specific improvements for better FAIR compliance."""
        suggestions = []

        # Attribution suggestions
        attribution = metadata.get("attribution", {})
        if not attribution.get("orcid"):
            suggestions.append("Add ORCID ID for better researcher identification")

        if not attribution.get("contact_email"):
            suggestions.append("Add contact email for data inquiries")

        # Licensing suggestions
        license_info = (
            metadata.get("fair_compliance", {}).get("reusable", {}).get("license")
        )
        if not license_info:
            suggestions.append(
                "Specify a data license (e.g., CC-BY-4.0) to clarify usage terms"
            )

        # EMMO suggestions
        if not metadata.get("emmo_compliance"):
            suggestions.append("Use EMMO vocabulary terms for better interoperability")

        # Publication linking
        if not metadata.get("related_work", {}).get("publication_doi"):
            suggestions.append("Link to related publications via DOI if available")

        # Dataset description
        dataset = metadata.get("dataset", {})
        if not dataset.get("description"):
            suggestions.append("Add detailed dataset description")

        return suggestions[:5]  # Return top 5 suggestions


# Convenience functions for Streamlit integration
def validate_metadata_comprehensive(metadata: Dict) -> Dict[str, List[str]]:
    """Validate metadata with comprehensive checks."""
    validator = ECDataValidator()
    return validator.validate_metadata(metadata)


def validate_data_comprehensive(
    df: pd.DataFrame, technique: str
) -> Dict[str, List[str]]:
    """Validate data file with comprehensive checks."""
    validator = ECDataValidator()
    return validator.validate_data_file(df, technique)


def generate_full_validation_report(
    metadata: Dict, df: pd.DataFrame = None, technique: str = None
) -> str:
    """Generate complete validation report."""
    validator = ECDataValidator()

    data_validation = None
    if df is not None and technique:
        data_validation = validator.validate_data_file(df, technique)

    return validator.generate_validation_report(metadata, data_validation)
