from setuptools import setup, find_packages

setup(name="python-mcs-sdk",
      version="0.0.9",
      description="A python software development kit for the Multi-Chain Storage",
      author="daniel8088",
      author_email="danilew8088@gmail.com",
      requires=["web3", "requests_toolbelt"],
      packages=["mcs", "mcs.api", "mcs.contract", "mcs.contract.abi", "mcs.common"],
      license="MIT",
      include_package_data=True
      )
