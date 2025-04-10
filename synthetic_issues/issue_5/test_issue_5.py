import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pytest
from matplotlib.collections import PathCollection
import matplotlib as mpl

def test_legend_elements_with_masked_array():
    """Test that PathCollection.legend_elements handles masked arrays correctly."""
    fig, ax = plt.subplots()
    
    # Create data with masked values
    x = np.arange(10)
    y = np.arange(10)
    c = np.ma.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], mask=[0, 0, 1, 0, 0, 1, 0, 0, 0, 0])
    
    scatter = ax.scatter(x, y, c=c, cmap='viridis')
    
    # This should not raise an error
    handles, labels = scatter.legend_elements()
    
    # Check that we get the expected number of legend elements
    # (should be the number of unique unmasked values)
    assert len(handles) == len(np.unique(c.compressed()))
    
    plt.close(fig)

def test_legend_elements_with_single_value():
    """Test that PathCollection.legend_elements handles arrays with a single unique value."""
    fig, ax = plt.subplots()
    
    # Create data with only one unique value
    x = np.arange(10)
    y = np.arange(10)
    c = np.ones(10) * 5  # All values are 5
    
    scatter = ax.scatter(x, y, c=c, cmap='viridis')
    
    # This should not raise an error
    handles, labels = scatter.legend_elements()
    
    # Check that we get at least one legend element
    assert len(handles) > 0
    
    plt.close(fig)

def test_legend_elements_with_negative_sizes():
    """Test that PathCollection.legend_elements handles negative sizes correctly."""
    fig, ax = plt.subplots()
    
    # Create scatter with some negative sizes (which will be clipped to 0)
    x = np.arange(10)
    y = np.arange(10)
    s = np.array([-10, 0, 10, 20, 30, 40, 50, 60, 70, 80])
    
    scatter = ax.scatter(x, y, s=s)
    
    # This should not raise an error
    handles, labels = scatter.legend_elements(prop="sizes")
    
    # Check that we only get legend elements for non-negative sizes
    assert len(handles) <= len(np.unique(s[s >= 0]))
    
    plt.close(fig)

def test_legend_elements_with_non_monotonic_function():
    """Test that PathCollection.legend_elements handles non-monotonic functions correctly."""
    fig, ax = plt.subplots()
    
    # Create data
    x = np.arange(10)
    y = np.arange(10)
    s = np.arange(1, 11) ** 2  # Square the sizes
    
    scatter = ax.scatter(x, y, s=s)
    
    # Use a non-monotonic function (sine) - this should not cause errors
    # but might produce unexpected results with the buggy implementation
    handles, labels = scatter.legend_elements(prop="sizes", func=np.sin)
    
    # Should still produce some legend elements
    assert len(handles) > 0
    
    plt.close(fig)

def test_legend_elements_with_empty_collection():
    """Test that PathCollection.legend_elements handles empty collections gracefully."""
    fig, ax = plt.subplots()
    
    # Create an empty PathCollection
    empty_collection = PathCollection([])
    
    # This should not raise an error
    handles, labels = empty_collection.legend_elements()
    
    # Should return empty lists
    assert len(handles) == 0
    assert len(labels) == 0
    
    plt.close(fig)

def create_test_figure():
    """Create a test figure showing the issue with PathCollection.legend_elements."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Create data with masked values
    x = np.arange(10)
    y = np.arange(10)
    c = np.ma.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], mask=[0, 0, 1, 0, 0, 1, 0, 0, 0, 0])
    
    # Plot on first axis - expected behavior
    scatter1 = ax1.scatter(x, y, c=c, cmap='viridis')
    handles1, labels1 = scatter1.legend_elements()
    ax1.legend(handles1, labels1, title="Expected Legend")
    ax1.set_title("Expected Behavior")
    
    # Plot on second axis - will show the bug
    scatter2 = ax2.scatter(x, y, c=c, cmap='viridis')
    try:
        handles2, labels2 = scatter2.legend_elements()
        ax2.legend(handles2, labels2, title="Buggy Legend")
    except Exception as e:
        ax2.text(0.5, 0.5, f"Error: {str(e)}", ha='center', va='center', transform=ax2.transAxes)
    ax2.set_title("Buggy Behavior")
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    test_legend_elements_with_masked_array()
    test_legend_elements_with_single_value()
    test_legend_elements_with_negative_sizes()
    test_legend_elements_with_non_monotonic_function()
    test_legend_elements_with_empty_collection()
    fig = create_test_figure()
    plt.show()