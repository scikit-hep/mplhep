import os
import matplotlib as mpl


# Backup options
def hardcopy_styles():
    path = os.path.abspath(__file__)
    pkg_dir = "/"+"/".join(path.split("/")[:-1])
    os.system('cp -r {}/stylelib/ '.format(pkg_dir) +
              os.path.join(mpl.get_configdir() + '/'))


def hardcopy_fonts():
    path = os.path.abspath(__file__)
    pkg_dir = "/"+"/".join(path.split("/")[:-1])
    os.system('cp -r {}/fonts/firasans/* '.format(pkg_dir) +
              os.path.join(mpl.rcParams['datapath'] + '/fonts/ttf/'))
    os.system('cp -r {}/fonts/firamath/* '.format(pkg_dir) +
              os.path.join(mpl.rcParams['datapath'] + '/fonts/ttf/'))
    os.system('cp -r {}/fonts/texgyreheros/* '.format(pkg_dir) +
              os.path.join(mpl.rcParams['datapath'] + '/fonts/ttf/'))
    os.system('rm ' + os.path.join(mpl.get_cachedir() + '/font*'))
