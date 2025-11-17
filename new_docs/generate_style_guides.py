#!/usr/bin/env python
"""Generate style-specific guide.md with tabs from template.

This script reads guide_template.md and generates a single guide.md file
with tabs for each experiment style by replacing placeholders.
"""

import argparse
import logging
import re
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Style configurations
STYLES = {
    "Default": {
        "STYLE_NAME": "Default",
        "STYLE_CODE": "None",
        "STYLE_USE_CODE": "mh.style.use()",
        "STYLE_DICT": "",
        "STYLE_DICTv2": "{}",
        "LABEL_CODE": "",
        "LABEL_CODE_NODATA": "",
        "LABEL_CODE_DATA": "",
        "LABEL_CODE_AX": "",
        "LABEL_CODE_LUMI": "",
        "LABEL_CODE_LUMI_OPEN": "",
        "LABEL_LOC_0": "# No label function for default style",
        "LABEL_LOC_1": "# No label function for default style",
        "LABEL_LOC_2": "# No label function for default style",
        "LABEL_LOC_3": "# No label function for default style",
        "LABEL_LOC_4": "# No label function for default style",
        "LABEL_COMMON_CONFIG": "# No label function for default style",
        "LABEL_CUSTOM": "# No label function for default style",
        "MAGIC_CODE": "",
        "MAGIC_CODE_INLINE": "",
        "MAGIC_CODE_INLINE_NESTED": "",
    },
    "plothist": {
        "STYLE_NAME": "plothist",
        "STYLE_CODE": "plothist",
        "STYLE_USE_CODE": "mh.style.use('plothist')",
        "STYLE_DICT": "mh.style.plothist",
        "STYLE_DICTv2": "mh.style.plothist",
        "LABEL_CODE": "txt_obj = mh.add_text('plothist', loc='over left')\n    mh.append_text('style', txt_obj, loc='right', fontsize='small')",
        "LABEL_CODE_NODATA": "txt_obj = mh.add_text('plothist', loc='over left')",
        "LABEL_CODE_DATA": "txt_obj = mh.add_text('plothist', loc='over left')",
        "LABEL_CODE_AX": "txt_obj = mh.add_text('plothist', loc='over left', ax=ax_main)",
        "LABEL_CODE_LUMI": "txt_obj = mh.add_text('plothist', loc='over left', ax=ax_main)",
        "LABEL_CODE_LUMI_OPEN": "txt_obj = mh.add_text('plothist', ax=ax)",
        "LABEL_LOC_0": "# No label function for default style",
        "LABEL_LOC_1": "# No label function for default style",
        "LABEL_LOC_2": "# No label function for default style",
        "LABEL_LOC_3": "# No label function for default style",
        "LABEL_LOC_4": "# No label function for default style",
        "LABEL_COMMON_CONFIG": "txt_obj = mh.add_text('plothist', loc='over left', ax=ax)",
        "LABEL_CUSTOM": "txt_obj = mh.add_text('Custom Text', loc='over left', ax=ax)",
        "MAGIC_CODE": "",
        "MAGIC_CODE_INLINE": "",
        "MAGIC_CODE_INLINE_NESTED": "",
    },
    "CMS": {
        "STYLE_NAME": "CMS",
        "STYLE_CODE": "CMS",
        "STYLE_USE_CODE": "mh.style.use('CMS')",
        "STYLE_DICT": "mh.style.CMS",
        "STYLE_DICTv2": "mh.style.CMS",
        "LABEL_CODE": "mh.cms.label('Preliminary', data=True, lumi=100, com=13)",
        "LABEL_CODE_NODATA": "mh.cms.label(data=False)",
        "LABEL_CODE_DATA": "mh.cms.label(data=True)",
        "LABEL_CODE_AX": "mh.cms.label(data=True, ax=ax_main)",
        "LABEL_CODE_LUMI": "mh.cms.label(data=True, lumi=100, ax=ax_main)",
        "LABEL_CODE_LUMI_OPEN": "mh.cms.label(data=True, lumi=100, ax=ax)",
        "LABEL_LOC_0": "mh.cms.label('Preliminary', data=True, lumi=100, ax=ax, loc=0, supp='arXiv:2024.12345')",
        "LABEL_LOC_1": "mh.cms.label('Preliminary', data=True, lumi=100, ax=ax, loc=1, supp='arXiv:2024.12345')",
        "LABEL_LOC_2": "mh.cms.label('Preliminary', data=True, lumi=100, ax=ax, loc=2, supp='arXiv:2024.12345')",
        "LABEL_LOC_3": "mh.cms.label('Preliminary', data=True, lumi=100, ax=ax, loc=3, supp='arXiv:2024.12345')",
        "LABEL_LOC_4": "mh.cms.label('Preliminary', data=True, lumi=100, ax=ax, loc=4, supp='arXiv:2024.12345')",
        "LABEL_COMMON_CONFIG": "mh.cms.label('Preliminary', data=True, year='2023', lumi=137.2, com=13, lumi_format='{0:.1f}', ax=ax)",
        "LABEL_CUSTOM": "mh.cms.label(llabel='Left Label', rlabel='Right Label', ax=ax)",
        "MAGIC_CODE": "",
        "MAGIC_CODE_INLINE": "",
        "MAGIC_CODE_INLINE_NESTED": "",
    },
    "ATLAS": {
        "STYLE_NAME": "ATLAS",
        "STYLE_CODE": "ATLAS",
        "STYLE_USE_CODE": "mh.style.use('ATLAS')",
        "STYLE_DICT": "mh.style.ATLAS",
        "STYLE_DICTv2": "mh.style.ATLAS",
        "LABEL_CODE": "mh.atlas.label('Internal', data=True, lumi=150, com=13)",
        "LABEL_CODE_NODATA": "mh.atlas.label(data=False)",
        "LABEL_CODE_DATA": "mh.atlas.label(data=True)",
        "LABEL_CODE_AX": "mh.atlas.label(data=True, ax=ax_main)",
        "LABEL_CODE_LUMI": "mh.atlas.label(data=True, lumi=150, ax=ax_main)",
        "LABEL_CODE_LUMI_OPEN": "mh.atlas.label(data=True, lumi=150, ax=ax)",
        "LABEL_LOC_0": "mh.atlas.label('Preliminary', data=True, lumi=150, ax=ax, loc=0, supp='arXiv:2024.12345')",
        "LABEL_LOC_1": "mh.atlas.label('Preliminary', data=True, lumi=150, ax=ax, loc=1, supp='arXiv:2024.12345')",
        "LABEL_LOC_2": "mh.atlas.label('Preliminary', data=True, lumi=150, ax=ax, loc=2, supp='arXiv:2024.12345')",
        "LABEL_LOC_3": "mh.atlas.label('Preliminary', data=True, lumi=150, ax=ax, loc=3, supp='arXiv:2024.12345')",
        "LABEL_LOC_4": "mh.atlas.label('Preliminary', data=True, lumi=150, ax=ax, loc=4, supp='arXiv:2024.12345')",
        "LABEL_COMMON_CONFIG": "mh.atlas.label('Preliminary', data=True, year='2023', lumi=150, com=13, lumi_format='{0:.0f}', ax=ax)",
        "LABEL_CUSTOM": "mh.atlas.label(llabel='Left Label', rlabel='Right Label', ax=ax)",
        "MAGIC_CODE": "    mh.mpl_magic(soft_fail=True)\n",
        "MAGIC_CODE_INLINE": "\n    mh.mpl_magic(soft_fail=True)",
        "MAGIC_CODE_INLINE_NESTED": "\n        mh.mpl_magic(soft_fail=True)",
    },
    "LHCb": {
        "STYLE_NAME": "LHCb",
        "STYLE_CODE": "LHCb2",
        "STYLE_USE_CODE": "mh.style.use('LHCb2')",
        "STYLE_DICT": "mh.style.LHCb2",
        "STYLE_DICTv2": "mh.style.LHCb2",
        "LABEL_CODE": "mh.lhcb.label('Preliminary', data=True, lumi=50, com=13)",
        "LABEL_CODE_NODATA": "mh.lhcb.label(data=False)",
        "LABEL_CODE_DATA": "mh.lhcb.label(data=True)",
        "LABEL_CODE_AX": "mh.lhcb.label(data=True, ax=ax_main)",
        "LABEL_CODE_LUMI": "mh.lhcb.label(data=True, lumi=50, ax=ax_main)",
        "LABEL_CODE_LUMI_OPEN": "mh.lhcb.label(data=True, lumi=50, ax=ax)",
        "LABEL_LOC_0": "mh.lhcb.label('Preliminary', data=True, lumi=50, ax=ax, loc=0, supp='arXiv:2024.12345')",
        "LABEL_LOC_1": "mh.lhcb.label('Preliminary', data=True, lumi=50, ax=ax, loc=1, supp='arXiv:2024.12345')",
        "LABEL_LOC_2": "mh.lhcb.label('Preliminary', data=True, lumi=50, ax=ax, loc=2, supp='arXiv:2024.12345')",
        "LABEL_LOC_3": "mh.lhcb.label('Preliminary', data=True, lumi=50, ax=ax, loc=3, supp='arXiv:2024.12345')",
        "LABEL_LOC_4": "mh.lhcb.label('Preliminary', data=True, lumi=50, ax=ax, loc=4, supp='arXiv:2024.12345')",
        "LABEL_COMMON_CONFIG": "mh.lhcb.label('Preliminary', data=True, year='2023', lumi=50, com=13, lumi_format='{0:.0f}', ax=ax)",
        "LABEL_CUSTOM": "mh.lhcb.label(llabel='Left Label', rlabel='Right Label', ax=ax)",
        "MAGIC_CODE": "",
        "MAGIC_CODE_INLINE": "",
        "MAGIC_CODE_INLINE_NESTED": "",
    },
    "ALICE": {
        "STYLE_NAME": "ALICE",
        "STYLE_CODE": "ALICE",
        "STYLE_USE_CODE": "mh.style.use('ALICE')",
        "STYLE_DICT": "mh.style.ALICE",
        "STYLE_DICTv2": "mh.style.ALICE",
        "LABEL_CODE": "mh.alice.label('Preliminary', data=True, lumi=100, com=13)",
        "LABEL_CODE_NODATA": "mh.alice.label(data=False)",
        "LABEL_CODE_DATA": "mh.alice.label(data=True)",
        "LABEL_CODE_AX": "mh.alice.label(data=True, ax=ax_main)",
        "LABEL_CODE_LUMI": "mh.alice.label(data=True, lumi=100, ax=ax_main)",
        "LABEL_CODE_LUMI_OPEN": "mh.alice.label(data=True, lumi=100, ax=ax)",
        "LABEL_LOC_0": "mh.alice.label('Preliminary', data=True, lumi=100, ax=ax, loc=0, supp='arXiv:2024.12345')",
        "LABEL_LOC_1": "mh.alice.label('Preliminary', data=True, lumi=100, ax=ax, loc=1, supp='arXiv:2024.12345')",
        "LABEL_LOC_2": "mh.alice.label('Preliminary', data=True, lumi=100, ax=ax, loc=2, supp='arXiv:2024.12345')",
        "LABEL_LOC_3": "mh.alice.label('Preliminary', data=True, lumi=100, ax=ax, loc=3, supp='arXiv:2024.12345')",
        "LABEL_LOC_4": "mh.alice.label('Preliminary', data=True, lumi=100, ax=ax, loc=4, supp='arXiv:2024.12345')",
        "LABEL_COMMON_CONFIG": "mh.alice.label('Preliminary', data=True, year='2023', lumi=100, com=13, lumi_format='{0:.0f}', ax=ax)",
        "LABEL_CUSTOM": "mh.alice.label(llabel='Left Label', rlabel='Right Label', ax=ax)",
        "MAGIC_CODE": "    mh.mpl_magic(soft_fail=True)\n",
        "MAGIC_CODE_INLINE": "\n    mh.mpl_magic(soft_fail=True)",
        "MAGIC_CODE_INLINE_NESTED": "\n        mh.mpl_magic(soft_fail=True)",
    },
    "DUNE": {
        "STYLE_NAME": "DUNE",
        "STYLE_CODE": "DUNE",
        "STYLE_USE_CODE": "mh.style.use('DUNE')",
        "STYLE_DICT": "mh.style.DUNE",
        "STYLE_DICTv2": "mh.style.DUNE",
        "LABEL_CODE": "mh.dune.label('Preliminary', data=True, lumi=100, com=13)",
        "LABEL_CODE_NODATA": "mh.dune.label(data=False)",
        "LABEL_CODE_DATA": "mh.dune.label(data=True)",
        "LABEL_CODE_AX": "mh.dune.label(data=True, ax=ax_main)",
        "LABEL_CODE_LUMI": "mh.dune.label(data=True, lumi=100, ax=ax_main)",
        "LABEL_CODE_LUMI_OPEN": "mh.dune.label(data=True, lumi=100, ax=ax)",
        "LABEL_LOC_0": "mh.dune.label('Preliminary', data=True, lumi=100, ax=ax, loc=0, supp='arXiv:2024.12345')",
        "LABEL_LOC_1": "mh.dune.label('Preliminary', data=True, lumi=100, ax=ax, loc=1, supp='arXiv:2024.12345')",
        "LABEL_LOC_2": "mh.dune.label('Preliminary', data=True, lumi=100, ax=ax, loc=2, supp='arXiv:2024.12345')",
        "LABEL_LOC_3": "mh.dune.label('Preliminary', data=True, lumi=100, ax=ax, loc=3, supp='arXiv:2024.12345')",
        "LABEL_LOC_4": "mh.dune.label('Preliminary', data=True, lumi=100, ax=ax, loc=4, supp='arXiv:2024.12345')",
        "LABEL_COMMON_CONFIG": "mh.dune.label('Preliminary', data=True, year='2023', lumi=100, lumi_format='{0:.0f}', ax=ax)",
        "LABEL_CUSTOM": "mh.dune.label(llabel='Left Label', rlabel='Right Label', ax=ax)",
        "MAGIC_CODE": "",
        "MAGIC_CODE_INLINE": "",
        "MAGIC_CODE_INLINE_NESTED": "",
    },
}

# Order of styles in tabs
STYLE_ORDER = ["Default", "plothist", "CMS", "ATLAS", "LHCb", "ALICE", "DUNE"]


def replace_placeholders(content: str, replacements: dict[str, str]) -> str:
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


def generate_tab_content(tab_content: str, _style_configs: list[dict[str, str]]) -> str:
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
        description="Generate guide.md files with style tabs from templates"
    )
    parser.add_argument(
        "--template-dir",
        type=Path,
        default=Path(__file__).parent / "docs",
        help="Directory containing template files (default: docs/)",
    )
    args = parser.parse_args()

    template_dir = args.template_dir

    # Define template to output mapping
    templates = {
        "guide_basic_plotting_template.md": "guide_basic_plotting.md",
        "guide_comparisons_template.md": "guide_comparisons.md",
        "guide_styling_template.md": "guide_styling.md",
        "guide_advanced_template.md": "guide_advanced.md",
        "guide_utilities_template.md": "guide_utilities.md",
    }

    # Process each template
    for template_name, output_name in templates.items():
        template_path = template_dir / template_name

        if not template_path.exists():
            logger.warning("Template not found: %s, skipping...", template_path)
            continue

        # Read template
        template = template_path.read_text()

        # Generate guide with tabs
        content = process_template(template)

        # Write output
        output_path = template_dir / output_name
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content)
        logger.info("Generated: %s", output_name)


if __name__ == "__main__":
    main()
