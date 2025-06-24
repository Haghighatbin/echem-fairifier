#!/usr/bin/env python3
"""
Test script to verify plotting functionality works with various data formats.
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add src to path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from echem_fairifier.ui.components import UIComponents


def create_test_datasets():
    """Create various test datasets to verify plotting."""

    datasets = {}

    # Perfect CV data
    datasets["perfect_cv"] = pd.DataFrame(
        {
            "Potential (V)": np.linspace(-0.2, 0.6, 50),
            "Current (A)": np.random.normal(0, 1e-6, 50),
            "Cycle": [1] * 50,
        }
    )

    # CV with different column names
    datasets["cv_alt_names"] = pd.DataFrame(
        {
            "Potential_V": np.linspace(-0.2, 0.6, 50),
            "Current_A": np.random.normal(0, 1e-6, 50),
        }
    )

    # CV with messy column names
    datasets["cv_messy"] = pd.DataFrame(
        {
            "  Potential (V)  ": np.linspace(-0.2, 0.6, 50),
            "Current / A": np.random.normal(0, 1e-6, 50),
        }
    )

    # EIS data
    frequencies = np.logspace(5, -2, 30)
    datasets["eis"] = pd.DataFrame(
        {
            "Frequency (Hz)": frequencies,
            "Z_real (Ohm)": 100 + 50 / np.sqrt(frequencies),
            "Z_imag (Ohm)": -20 * np.sqrt(frequencies),
            "Phase (deg)": (
                -np.arctan(datasets["eis"]["Z_imag"] / datasets["eis"]["Z_real"])
                * 180
                / np.pi
                if "eis" in datasets
                else np.zeros(30)
            ),
        }
    )

    # CA data
    time = np.linspace(0, 100, 200)
    datasets["ca"] = pd.DataFrame(
        {
            "Time (s)": time,
            "Current (A)": 1e-5 * np.exp(-time / 20),
            "Potential (V)": np.where(time < 10, 0.0, 0.5),
        }
    )

    # Generic numeric data
    datasets["generic"] = pd.DataFrame(
        {
            "X_data": np.linspace(0, 10, 100),
            "Y_measurement": np.sin(np.linspace(0, 10, 100))
            + np.random.normal(0, 0.1, 100),
        }
    )

    # Single column
    datasets["single_col"] = pd.DataFrame({"Signal": np.random.normal(0, 1, 50)})

    # Non-numeric data
    datasets["non_numeric"] = pd.DataFrame(
        {
            "Name": ["Sample A", "Sample B", "Sample C"],
            "Type": ["CV", "EIS", "CA"],
            "Status": ["Complete", "Running", "Pending"],
        }
    )

    # Empty dataframe
    datasets["empty"] = pd.DataFrame()

    return datasets


def test_plotting():
    """Test plotting with various datasets."""

    print("🧪 Testing EChem FAIRifier Plotting System\n")

    ui = UIComponents()
    datasets = create_test_datasets()
    techniques = ["CV", "EIS", "CA", "DPV", "SWV"]

    results = {}

    for dataset_name, df in datasets.items():
        print(f"📊 Testing dataset: {dataset_name}")
        print(f"   Shape: {df.shape}")
        print(f"   Columns: {list(df.columns)}")

        dataset_results = {}

        for technique in techniques:
            try:
                # Test column finding
                columns = ui._find_data_columns(df, technique)

                # Test plotting
                fig = ui._create_technique_plot(df, technique)

                # Test fallback
                fallback_fig = ui._create_fallback_plot(df)

                dataset_results[technique] = {
                    "columns_found": len(columns),
                    "technique_plot": fig is not None,
                    "fallback_plot": fallback_fig is not None,
                    "identified_columns": columns,
                }

                status = "✅" if (fig is not None or fallback_fig is not None) else "❌"
                print(f"   {technique}: {status}")

            except Exception as e:
                dataset_results[technique] = {
                    "error": str(e),
                    "columns_found": 0,
                    "technique_plot": False,
                    "fallback_plot": False,
                }
                print(f"   {technique}: ❌ Error: {str(e)}")

        results[dataset_name] = dataset_results
        print()

    return results


def test_column_detection():
    """Test flexible column detection."""

    print("🔍 Testing Column Detection\n")

    ui = UIComponents()

    # Test various column name formats
    test_columns = [
        # Potential variations
        ["Potential (V)", "Current (A)"],
        ["Potential_V", "Current_A"],
        ["E (V)", "I (A)"],
        ["Voltage", "Amperage"],
        ["potential", "current"],
        ["POTENTIAL (V)", "CURRENT (A)"],
        ["  Potential (V)  ", "  Current (A)  "],
        # EIS variations
        ["Frequency (Hz)", "Z_real (Ohm)", "Z_imag (Ohm)"],
        ["Freq", "Z'", "Z''"],
        ["f (Hz)", "Re(Z)", "Im(Z)"],
        # CA variations
        ["Time (s)", "Current (A)", "Potential (V)"],
        ["t", "I", "E"],
        ["Time_s", "Current_A", "Potential_V"],
    ]

    for i, cols in enumerate(test_columns):
        print(f"Test {i+1}: {cols}")

        # Create dummy dataframe
        data = {col: np.random.random(10) for col in cols}
        df = pd.DataFrame(data)

        for technique in ["CV", "EIS", "CA"]:
            detected = ui._find_data_columns(df, technique)
            print(f"  {technique}: {detected}")

        print()


def main():
    """Run all plotting tests."""

    print("🎨 EChem FAIRifier Plotting Test Suite\n")

    try:
        # Test basic plotting
        results = test_plotting()

        # Test column detection
        test_column_detection()

        # Summary
        print("📈 Summary:")

        total_tests = 0
        successful_plots = 0

        for dataset_name, dataset_results in results.items():
            for technique, result in dataset_results.items():
                total_tests += 1
                if result.get("technique_plot") or result.get("fallback_plot"):
                    successful_plots += 1

        success_rate = (successful_plots / total_tests) * 100 if total_tests > 0 else 0

        print(
            f"✅ {successful_plots}/{total_tests} tests created plots ({success_rate:.1f}%)"
        )

        if success_rate >= 80:
            print("🎉 Plotting system is working well!")
        elif success_rate >= 60:
            print("⚠️ Plotting system works but could be improved")
        else:
            print("❌ Plotting system needs attention")

        return success_rate >= 60

    except Exception as e:
        print(f"❌ Test suite error: {str(e)}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
