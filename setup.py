from setuptools import setup, find_packages

setup(
    name="newsroom-ai-assistant",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.31.0",
        "google-generativeai>=0.3.0",
        "python-dotenv>=1.0.0",
        "pandas>=2.1.4",
        "nltk>=3.8.1",
        "transformers", 
        "torch", 
        "requests",
        "sentencepiece"
    ],
    author="We-Bee Tech",
    description="AI-powered newsroom assistant using Gemini 2.0",
    keywords="news, AI, journalism, streamlit, gemini",
)
