from setuptools import setup, find_packages

setup(
    name="grc-agentic-ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit==1.45.0",
        "openai==1.12.0",
        "python-dotenv==1.0.1",
        "requests==2.31.0",
        "beautifulsoup4>=4.12.3,<5.0.0",
        "tiktoken==0.5.2",
        "plotly==5.19.0",
        "altair==5.2.0",
        "streamlit-extras==0.6.0",
        "streamlit-option-menu==0.4.0",
        "streamlit-chat==0.1.1",
        "streamlit-ace==0.1.1",
        "streamlit-autorefresh==1.0.1",
        "pypdf"
    ],    
)
