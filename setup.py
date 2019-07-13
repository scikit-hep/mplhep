from setuptools                 import setup
from setuptools.command.install import install

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        
        import os
        import matplotlib as mpl
        os.system('cp -r cmsstyle/stylelib/ '+os.path.join(mpl.get_configdir()+'/'))
        os.system('cp -r cmsstyle/fonts/firasans/* '+os.path.join(mpl.rcParams['datapath']+'/fonts/ttf/'))
        os.system('cp -r cmsstyle/fonts/firamath/* '+os.path.join(mpl.rcParams['datapath']+'/fonts/ttf/'))
        #os.system('cp -r cmsstyle/fonts/firasans/ '+os.path.join(mpl.rcParams['datapath']+'/fonts/ttf/'))
        #os.system('cp -r cmsstyle/fonts/firamath/ '+os.path.join(mpl.rcParams['datapath']+'/fonts/ttf/'))

        install.run(self)

__version__ = '0.0.2'

setup(
    name              = 'cmsstyle',
    version           = __version__,
    author            = 'andrzejnovak',
    author_email      = 'novak5andrzej@gmail.com',
    license           = 'MIT License',
    description       = 'Matplotlib styles for CMS/HEP',
    long_description  = open('README.md').read(),
    long_description_content_type = "text/markdown",
    url               = "https://github.com/andrzejnovak/cmsstyle/",
    install_requires  = ['matplotlib>=2.0.0'],
    packages          = ['cmsstyle'],
    cmdclass          = {'install': PostInstallCommand},
    include_package_data=True
)

# To push on pypi
# python setup.py sdist
# twine upload dist/*