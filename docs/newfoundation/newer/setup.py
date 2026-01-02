from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="irh-phase3-framework",
    version="1.0.0",
    author="IRH Research Team",
    author_email="irh-research@institution.edu",
    description="Computational framework for Intrinsic Resonance Holography Phase 3 implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/IRH-Phase3-Framework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "sympy>=1.9",
        "matplotlib>=3.4.0",
        "h5py>=3.2.0",
        "pandas>=1.3.0",
        "requests>=2.25.0",
        "pytest>=6.2.0",
    ],
    extras_require={
        "hpc": ["numba>=0.55.0"],
        "mpi": ["mpi4py>=3.1.0"],
        "dashboard": ["plotly>=5.0.0", "dash>=2.0.0"],
        "dev": ["pytest>=6.2.0", "black>=21.0", "flake8>=3.9.0"],
    },
    entry_points={
        "console_scripts": [
            "irh-run=IRH_Phase3_Toolkit:main",
            "irh-optimize=scripts.parameter_optimization:main",
            "irh-experiments=scripts.experiment_generator:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)