import json
from setuptools import setup

# Read package.json for version and basic info
with open('package.json') as f:
    package = json.load(f)

# Read README for long description
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

package_name = package["name"].replace(" ", "_").replace("-", "_")

setup(
    name=package_name,
    version=package["version"],
    author="Pip Install Python",
    author_email="pip@pip-install-python.com",
    maintainer="Pip Install Python",
    maintainer_email="pip@pip-install-python.com",
    packages=["dash_email"],
    package_data={
        package_name: [
            "*.js",
            "*.js.map",
            "*.json",
            "*.txt",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    license="MIT",
    description=package.get("description", package_name),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pip-install-python/dash-email",
    project_urls={
        "Bug Reports": "https://github.com/pip-install-python/dash-email/issues",
        "Source": "https://github.com/pip-install-python/dash-email",
        "Documentation": "https://github.com/pip-install-python/dash-email#readme",
        "Changelog": "https://github.com/pip-install-python/dash-email/releases",
    },
    install_requires=[
        "dash>=4.1",
    ],
    extras_require={
        "demo": [
            "dash-mantine-components>=2.8.0",
            "dash-iconify>=0.1.2",
            "google-genai>=1.0.0",
            "resend>=2.0.0",
            "python-dotenv>=1.0.0",
            "pandas>=2.0.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "black",
            "flake8",
        ],
    },
    keywords=[
        "dash",
        "plotly",
        "email",
        "react-email",
        "email-templates",
        "html-email",
        "email-builder",
        "python",
        "components",
        "newsletter",
        "transactional-email",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Dash",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Communications :: Email",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: JavaScript",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Environment :: Web Environment",
    ],
    python_requires=">=3.9",
)