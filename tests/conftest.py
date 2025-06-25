"""
Pytest configuration and fixtures for EChem FAIRifier tests.
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

# Add src directory to Python path for all tests
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))


@pytest.fixture(scope="session")
def sample_cv_data():
    """Sample CV data for testing across multiple test files."""
    return pd.DataFrame(
        {
            "Potential (V)": [
                -0.2,
                -0.1,
                0.0,
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
                0.5,
                0.4,
                0.3,
                0.2,
                0.1,
                0.0,
                -0.1,
                -0.2,
            ],
            "Current (A)": [
                1e-6,
                1.5e-6,
                2e-6,
                3e-6,
                5e-6,
                8e-6,
                12e-6,
                15e-6,
                18e-6,
                15e-6,
                12e-6,
                8e-6,
                5e-6,
                3e-6,
                2e-6,
                1.5e-6,
                1e-6,
            ],
            "Cycle": [1] * 17,
        }
    )


@pytest.fixture(scope="session")
def sample_eis_data():
    """Sample EIS data for testing across multiple test files."""
    return pd.DataFrame(
        {
            "Frequency (Hz)": [
                100000,
                31623,
                10000,
                3162,
                1000,
                316,
                100,
                31.6,
                10,
                3.16,
                1,
                0.316,
                0.1,
                0.0316,
                0.01,
            ],
            "Z_real (Ohm)": [
                100,
                102,
                105,
                110,
                120,
                140,
                180,
                250,
                350,
                500,
                700,
                900,
                1100,
                1200,
                1250,
            ],
            "Z_imag (Ohm)": [
                -5,
                -8,
                -15,
                -25,
                -40,
                -60,
                -80,
                -90,
                -85,
                -70,
                -50,
                -30,
                -15,
                -8,
                -5,
            ],
            "Phase (deg)": [
                -3,
                -4,
                -8,
                -13,
                -18,
                -23,
                -24,
                -20,
                -14,
                -8,
                -4,
                -2,
                -1,
                -0.4,
                -0.2,
            ],
        }
    )


@pytest.fixture(scope="session")
def sample_dpv_data():
    """Sample DPV data for testing."""
    return pd.DataFrame(
        {
            "Potential (V)": [
                -0.8,
                -0.7,
                -0.6,
                -0.5,
                -0.4,
                -0.3,
                -0.2,
                -0.1,
                0.0,
                0.1,
                0.2,
            ],
            "Current (A)": [
                1e-8,
                2e-8,
                5e-8,
                15e-8,
                45e-8,
                80e-8,
                50e-8,
                20e-8,
                8e-8,
                4e-8,
                2e-8,
            ],
        }
    )


@pytest.fixture
def minimal_valid_metadata():
    """Minimal but valid metadata for testing."""
    return {
        "experiment_id": "test-12345",
        "technique": {
            "name": "CV",
            "parameters": {
                "scan_rate": 0.1,
                "start_potential": -0.2,
                "end_potential": 0.6,
            },
        },
        "experimental_setup": {
            "working_electrode": "Glassy carbon, 3 mm",
            "reference_electrode": "Ag/AgCl",
            "counter_electrode": "Pt wire",
            "electrolyte": "0.1 M KCl",
        },
        "dataset": {"filename": "test_data.csv", "format": "CSV"},
    }


@pytest.fixture
def complete_metadata():
    """Complete metadata with all optional fields for testing."""
    return {
        "experiment_id": "550e8400-e29b-41d4-a716-446655440000",
        "created_date": "2024-06-24T10:30:00",
        "schema_version": "1.0.0",
        "technique": {
            "name": "CV",
            "description": "Cyclic voltammetry of ferrocyanide redox couple",
            "parameters": {
                "scan_rate": 0.1,
                "start_potential": -0.2,
                "end_potential": 0.6,
                "step_size": 0.002,
                "cycles": 3,
            },
        },
        "experimental_setup": {
            "working_electrode": "Glassy carbon, 3 mm diameter",
            "reference_electrode": "Ag/AgCl (3M KCl)",
            "counter_electrode": "Platinum wire",
            "electrolyte": "3 mM K3[Fe(CN)6]/K4[Fe(CN)6] in 0.1 M KNO3",
            "temperature": "25 ± 1°C",
            "atmosphere": "Nitrogen",
        },
        "dataset": {
            "filename": "cv_ferrocyanide_complete.csv",
            "format": "CSV",
            "encoding": "UTF-8",
            "description": "High-quality CV measurement of ferrocyanide redox couple",
        },
        "fair_compliance": {
            "findable": {
                "unique_identifier": "550e8400-e29b-41d4-a716-446655440000",
                "metadata_standard": "EChem-FAIR v1.0",
            },
            "accessible": {
                "access_protocol": "HTTP download",
                "format": "Open format (CSV, YAML)",
            },
            "interoperable": {
                "metadata_vocabulary": "EMMO Electrochemistry Domain",
                "data_format_standard": "CSV with standardised headers",
            },
            "reusable": {
                "license": "CC-BY-4.0",
                "provenance": "Generated by EChem FAIRifier",
                "quality_assessment": "Automated validation applied",
            },
        },
        "attribution": {
            "creator": "Dr. Test Researcher",
            "institution": "University of Testing",
            "contact_email": "test.researcher@university.edu",
            "orcid": "0000-0002-1825-0097",
        },
        "related_work": {
            "publication_doi": "10.1021/acs.analchem.1c00123",
            "funding_source": "National Science Foundation Grant CHE-1234567",
        },
    }


@pytest.fixture
def invalid_metadata_missing_required():
    """Invalid metadata missing required fields."""
    return {
        "technique": {"name": "CV"}
        # Missing experimental_setup, dataset, etc.
    }


# Test data creation helpers
def create_problematic_dataframe():
    """Create a DataFrame with various data quality issues."""
    return pd.DataFrame(
        {
            "Potential (V)": [0.1, 0.2, 0.2, 0.3, None],  # Duplicate and missing value
            "Current (A)": [1e-6, 2e-6, 2e-6, 3e-6, 4e-6],  # Duplicate
            "Constant": [1.0, 1.0, 1.0, 1.0, 1.0],  # Constant values
            "Noise": [0.1, 0.1, 0.1, 0.1, 0.1],  # Another constant column
        }
    )


def create_empty_dataframe():
    """Create an empty DataFrame for testing error handling."""
    return pd.DataFrame()


def create_single_column_dataframe():
    """Create DataFrame with only one column."""
    return pd.DataFrame({"Potential (V)": [0.1, 0.2, 0.3, 0.4, 0.5]})


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "ui: marks tests that require UI interaction")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Mark slow tests
        if "slow" in item.name.lower() or "integration" in item.name.lower():
            item.add_marker(pytest.mark.slow)

        # Mark UI tests
        if "ui" in item.name.lower() or "streamlit" in item.name.lower():
            item.add_marker(pytest.mark.ui)
