# Deployment Guide

## Streamlit Cloud (Recommended)

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repository
5. Set main file path: `src/app.py`
6. Deploy!

## Local Development

```bash
git clone https://github.com/Haghighatbin/echem-fairifier.git
cd echem-fairifier
pip install -r requirements.txt
streamlit run src/app.py