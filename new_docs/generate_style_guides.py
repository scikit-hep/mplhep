#!/usr/bin/env python
"""Generate style-specific guide.md with tabs from template.

This script reads guide_template.md and generates a single guide.md file
with tabs for each experiment style by replacing placeholders.
"""

import argparse
import re
from pathlib import Path
from typing import Dict, List

# Style configurations
STYLES = {
    "Default": {
        "STYLE_NAME": "Default",
        "STYLE_CODE": "",
        "STYLE_USE_CODE": "",
        "LABEL_CODE": "",
        "LABEL_CODE_NODATA": "",
        "LABEL_CODE_DATA": "",
        "LABEL_CODE_AX": "",
        "LABEL_CODE_LUMI": "",
        "MAGIC_CODE": "",
        "MAGIC_CODE_INLINE": "",
        "MAGIC_CODE_INLINE_NESTED": "",
    },
    "plothist": {
        "STYLE_NAME": "plothist",
        "STYLE_CODE": "plothist",
        "STYLE_USE_CODE": "mh.style.use('plothist')",
        "LABEL_CODE": "txt_obj = mh.add_text('plothist', loc='over left')\n    mh.append_text('style', txt_obj, loc='right', fontsize='small')",
        "LABEL_CODE_NODATA": "txt_obj = mh.add_text('plothist', loc='over left')",
        "LABEL_CODE_DATA": "txt_obj = mh.add_text('plothist', loc='over left')",
        "LABEL_CODE_AX": "txt_obj = mh.add_text('plothist', loc='over left', ax=ax_main)",
        "LABEL_CODE_LUMI": "txt_obj = mh.add_text('plothist', loc='over left', ax=ax_main)",
        "MAGIC_CODE": "",
        "MAGIC_CODE_INLINE": "",
        "MAGIC_CODE_INLINE_NESTED": "",
    },
    "CMS": {
        "STYLE_NAME": "CMS",
        "STYLE_CODE": "CMS",
        "STYLE_USE_CODE": "mh.style.use('CMS')",
        "LABEL_CODE": "mh.cms.label('Preliminary', data=True, lumi=100, com=13)",
        "LABEL_CODE_NODATA": "mh.cms.label(data=False)",
        "LABEL_CODE_DATA": "mh.cms.label(data=True)",
        "LABEL_CODE_AX": "mh.cms.label(data=True, ax=ax_main)",
        "LABEL_CODE_LUMI": "mh.cms.label(data=True, lumi=100, ax=ax_main)",
        "MAGIC_CODE": "",
        "MAGIC_CODE_INLINE": "",
        "MAGIC_CODE_INLINE_NESTED": "",
    },
    "ATLAS": {
        "STYLE_NAME": "ATLAS",
        "STYLE_CODE": "ATLAS",
        "STYLE_USE_CODE": "mh.style.use('ATLAS')",
        "LABEL_CODE": "mh.atlas.label('Internal', data=True, lumi=150, com=13)",
        "LABEL_CODE_NODATA": "mh.atlas.label(data=False)",
        "LABEL_CODE_DATA": "mh.atlas.label(data=True)",
        "LABEL_CODE_AX": "mh.atlas.label(data=True, ax=ax_main)",
        "LABEL_CODE_LUMI": "mh.atlas.label(data=True, lumi=150, ax=ax_main)",
        "MAGIC_CODE": "    mh.mpl_magic(soft_fail=True)\n",
        "MAGIC_CODE_INLINE": "\n    mh.mpl_magic(soft_fail=True)",
        "MAGIC_CODE_INLINE_NESTED": "\n        mh.mpl_magic(soft_fail=True)",
    },
    "LHCb": {
        "STYLE_NAME": "LHCb",
        "STYLE_CODE": "LHCb2",
        "STYLE_USE_CODE": "mh.style.use('LHCb2')",
        "LABEL_CODE": "mh.lhcb.label('Preliminary', data=True, lumi=50, com=13)",
        "LABEL_CODE_NODATA": "mh.lhcb.label(data=False)",
        "LABEL_CODE_DATA": "mh.lhcb.label(data=True)",
        "LABEL_CODE_AX": "mh.lhcb.label(data=True, ax=ax_main)",
        "LABEL_CODE_LUMI": "mh.lhcb.label(data=True, lumi=50, ax=ax_main)",
        "MAGIC_CODE": "",
        "MAGIC_CODE_INLINE": "",
        "MAGIC_CODE_INLINE_NESTED": "",
    },
    "ALICE": {
        "STYLE_NAME": "ALICE",
        "STYLE_CODE": "ALICE",
        "STYLE_USE_CODE": "mh.style.use('ALICE')",
        "LABEL_CODE": "mh.alice.label('Preliminary', data=True, lumi=100, com=13)",
        "LABEL_CODE_NODATA": "mh.alice.label(data=False)",
        "LABEL_CODE_DATA": "mh.alice.label(data=True)",
        "LABEL_CODE_AX": "mh.alice.label(data=True, ax=ax_main)",
        "LABEL_CODE_LUMI": "mh.alice.label(data=True, lumi=100, ax=ax_main)",
        "MAGIC_CODE": "    mh.mpl_magic(soft_fail=True)\n",
        "MAGIC_CODE_INLINE": "\n    mh.mpl_magic(soft_fail=True)",
        "MAGIC_CODE_INLINE_NESTED": "\n        mh.mpl_magic(soft_fail=True)",
    },
    "DUNE": {
        "STYLE_NAME": "DUNE",
        "STYLE_CODE": "DUNE",
        "STYLE_USE_CODE": "mh.style.use('DUNE')",
        "LABEL_CODE": "mh.dune.label('Preliminary', data=True, lumi=100, com=13)",
        "LABEL_CODE_NODATA": "mh.dune.label(data=False)",
        "LABEL_CODE_DATA": "mh.dune.label(data=True)",
        "LABEL_CODE_AX": "mh.dune.label(data=True, ax=ax_main)",
        "LABEL_CODE_LUMI": "mh.dune.label(data=True, lumi=100, ax=ax_main)",
        "MAGIC_CODE": "",
        "MAGIC_CODE_INLINE": "",
        "MAGIC_CODE_INLINE_NESTED": "",
    },
}

# Order of styles in tabs
STYLE_ORDER = ["Default", "plothist", "CMS", "ATLAS", "LHCb", "ALICE", "DUNE"]


def replace_placeholders(content: str, replacements: Dict[str, str]) -> str:
    """Replace {{PLACEHOLDER}} style markers with actual values.

    Parameters
    ----------
    content : str
        Content with placeholders
    replacements : dict
        Dictionary mapping placeholder names to replacement values

    Returns
    -------
    str
        Content with placeholders replaced
    """
    result = content
    for placeholder, value in replacements.items():
        result = result.replace(f"{{{{{placeholder}}}}}", value)
    return result


def generate_tab_content(tab_content: str, _style_configs: List[Dict[str, str]]) -> str:
    """Generate tabbed content for all styles.

    Parameters
    ----------
    tab_content : str
        Template content between {{TABS_START}} and {{TABS_END}}
    _style_configs : list
        List of style configuration dicts (unused)

    Returns
    -------
    str
        Generated content with tabs for all styles
    """
    tabs = []

    for style_name in STYLE_ORDER:
        replacements = STYLES[style_name]

        # Replace placeholders in this tab's content
        style_content = replace_placeholders(tab_content, replacements)

        # Replace the {{TAB_HEADER}} with the tab declaration (no leading whitespace)
        style_content = style_content.replace("{{TAB_HEADER}}", f'=== "{style_name}"')

        tabs.append(style_content)

    # Join tabs, ensuring proper spacing between them
    return "\n\n".join(tabs)


def process_template(template: str) -> str:
    """Process template and generate final guide with tabs.

    Parameters
    ----------
    template : str
        Template content with {{TABS_START}}/{{TABS_END}} markers

    Returns
    -------
    str
        Generated guide content with tabs
    """
    # Find all tabbed sections
    pattern = r"{{TABS_START}}(.*?){{TABS_END}}"

    def replace_tabs(match):
        tab_template = match.group(1)
        return generate_tab_content(tab_template, list(STYLES.values()))

    # Replace all tabbed sections
    return re.sub(pattern, replace_tabs, template, flags=re.DOTALL)


def main():
    """Generate style-specific guide with tabs from template."""
    parser = argparse.ArgumentParser(
        description="Generate guide.md with style tabs from template"
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).parent / "docs" / "guide_template.md",
        help="Path to template file (default: docs/guide_template.md)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent / "docs" / "guide.md",
        help="Output file path (default: docs/guide.md)",
    )
    args = parser.parse_args()

    # Read template
    template_path = args.template
    if not template_path.exists():
        msg = f"Template not found: {template_path}"
        raise FileNotFoundError(msg)

    template = template_path.read_text()

    # Generate guide with tabs
    content = process_template(template)

    # Write output
    output_path = args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)


if __name__ == "__main__":
    main()
