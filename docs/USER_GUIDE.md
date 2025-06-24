# EChem FAIRifier User Guide

Welcome to EChem FAIRifier! This guide will help you make your electrochemical data FAIR-compliant.

## 🎯 What is FAIR Data?

**FAIR** stands for:
- **F**indable: Easy to locate and identify with unique identifiers
- **A**ccessible: Retrievable using standard protocols
- **I**nteroperable: Can be integrated with other data using standard vocabularies
- **R**eusable: Well-documented with clear licensing for replication

## 🚀 Quick Start

### 1. Access the Tool
Visit the [live demo](https://echem-fairifier-aminhb.streamlit.app/) or run locally:

```bash
git clone https://github.com/haghighatbin/echem-fairifier.git
cd echem-fairifier
pip install -r requirements.txt
streamlit run run_app.py
```

### 2. Upload Your Data
- Navigate to the **Data Upload** tab
- Click "Choose your electrochemical data file"
- Upload a CSV file containing your measurements

**Supported formats:**
- CSV files with headers
- Common column names like "Potential (V)", "Current (A)", "Time (s)"

### 3. Configure Metadata
- Navigate to the **Metadata** tab
- Select your electrochemical technique
- Configure technique-specific parameters
- Fill in experimental details

### 4. Export FAIR Bundle
- Navigate to the **Export** tab
- Review the generated metadata
- Download your FAIR bundle (ZIP file)

## 📊 Supported Techniques

### Cyclic Voltammetry (CV)
**Parameters:**
- Scan rate (V/s)
- Start/end potentials (V)
- Step size (V)
- Number of cycles

**Expected data columns:**
- Potential (V)
- Current (A)
- Cycle (optional)

### Differential Pulse Voltammetry (DPV)
**Parameters:**
- Pulse amplitude (V)
- Pulse width (s)
- Step potential (V)
- Scan rate (V/s)

**Expected data columns:**
- Potential (V)
- Current (A)

### Square Wave Voltammetry (SWV)
**Parameters:**
- Frequency (Hz)
- Amplitude (V)
- Step height (V)

**Expected data columns:**
- Potential (V)
- Current (A)
- Forward/Reverse currents (optional)

### Electrochemical Impedance Spectroscopy (EIS)
**Parameters:**
- Frequency range (Hz)
- AC amplitude (V)
- Bias potential (V)
- Equilibration time (s)

**Expected data columns:**
- Frequency (Hz)
- Z_real (Ohm)
- Z_imag (Ohm)
- Phase (deg)

### Chronoamperometry (CA)
**Parameters:**
- Step potentials (V)
- Step times (s)
- Total duration (s)

**Expected data columns:**
- Time (s)
- Current (A)
- Potential (V)

## 📝 Data Preparation

### File Format Requirements
- **Format:** CSV (Comma-Separated Values)
- **Encoding:** UTF-8 (recommended)
- **Headers:** First row should contain column names
- **Data types:** Numeric data for measurements

### Column Naming Conventions
Use descriptive column names with units:

**Good examples:**
- `Potential (V)`
- `Current (A)`
- `Time (s)`
- `Frequency (Hz)`
- `Z_real (Ohm)`

**Avoid:**
- `X`, `Y`, `Data1`
- Missing units
- Special characters or spaces at start/end

### Data Quality Tips
- Remove any header text above column names
- Ensure consistent decimal separators
- Remove empty rows and columns
- Check for missing values
- Verify units are consistent throughout

## 🏷️ Metadata Best Practices

### Required Information
Always provide:
- **Technique name** and parameters
- **Working electrode** material and dimensions
- **Reference electrode** type
- **Counter electrode** material
- **Electrolyte** composition and concentration

### Recommended Information
For better FAIR compliance:
- **Creator name** and ORCID ID
- **Institution** or organisation
- **Contact email** for inquiries
- **Data license** (e.g., CC-BY-4.0)
- **Related publications** (DOI)
- **Experimental conditions** (temperature, atmosphere)

### Attribution Guidelines
- Use full names for researchers
- Include institutional affiliations
- Provide ORCID IDs when available
- Credit funding sources
- Link to related publications

## 🎨 Using the Interface

### Navigation
The app has three main tabs:
1. **📁 Data Upload** - File upload and preview
2. **📝 Metadata** - Configuration and generation
3. **📦 Export** - Review and download

### Progress Tracking
The sidebar shows your progress:
- ✅ Completed steps
- ⏳ Current step
- Progress percentage

### Validation Feedback
The tool provides three types of feedback:
- **❌ Errors** - Must be fixed before export
- **⚠️ Warnings** - Recommendations for improvement
- **ℹ️ Information** - Additional details and suggestions

### FAIR Scoring
The tool calculates:
- **FAIR Compliance Score** (0-100%)
- **Metadata Completeness Score** (0-100%)
- Specific recommendations for improvement

## 📦 Understanding Your FAIR Bundle

### Bundle Contents
Your downloaded ZIP file contains:
- **Original data file** (your CSV)
- **metadata.yaml** - FAIR metadata
- **README.md** - Human-readable description
- **CITATION.cff** - Citation information

### Metadata Structure
The YAML metadata includes:
- **Experiment identification** (unique ID, creation date)
- **Technique information** (parameters, EMMO terms)
- **Experimental setup** (electrodes, electrolyte)
- **Dataset description** (format, columns)
- **FAIR compliance** (findability, accessibility, etc.)
- **Attribution** (creator, institution, contact)

### Using Your FAIR Data

**For immediate use:**
- Extract the ZIP file
- Use the CSV data as normal
- Reference the metadata for experimental details

**For sharing:**
- Upload to data repositories (Zenodo, Figshare)
- Include the full bundle (data + metadata)
- Use the generated citation format

**For publications:**
- Reference the dataset DOI (if uploaded to repository)
- Include experimental parameters from metadata
- Credit collaborators listed in attribution

## 🔍 EMMO Integration

### What is EMMO?
The Elementary Multiperspective Material Ontology (EMMO) provides standardised vocabulary for materials science and electrochemistry.

### Benefits of EMMO Compliance
- **Standardised terminology** for better communication
- **Improved searchability** in databases
- **International compatibility** with other tools
- **Future-proof** data representation

### EMMO Features in EChem FAIRifier
- **Automatic validation** against EMMO vocabulary
- **Terminology suggestions** for better compliance
- **Controlled vocabulary** integration
- **International standard** alignment

## 🔧 Troubleshooting

### Common Issues

**"File upload failed"**
- Check file format is CSV
- Ensure file size is reasonable (<100MB)
- Verify file is not corrupted

**"No expected columns found"**
- Check column names include units
- Use standard naming conventions
- Ensure headers are in first row

**"Validation errors"**
- Fill in required fields (electrodes, electrolyte)
- Check parameter values are reasonable
- Verify data types are correct

**"Low FAIR score"**
- Add creator and institution information
- Specify a data license
- Include more experimental details
- Link to related publications

### Getting Help

**If you encounter problems:**
1. Check this user guide
2. Review error messages carefully
3. Try with example data first
4. Contact support or create an issue

**For technique requests:**
- Use the "New technique support" issue template
- Provide sample data and parameter descriptions
- Include literature references

## 📚 Examples and Templates

### Example Data Files
Sample CSV files are available in the `examples/` directory:
- `cv_ferrocyanide.csv` - Typical CV measurement
- `eis_electrode.csv` - EIS frequency sweep
- `dpv_analyte.csv` - DPV analytical measurement

### Metadata Templates
Common experimental setups:
- **Aqueous electrochemistry** (standard three-electrode cell)
- **Organic solvents** (glove box conditions)
- **Solid-state** (battery materials)
- **Biosensors** (biological applications)

### Best Practice Examples
- **Complete dataset** with full metadata
- **Minimal viable** for quick sharing
- **Publication-ready** for journal submission

## 🌟 Advanced Features

### Batch Processing
For multiple files:
1. Process each file individually
2. Use consistent metadata where possible
3. Maintain naming conventions
4. Consider creating dataset collections

### Integration Workflows
**With Laboratory Information Management Systems (LIMS):**
- Export standard metadata formats
- Use consistent identifiers
- Maintain traceability

**With Data Repositories:**
- Prepare FAIR bundles
- Include comprehensive metadata
- Use recommended file formats

**With Analysis Software:**
- Maintain data provenance
- Document processing steps
- Include analysis parameters

## 📖 Further Reading

### FAIR Data Principles
- [GO FAIR Initiative](https://www.go-fair.org/)
- [FAIR Data Management](https://www.openaire.eu/how-to-make-your-data-fair)

### EMMO Documentation
- [EMMO Website](https://emmo-repo.github.io/)
- [Electrochemistry Domain](https://github.com/emmo-repo/domain-electrochemistry)

### Electrochemistry Standards
- [IUPAC Recommendations](https://iupac.org/what-we-do/periodic-table-of-elements/)
- [International Society of Electrochemistry](https://www.ise-online.org/)

### Data Management
- [Research Data Alliance](https://www.rd-alliance.org/)
- [Digital Object Identifier System](https://www.doi.org/)

---

## 💡 Tips for Success

1. **Start early** - Consider FAIR principles when designing experiments
2. **Be consistent** - Use standard naming and formatting
3. **Document everything** - Include all relevant experimental details
4. **Share responsibly** - Use appropriate licenses and attribution
5. **Stay updated** - Check for new techniques and features

**Remember:** Making data FAIR is an investment in the future of science. Your well-documented data can accelerate research, enable collaborations, and increase the impact of your work.

For questions or suggestions, please [contact us](mailto:aminhb@tutanota.com) or [create an issue](https://github.com/haghighatbin/echem-fairifier/issues).