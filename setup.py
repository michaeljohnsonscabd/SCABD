from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    # Separate dev dependencies
    install_requires = [req for req in requirements if req not in ["pytest>=7.4.0", "pytest-cov>=4.1.0", "pytest-asyncio>=0.21.0", "black>=23.0.0", "flake8>=6.1.0", "mypy>=1.5.0"]]
    extras_require = {
        "dev": ["pytest>=7.4.0", "pytest-cov>=4.1.0", "pytest-asyncio>=0.21.0", "black>=23.0.0", "flake8>=6.1.0", "mypy>=1.5.0"],
    }

setup(
    name="SCABD",
    version="0.1.0",
    author="michaeljohnsonscabd",
    description="SCABD: Strategically Connecting Analyzed Business Data - A unified architecture for business and trading ecosystem",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michaeljohnsonscabd/SCABD",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial",
    ],
    python_requires=">=3.9",
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={
        "console_scripts": [
            "scabd-diagnostics=diagnostics:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
