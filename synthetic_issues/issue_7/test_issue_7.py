import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.contour import ContourSet

def test_contour_with_small_data_range():
    """Test contour with a very small data range."""
    # Create data with a very small range
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.ones_like(X) + 1e-10 * X  # Very small variation
    
    fig, ax = plt.subplots()
    
    # This should not produce NaN levels
    cs = ax.contour(X, Y, Z, 5)
    
    # Check that levels are valid
    assert not np.any(np.isnan(cs.levels))
    assert len(cs.levels) == 5
    assert np.all(np.diff(cs.levels) > 0)
    
    plt.close(fig)

def test_contour_with_duplicate_levels():
    """Test contour with duplicate levels."""
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    Z = X + Y
    
    fig, ax = plt.subplots()
    
    # This should raise an error
    with pytest.raises(ValueError, match="Contour levels must be increasing"):
        cs = ax.contour(X, Y, Z, [1, 1, 1, 2, 3])
    
    plt.close(fig)

def test_contour_with_non_increasing_levels():
    """Test contour with non-increasing levels."""
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    Z = X + Y
    
    fig, ax = plt.subplots()
    
    # This should raise an error
    with pytest.raises(ValueError, match="Contour levels must be increasing"):
        cs = ax.contour(X, Y, Z, [1, 2, 1.5, 3])
    
    plt.close(fig)

def test_filled_contour_with_single_level():
    """Test filled contour with a single level."""
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    Z = X + Y
    
    fig, ax = plt.subplots()
    
    # This should raise an error
    with pytest.raises(ValueError, match="Filled contours require at least 2 levels"):
        cs = ax.contourf(X, Y, Z, [1])
    
    plt.close(fig)

def test_contour_with_nan_data():
    """Test contour with NaN data."""
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    Z = X + Y
    Z[10:20, 10:20] = np.nan  # Add some NaNs
    
    fig, ax = plt.subplots()
    
    # This should not produce NaN levels
    cs = ax.contour(X, Y, Z, 5)
    
    # Check that levels are valid
    assert not np.any(np.isnan(cs.levels))
    assert len(cs.levels) == 5
    assert np.all(np.diff(cs.levels) > 0)
    
    plt.close(fig)

def test_contour_with_all_nan_data():
    """Test contour with all NaN data."""
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.full_like(X, np.nan)  # All NaNs
    
    fig, ax = plt.subplots()
    
    # This should not crash
    cs = ax.contour(X, Y, Z, 5)
    
    # Check that levels are valid (may be empty)
    assert not np.any(np.isnan(cs.levels)) if len(cs.levels) > 0 else True
    
    plt.close(fig)

def test_contour_with_constant_data():
    """Test contour with constant data."""
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.ones_like(X)  # Constant data
    
    fig, ax = plt.subplots()
    
    # This should not crash
    cs = ax.contour(X, Y, Z, 5)
    
    # Check that levels are valid
    assert not np.any(np.isnan(cs.levels))
    
    plt.close(fig)

def create_test_figure():
    """Create a test figure showing the issue with contour levels."""
    # Create a figure with 2x2 subplots
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    
    # Create data with a very small range
    x = np.linspace(0, 1, 100)
    y = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x, y)
    
    # Test case 1: Small data range
    Z1 = np.ones_like(X) + 1e-10 * X  # Very small variation
    cs1 = axs[0, 0].contour(X, Y, Z1, 5)
    axs[0, 0].set_title('Small Data Range')
    fig.colorbar(cs1, ax=axs[0, 0])
    
    # Test case 2: Duplicate levels
    Z2 = X + Y
    try:
        cs2 = axs[0, 1].contour(X, Y, Z2, [0.5, 0.5, 0.5, 1.0, 1.5])
        fig.colorbar(cs2, ax=axs[0, 1])
    except ValueError:
        axs[0, 1].text(0.5, 0.5, 'Error: Duplicate levels',
                     ha='center', va='center', fontsize=12)
    axs[0, 1].set_title('Duplicate Levels')
    
    # Test case 3: Non-increasing levels
    Z3 = X + Y
    try:
        cs3 = axs[1, 0].contour(X, Y, Z3, [0.5, 1.0, 0.8, 1.5])
        fig.colorbar(cs3, ax=axs[1, 0])
    except ValueError:
        axs[1, 0].text(0.5, 0.5, 'Error: Non-increasing levels',
                     ha='center', va='center', fontsize=12)
    axs[1, 0].set_title('Non-increasing Levels')
    
    # Test case 4: Constant data
    Z4 = np.ones_like(X)  # Constant data
    cs4 = axs[1, 1].contour(X, Y, Z4, 5)
    axs[1, 1].set_title('Constant Data')
    fig.colorbar(cs4, ax=axs[1, 1])
    
    fig.suptitle('Contour Level Processing Issues', fontsize=16)
    fig.tight_layout()
    
    return fig

if __name__ == "__main__":
    test_contour_with_small_data_range()
    test_contour_with_duplicate_levels()
    test_contour_with_non_increasing_levels()
    test_filled_contour_with_single_level()
    test_contour_with_nan_data()
    test_contour_with_all_nan_data()
    test_contour_with_constant_data()
    
    fig = create_test_figure()
    plt.show()