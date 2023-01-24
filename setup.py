from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "PipReleaseDoc.md").read_text()

setup(name="python-mcs-sdk",
      version="0.2.1",
      author="daniel8088",
      author_email="danilew8088@gmail.com",
      install_requires=["web3==5.31.1", "requests==2.28.1", "requests_toolbelt==0.10.1", "tqdm==4.64.1"],
      packages=["mcs", "mcs.api", "mcs.contract", "mcs.contract.abi", "mcs.common", "mcs.upload", "mcs.object"],
      license="MIT",
      include_package_data=True,
      description="A python software development kit for the Multi-Chain Storage",
      long_description=long_description,
      long_description_content_type='text/markdown',
      )
