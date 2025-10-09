"""
Test for matplotlib version compatibility.

This test verifies that mplhep's dependency on matplotlib._docstring
matches the declared matplotlib version requirement in pyproject.toml.
"""

from __future__ import annotations

try:
    import pytest
except ImportError:
    pytest = None


def test_matplotlib_version_compatibility():
    """
    Test that matplotlib version is compatible with mplhep's requirements.
    
    The package uses matplotlib._docstring which was introduced in matplotlib 3.8.0.
    This test ensures that the installed matplotlib version is compatible.
    """
    import matplotlib
    
    # Get matplotlib version
    version = matplotlib.__version__
    version_parts = version.split('.')
    major = int(version_parts[0])
    minor = int(version_parts[1].split('rc')[0].split('a')[0].split('b')[0]) if len(version_parts) > 1 else 0
    
    # matplotlib._docstring was introduced in 3.8.0
    assert (major, minor) >= (3, 8), (
        f"mplhep requires matplotlib >= 3.8 for _docstring module, "
        f"but found matplotlib {version}. "
        "Please update matplotlib or check pyproject.toml dependencies."
    )


def test_docstring_module_exists():
    """Test that matplotlib._docstring module is available."""
    try:
        from matplotlib import _docstring
        assert hasattr(_docstring, 'copy'), "_docstring module should have 'copy' function"
    except ImportError:
        if pytest:
            pytest.fail("matplotlib._docstring module is not available. This indicates matplotlib < 3.8")
        else:
            raise AssertionError("matplotlib._docstring module is not available. This indicates matplotlib < 3.8")


def test_mplhep_compat_import():
    """Test that mplhep._compat.docstring can be imported."""
    from mplhep._compat import docstring
    assert hasattr(docstring, 'copy'), "docstring should have 'copy' function"


def test_experiment_modules_import():
    """
    Test that all experiment modules can be imported.
    
    These modules depend on docstring.copy from _compat, which depends on
    matplotlib._docstring being available.
    """
    import mplhep
    
    # All experiment modules should be importable
    experiment_modules = ['cms', 'atlas', 'alice', 'lhcb', 'dune']
    
    for mod_name in experiment_modules:
        assert hasattr(mplhep, mod_name), f"mplhep.{mod_name} should be available"
        mod = getattr(mplhep, mod_name)
        assert hasattr(mod, 'label'), f"mplhep.{mod_name}.label should exist"
        assert hasattr(mod, 'text'), f"mplhep.{mod_name}.text should exist"


if __name__ == "__main__":
    # Run tests when executed directly
    test_matplotlib_version_compatibility()
    print("✓ matplotlib version compatibility test passed")
    
    test_docstring_module_exists()
    print("✓ matplotlib._docstring module exists")
    
    test_mplhep_compat_import()
    print("✓ mplhep._compat.docstring import test passed")
    
    test_experiment_modules_import()
    print("✓ experiment modules import test passed")
    
    print("\nAll compatibility tests passed!")
