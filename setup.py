from setuptools import setup, find_packages

setup(name="python-mcs-sdk",
      version="0.2.0",
      description="A python software development kit for the Multi-Chain Storage",
      author="daniel8088",
      author_email="danilew8088@gmail.com",
      install_requires=["web3==5.31.1", "requests==2.28.1", "requests_toolbelt==0.10.1", "tqdm==4.64.1"],
      packages=["mcs", "mcs.api", "mcs.contract", "mcs.contract.abi", "mcs.common", "mcs.upload"],
      license="MIT",
      include_package_data=True
      )
