"""
Setup configuration for Agent-Zero-HCK
Himiko Toga Cognitive Kernel (Advanced) - Multi-Agent Security Research System
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip()
        for line in fh
        if line.strip() and not line.startswith("#") and not line.startswith("-e")
    ]

# Version
VERSION = "0.1.0"

setup(
    name="agent-zero-hck",
    version=VERSION,
    author="CogPy",
    author_email="",
    description="Himiko Toga Cognitive Kernel (Advanced) - Multi-Agent Security Research System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cogpy/agent-zero-hck",
    project_urls={
        "Bug Tracker": "https://github.com/cogpy/agent-zero-hck/issues",
        "Documentation": "https://github.com/cogpy/agent-zero-hck/blob/main/README.md",
        "Source Code": "https://github.com/cogpy/agent-zero-hck",
    },
    packages=find_packages(exclude=["tests", "tests.*", "docs", "docs.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
        ],
        "npu": [
            "llama-cpp-python>=0.2.0",
        ],
        "atomspace": [
            "opencog-atomspace>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "agent-zero-hck=agents.toga_hck.agent:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.yml", "*.md", "*.txt"],
    },
    zip_safe=False,
)
