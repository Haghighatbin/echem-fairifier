#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quick test to verify the Phase 3 & 4 setup works correctly.
Run this before starting the Streamlit app.
"""
import os
import sys
from pathlib import Path

if os.name == "nt":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding="utf-8")

# Add src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))


def test_imports():
    """Test that all modules can be imported."""
    print("🔄 Testing imports...")

    try:
        from echem_fairifier.config.techniques import ElectrochemicalTechniques
        from echem_fairifier.core.metadata_generator import FAIRMetadataGenerator
        from echem_fairifier.core.validator import ECDataValidator
        from echem_fairifier.core.emmo_integration import (
            EMMOElectrochemistryIntegration,
        )
        from echem_fairifier.ui.components import UIComponents

        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_technique_config():
    """Test technique configuration."""
    print("🔄 Testing technique configuration...")

    try:
        from echem_fairifier.config.techniques import ElectrochemicalTechniques

        techniques = ElectrochemicalTechniques.get_technique_list()
        print(f"✅ Found {len(techniques)} techniques: {techniques}")

        cv_params = ElectrochemicalTechniques.get_technique_parameters("CV")
        print(f"✅ CV has {len(cv_params)} parameters")

        return True
    except Exception as e:
        print(f"❌ Technique config error: {e}")
        return False


def test_metadata_generator():
    """Test metadata generation."""
    print("🔄 Testing metadata generation...")

    try:
        from echem_fairifier.core.metadata_generator import FAIRMetadataGenerator

        generator = FAIRMetadataGenerator()

        # Test minimal metadata
        metadata = generator.create_minimal_metadata(technique="CV", parameters={"scan_rate": 0.1}, filename="test.csv")

        print(f"✅ Generated minimal metadata with {len(metadata)} fields")
        return True
    except Exception as e:
        print(f"❌ Metadata generator error: {e}")
        return False


def test_validator():
    """Test validation functionality."""
    print("🔄 Testing validator...")

    try:
        from echem_fairifier.core.validator import ECDataValidator

        validator = ECDataValidator()

        # Test with sample metadata
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

        results = validator.validate_metadata(sample_metadata)
        print(f"✅ Validation completed. FAIR score: {results.get('fair_score', 0):.1%}")
        return True
    except Exception as e:
        print(f"❌ Validator error: {e}")
        return False


def test_emmo_integration():
    """Test EMMO integration."""
    print("🔄 Testing EMMO integration...")

    try:
        from echem_fairifier.core.emmo_integration import (
            EMMOElectrochemistryIntegration,
        )

        emmo = EMMOElectrochemistryIntegration()

        # Test technique validation
        cv_term = emmo.validate_technique("CV")
        if cv_term:
            print(f"✅ CV validated as EMMO term: {cv_term.label}")
        else:
            print("⚠️ CV not found in EMMO terms (using local fallback)")

        # Test suggestions
        suggestions = emmo.suggest_terms("carbon", "materials")
        print(f"✅ Found {len(suggestions)} suggestions for 'carbon'")

        return True
    except Exception as e:
        print(f"❌ EMMO integration error: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 EChem FAIRifier - Phase 3 & 4 Setup Test\n")

    tests = [
        test_imports,
        test_technique_config,
        test_metadata_generator,
        test_validator,
        test_emmo_integration,
    ]

    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()

    print(f"📊 Test Results: {passed}/{len(tests)} tests passed")

    if passed == len(tests):
        print("🎉 All tests passed! Ready to run the Streamlit app.")
        print("\nTo start the app, run:")
        print("  streamlit run run_app.py")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")

    return passed == len(tests)


if __name__ == "__main__":
    main()
