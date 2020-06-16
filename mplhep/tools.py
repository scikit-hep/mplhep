import os
import matplotlib as mpl
import mplhep._deprecate as deprecate


@deprecate.deprecate(
    "Hardcoded style sheets and fonts will be deprecated, let us know"
    "if this is affection your workflow"
)
def hardcopy_styles():
    path = os.path.abspath(__file__)
    pkg_dir = "/" + "/".join(path.split("/")[:-1])
    os.system(
        "cp -r {}/stylelib/ ".format(pkg_dir) + os.path.join(mpl.get_configdir() + "/")
    )


@deprecate.deprecate(
    "Hardcoded style sheets and fonts will be deprecated, let us know"
    "if this is affection your workflow"
)
def hardcopy_fonts():
    path = os.path.abspath(__file__)
    pkg_dir = "/" + "/".join(path.split("/")[:-1])
    os.system(
        "cp -r {}/fonts/firasans/* ".format(pkg_dir)
        + os.path.join(mpl.rcParams["datapath"] + "/fonts/ttf/")
    )
    os.system(
        "cp -r {}/fonts/firamath/* ".format(pkg_dir)
        + os.path.join(mpl.rcParams["datapath"] + "/fonts/ttf/")
    )
    os.system(
        "cp -r {}/fonts/texgyreheros/* ".format(pkg_dir)
        + os.path.join(mpl.rcParams["datapath"] + "/fonts/ttf/")
    )
    os.system("rm " + os.path.join(mpl.get_cachedir() + "/font*"))
