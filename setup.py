import os
from setuptools import find_packages, setup

# Load the README.md
BASE_DIR = os.path.dirname(__file__)
f = open(os.path.join(BASE_DIR, "README.md"))
readme = f.read()
f.close()

setup(
    name="vinnie",
    version="0.8.2",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=["Click>=7.1,<9.0", "semver==2.13.0", "GitPython==3.1.13"],
    tests_require=["pytest==7.1.3", "pytest-sugar==0.9.5", "pytest-cov==3.0.0"],
    setup_requires=["pytest-runner"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Frank Wiles",
    author_email="frank@revsys.com",
    url="https://github.com/revsys/vinnie/",
    include_package_data=True,
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
