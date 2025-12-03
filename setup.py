"""
Setup configuration for agent-zero-hck package.
"""

from setuptools import setup, find_packages
import os

# Read the long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="agent-zero-hck",
    version="0.9.7",
    author="Agent Zero Contributors",
    author_email="",
    description="Agent Zero AI framework - Hacking Edition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cogpy/agent-zero-hck",
    project_urls={
        "Bug Tracker": "https://github.com/cogpy/agent-zero-hck/issues",
        "Documentation": "https://github.com/cogpy/agent-zero-hck/docs",
        "Source Code": "https://github.com/cogpy/agent-zero-hck",
    },
    packages=find_packages(exclude=["tests", "tests.*", "docker", "docs"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
            "isort>=5.0",
        ],
        "docs": [
            "sphinx>=5.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "agent-zero=run_ui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml", "*.json"],
    },
    zip_safe=False,
)
