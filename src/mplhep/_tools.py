import os
import argparse
import matplotlib as mpl
import matplotlib.font_manager as fm


class Config(argparse.Namespace):
    def clear(self):
        for key, value in dict(self._get_kwargs()).items():
            if isinstance(value, Config):
                value.clear()
            else:
                setattr(self, key, None)


class FontLoader:
    """Utility to load fun fonts from https://fonts.google.com/ for matplotlib.
    Find a nice font at https://fonts.google.com/, and then get its corresponding URL
    from https://github.com/google/fonts/
    Use like:
    fl = FontLoader()
    fig, ax = plt.subplots()
    ax.text("Good content.", fontproperties=fl.prop, size=60)

    Adapted from https://github.com/ColCarroll/ridge_map
    """

    def __init__(
        self,
        github_url="https://github.com/google/fonts/blob/master/ofl/cinzel/static/Cinzel-Regular.ttf?raw=true",
        persist=False,
        filename=None,
    ):
        """
        Lazily download a font.
        Parameters
        ----------
        github_url : str
            Can really be any .ttf file, but probably looks like
            "https://github.com/google/fonts/blob/master/ofl/cinzel/Cinzel-Regular.ttf?raw=true"
        """
        self.github_url = github_url
        self._prop = None
        self._persist = persist
        self._filename = filename

    @property
    def prop(self):
        """Get matplotlib.font_manager.FontProperties object that sets the custom font."""
        if self._prop is None:
            if self._persist:
                if self._filename is not None:
                    file_name = self._filename
                else:
                    _file_name = self.github_url.split("/")[-1]
                    if "ttf" in _file_name:
                        file_name = _file_name[: _file_name.find("ttf")] + "ttf"
                    elif "otf" in _file_name:
                        file_name = _file_name[: _file_name.find("otf")] + "otf"
                    else:
                        raise ValueError("Unknown font extension")
                path = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), "fonts/downloaded"
                )
                file_path = os.path.join(path, file_name)
                if os.path.exists(file_path):
                    self._prop = fm.FontProperties(fname=file_path)
                else:
                    import requests

                    r = requests.get(self.github_url, allow_redirects=True)
                    with open(file_path, "wb") as font_file:
                        font_file.write(r.content)
                    self._prop = fm.FontProperties(fname=file_path)
            else:
                from urllib.request import urlopen
                from tempfile import NamedTemporaryFile

                with NamedTemporaryFile(delete=False, suffix=".ttf") as temp_file:
                    temp_file.write(urlopen(self.github_url).read())
                    self._prop = fm.FontProperties(fname=temp_file.name)
        return self._prop
