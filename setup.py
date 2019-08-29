from setuptools import setup
from setuptools.command.install import install


class PostInstallCommand(install):
    # Currently disabled, done on the fly
    """Post-installation for installation mode."""
    def run(self):

        import os
        import matplotlib as mpl
        os.system('cp -r hepstyle/stylelib/ ' +
                  os.path.join(mpl.get_configdir() + '/'))
        os.system('cp -r hepstyle/fonts/firasans/* ' +
                  os.path.join(mpl.rcParams['datapath'] + '/fonts/ttf/'))
        os.system('cp -r hepstyle/fonts/firamath/* ' +
                  os.path.join(mpl.rcParams['datapath'] + '/fonts/ttf/'))
        os.system('cp -r hepstyle/fonts/texgyreheros/* ' +
                  os.path.join(mpl.rcParams['datapath'] + '/fonts/ttf/'))
        os.system('rm ' + os.path.join(mpl.get_cachedir() + '/font*'))
        install.run(self)


__version__ = '0.0.4'

setup(
    name='hepstyle',
    version=__version__,
    author='andrzejnovak',
    author_email='novak5andrzej@gmail.com',
    license='MIT License',
    description='Matplotlib styles for HEP',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/andrzejnovak/hepstyle/",
    install_requires=['matplotlib>=3.1.0', 'requests>=2.21.0'],
    packages=['hepstyle'],
    # cmdclass          = {'install': PostInstallCommand}, # Currently disabled
    include_package_data=True)

# To push on pypi
# python setup.py sdist
# twine upload dist/*
