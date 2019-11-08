from setuptools import setup
from setuptools.command.install import install
import sys

INSTALL_REQUIRES = [
    'matplotlib<3' if sys.version_info.major < 3 else 'matplotlib~=3.1',
    'requests~=2.21',
]


class PostInstallCommand(install):
    # Currently disabled, done on the fly
    """Post-installation for installation mode."""
    """
    def run(self):

        import os
        import matplotlib as mpl
        os.system('cp -r mplhep/stylelib/ ' +
                  os.path.join(mpl.get_configdir() + '/'))
        os.system('cp -r mplhep/fonts/firasans/* ' +
                  os.path.join(mpl.rcParams['datapath'] + '/fonts/ttf/'))
        os.system('cp -r mplhep/fonts/firamath/* ' +
                  os.path.join(mpl.rcParams['datapath'] + '/fonts/ttf/'))
        os.system('cp -r mplhep/fonts/texgyreheros/* ' +
                  os.path.join(mpl.rcParams['datapath'] + '/fonts/ttf/'))
        os.system('rm ' + os.path.join(mpl.get_cachedir() + '/font*'))
        install.run(self)
    """


__version__ = '0.0.12'

setup(
    name='mplhep',
    version=__version__,
    author='andrzejnovak',
    author_email='novak5andrzej@gmail.com',
    license='MIT License',
    description='Matplotlib styles for HEP',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/andrzejnovak/mplhep/",
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*",
    install_requires=INSTALL_REQUIRES,
    # packages=find_packages(exclude=['tests']),
    # cmdclass= {'install': PostInstallCommand}, # Currently disabled
    packages=['mplhep'],
    include_package_data=True)

# To push on pypi
# python setup.py sdist
# twine upload dist/*
