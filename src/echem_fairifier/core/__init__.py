"""Core functionality for EChem FAIRifier."""

from .metadata_generator import FAIRMetadataGenerator
from .validator import ECDataValidator
from .emmo_integration import EMMOElectrochemistryIntegration

__all__ = [
    "FAIRMetadataGenerator",
    "ECDataValidator", 
    "EMMOElectrochemistryIntegration"
]