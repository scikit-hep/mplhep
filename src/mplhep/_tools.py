from __future__ import annotations

import argparse


class Config(argparse.Namespace):
    def clear(self):
        for key, value in dict(self._get_kwargs()).items():
            if isinstance(value, Config):
                value.clear()
            else:
                setattr(self, key, None)
