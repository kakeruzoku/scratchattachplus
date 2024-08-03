from setuptools import setup
from scratchattachplus import __version__

with open('README.md', 'r') as fp:
    readme = fp.read()

setup(
    author="kakeruzoku",
    author_email="kakeruzoku@gmail.com",
    maintainer="kakeruzoku",
    maintainer_email="kakeruzoku@gmail.com",
    description="Extending scratchattach. *informal",
    long_description=readme,
    license="MIT License",
    url="https://github.com/kakeruzoku/scratchattachplus",
    version=__version__,
    download_url="https://github.com/kakeruzoku/scratchattachplus",
    install_requires=["scratchattach"],
    packages="scratchattachplus",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)