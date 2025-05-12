from setuptools import setup, find_packages

setup(
    name="grc-agentic-ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "openai",
        "python-dotenv",
        "requests",
        "beautifulsoup4",
        "langchain",
        "tiktoken",
        "plotly",
        "altair",
        "streamlit-extras",
        "streamlit-option-menu",
        "streamlit-chat",
        "streamlit-ace",
        "streamlit-autorefresh"
    ],
) 