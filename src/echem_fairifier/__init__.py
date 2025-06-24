"""
EChem FAIRifier - Making electrochemical data FAIR-compliant.

This package provides tools for generating FAIR (Findable, Accessible,
Interoperable, Reusable) metadata for electrochemical experiments.
"""

__version__ = "1.0.0"
__author__ = "Amin Haghighatbin"
__email__ = "aminhb@tutanota.com"
__description__ = "Making electrochemical data FAIR-compliant"

# Core imports for easy access
from .core.metadata_generator import FAIRMetadataGenerator
from .core.validator import ECDataValidator
from .core.emmo_integration import EMMOElectrochemistryIntegration
from .config.techniques import ElectrochemicalTechniques

# UI components for Streamlit apps
from .ui.components import UIComponents

__all__ = [
    "FAIRMetadataGenerator",
    "ECDataValidator",
    "EMMOElectrochemistryIntegration",
    "ElectrochemicalTechniques",
    "UIComponents",
]
