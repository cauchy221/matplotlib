import matplotlib.pyplot as plt
import matplotlib.legend as mlegend
import numpy as np
import pytest

def test_figure_legend_empty_axes():
    """Test that Figure.legend works correctly with empty axes list."""
    # Create a figure with no axes
    fig = plt.figure()
    
    # This should not raise an error
    leg = fig.legend()
    
    # The legend should be created but have no entries
    assert len(leg.get_texts()) == 0
    
    plt.close(fig)

def test_figure_legend_duplicate_labels():
    """Test that Figure.legend correctly handles duplicate labels."""
    fig, ax = plt.subplots()
    
    # Create multiple lines with the same label
    line1 = ax.plot([1, 2, 3], label="Same Label")[0]
    line2 = ax.plot([2, 3, 4], label="Same Label")[0]
    line3 = ax.plot([3, 4, 5], label="Different Label")[0]
    
    # Create a legend
    leg = fig.legend()
    
    # The legend should have only 2 entries (one for each unique label)
    assert len(leg.get_texts()) == 2
    
    # Create a legend with explicit handles and labels
    leg2 = fig.legend(handles=[line1, line2, line3])
    
    # This should also have 2 entries
    assert len(leg2.get_texts()) == 2
    
    plt.close(fig)

def test_figure_legend_multiple_legends():
    """Test that Figure.legend correctly handles multiple legends."""
    fig, ax = plt.subplots()
    
    # Create some lines
    line1 = ax.plot([1, 2, 3], label="Line 1")[0]
    line2 = ax.plot([2, 3, 4], label="Line 2")[0]
    
    # Create first legend
    leg1 = fig.legend(handles=[line1], loc="upper left")
    
    # Create second legend
    leg2 = fig.legend(handles=[line2], loc="upper right")
    
    # Both legends should exist
    assert len(fig.legends) == 2
    
    # Remove the first legend
    leg1.remove()
    
    # Only the second legend should remain
    assert len(fig.legends) == 1
    
    plt.close(fig)

def test_figure_legend_non_string_labels():
    """Test that Figure.legend correctly handles non-string labels."""
    fig, ax = plt.subplots()
    
    # Create a line with a non-string label
    line = ax.plot([1, 2, 3], label=123)[0]
    
    # Create a legend
    leg = fig.legend()
    
    # The legend should convert the label to a string
    assert leg.get_texts()[0].get_text() == "123"
    
    plt.close(fig)

def test_figure_legend_transform():
    """Test that Figure.legend correctly handles transforms."""
    fig, ax = plt.subplots()
    
    # Create a line
    line = ax.plot([1, 2, 3], label="Line")[0]
    
    # Create a legend with a custom transform
    from matplotlib.transforms import Affine2D
    custom_transform = Affine2D().scale(0.5, 0.5) + fig.transFigure
    leg = fig.legend(bbox_transform=custom_transform)
    
    # The legend should use the custom transform
    assert leg.get_bbox_to_anchor().get_transform() == custom_transform
    
    plt.close(fig)

def create_test_figure():
    """Create a test figure showing the issue with Figure.legend."""
    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    
    # Create some lines
    line1 = ax1.plot([1, 2, 3], label="Line 1")[0]
    line2 = ax2.plot([3, 2, 1], label="Line 2")[0]
    
    # Create a legend - this will replace any existing legends
    leg1 = fig.legend(handles=[line1], loc="upper left")
    
    # Create another legend - this should add a new legend, not replace the existing one
    leg2 = fig.legend(handles=[line2], loc="upper right")
    
    # Add a title
    fig.suptitle("Figure Legend Bug: Only the last legend is shown")
    
    return fig

if __name__ == "__main__":
    test_figure_legend_empty_axes()
    test_figure_legend_duplicate_labels()
    test_figure_legend_multiple_legends()
    test_figure_legend_non_string_labels()
    test_figure_legend_transform()
    
    fig = create_test_figure()
    plt.show()