# Contributing to EChem FAIRifier

Thank you for your interest in contributing to EChem FAIRifier! This project aims to make electrochemical data more FAIR (Findable, Accessible, Interoperable, Reusable), and we welcome contributions from the electrochemistry community.

## 🎯 Ways to Contribute

### For Electrochemists
- **Report bugs** with data files or metadata generation
- **Request new techniques** that aren't currently supported  
- **Provide sample data** for testing and validation
- **Suggest FAIR improvements** based on your workflow needs
- **Share use cases** and success stories

### For Developers
- **Fix bugs** and improve error handling
- **Add new features** (UI improvements, new techniques, integrations)
- **Improve performance** and code quality
- **Enhance testing** coverage and validation
- **Update documentation** and examples

### For Data Scientists
- **Improve validation logic** and quality metrics
- **Enhance EMMO integration** and vocabulary mapping
- **Add statistical analysis** features
- **Optimize data processing** workflows

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git for version control
- Basic familiarity with electrochemistry (helpful but not required)

### Setting Up Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork:**
   ```bash
   git clone https://github.com/haghighatbin/echem-fairifier.git
   cd echem-fairifier
   ```

3. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install pytest black flake8 mypy  # Development tools
   ```

5. **Verify setup:**
   ```bash
   python test_setup.py
   streamlit run run_app.py
   ```

## 📝 Development Workflow

### Before Making Changes

1. **Create a new branch:**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```

2. **Check existing issues** to avoid duplicate work

3. **Discuss major changes** by opening an issue first

### Making Changes

1. **Follow the code structure:**
   - `src/echem_fairifier/config/` - Technique definitions
   - `src/echem_fairifier/core/` - Core functionality  
   - `src/echem_fairifier/ui/` - Streamlit components
   - `tests/` - Test files

2. **Code style guidelines:**
   - Use [Black](https://black.readthedocs.io/) for formatting: `black src/ tests/`
   - Follow [PEP 8](https://pep8.org/) style guidelines
   - Use type hints where possible
   - Add docstrings for new functions and classes

3. **Testing requirements:**
   - Add tests for new functionality
   - Ensure existing tests pass: `pytest tests/`
   - Test with real electrochemical data files
   - Test the Streamlit UI manually

4. **Documentation:**
   - Update docstrings and comments
   - Add examples for new features
   - Update README if needed

### Quality Checks

Run these before submitting:

```bash
# Code formatting
black src/ tests/ *.py

# Linting
flake8 src/ --max-line-length=127 --extend-ignore=E203,W503

# Type checking (optional but recommended)
mypy src/ --ignore-missing-imports

# Tests
pytest tests/ -v

# Setup validation
python test_setup.py
```

## 🧪 Adding New Techniques

Adding support for a new electrochemical technique involves several steps:

### 1. Define Technique Parameters

Add to `src/echem_fairifier/config/techniques.py`:

```python
"NEW_TECHNIQUE": {
    "parameter_name": TechniqueParameter(
        name="parameter_name",
        default_value=0.1,
        description="Description of the parameter",
        unit="V/s",
        min_value=0.001,
        max_value=10.0
    ),
    # ... more parameters
}
```

### 2. Add Validation Logic

Update `src/echem_fairifier/core/validator.py`:

```python
def _validate_new_technique_parameters(self, params: Dict) -> Dict[str, List[str]]:
    """Validate NEW_TECHNIQUE-specific parameters."""
    results = {"errors": [], "warnings": []}
    
    # Add validation logic
    
    return results
```

### 3. Update Column Patterns

Add expected data columns in `validator.py`:

```python
self.column_patterns = {
    # ... existing techniques
    "NEW_TECHNIQUE": [
        r"[Xx].*[Units]",
        r"[Yy].*[Units]"
    ]
}
```

### 4. Add Plotting Support

Update `src/echem_fairifier/ui/components.py`:

```python
def _create_technique_plot(self, df: pd.DataFrame, technique: str) -> Optional[go.Figure]:
    # ... existing techniques
    elif technique == "NEW_TECHNIQUE":
        # Add plotting logic for new technique
        pass
```

### 5. Add EMMO Integration

Update `src/echem_fairifier/core/emmo_integration.py` with EMMO terms if available.

### 6. Add Tests

Create tests in `tests/test_techniques.py` or similar.

## 🐛 Bug Reports

When reporting bugs, please include:

- **Clear description** of the problem
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Environment information** (OS, Python version, browser)
- **Sample data file** (if the bug involves data processing)
- **Error messages** (full stack trace if applicable)

Use the bug report template when creating issues.

## 💡 Feature Requests

For new features, please:

- **Check existing issues** to avoid duplicates
- **Describe the use case** and benefits
- **Provide examples** of the desired functionality
- **Consider FAIR implications** (how does this improve findability, accessibility, interoperability, or reusability?)
- **Suggest implementation approach** if you have ideas

Use the feature request template when creating issues.

## 📊 FAIR and EMMO Guidelines

When contributing, please consider:

### FAIR Principles
- **Findable:** Does this help users discover and identify data?
- **Accessible:** Does this use open standards and protocols?
- **Interoperable:** Does this work with existing tools and vocabularies?
- **Reusable:** Does this include proper metadata and licensing?

### EMMO Integration
- Use EMMO vocabulary terms when available
- Check [EMMO Electrochemistry Domain](https://github.com/emmo-repo/domain-electrochemistry) for relevant concepts
- Propose new EMMO terms if concepts are missing
- Maintain compatibility with international standards

## 🤝 Community Guidelines

### Code of Conduct
- Be respectful and inclusive
- Welcome newcomers and different perspectives  
- Focus on what's best for the community
- Be patient with questions and learning

### Communication
- Use clear, descriptive commit messages
- Comment your code, especially complex logic
- Be responsive to feedback and suggestions
- Ask questions if something is unclear

### Attribution
- Credit original authors when building on existing work
- Reference relevant papers and standards
- Acknowledge data providers and collaborators

## 📚 Resources

### Electrochemistry
- [IUPAC Electrochemistry Compendium](https://goldbook.iupac.org/)
- [Electrochemical Society Resources](https://www.electrochem.org/)
- [International Society of Electrochemistry](https://www.ise-online.org/)

### FAIR Data
- [FAIR Principles](https://www.go-fair.org/fair-principles/)
- [FAIR Data Management](https://www.openaire.eu/how-to-make-your-data-fair)

### EMMO
- [EMMO Documentation](https://emmo-repo.github.io/)
- [EMMO Electrochemistry Domain](https://github.com/emmo-repo/domain-electrochemistry)

### Technical
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [JSON Schema](https://json-schema.org/)

## 🏆 Recognition

Contributors will be:
- Listed in the CONTRIBUTORS.md file
- Credited in release notes for significant contributions
- Mentioned in related publications (with permission)
- Invited to present work at conferences (when applicable)

## ❓ Questions?

- **General questions:** Open a [Discussion](https://github.com/haghighatbin/echem-fairifier/discussions)
- **Bug reports:** Create an [Issue](https://github.com/haghighatbin/echem-fairifier/issues)
- **Feature requests:** Create an [Issue](https://github.com/haghighatbin/echem-fairifier/issues)
- **Direct contact:** [Email Amin Haghighatbin](mailto:aminhb@tutatnota.com)

Thank you for helping make electrochemical data more FAIR! 🚀