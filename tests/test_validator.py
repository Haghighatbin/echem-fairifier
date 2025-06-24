"""
Tests for ECDataValidator class.
"""

import streamlit as st
import pytest
import pandas as pd
import sys
from pathlib import Path

# Add src to path for testing
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from echem_fairifier.core.validator import ECDataValidator


class TestECDataValidator:
    """Test suite for electrochemical data validation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.validator = ECDataValidator()

        # Mock streamlit session state if not available
        if "st" not in globals():
            import unittest.mock

            st_mock = unittest.mock.MagicMock()
            st_mock.session_state = {}
            globals()["st"] = st_mock

    def test_validator_initialization(self):
        """Test validator initialises correctly."""
        assert self.validator is not None
        assert hasattr(self.validator, "schema")
        assert hasattr(self.validator, "column_patterns")

    def test_fair_compliance_scoring(self):
        """Test FAIR compliance scoring."""
        # High-quality metadata
        good_metadata = {
            "experiment_id": "test-123-456",
            "technique": {
                "name": "CV",
                "description": "Cyclic voltammetry measurement",
            },
            "experimental_setup": {
                "working_electrode": "GC",
                "reference_electrode": "Ag/AgCl",
                "electrolyte": "0.1 M KCl",
            },
            "attribution": {
                "creator": "Test Researcher",
                "institution": "Test University",
            },
            "fair_compliance": {
                "reusable": {"license": "CC-BY-4.0"},
                "accessible": {"access_protocol": "Download"},
            },
            "related_work": {"publication_doi": "10.1000/test123"},
        }

        results = self.validator._check_fair_compliance(good_metadata)
        assert results["score"] > 0.6  # Should score well

        # Poor metadata
        poor_metadata = {"technique": {"name": "CV"}}

        results_poor = self.validator._check_fair_compliance(poor_metadata)
        assert results_poor["score"] < 0.3  # Should score poorly

    def test_cv_parameter_validation(self):
        """Test CV-specific parameter validation."""
        # Valid CV parameters
        valid_params = {"scan_rate": 0.1, "start_potential": -0.2, "end_potential": 0.6}

        results = self.validator._validate_cv_parameters(valid_params)
        assert len(results["errors"]) == 0

        # Invalid CV parameters
        invalid_params = {
            "scan_rate": -0.1,  # Negative scan rate
            "start_potential": 0.5,
            "end_potential": 0.51,  # Very narrow window
        }

        results_invalid = self.validator._validate_cv_parameters(invalid_params)
        assert len(results_invalid["errors"]) > 0
        assert len(results_invalid["warnings"]) > 0

    def test_eis_parameter_validation(self):
        """Test EIS-specific parameter validation."""
        # Valid EIS parameters
        valid_params = {"frequency_range": [100000, 0.01], "ac_amplitude": 0.01}

        results = self.validator._validate_eis_parameters(valid_params)
        assert len(results["errors"]) == 0

        # Invalid EIS parameters
        invalid_params = {
            "frequency_range": [0.01, 100000],  # Wrong order
            "ac_amplitude": 0.5,  # Too high amplitude
        }

        results_invalid = self.validator._validate_eis_parameters(invalid_params)
        assert len(results_invalid["warnings"]) > 0

    def test_data_file_validation_cv(self):
        """Test CV data file validation."""
        # Valid CV data
        cv_data = pd.DataFrame(
            {
                "Potential (V)": [-0.2, 0.0, 0.2, 0.4, 0.6],
                "Current (A)": [1e-6, 2e-6, 5e-6, 3e-6, 1e-6],
                "Cycle": [1, 1, 1, 1, 1],
            }
        )

        results = self.validator.validate_data_file(cv_data, "CV")
        assert len(results["errors"]) == 0
        assert "Found expected columns" in " ".join(results["info"])

    def test_data_file_validation_missing_columns(self):
        """Test data validation with missing expected columns."""
        # Data missing expected columns
        incomplete_data = pd.DataFrame({"X": [1, 2, 3], "Y": [4, 5, 6]})

        results = self.validator.validate_data_file(incomplete_data, "CV")
        assert len(results["warnings"]) > 0

        warning_text = " ".join(results["warnings"])
        assert "pattern" in warning_text.lower()

    def test_data_quality_checks(self):
        """Test data quality validation."""
        # Data with issues
        problematic_data = pd.DataFrame(
            {
                "Potential (V)": [0.1, 0.2, 0.2, 0.3],  # Duplicate row
                "Current (A)": [1e-6, 2e-6, 2e-6, None],  # Missing value and duplicate
                "Constant": [1.0, 1.0, 1.0, 1.0],  # Constant column
            }
        )

        results = self.validator.validate_data_file(problematic_data, "CV")

        warning_text = " ".join(results["warnings"])
        assert "duplicate" in warning_text.lower() or "missing" in warning_text.lower()

    def test_empty_dataframe_validation(self):
        """Test validation of empty dataframe."""
        empty_df = pd.DataFrame()

        results = self.validator.validate_data_file(empty_df, "CV")
        assert len(results["errors"]) > 0
        assert "empty" in results["errors"][0].lower()

    def test_completeness_assessment(self):
        """Test metadata completeness scoring."""
        # Complete metadata
        complete_metadata = {
            "technique": {"name": "CV", "parameters": {"scan_rate": 0.1}},
            "experimental_setup": {
                "working_electrode": "GC",
                "reference_electrode": "Ag/AgCl",
                "electrolyte": "0.1 M KCl",
                "temperature": "25°C",
            },
            "dataset": {"filename": "test.csv"},
            "attribution": {"creator": "Test User", "institution": "Test Uni"},
            "fair_compliance": {"reusable": {"license": "CC-BY-4.0"}},
            "related_work": {"publication_doi": "10.1000/test"},
        }

        results = self.validator._assess_completeness(complete_metadata)
        assert results["score"] > 0.8  # Should be high completeness

        # Minimal metadata
        minimal_metadata = {
            "technique": {"name": "CV"},
            "experimental_setup": {
                "working_electrode": "GC",
                "reference_electrode": "Ag/AgCl",
                "electrolyte": "0.1 M KCl",
            },
            "dataset": {"filename": "test.csv"},
        }

        results_minimal = self.validator._assess_completeness(minimal_metadata)
        assert results_minimal["score"] < 0.7  # Should be lower

    def test_orcid_validation(self):
        """Test ORCID format validation."""
        valid_orcids = [
            "0000-0000-0000-0000",
            "0000-0002-1825-0097",
            "0000-0002-1825-009X",
        ]

        invalid_orcids = [
            "000-0000-0000-0000",  # Too short
            "0000-0000-0000-00000",  # Too long
            "0000-0000-0000-000Y",  # Invalid character
            "not-an-orcid",
        ]

        for orcid in valid_orcids:
            assert self.validator.validate_orcid(orcid), f"Should be valid: {orcid}"

        for orcid in invalid_orcids:
            assert not self.validator.validate_orcid(
                orcid
            ), f"Should be invalid: {orcid}"

    def test_doi_validation(self):
        """Test DOI format validation."""
        valid_dois = ["10.1000/xyz123", "10.1038/nature12373", "10.1021/ja01268a023"]

        invalid_dois = [
            "not-a-doi",
            "10.abc/xyz",  # Invalid prefix format
            "doi:10.1000/xyz",  # With prefix
        ]

        for doi in valid_dois:
            assert self.validator.validate_doi(doi), f"Should be valid: {doi}"

        for doi in invalid_dois:
            assert not self.validator.validate_doi(doi), f"Should be invalid: {doi}"

    def test_nested_value_extraction(self):
        """Test nested dictionary value extraction."""
        test_data = {"level1": {"level2": {"target": "found_it"}, "other": "not_this"}}

        # Valid path
        result = self.validator._get_nested_value(test_data, "level1.level2.target")
        assert result == "found_it"

        # Invalid path
        result_none = self.validator._get_nested_value(
            test_data, "level1.nonexistent.target"
        )
        assert result_none is None

        # Partial path
        result_dict = self.validator._get_nested_value(test_data, "level1.level2")
        assert isinstance(result_dict, dict)
        assert result_dict["target"] == "found_it"

    def test_validation_report_generation(self):
        """Test validation report generation."""
        sample_metadata = {
            "experiment_id": "test-123",
            "technique": {"name": "CV", "parameters": {}},
            "experimental_setup": {
                "working_electrode": "GC",
                "reference_electrode": "Ag/AgCl",
                "electrolyte": "0.1 M KCl",
            },
            "dataset": {"filename": "test.csv", "format": "CSV"},
        }

        report = self.validator.generate_validation_report(sample_metadata)

        assert isinstance(report, str)
        assert "Validation Report" in report
        assert "Summary Scores" in report
        assert "FAIR Compliance" in report
        assert "Metadata Completeness" in report

    def test_improvement_suggestions(self):
        """Test improvement suggestions generation."""
        minimal_metadata = {
            "technique": {"name": "CV"},
            "experimental_setup": {
                "working_electrode": "GC",
                "reference_electrode": "Ag/AgCl",
                "electrolyte": "0.1 M KCl",
            },
        }

        suggestions = self.validator.suggest_improvements(minimal_metadata)

        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
        assert len(suggestions) <= 5  # Should limit to top 5

        # Check for common suggestions
        suggestion_text = " ".join(suggestions).lower()
        assert any(
            keyword in suggestion_text
            for keyword in ["orcid", "license", "email", "emmo"]
        )

    def test_technique_specific_validation(self):
        """Test technique-specific parameter validation integration."""
        # Test CV technique validation
        cv_metadata = {
            "technique": {
                "name": "CV",
                "parameters": {
                    "scan_rate": 15.0,  # Very high scan rate
                    "start_potential": 0.5,
                    "end_potential": 0.51,  # Very narrow window
                },
            },
            "experimental_setup": {
                "working_electrode": "GC",
                "reference_electrode": "Ag/AgCl",
                "electrolyte": "0.1 M KCl",
            },
        }

        results = self.validator._validate_technique_parameters(cv_metadata)
        assert (
            len(results["warnings"]) > 0
        )  # Should warn about high scan rate and narrow window

    def test_pulse_technique_validation(self):
        """Test DPV and SWV parameter validation."""
        # Test DPV with very short pulse width
        dpv_params = {"pulse_width": 0.005}  # 5ms - quite short
        results = self.validator._validate_pulse_parameters(dpv_params, "DPV")
        assert len(results["warnings"]) > 0

        # Test SWV with very high frequency
        swv_params = {"frequency": 1500}  # Very high frequency
        results = self.validator._validate_pulse_parameters(swv_params, "SWV")
        assert len(results["warnings"]) > 0

    def test_ca_parameter_validation(self):
        """Test chronoamperometry parameter validation."""
        # Test CA with very short step times
        ca_params = {"step_times": [0.05, 0.08]}  # Very short steps
        results = self.validator._validate_ca_parameters(ca_params)
        assert len(results["warnings"]) > 0

    def test_checksum_calculation(self):
        """Test data checksum calculation."""
        test_data = b"test data content"
        checksum = self.validator.calculate_data_checksum(test_data)

        assert isinstance(checksum, str)
        assert len(checksum) == 64  # SHA-256 produces 64-character hex string

        # Same data should produce same checksum
        checksum2 = self.validator.calculate_data_checksum(test_data)
        assert checksum == checksum2

        # Different data should produce different checksum
        different_data = b"different test data"
        checksum3 = self.validator.calculate_data_checksum(different_data)
        assert checksum != checksum3

    def test_schema_loading_fallback(self):
        """Test schema loading with fallback to minimal schema."""
        # Test with non-existent schema path
        validator_with_bad_path = ECDataValidator("/non/existent/path.json")
        assert validator_with_bad_path.schema is not None
        assert "type" in validator_with_bad_path.schema

    def test_comprehensive_metadata_validation(self):
        """Test full metadata validation integration."""
        metadata = {
            "experiment_id": "test-uuid",
            "technique": {"name": "CV", "parameters": {"scan_rate": 0.1}},
            "experimental_setup": {
                "working_electrode": "GC",
                "reference_electrode": "Ag/AgCl",
                "counter_electrode": "Pt",
                "electrolyte": "0.1 M KCl",
            },
            "dataset": {"filename": "test.csv", "format": "CSV"},
        }

        results = self.validator.validate_metadata(metadata)

        # Should have all required result keys
        assert "errors" in results
        assert "warnings" in results
        assert "fair_score" in results
        assert "completeness_score" in results

        # Scores should be valid ranges
        assert 0 <= results["fair_score"] <= 1
        assert 0 <= results["completeness_score"] <= 1

    def test_data_validation_edge_cases(self):
        """Test edge cases in data validation."""
        # Test with only one row
        single_row_df = pd.DataFrame({"Potential (V)": [0.1], "Current (A)": [1e-6]})

        results = self.validator.validate_data_file(single_row_df, "CV")
        assert len(results["warnings"]) >= 0  # Should handle gracefully

        # Test with very large dataset
        large_df = pd.DataFrame(
            {"Potential (V)": list(range(10000)), "Current (A)": [1e-6] * 10000}
        )

        results = self.validator.validate_data_file(large_df, "CV")
        assert "info" in results

    def test_unknown_technique_handling(self):
        """Test handling of unknown techniques."""
        unknown_metadata = {
            "technique": {"name": "UNKNOWN_TECHNIQUE", "parameters": {}},
            "experimental_setup": {
                "working_electrode": "GC",
                "reference_electrode": "Ag/AgCl",
                "electrolyte": "0.1 M KCl",
            },
        }

        results = self.validator._validate_technique_parameters(unknown_metadata)
        # Should handle gracefully without crashing
        assert isinstance(results, dict)


# Test fixtures
@pytest.fixture
def sample_cv_dataframe():
    """Sample CV dataframe for testing."""
    return pd.DataFrame(
        {
            "Potential (V)": [-0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
            "Current (A)": [1e-6, 1.5e-6, 2e-6, 3e-6, 5e-6, 4e-6, 3e-6, 2e-6, 1e-6],
            "Cycle": [1, 1, 1, 1, 1, 1, 1, 1, 1],
        }
    )


@pytest.fixture
def sample_eis_dataframe():
    """Sample EIS dataframe for testing."""
    return pd.DataFrame(
        {
            "Frequency (Hz)": [100000, 10000, 1000, 100, 10, 1, 0.1, 0.01],
            "Z_real (Ohm)": [100, 105, 120, 150, 200, 300, 500, 800],
            "Z_imag (Ohm)": [-5, -10, -20, -50, -80, -100, -80, -50],
            "Phase (deg)": [-3, -5, -10, -18, -22, -18, -9, -4],
        }
    )


@pytest.fixture
def complete_metadata():
    """Complete metadata for testing."""
    return {
        "experiment_id": "550e8400-e29b-41d4-a716-446655440000",
        "created_date": "2024-01-15T10:30:00",
        "technique": {
            "name": "CV",
            "description": "Cyclic voltammetry measurement",
            "parameters": {
                "scan_rate": 0.1,
                "start_potential": -0.2,
                "end_potential": 0.6,
                "cycles": 3,
            },
        },
        "experimental_setup": {
            "working_electrode": "Glassy carbon, 3 mm diameter",
            "reference_electrode": "Ag/AgCl (3M KCl)",
            "counter_electrode": "Platinum wire",
            "electrolyte": "3 mM [Fe(CN)6]3-/4- in 0.1 M KNO3",
            "temperature": "25 ± 1°C",
            "atmosphere": "Nitrogen",
        },
        "dataset": {
            "filename": "cv_ferrocyanide_test.csv",
            "format": "CSV",
            "encoding": "UTF-8",
            "description": "Cyclic voltammetry of ferrocyanide redox couple",
        },
        "attribution": {
            "creator": "Dr. Test Researcher",
            "institution": "University of Testing",
            "contact_email": "test@example.com",
            "orcid": "0000-0002-1825-0097",
        },
        "fair_compliance": {
            "reusable": {"license": "CC-BY-4.0"},
            "accessible": {"access_protocol": "HTTP download"},
        },
        "related_work": {
            "publication_doi": "10.1021/test.example",
            "funding_source": "Test Grant Agency",
        },
    }


if __name__ == "__main__":
    pytest.main([__file__])
