"""
Electrochemical technique definitions and parameter templates.
"""

from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class TechniqueParameter:
    """Definition of a technique parameter."""

    name: str
    default_value: Any
    description: str
    unit: str = ""
    parameter_type: str = "number"  # number, text, list
    min_value: float = None
    max_value: float = None


class ElectrochemicalTechniques:
    """Registry of electrochemical techniques and their parameters."""

    TECHNIQUE_PARAMETERS = {
        "CV": {
            "scan_rate": TechniqueParameter(
                name="scan_rate",
                default_value=0.1,
                description="Rate at which potential is swept",
                unit="V/s",
                min_value=0.001,
                max_value=10.0,
            ),
            "start_potential": TechniqueParameter(
                name="start_potential",
                default_value=-0.2,
                description="Initial potential for the sweep",
                unit="V",
                min_value=-5.0,
                max_value=5.0,
            ),
            "end_potential": TechniqueParameter(
                name="end_potential",
                default_value=0.6,
                description="Final potential for the sweep",
                unit="V",
                min_value=-5.0,
                max_value=5.0,
            ),
            "step_size": TechniqueParameter(
                name="step_size",
                default_value=0.002,
                description="Potential step increment",
                unit="V",
                min_value=0.0001,
                max_value=0.1,
            ),
            "cycles": TechniqueParameter(
                name="cycles",
                default_value=1,
                description="Number of CV cycles",
                unit="",
                parameter_type="number",
                min_value=1,
                max_value=100,
            ),
        },
        "DPV": {
            "pulse_amplitude": TechniqueParameter(
                name="pulse_amplitude",
                default_value=0.05,
                description="Amplitude of the differential pulse",
                unit="V",
                min_value=0.001,
                max_value=0.5,
            ),
            "pulse_width": TechniqueParameter(
                name="pulse_width",
                default_value=0.05,
                description="Width of each pulse",
                unit="s",
                min_value=0.001,
                max_value=1.0,
            ),
            "step_potential": TechniqueParameter(
                name="step_potential",
                default_value=0.005,
                description="Potential step between pulses",
                unit="V",
                min_value=0.001,
                max_value=0.1,
            ),
            "scan_rate": TechniqueParameter(
                name="scan_rate",
                default_value=0.01,
                description="Effective scan rate",
                unit="V/s",
                min_value=0.001,
                max_value=1.0,
            ),
        },
        "SWV": {
            "frequency": TechniqueParameter(
                name="frequency",
                default_value=25,
                description="Square wave frequency",
                unit="Hz",
                min_value=1,
                max_value=1000,
            ),
            "amplitude": TechniqueParameter(
                name="amplitude",
                default_value=0.025,
                description="Square wave amplitude",
                unit="V",
                min_value=0.001,
                max_value=0.5,
            ),
            "step_height": TechniqueParameter(
                name="step_height",
                default_value=0.004,
                description="Potential step height",
                unit="V",
                min_value=0.001,
                max_value=0.1,
            ),
        },
        "EIS": {
            "frequency_range": TechniqueParameter(
                name="frequency_range",
                default_value=[100000, 0.01],
                description="Frequency range [high, low]",
                unit="Hz",
                parameter_type="list",
            ),
            "ac_amplitude": TechniqueParameter(
                name="ac_amplitude",
                default_value=0.01,
                description="AC perturbation amplitude",
                unit="V",
                min_value=0.001,
                max_value=0.1,
            ),
            "bias_potential": TechniqueParameter(
                name="bias_potential",
                default_value=0.0,
                description="DC bias potential",
                unit="V",
                min_value=-5.0,
                max_value=5.0,
            ),
            "equilibration_time": TechniqueParameter(
                name="equilibration_time",
                default_value=10,
                description="Pre-equilibration time",
                unit="s",
                min_value=0,
                max_value=3600,
            ),
        },
        "CA": {
            "step_potentials": TechniqueParameter(
                name="step_potentials",
                default_value=[0.0, 0.5],
                description="Applied potentials for each step",
                unit="V",
                parameter_type="list",
            ),
            "step_times": TechniqueParameter(
                name="step_times",
                default_value=[5, 60],
                description="Duration of each potential step",
                unit="s",
                parameter_type="list",
            ),
            "total_duration": TechniqueParameter(
                name="total_duration",
                default_value=65,
                description="Total experiment duration",
                unit="s",
                min_value=1,
                max_value=86400,
            ),
        },
    }

    TECHNIQUE_DESCRIPTIONS = {
        "CV": "Cyclic Voltammetry - Potential swept linearly between limits",
        "DPV": "Differential Pulse Voltammetry - Series of potential pulses",
        "SWV": "Square Wave Voltammetry - Square wave potential modulation",
        "EIS": "Electrochemical Impedance Spectroscopy - AC frequency response",
        "CA": "Chronoamperometry - Current response to potential steps",
    }

    @classmethod
    def get_technique_list(cls) -> List[str]:
        """Get list of available techniques."""
        return list(cls.TECHNIQUE_PARAMETERS.keys())

    @classmethod
    def get_technique_parameters(cls, technique: str) -> Dict[str, TechniqueParameter]:
        """Get parameters for a specific technique."""
        return cls.TECHNIQUE_PARAMETERS.get(technique, {})

    @classmethod
    def get_default_values(cls, technique: str) -> Dict[str, Any]:
        """Get default parameter values for a technique."""
        params = cls.get_technique_parameters(technique)
        return {name: param.default_value for name, param in params.items()}

    @classmethod
    def get_technique_description(cls, technique: str) -> str:
        """Get description of a technique."""
        return cls.TECHNIQUE_DESCRIPTIONS.get(technique, "Unknown technique")
