# EChem FAIRifier

[![Live Demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://echem-fairifier.up.railway.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/haghighatbin/echem-fairifier/actions/workflows/ci.yml/badge.svg)](https://github.com/haghighatbin/echem-fairifier/actions)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15737409.svg)](https://doi.org/10.5281/zenodo.15737409)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![FAIR](https://img.shields.io/badge/FAIR-compliant-brightgreen.svg)](https://www.go-fair.org/fair-principles/)
[![EMMO](https://img.shields.io/badge/EMMO-integrated-blue.svg)](https://emmo-repo.github.io/)
[![Last Commit](https://img.shields.io/github/last-commit/haghighatbin/echem-fairifier.svg)](https://github.com/haghighatbin/echem-fairifier/commits/main)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/haghighatbin/echem-fairifier/releases)

> **Making electrochemical data FAIR-compliant**  
> A tool for generating FAIR (Findable, Accessible, Interoperable, Reusable) metadata for electrochemical experiments.

## Keywords
FAIR data, electrochemistry, metadata generation, cyclic voltammetry, electrochemical impedance spectroscopy, differential pulse voltammetry, square wave voltammetry, chronoamperometry, EMMO ontology, scientific data management, research reproducibility

## Use Cases
- Making electrochemical research data FAIR-compliant
- Automated metadata generation for CV, EIS, DPV, SWV, CA experiments
- Research data management for electrochemistry laboratories
- Preparing data for scientific repositories and publications

## Overview

**EChem FAIRifier** transforms raw electrochemical data into FAIR-compliant datasets with comprehensive metadata, automated validation, and complete documentation. Built for the electrochemistry community to improve data sharing, reproducibility, and collaboration.

👉 Read my Substack post: [**The Missing Infrastructure Problem**](https://open.substack.com/pub/aminhaghighatbin/p/the-missing-infrastructure-problem?r=45weci&utm_campaign=post&utm_medium=web&showWelcomeOnShare=false)

## 🚀 Quick Start

### Try Online (Recommended)
Visit the **[Live Demo](https://echem-fairifier.up.railway.app)** - no installation required!

### Local Installation
```bash
# Clone the repository
git clone https://github.com/haghighatbin/echem-fairifier.git
cd echem-fairifier

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run run_app.py
```

## Key Features

### **Technique Support**
- **Cyclic Voltammetry (CV)** - Full parameter validation and visualisation
- **Electrochemical Impedance Spectroscopy (EIS)** - Nyquist plot generation
- **Differential Pulse Voltammetry (DPV)** - Pulse parameter optimisation
- **Square Wave Voltammetry (SWV)** - Frequency domain analysis
- **Chronoamperometry (CA)** - Time-based measurements

### **FAIR Compliance**
- **Findable:** Unique identifiers, rich metadata, controlled vocabularies
- **Accessible:** Open formats (CSV, YAML), standard protocols
- **Interoperable:** EMMO ontology integration, JSON schema validation
- **Reusable:** Clear licensing, attribution, comprehensive documentation

### **Interface**
- **Intuitive UI** with guided workflows and progress tracking
- **Robust error handling** that never crashes, always recovers
- **Flexible data import** supporting various CSV formats and encodings
- **Real-time validation** with actionable feedback and suggestions
- **Beautiful visualisations** with automatic plot generation and fallbacks

### **Export Options**
- **YAML metadata** following international standards
- **FAIR bundles** (ZIP) with data, metadata, and documentation
- **Citation files** (CFF) for academic attribution
- **README generation** with usage instructions

## After Download - What Next?

Your FAIR bundle contains everything needed for data sharing and publication:

### 📁 **Bundle Contents**
```
your-experiment-FAIR-bundle.zip
├── data/
│   └── your_original_data.csv      # Original uploaded file
├── metadata/
│   ├── metadata.yaml               # Complete FAIR metadata with compliance scores
│   └── CITATION.cff                # Citation file for dataset attribution
└── documentation/
    └── README.md                   # Experiment documentation and usage guide
```

### 🚀 **Repository Submission**
1. **Upload to Zenodo/Figshare:**
   - Create new upload
   - Drag entire ZIP file
   - Copy metadata from `experiment_metadata.yaml`
   - Publish with DOI

2. **GitHub/GitLab Data Repository:**
   - Extract bundle contents
   - Add your own visualisations to a plots/ or figures/ folder
   - Commit to version control
   - Tag release with version number

### 📝 **Citation Integration**
- **For Papers:** Copy citation from `CITATION.cff`
- **For Data Availability Statements:** Use generated DOI
- **For Methods Sections:** Reference `methodology.md`

### ✅ **Quality Assurance**
Check the fair_compliance section in metadata.yaml for:

- **FAIR Compliance:** All four principles addressed (Findable, Accessible, Interoperable, Reusable)
- **EMMO Integration:** Controlled vocabulary terms and mappings
- **Completeness:** Ensure all required experimental parameters are documented

### 🤝 **Sharing Best Practices**
- Include the entire bundle when sharing data
- Add your own publication-ready plots before repository submission
- Always reference the DOI in publications
- Credit EChem FAIRifier in acknowledgments
- Share feedback for tool improvement

**Questions?** Check our [User Guide](docs/USER_GUIDE.md) or [open an issue](https://github.com/haghighatbin/echem-fairifier/issues).

## Usage Example

### 1. **Upload Data**
```csv
Potential (V),Current (A),Cycle
-0.2,1.2e-6,1
0.0,2.5e-6,1
0.2,5.1e-6,1
...
```

### 2. **Configure Experiment**
- Select technique (e.g., Cyclic Voltammetry)
- Set parameters (scan rate, potential window)
- Add experimental details (electrodes, electrolyte)

### 3. **Generate FAIR Bundle**
- Automated metadata generation with EMMO vocabulary
- Comprehensive validation with FAIR scoring
- Download complete package with documentation

## 🏗️ Architecture

```
EChem FAIRifier/
├──  User Interface (Streamlit)
├──  Core Engine
│   ├── Metadata Generator (FAIR compliance)
│   ├── Validator (Quality assessment) 
│   └── EMMO Integration (Controlled vocabulary)
├──  Configuration (Technique definitions)
└──  Data Processing (Plotting & analysis)
```

## FAIR Compliance Features

### Findable
- **Unique identifiers** (UUID) for each experiment
- **Rich metadata** with technique-specific parameters
- **Controlled vocabularies** using EMMO electrochemistry domain
- **Searchable attributes** with standardised terminology

### Accessible
- **Open formats** (CSV for data, YAML for metadata)
- **Standard protocols** (HTTP download, ZIP packaging)
- **Multiple encodings** support for international data
- **Clear access instructions** in generated documentation

### Interoperable
- **EMMO ontology** integration for semantic interoperability
- **JSON schema** validation for metadata structure
- **Standard vocabularies** for technique parameters
- **Cross-platform** compatibility (Windows, macOS, Linux)

### Reusable
- **Open licensing** options (CC-BY-4.0, MIT, etc.)
- **Complete attribution** with ORCID integration
- **Comprehensive documentation** auto-generated
- **Citation files** (CFF) for academic use

## Scientific Impact

### For Researchers
- **Reduce metadata overhead** - automated generation saves hours
- **Improve reproducibility** - standardised documentation
- **Enable collaboration** - interoperable data formats
- **Accelerate publication** - citation-ready outputs

### For Institutions
- **Meet FAIR requirements** for funding agencies
- **Improve data management** practices
- **Enable data sharing** with confidence
- **Support open science** initiatives

### For the Community
- **Standardise practices** across electrochemistry
- **Enable meta-analyses** with consistent metadata
- **Improve data discovery** through better indexing
- **Accelerate research** through data reuse

## 🤝 Contributing

We welcome contributions from the electrochemistry community! 

### Ways to Contribute
- **🐛 Report bugs** - Help us improve reliability
- **💡 Request features** - Suggest new techniques or capabilities
- **📖 Improve docs** - Make the tool more accessible
- **🔬 Add techniques** - Expand instrument support
- **🧪 Provide test data** - Help validate functionality

### Getting Started
1. Read our [Contributing Guide](docs/CONTRIBUTING.md)
2. Check [open issues](https://github.com/haghighatbin/echem-fairifier/issues)
3. Join discussions in [GitHub Discussions](https://github.com/haghighatbin/echem-fairifier/discussions)

## 📚 Documentation

- **[User Guide](docs/USER_GUIDE.md)** - Complete usage instructions
- **[Contributing](docs/CONTRIBUTING.md)** - How to contribute
- **[API Reference](docs/API_REFERENCE.md)** - Developer documentation
- **[Examples](examples/)** - Sample data and tutorials

## 📈 Roadmap

### Current Version (1.0.0)
- ✅ Core FAIR metadata generation
- ✅ Five major electrochemical techniques
- ✅ EMMO ontology integration
- ✅ Professional web interface

### Planned Features
- 🔄 **Additional techniques** (LSV, NPV, SECM)
- 🔄 **Instrument integration** (Gamry, BioLogic, Zahner)
- 🔄 **API development** for programmatic access
- 🔄 **Batch processing** for multiple files
- 🔄 **Advanced analytics** and quality metrics

## 📖 Citation

If you use EChem FAIRifier in your research, please cite:

Haghighatbin, A. (2025). EChem FAIRifier: Making electrochemical data FAIR-compliant (v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.15737409

### BibTeX

```bibtex
@software{haghighatbin2025echem,
  title = {EChem FAIRifier: Making electrochemical data FAIR-compliant},
  author = {Haghighatbin, Amin},
  year = {2025},
  publisher = {Zenodo},
  version = {v1.0.0},
  doi = {10.5281/zenodo.15737409},
  url = {https://doi.org/10.5281/zenodo.15737409}
}
```

## 💬 Community

- **📧 Contact:** [aminhb@tutanota.com](mailto:aminhb@tutanota.com)
- **💼 LinkedIn:** [Connect with Amin](https://www.linkedin.com/in/amin-haghighatbin/)
- **🐛 Issues:** [GitHub Issues](https://github.com/haghighatbin/echem-fairifier/issues)
- **💡 Discussions:** [GitHub Discussions](https://github.com/haghighatbin/echem-fairifier/discussions)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **EMMO Community** for electrochemistry ontology development
- **Streamlit Team** for the excellent web framework
- **Electrochemistry Community** for feedback and requirements
- **Open Science Movement** for inspiration and standards

---

<div align="center">

**[Try EChem FAIRifier](https://echem-fairifier.up.railway.app)**

*Making electrochemical research more reproducible, one dataset at a time.*

</div>