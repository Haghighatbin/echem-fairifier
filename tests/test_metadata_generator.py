"""
Tests for FAIRMetadataGenerator class.
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime

# Add src to path for testing
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from echem_fairifier.core.metadata_generator import FAIRMetadataGenerator


class TestFAIRMetadataGenerator:
    """Test suite for FAIR metadata generation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.generator = FAIRMetadataGenerator()

        self.sample_technique_params = {
            "scan_rate": 0.1,
            "start_potential": -0.2,
            "end_potential": 0.6,
            "cycles": 1,
        }

        self.sample_experimental_details = {
            "working_electrode": "Glassy carbon, 3 mm",
            "reference_electrode": "Ag/AgCl",
            "counter_electrode": "Pt wire",
            "electrolyte": "3 mM [Fe(CN)6]3-/4- in 0.1 M KNO3",
            "creator": "Test Researcher",
            "institution": "Test University",
        }

        self.sample_dataset_info = {"filename": "test_cv.csv"}

    def test_generate_minimal_metadata(self):
        """Test minimal metadata generation."""
        metadata = self.generator.create_minimal_metadata(technique="CV", parameters={"scan_rate": 0.1}, filename="test.csv")

        assert metadata["technique"] == "CV"
        assert metadata["technique_parameters"]["scan_rate"] == 0.1
        assert metadata["dataset_link"] == "test.csv"
        assert "created_date" in metadata
        assert "schema_version" in metadata

    def test_generate_full_metadata(self):
        """Test full metadata generation."""
        metadata = self.generator.generate_metadata(
            technique="CV",
            technique_parameters=self.sample_technique_params,
            experimental_details=self.sample_experimental_details,
            dataset_info=self.sample_dataset_info,
        )

        # Check required sections exist
        assert "experiment_id" in metadata
        assert "technique" in metadata
        assert "experimental_setup" in metadata
        assert "dataset" in metadata
        assert "fair_compliance" in metadata
        assert "attribution" in metadata

        # Check technique information
        assert metadata["technique"]["name"] == "CV"
        assert metadata["technique"]["parameters"] == self.sample_technique_params

        # Check experimental setup
        exp_setup = metadata["experimental_setup"]
        assert exp_setup["working_electrode"] == "Glassy carbon, 3 mm"
        assert exp_setup["electrolyte"] == "3 mM [Fe(CN)6]3-/4- in 0.1 M KNO3"

        # Check FAIR compliance structure
        fair = metadata["fair_compliance"]
        assert "findable" in fair
        assert "accessible" in fair
        assert "interoperable" in fair
        assert "reusable" in fair

    def test_yaml_generation(self):
        """Test YAML string generation."""
        metadata = self.generator.create_minimal_metadata("CV", {}, "test.csv")
        yaml_str = self.generator.generate_yaml(metadata)

        assert isinstance(yaml_str, str)
        assert "technique: CV" in yaml_str
        assert "dataset_link: test.csv" in yaml_str
        assert yaml_str.startswith("technique:")  # YAML format check

    def test_metadata_validation(self):
        """Test metadata validation."""
        # Valid metadata
        valid_metadata = {
            "technique": {"name": "CV", "parameters": {}},
            "experimental_setup": {
                "working_electrode": "GC",
                "reference_electrode": "Ag/AgCl",
                "counter_electrode": "Pt",
                "electrolyte": "0.1 M KCl",
            },
        }

        results = self.generator.validate_metadata(valid_metadata)
        assert "errors" in results
        assert "warnings" in results

        # Should have minimal errors for valid metadata
        assert len(results["errors"]) <= 2  # Only missing experiment_id acceptable

    def test_missing_required_fields(self):
        """Test validation with missing required fields."""
        incomplete_metadata = {
            "technique": {"name": "CV"}
            # Missing experimental_setup
        }

        results = self.generator.validate_metadata(incomplete_metadata)
        assert len(results["errors"]) > 0

        # Check specific required fields are flagged
        error_text = " ".join(results["errors"])
        assert "working_electrode" in error_text
        assert "electrolyte" in error_text

    def test_expected_columns_generation(self):
        """Test expected column generation for different techniques."""
        # Test CV columns
        cv_cols = self.generator._get_expected_columns("CV")
        assert "Potential (V)" in cv_cols
        assert "Current (A)" in cv_cols

        # Test EIS columns
        eis_cols = self.generator._get_expected_columns("EIS")
        assert "Frequency (Hz)" in eis_cols
        assert "Z_real (Ohm)" in eis_cols

        # Test unknown technique (should return default)
        unknown_cols = self.generator._get_expected_columns("UNKNOWN")
        assert "Potential (V)" in unknown_cols

    def test_technique_descriptions(self):
        """Test technique description generation."""
        cv_desc = self.generator._get_technique_description("CV")
        assert "cyclic voltammetry" in cv_desc.lower()

        eis_desc = self.generator._get_technique_description("EIS")
        assert "impedance" in eis_desc.lower()

        unknown_desc = self.generator._get_technique_description("UNKNOWN")
        assert "UNKNOWN" in unknown_desc

    def test_uuid_generation(self):
        """Test that unique IDs are generated."""
        metadata1 = self.generator.generate_metadata("CV", {}, {"working_electrode": "test"}, {"filename": "test1.csv"})
        metadata2 = self.generator.generate_metadata("CV", {}, {"working_electrode": "test"}, {"filename": "test2.csv"})

        # Should have different experiment IDs
        assert metadata1["experiment_id"] != metadata2["experiment_id"]

        # Should be valid UUID format
        import uuid

        try:
            uuid.UUID(metadata1["experiment_id"])
            uuid.UUID(metadata2["experiment_id"])
        except ValueError:
            pytest.fail("Generated IDs are not valid UUIDs")

    def test_datetime_format(self):
        """Test that created_date is in ISO format."""
        metadata = self.generator.create_minimal_metadata("CV", {}, "test.csv")
        created_date = metadata["created_date"]

        # Should be parseable as ISO datetime
        try:
            parsed_date = datetime.fromisoformat(created_date.replace("Z", "+00:00"))
            assert isinstance(parsed_date, datetime)
        except ValueError:
            pytest.fail(f"Created date '{created_date}' is not in ISO format")


# Fixtures for test data
@pytest.fixture
def sample_cv_metadata():
    """Sample CV metadata for testing."""
    return {
        "technique": {
            "name": "CV",
            "parameters": {
                "scan_rate": 0.1,
                "start_potential": -0.2,
                "end_potential": 0.6,
            },
        },
        "experimental_setup": {
            "working_electrode": "Glassy carbon",
            "reference_electrode": "Ag/AgCl",
            "counter_electrode": "Pt wire",
            "electrolyte": "0.1 M KCl",
        },
        "dataset": {"filename": "test_cv.csv", "format": "CSV"},
    }


@pytest.fixture
def sample_eis_metadata():
    """Sample EIS metadata for testing."""
    return {
        "technique": {
            "name": "EIS",
            "parameters": {"frequency_range": [100000, 0.01], "ac_amplitude": 0.01},
        },
        "experimental_setup": {
            "working_electrode": "Gold electrode",
            "reference_electrode": "SCE",
            "counter_electrode": "Pt mesh",
            "electrolyte": "1 M H2SO4",
        },
        "dataset": {"filename": "test_eis.csv", "format": "CSV"},
    }


if __name__ == "__main__":
    pytest.main([__file__])
