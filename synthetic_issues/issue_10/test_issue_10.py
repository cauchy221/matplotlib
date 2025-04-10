import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.legend import Legend
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.collections import PathCollection

def test_legend_with_empty_handles_and_labels():
    """Test legend with empty handles and labels."""
    fig, ax = plt.subplots()
    
    # Create a legend with empty handles and labels
    with pytest.raises(ValueError):
        legend = Legend(ax, [], [])
        fig.canvas.draw()
    
    plt.close(fig)

def test_legend_with_mismatched_handles_and_labels():
    """Test legend with mismatched handles and labels."""
    fig, ax = plt.subplots()
    
    # Create a legend with mismatched handles and labels
    line = Line2D([0], [0])
    with pytest.raises(ValueError):
        legend = Legend(ax, [line], ["label1", "label2"])
        fig.canvas.draw()
    
    plt.close(fig)

def test_legend_with_none_labels():
    """Test legend with None labels."""
    fig, ax = plt.subplots()
    
    # Create a legend with None labels
    line = Line2D([0], [0])
    with pytest.raises(TypeError):
        legend = Legend(ax, [line], [None])
        fig.canvas.draw()
    
    plt.close(fig)

def test_legend_with_non_string_labels():
    """Test legend with non-string labels."""
    fig, ax = plt.subplots()
    
    # Create a legend with non-string labels
    line = Line2D([0], [0])
    
    # This should convert the object to string, not raise an error
    legend = Legend(ax, [line], [object()])
    fig.canvas.draw()
    
    plt.close(fig)

def test_legend_with_zero_ncols():
    """Test legend with zero ncols."""
    fig, ax = plt.subplots()
    
    # Create a legend with zero ncols
    line = Line2D([0], [0])
    with pytest.raises(ValueError):
        legend = Legend(ax, [line], ["label"], ncols=0)
        fig.canvas.draw()
    
    plt.close(fig)

def test_legend_with_negative_handleheight():
    """Test legend with negative handleheight."""
    fig, ax = plt.subplots()
    
    # Create a legend with negative handleheight
    line = Line2D([0], [0])
    with pytest.raises(ValueError):
        legend = Legend(ax, [line], ["label"], handleheight=-1)
        fig.canvas.draw()
    
    plt.close(fig)

def test_legend_with_no_figure():
    """Test legend with no figure."""
    # Create an axes without a figure
    ax = plt.Axes(Figure(), [0, 0, 1, 1])
    
    # Create a legend with no figure
    line = Line2D([0], [0])
    with pytest.raises(AttributeError):
        legend = Legend(ax, [line], ["label"])
        legend.draw(ax.figure.canvas.get_renderer())
    
def test_legend_with_unsupported_handle():
    """Test legend with unsupported handle."""
    fig, ax = plt.subplots()
    
    # Create a legend with unsupported handle
    with pytest.warns(UserWarning):
        legend = Legend(ax, [object()], ["label"])
        fig.canvas.draw()
    
    plt.close(fig)

def test_legend_with_invalid_alignment():
    """Test legend with invalid alignment."""
    fig, ax = plt.subplots()
    
    # Create a legend with invalid alignment
    line = Line2D([0], [0])
    with pytest.raises(ValueError):
        legend = Legend(ax, [line], ["label"], alignment="invalid")
        fig.canvas.draw()
    
    plt.close(fig)

def create_test_figure():
    """Create a test figure showing the issue with legend initialization."""
    # Create a figure with 2x2 subplots
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    
    # Test case 1: Normal legend
    ax = axs[0, 0]
    x = np.linspace(0, 10, 100)
    ax.plot(x, np.sin(x), label="sin(x)")
    ax.plot(x, np.cos(x), label="cos(x)")
    ax.legend()
    ax.set_title('Normal Legend')
    
    # Test case 2: Legend with empty label
    ax = axs[0, 1]
    ax.plot(x, np.sin(x), label="sin(x)")
    ax.plot(x, np.cos(x), label="")
    ax.legend()
    ax.set_title('Legend with Empty Label')
    
    # Test case 3: Legend with non-string label
    ax = axs[1, 0]
    ax.plot(x, np.sin(x), label=123)  # Non-string label
    ax.plot(x, np.cos(x), label="cos(x)")
    ax.legend()
    ax.set_title('Legend with Non-string Label')
    
    # Test case 4: Legend with multiple columns
    ax = axs[1, 1]
    for i in range(6):
        ax.plot(x, np.sin(x + i), label=f"sin(x+{i})")
    ax.legend(ncols=3)
    ax.set_title('Legend with Multiple Columns')
    
    fig.suptitle('Legend Initialization Issues', fontsize=16)
    fig.tight_layout()
    
    return fig

if __name__ == "__main__":
    test_legend_with_empty_handles_and_labels()
    test_legend_with_mismatched_handles_and_labels()
    test_legend_with_none_labels()
    test_legend_with_non_string_labels()
    test_legend_with_zero_ncols()
    test_legend_with_negative_handleheight()
    test_legend_with_no_figure()
    test_legend_with_unsupported_handle()
    test_legend_with_invalid_alignment()
    
    fig = create_test_figure()
    plt.show()