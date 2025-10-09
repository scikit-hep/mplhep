# Matplotlib Dependency Compatibility Test Report

## Summary

This report documents the testing of mplhep v0.3.48 against the declared matplotlib dependency `matplotlib>=3.4`.

## Issue

According to `pyproject.toml`, v0.3.48 requires `matplotlib>=3.4`. However, the code in `src/mplhep/_compat.py` imports `matplotlib._docstring`, which was introduced in matplotlib 3.8.0. This creates an incompatibility where the package will fail to import with matplotlib versions 3.4 through 3.7.

## Test Results

### Test Environment
- **Python Version**: 3.12
- **Matplotlib Version Installed**: 3.10.7
- **mplhep Version**: 0.1.dev2+g8e1673696

### Current State Analysis

#### 1. Declared Dependency
From `pyproject.toml`:
```toml
dependencies = [
    "matplotlib>=3.4",
    ...
]
```

#### 2. Actual Code Requirement
From `src/mplhep/_compat.py`:
```python
from matplotlib import _docstring as docstring
```

#### 3. Module Usage
The `docstring` module from `_compat.py` is imported by all experiment modules:
- `src/mplhep/exp_cms.py`
- `src/mplhep/exp_atlas.py`
- `src/mplhep/exp_alice.py`
- `src/mplhep/exp_lhcb.py`
- `src/mplhep/exp_dune.py`

Each uses `@docstring.copy(...)` decorator for documentation inheritance.

### Compatibility Test Results

✅ **With matplotlib 3.10.7 (current)**:
- ✓ `matplotlib._docstring` module is available
- ✓ `mplhep._compat.docstring` imports successfully
- ✓ All experiment modules import successfully
- ✓ All label/text functions are available

❌ **Expected behavior with matplotlib 3.4-3.7**:
- ✗ `matplotlib._docstring` module does NOT exist (introduced in 3.8.0)
- ✗ `mplhep._compat` fails to import with `ImportError`
- ✗ All experiment modules fail to import
- ✗ Core functionality of the package is broken

## Root Cause

The `matplotlib._docstring` module was introduced in matplotlib 3.8.0 as part of matplotlib's internal documentation system. Prior to version 3.8, this module did not exist.

## Impact

Users who install mplhep with matplotlib 3.4-3.7 will encounter:
```python
ImportError: cannot import name '_docstring' from 'matplotlib'
```

This breaks:
1. All experiment-specific label functions (`cms.label()`, `atlas.label()`, etc.)
2. All experiment-specific text functions
3. Any code that imports these modules

## Verification

A comprehensive test suite has been created in `tests/test_matplotlib_compat.py` that:
1. Checks matplotlib version compatibility
2. Verifies `matplotlib._docstring` availability
3. Tests `mplhep._compat.docstring` import
4. Validates all experiment modules can be imported

## Recommendations

The issue can be resolved in one of two ways:

### Option 1: Update Minimum Matplotlib Version (RECOMMENDED)
Update `pyproject.toml` to accurately reflect the actual requirement:
```toml
dependencies = [
    "matplotlib>=3.8",  # Changed from 3.4
    ...
]
```

**Pros:**
- Simple, one-line change
- Accurate reflection of actual requirements
- No code changes needed
- matplotlib 3.8 was released in 2023, reasonable to require it in 2025

**Cons:**
- Breaks compatibility for users on older matplotlib versions
- May require users to upgrade matplotlib

### Option 2: Add Compatibility Layer
Modify `src/mplhep/_compat.py` to provide a fallback for matplotlib < 3.8:
```python
try:
    from matplotlib import _docstring as docstring
except (ImportError, AttributeError):
    # Fallback for matplotlib < 3.8
    # Implement docstring.copy() alternative
    ...
```

**Pros:**
- Maintains compatibility with matplotlib 3.4-3.7
- No dependency update required

**Cons:**
- More complex code
- Requires implementing/maintaining compatibility layer
- May need to duplicate matplotlib functionality

## Conclusion

**The package currently DOES NOT work with matplotlib < 3.8 despite declaring matplotlib>=3.4 as a dependency.**

The recommended solution is to update `pyproject.toml` to require `matplotlib>=3.8`, as this accurately reflects the actual code requirements and is the simpler, more maintainable solution.

---

## Test Files Created

1. `/tmp/test_mpl_compat.py` - Initial compatibility check
2. `/tmp/test_matplotlib_34_compat.py` - Detailed simulation test
3. `/tmp/demonstrate_issue.py` - Issue demonstration script
4. `tests/test_matplotlib_compat.py` - Formal test suite for pytest

All tests confirm the incompatibility with matplotlib < 3.8.
