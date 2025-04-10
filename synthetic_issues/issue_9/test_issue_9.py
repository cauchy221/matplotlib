import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.text import Annotation
from matplotlib.transforms import Bbox

def test_annotation_empty_text():
    """Test annotation with empty text."""
    fig, ax = plt.subplots()
    
    # Create an annotation with empty text
    ann = ax.annotate("", xy=(0.5, 0.5), xytext=(0.2, 0.2),
                     arrowprops=dict(arrowstyle="->"))
    
    # This should not raise an error
    fig.canvas.draw()
    
    plt.close(fig)

def test_annotation_with_nan_position():
    """Test annotation with NaN position."""
    fig, ax = plt.subplots()
    
    # Create an annotation with NaN position
    with pytest.raises(ValueError):
        ann = ax.annotate("Test", xy=(np.nan, 0.5), xytext=(0.2, 0.2),
                         arrowprops=dict(arrowstyle="->"))
        fig.canvas.draw()
    
    plt.close(fig)

def test_annotation_with_zero_mutation_scale():
    """Test annotation with zero mutation scale."""
    fig, ax = plt.subplots()
    
    # Create an annotation with zero mutation scale
    with pytest.raises(ValueError):
        ann = ax.annotate("Test", xy=(0.5, 0.5), xytext=(0.2, 0.2),
                         arrowprops=dict(arrowstyle="->", mutation_scale=0))
        fig.canvas.draw()
    
    plt.close(fig)

def test_annotation_with_zero_size_text():
    """Test annotation with zero size text."""
    fig, ax = plt.subplots()
    
    # Create an annotation with zero size text
    ann = ax.annotate("Test", xy=(0.5, 0.5), xytext=(0.2, 0.2),
                     arrowprops=dict(arrowstyle="->"))
    ann.set_size(0)
    
    # This should not raise an error
    with pytest.raises(ValueError):
        fig.canvas.draw()
    
    plt.close(fig)

def test_annotation_with_same_xy_and_xytext():
    """Test annotation with same xy and xytext."""
    fig, ax = plt.subplots()
    
    # Create an annotation with same xy and xytext
    ann = ax.annotate("Test", xy=(0.5, 0.5), xytext=(0.5, 0.5),
                     arrowprops=dict(arrowstyle="->"))
    
    # This should not raise an error
    fig.canvas.draw()
    
    plt.close(fig)

def test_annotation_with_custom_bbox():
    """Test annotation with custom bbox."""
    fig, ax = plt.subplots()
    
    # Create an annotation with custom bbox
    ann = ax.annotate("Test", xy=(0.5, 0.5), xytext=(0.2, 0.2),
                     bbox=dict(boxstyle="round", fc="0.8"),
                     arrowprops=dict(arrowstyle="->"))
    
    # This should not raise an error
    fig.canvas.draw()
    
    plt.close(fig)

def test_annotation_with_custom_patchA():
    """Test annotation with custom patchA."""
    fig, ax = plt.subplots()
    
    # Create a rectangle patch
    rect = plt.Rectangle((0.1, 0.1), 0.1, 0.1, fc="0.8")
    
    # Create an annotation with custom patchA
    ann = ax.annotate("Test", xy=(0.5, 0.5), xytext=(0.2, 0.2),
                     arrowprops=dict(arrowstyle="->", patchA=rect))
    
    # This should not raise an error
    fig.canvas.draw()
    
    plt.close(fig)

def test_annotation_closest_point_calculation():
    """Test annotation closest point calculation."""
    fig, ax = plt.subplots()
    
    # Create an annotation
    ann = ax.annotate("Test", xy=(0.1, 0.1), xytext=(0.5, 0.5),
                     arrowprops=dict(arrowstyle="->"))
    
    # Force update_positions to be called
    fig.canvas.draw()
    
    # Check that _arrow_relpos is set correctly
    assert hasattr(ann, "_arrow_relpos")
    assert len(ann._arrow_relpos) == 2
    assert 0 <= ann._arrow_relpos[0] <= 1
    assert 0 <= ann._arrow_relpos[1] <= 1
    
    plt.close(fig)

def create_test_figure():
    """Create a test figure showing the issue with annotation positioning."""
    # Create a figure with 2x2 subplots
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    
    # Test case 1: Correct annotation
    ax = axs[0, 0]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.annotate("Correct", xy=(0.7, 0.7), xytext=(0.2, 0.2),
               arrowprops=dict(arrowstyle="->"))
    ax.set_title('Correct Annotation')
    
    # Test case 2: Empty text annotation
    ax = axs[0, 1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.annotate("", xy=(0.7, 0.7), xytext=(0.2, 0.2),
               arrowprops=dict(arrowstyle="->"))
    ax.set_title('Empty Text Annotation')
    
    # Test case 3: Same xy and xytext
    ax = axs[1, 0]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.annotate("Same Points", xy=(0.5, 0.5), xytext=(0.5, 0.5),
               arrowprops=dict(arrowstyle="->"))
    ax.set_title('Same xy and xytext')
    
    # Test case 4: Custom bbox
    ax = axs[1, 1]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.annotate("Custom\nBbox", xy=(0.7, 0.7), xytext=(0.2, 0.2),
               bbox=dict(boxstyle="round", fc="0.8"),
               arrowprops=dict(arrowstyle="->"))
    ax.set_title('Custom Bbox')
    
    fig.suptitle('Annotation Positioning Issues', fontsize=16)
    fig.tight_layout()
    
    return fig

if __name__ == "__main__":
    test_annotation_empty_text()
    test_annotation_with_nan_position()
    test_annotation_with_zero_mutation_scale()
    test_annotation_with_zero_size_text()
    test_annotation_with_same_xy_and_xytext()
    test_annotation_with_custom_bbox()
    test_annotation_with_custom_patchA()
    test_annotation_closest_point_calculation()
    
    fig = create_test_figure()
    plt.show()