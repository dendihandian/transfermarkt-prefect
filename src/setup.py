import setuptools

setuptools.setup(
    name="transfermarkt_prefect",
    version="0.0.1",
    author="Dendi Handian",
    description="transfermarkt data pipeline built using prefect.io",
    packages=setuptools.find_packages(),
    package_dir={'': '.'},
)
