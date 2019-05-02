from setuptools                 import setup
from setuptools.command.install import install

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        
        import os
        import matplotlib as mpl
        os.system('cp -r mplhep/stylelib/ '+os.path.join(mpl.get_configdir()+'/'))
        os.system('cp -r mplhep/fonts/ '+os.path.join(mpl.rcParams['datapath']+'/'))

        install.run(self)

__version__ = '0.1.0'

setup(
    name              = 'mplhep',
    version           = __version__,
    install_requires  = ['matplotlib>=2.0.0'],
    packages          = ['mplhep'],
    cmdclass          = {'install': PostInstallCommand},
    include_package_data=True
)