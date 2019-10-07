from setuptools import setup
from setuptools.command.install import install


class PostInstallCommand(install):
    # Currently disabled, done on the fly
    """Post-installation for installation mode."""
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


__version__ = '0.0.8'

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
    install_requires=['matplotlib>=3.1.0', 'requests>=2.21.0'],
    packages=['mplhep'],
    # cmdclass          = {'install': PostInstallCommand}, # Currently disabled
    include_package_data=True)

# To push on pypi
# python setup.py sdist
# twine upload dist/*
