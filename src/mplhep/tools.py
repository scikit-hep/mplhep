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
    os.system(f"cp -r {pkg_dir}/stylelib/ " + os.path.join(mpl.get_configdir() + "/"))


@deprecate.deprecate(
    "Hardcoded style sheets and fonts will be deprecated, let us know"
    "if this is affection your workflow"
)
def hardcopy_fonts():
    path = os.path.abspath(__file__)
    pkg_dir = "/" + "/".join(path.split("/")[:-1])
    os.system(
        f"cp -r {pkg_dir}/fonts/firasans/* "
        + os.path.join(mpl.rcParams["datapath"] + "/fonts/ttf/")
    )
    os.system(
        f"cp -r {pkg_dir}/fonts/firamath/* "
        + os.path.join(mpl.rcParams["datapath"] + "/fonts/ttf/")
    )
    os.system(
        f"cp -r {pkg_dir}/fonts/texgyreheros/* "
        + os.path.join(mpl.rcParams["datapath"] + "/fonts/ttf/")
    )
    os.system("rm " + os.path.join(mpl.get_cachedir() + "/font*"))
