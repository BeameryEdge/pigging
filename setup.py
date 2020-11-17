import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pigging",
    version="0.0.1",
    description="Data engineering toolkit to track ETL pipelines and improve cloud connection reliability",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BeameryEdge/pigging",
    author="Sebastian Montero",
    author_email="sebastian.montero@beamery.com",
    packages=setuptools.find_packages(),
    license="Apache Software License",
    python_requires='>=3.6',
    classifiers=[ 
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    install_requires = [
        "google-auth>=1.23.0",
"google-auth-oauthlib>=0.4.2",
"pandas>=1.1.4",
"pandas-gbq>=0.14.1",
"retry>=0.9.2",
    ]
)


