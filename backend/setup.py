"""Setup configuration for SAP Process Discovery package."""

from setuptools import setup, find_packages

setup(
    name="sap-discovery",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        line.strip()
        for line in open("requirements.txt")
        if line.strip() and not line.startswith("#")
    ],
    python_requires=">=3.10",
    author="Syntax GenAI Assessment",
    description="LangGraph-based SAP business process discovery agent",
    entry_points={
        "console_scripts": [
            "sap-discovery=scripts.run_main_agent:main",
            "sap-test=scripts.test_subagent:main",
        ],
    },
)
