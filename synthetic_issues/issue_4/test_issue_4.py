import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pytest

def test_twoslope_norm_center_value():
    """Test that TwoSlopeNorm correctly handles values exactly at vcenter."""
    norm = mcolors.TwoSlopeNorm(vcenter=0, vmin=-10, vmax=10)
    
    # Test single value at center
    result = norm(0)
    assert result == 0.5, f"Expected 0.5 for center value, got {result}"
    
    # Test array with center value
    result_array = norm(np.array([-10, -5, 0, 5, 10]))
    expected = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
    np.testing.assert_allclose(result_array, expected, rtol=1e-5)

def test_twoslope_norm_extreme_ranges():
    """Test that TwoSlopeNorm correctly handles very different scales on each side."""
    # Very different scales: -1 to 0 and 0 to 1000
    norm = mcolors.TwoSlopeNorm(vcenter=0, vmin=-1, vmax=1000)
    
    # Test values in both ranges
    result = norm(np.array([-1, -0.5, 0, 500, 1000]))
    expected = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
    np.testing.assert_allclose(result, expected, rtol=1e-5)
    
    # Test with reversed extreme ranges: -1000 to 0 and 0 to 1
    norm = mcolors.TwoSlopeNorm(vcenter=0, vmin=-1000, vmax=1)
    
    # Test values in both ranges
    result = norm(np.array([-1000, -500, 0, 0.5, 1]))
    expected = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
    np.testing.assert_allclose(result, expected, rtol=1e-5)

def test_twoslope_norm_masked_values():
    """Test that TwoSlopeNorm correctly handles masked arrays."""
    norm = mcolors.TwoSlopeNorm(vcenter=0, vmin=-10, vmax=10)
    
    # Create masked array with some masked values
    data = np.ma.array([-10, -5, 0, 5, 10], mask=[False, True, False, False, True])
    result = norm(data)
    
    # Check that mask is preserved
    assert np.array_equal(result.mask, data.mask), "Mask was not preserved"
    
    # Check values
    expected = np.ma.array([0.0, 0.25, 0.5, 0.75, 1.0], mask=[False, True, False, False, True])
    np.testing.assert_allclose(result.compressed(), expected.compressed(), rtol=1e-5)

def create_test_figure():
    """Create a test figure showing the issue with TwoSlopeNorm."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Create data with extreme ranges
    x = np.linspace(-1, 1, 100)
    y = np.linspace(-1, 1, 100)
    X, Y = np.meshgrid(x, y)
    Z1 = X + Y  # Values range from -2 to 2
    
    # Create extreme range data
    Z2 = np.zeros_like(Z1)
    Z2[Z1 < 0] = Z1[Z1 < 0] * 0.01  # Small negative range
    Z2[Z1 >= 0] = Z1[Z1 >= 0] * 100  # Large positive range
    
    # Plot with correct normalization
    pcm1 = ax1.pcolormesh(X, Y, Z1, cmap='coolwarm', 
                         norm=mcolors.TwoSlopeNorm(vcenter=0, vmin=-2, vmax=2))
    fig.colorbar(pcm1, ax=ax1)
    ax1.set_title('Expected TwoSlopeNorm Behavior')
    
    # Plot with buggy normalization (will show the issue)
    pcm2 = ax2.pcolormesh(X, Y, Z2, cmap='coolwarm',
                         norm=mcolors.TwoSlopeNorm(vcenter=0, vmin=-0.02, vmax=200))
    fig.colorbar(pcm2, ax=ax2)
    ax2.set_title('Buggy TwoSlopeNorm Behavior')
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    test_twoslope_norm_center_value()
    test_twoslope_norm_extreme_ranges()
    test_twoslope_norm_masked_values()
    fig = create_test_figure()
    plt.show()