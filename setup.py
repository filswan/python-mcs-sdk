from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "PIPRELEASEDOC.md").read_text()

setup(name="python-mcs-sdk",
      version="0.3.2",
      author="daniel8088",
      author_email="danilew8088@gmail.com",
      install_requires=["web3==5.31.1", "requests==2.28.1", "requests_toolbelt==0.10.1", "tqdm==4.64.1"],
      packages=["swan_mcs", "swan_mcs.api", "swan_mcs.contract", "swan_mcs.contract.abi", "swan_mcs.common", "swan_mcs.object"],
      license="MIT",
      include_package_data=True,
      description="A python software development kit for the Multi-Chain Storage",
      long_description=long_description,
      long_description_content_type='text/markdown',
      )
