import os
from setuptools import setup

# Load the README.md
BASE_DIR = os.path.dirname(__file__)
f = open(os.path.join(BASE_DIR, "README.md"))
readme = f.read()
f.close()

setup(
    name="vinnie",
    version="0.5.0",
    py_modules=["vinnie"],
    install_requires=["Click==7.0", "semver==2.8.1", "GitPython==2.1.11"],
    tests_require=["pytest==5.0.1", "pytest-sugar==0.9.2", "pytest-cov==2.7.1"],
    entry_points="""
        [console_scripts]
        vinnie=vinnie.cli:cli
    """,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
        "Topic :: System :: Systems Administration",
    ],
)
