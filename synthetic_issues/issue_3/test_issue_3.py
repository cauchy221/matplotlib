import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pytest

def test_scalar_formatter_zero():
    """Test that ScalarFormatter handles zero correctly."""
    formatter = ticker.ScalarFormatter()
    formatter._useMathText = False
    formatter._usetex = False
    
    # Test formatting of zero
    result = formatter.format_data(0)
    assert result == "0", f"Expected '0', got '{result}'"

def test_scalar_formatter_small_values():
    """Test that ScalarFormatter handles very small values correctly."""
    formatter = ticker.ScalarFormatter()
    formatter._useMathText = False
    formatter._usetex = False
    
    # Test formatting of very small values
    small_value = 1e-323  # Close to the smallest representable float
    result = formatter.format_data(small_value)
    assert "e-" in result, f"Expected scientific notation with negative exponent, got '{result}'"

def test_scalar_formatter_integer_significand():
    """Test that ScalarFormatter handles integer significands correctly."""
    formatter = ticker.ScalarFormatter()
    formatter._useMathText = False
    formatter._usetex = False
    
    # Test formatting of values with integer significands
    value = 2000
    result = formatter.format_data(value)
    assert result == "2e3", f"Expected '2e3', got '{result}'"

def test_scalar_formatter_rounding():
    """Test that ScalarFormatter rounds significands correctly."""
    formatter = ticker.ScalarFormatter()
    formatter._useMathText = False
    formatter._usetex = False
    
    # Test rounding of significand
    value = 1.9999999999e5
    result = formatter.format_data(value)
    assert result == "2e5", f"Expected '2e5', got '{result}'"

def test_scalar_formatter_mathtext():
    """Test that ScalarFormatter handles math text formatting correctly."""
    formatter = ticker.ScalarFormatter()
    formatter._useMathText = True
    formatter._usetex = False
    
    # Test special case where significand is 1
    value = 1e5
    result = formatter.format_data(value)
    assert result == "10^{5}", f"Expected '10^{{5}}', got '{result}'"
    
    # Test regular case
    value = 2e5
    result = formatter.format_data(value)
    assert "2 \\times 10^{5}" in result, f"Expected '2 \\times 10^{{5}}', got '{result}'"

def create_test_figure():
    """Create a test figure showing the issue with ScalarFormatter."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Create data with various scales
    x = np.linspace(0, 1, 10)
    y_values = [0, 1, 1e5, 2e5, 1e-10, 1e-300, 1.9999999e5]
    
    # Plot on first axis - expected behavior
    ax1.plot(x, x, label="y = x")
    ax1.set_title("Expected Formatting")
    
    # Add text annotations with expected formatting
    for i, val in enumerate(y_values):
        if i < len(x):
            ax1.annotate(f"Value: {val}", (x[i], 0.1 * i + 0.1))
    
    # Plot on second axis - will show the bug
    ax2.plot(x, x, label="y = x")
    ax2.set_title("Buggy Formatting")
    
    # Add text annotations with buggy formatting
    for i, val in enumerate(y_values):
        if i < len(x):
            ax2.annotate(f"Value: {val}", (x[i], 0.1 * i + 0.1))
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    test_scalar_formatter_zero()
    test_scalar_formatter_small_values()
    test_scalar_formatter_integer_significand()
    test_scalar_formatter_rounding()
    test_scalar_formatter_mathtext()
    fig = create_test_figure()
    plt.show()