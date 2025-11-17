"""MkDocs hooks for documentation generation.

This module provides hooks for MkDocs to run before building the documentation.
"""

import contextlib
import subprocess
import sys
from pathlib import Path


def on_pre_build(config):  # noqa: ARG001
    """Run before the build process starts.

    This hook runs the generation scripts to create style-specific
    guide files and the guide overview from templates.

    Parameters
    ----------
    config : MkDocsConfig
        The MkDocs configuration object (unused)
    """
    docs_root = Path(__file__).parent

    # Run the style guides generation script
    style_guides_script = docs_root / "generate_style_guides.py"
    if style_guides_script.exists():
        with contextlib.suppress(subprocess.CalledProcessError):
            subprocess.run(
                [sys.executable, str(style_guides_script)],
                cwd=docs_root,
                capture_output=True,
                text=True,
                check=True,
            )

    # Run the guide overview generation script
    guide_overview_script = docs_root / "generate_guide_overview.py"
    if guide_overview_script.exists():
        with contextlib.suppress(subprocess.CalledProcessError):
            subprocess.run(
                [sys.executable, str(guide_overview_script)],
                cwd=docs_root,
                capture_output=True,
                text=True,
                check=True,
            )
