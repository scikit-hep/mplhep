# Documentation

The documentation for `mplhep` is built using [MkDocs](https://www.mkdocs.org/) with the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme.

To build the documentation locally, run the following command from the root directory of the repository:

**With MkDocs:**

 Additional requirements for building the docs are listed in `new_docs/requirements_docs.txt` and can be installed via:

```bash
pip install -r new_docs/requirements_docs.txt
```
Then run:

```bash
mkdocs build   # Builds the documentation into the site/ directory
mkdocs serve   # Serves the documentation locally
```

**With Nox:**

```bash
nox -s docs   # Builds the documentation into the site/ directory
nox -s docs -- --fast   # Builds the documentation quickly without rendering code blocks (much faster building time)
nox -s docs -- --serve (--fast)  # Serves the documentation locally
```

## Style-Specific Guide Generation

This directory contains an automated system for generating the documentation files with tabs for each experiment style from a template.

### Overview

Instead of manually maintaining separate guide files for each experiment style or manually maintaining one file with all the tabs, we use a template-based approach:

1. **Template Files**: `docs/*_template.md` contains the contents with tab placeholders ({{TABS_START}}/{{TABS_END}})
2. **Generation Script**: `generate_style_guides.py` expands tabs with style-specific code for each experiment
3. **MkDocs Hook**: `docs_hooks.py` automatically runs the script before each build
4. **Generated Files**: `docs/*.md` without the `_template`, with tabs for CMS, ATLAS, LHCb, ALICE, DUNE, and plothist

### Files

- `docs/*_template.md` - Templates with `{{TABS_START}}/{{TABS_END}}` markers
- `generate_style_guides.py` - Script to generate guide.md with experiment tabs
- `docs_hooks.py` - MkDocs hook that runs the generation script automatically

### How It Works

#### Template Structure

The template uses special markers to denote tabbed sections:

```markdown
{{TABS_START}}
{{TAB_HEADER}}

    ```python
    # mkdocs: render
    import mplhep as mh

    mh.style.use('{{STYLE_CODE}}')
    # ... code ...
    {{LABEL_CODE}}
{{MAGIC_CODE}}    ax.legend()
    ```

{{TABS_END}}
```

This generates tabs for all 6 styles (CMS, ATLAS, LHCb, ALICE, DUNE, plothist).

#### Placeholders

Within tabbed sections, these placeholders get replaced per style:

- `{{STYLE_NAME}}` - Full style name (e.g., "CMS", "ATLAS")
- `{{STYLE_CODE}}` - Style code for `mh.style.use()` (e.g., "CMS", "LHCb2")
- `{{LABEL_CODE}}` - Label code with all parameters
- `{{LABEL_CODE_NODATA}}` - Label code without data parameter
- `{{LABEL_CODE_DATA}}` - Label code with data=True
- `{{LABEL_CODE_AX}}` - Label code with ax parameter
- `{{LABEL_CODE_LUMI}}` - Label code with luminosity
- `{{MAGIC_CODE}}` - mpl_magic() call if needed (ATLAS, ALICE only)

#### Generation Script

Run manually:
```bash
# Generate guide.md with tabs
python generate_style_guides.py

# Custom paths
python generate_style_guides.py --template my_template.md --output my_output/guide.md
```

#### Automatic Generation

The MkDocs hook automatically runs the generation script before every build:

**With MkDocs:**

```bash
mkdocs build   # Guide is generated automatically
mkdocs serve   # Guide is generated on startup
```

**With Nox:**

```bash
nox -s docs   # Guide is generated automatically
nox -s docs -- --serve   # Guide is generated on startup
```

### Making Changes

#### To update the templates:

1. Edit `docs/*_template.md`
2. For content that should be the same across all styles, edit it directly
3. For content that varies by style, use `{{TABS_START}}` ... `{{TABS_END}}` markers
4. Test generation: `python generate_style_guides.py`
5. Build docs via MkDocs or Nox to see changes
6. `docs/*.md` without the `_template` files will be regenerated automatically

#### To add a new style:

1. Add style configuration to `generate_style_guides.py` in the `STYLES` dict
2. Add the style name to `STYLE_ORDER` list
3. Run the generation script

#### To modify style-specific code:

1. Edit the appropriate entry in the `STYLES` dict in `generate_style_guides.py`
2. Regenerate: `python generate_style_guides.py`

### Example Template Usage

```markdown
#### Simple Example

This shows a basic histogram with different styles:

{{TABS_START}}
{{TAB_HEADER}}

    ```python
    # mkdocs: render
    import mplhep as mh

    mh.style.use('{{STYLE_CODE}}')
    # Create plot
    {{LABEL_CODE}}
{{MAGIC_CODE}}    plt.show()
    ```

{{TABS_END}}
```

This generates:

```markdown
=== "CMS"

    ```python
    # mkdocs: render
    import mplhep as mh

    mh.style.use('CMS')
    # Create plot
    mh.cms.label('Preliminary', data=True, lumi=100, com=13)
    plt.show()
    ```

=== "ATLAS"

    ```python
    # mkdocs: render
    import mplhep as mh

    mh.style.use('ATLAS')
    # Create plot
    mh.atlas.label('Internal', data=True, lumi=150, com=13)
    mh.mpl_magic(soft_fail=True)
    plt.show()
    ```

...
```

### Benefits

1. **Single Source of Truth**: Edit one template, update all style tabs
2. **Consistency**: All style tabs have identical structure and examples
3. **Easy Maintenance**: No need to manually sync changes across tabs
4. **Automatic**: Integrated into the build process via MkDocs hook
5. **Flexible**: Easy to add new styles or modify existing ones
6. **Clean**: Template is much simpler than manually maintaining all tabs

### Troubleshooting

#### Guide not updating

Make sure you're editing `docs/*_template.md`.

#### Build errors

Check that all placeholders in the template are defined in the `STYLES` dict in `generate_style_guides.py`.

#### Missing mpl_magic calls

ATLAS and ALICE styles need `mh.mpl_magic(soft_fail=True)` after labels. This is handled automatically via the `MAGIC_CODE` placeholder which includes proper indentation.

#### Testing changes

Always test locally before committing:
```bash
python generate_style_guides.py
mkdocs build / nox -s docs
# Check the generated file
less docs/guide.md
```

#### Manual regeneration

If the hook doesn't run for some reason:
```bash
cd new_docs
python generate_style_guides.py
```
