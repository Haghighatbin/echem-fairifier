"""
Version information for EChem FAIRifier.
"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

# Release information
__release_date__ = "2024-06-24"
__release_name__ = "First Release"

# Build information
__build__ = "stable"
__author__ = "Amin Haghighatbin"
__email__ = "aminhb@tutanota.com"

# Version history and changelog
CHANGELOG = {
    "1.0.0": {
        "date": "2024-06-24",
        "name": "First Release",
        "features": [
            "Complete FAIR metadata generation for CV, EIS, DPV, SWV, CA",
            "EMMO ontology integration",
            "Comprehensive validation with FAIR scoring",
            "Professional UI with error handling",
            "Citation-ready output (CITATION.cff)",
            "Robust data plotting with fallback options",
            "Multi-encoding CSV support",
            "ZIP bundle export with documentation",
        ],
        "fixes": [],
        "breaking_changes": [],
    }
}


def get_version():
    """Get the current version string."""
    return __version__


def get_version_info():
    """Get detailed version information."""
    return {
        "version": __version__,
        "version_info": __version_info__,
        "release_date": __release_date__,
        "release_name": __release_name__,
        "build": __build__,
        "author": __author__,
    }


def print_version():
    """Print version information in a nice format."""
    info = get_version_info()
    print(f"EChem FAIRifier v{info['version']} ({info['release_name']})")
    print(f"Released: {info['release_date']}")
    print(f"Author: {info['author']}")
    print(f"Build: {info['build']}")
