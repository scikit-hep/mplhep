"""MkDocs hooks for documentation generation.

This module provides hooks for MkDocs to run before building the documentation.
"""

import contextlib
import subprocess
import sys
from pathlib import Path


def on_config(config):
    """Run after the configuration is loaded, before the build starts.

    Pins ``pymdownx.snippets``' ``base_path`` to the repository root. The value
    configured in ``mkdocs.yml`` is resolved against the *current working
    directory*, not against the config file, so ``../`` only means "repo root"
    when the build is launched from ``new_docs/`` (as ``noxfile.py`` and the
    docs workflow do). Read the Docs builds from the checkout root with
    ``--config-file new_docs/mkdocs.yml``, where ``../`` escapes the repository
    and every ``--8<--`` snippet silently resolves to nothing, leaving the
    gallery code blocks empty. Rewriting it to an absolute path makes snippet
    resolution independent of where mkdocs is invoked from.

    Parameters
    ----------
    config : MkDocsConfig
        The MkDocs configuration object.

    Returns
    -------
    MkDocsConfig
        The configuration with an absolute snippets ``base_path``.
    """
    repo_root = Path(__file__).parent.parent.resolve()
    snippets = config["mdx_configs"].setdefault("pymdownx.snippets", {})
    snippets["base_path"] = [str(repo_root)]
    return config


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
