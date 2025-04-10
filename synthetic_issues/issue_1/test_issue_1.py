import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pytest

def test_normalize_with_close_bounds():
    """Test that Normalize works correctly with close vmin and vmax values."""
    # Create data with small range
    data = np.linspace(0.1, 0.11, 100)
    
    # Create a Normalize instance with close bounds
    norm = mcolors.Normalize(vmin=0.1, vmax=0.11)
    
    # Normalize the data
    normalized = norm(data)
    
    # Check that the normalized data spans from 0 to 1
    assert np.isclose(normalized[0], 0.0)
    assert np.isclose(normalized[-1], 1.0)
    
    # Check that the normalization is linear (values should be evenly distributed)
    expected = np.linspace(0, 1, 100)
    np.testing.assert_allclose(normalized, expected, rtol=1e-5)
    
    # Test inverse transform
    inverse = norm.inverse(normalized)
    np.testing.assert_allclose(inverse, data, rtol=1e-5)
    
    # Visual test (uncomment for debugging)
    # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    # ax1.plot(data, normalized, 'o-')
    # ax1.set_title('Normalized values')
    # ax2.plot(normalized, inverse, 'o-')
    # ax2.set_title('Inverse transform')
    # plt.tight_layout()
    # plt.show()

def test_colormap_with_close_bounds():
    """Test that colormaps work correctly with close vmin and vmax values."""
    # Create data with small range
    data = np.linspace(0.1, 0.11, 10)
    
    # Create a colormap with close bounds
    cmap = plt.cm.viridis
    norm = mcolors.Normalize(vmin=0.1, vmax=0.11)
    
    # Get colors from the colormap
    colors = cmap(norm(data))
    
    # Check that we get a range of colors, not just 0s and 1s
    # If the normalization is broken, we'd get only two colors
    unique_colors = np.unique(colors, axis=0)
    assert len(unique_colors) > 2, "Colormap should produce a range of colors"
    
    # Check that the first and last colors are different
    assert not np.allclose(colors[0], colors[-1]), "First and last colors should be different"

if __name__ == "__main__":
    test_normalize_with_close_bounds()
    test_colormap_with_close_bounds()
    print("All tests passed!")