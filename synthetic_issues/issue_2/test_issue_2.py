import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mcollections
import matplotlib.path as mpath
import pytest
from matplotlib.testing.decorators import image_comparison

def test_empty_segments():
    """Test that LineCollection handles empty segments correctly."""
    # Create a list of segments with an empty segment
    segments = [
        np.array([[0, 0], [1, 1]]),
        np.array([]),  # Empty segment
        np.array([[2, 0], [3, 1]])
    ]
    
    # Create a LineCollection with these segments
    collection = mcollections.LineCollection(segments)
    
    # Check that the collection has the correct number of paths
    # Should have 3 paths, including one for the empty segment
    assert len(collection._paths) == 3, "LineCollection should preserve empty segments"
    
    # Check that the empty segment is represented by a valid Path object
    assert isinstance(collection._paths[1], mpath.Path)
    
    # Check that the empty path has no vertices
    assert len(collection._paths[1].vertices) == 0

def test_masked_array_segments():
    """Test that LineCollection handles masked arrays correctly."""
    # Create a masked array segment
    data = np.array([[0, 0], [1, 1], [2, 2], [3, 3]])
    mask = np.array([False, False, True, False])  # Mask the third point
    masked_segment = np.ma.MaskedArray(data, mask=np.column_stack([mask, mask]))
    
    # Create a LineCollection with this masked segment
    collection = mcollections.LineCollection([masked_segment])
    
    # Check that the mask information is preserved
    # The path should have vertices with NaN values where the mask was True
    path_vertices = collection._paths[0].vertices
    assert np.isnan(path_vertices[2, 0]) or np.isnan(path_vertices[2, 1]), \
        "Masked points should be converted to NaN values"

def test_float_conversion():
    """Test that LineCollection converts segments to float for precision."""
    # Create a segment with integer values
    segment = np.array([[0, 0], [1, 1], [2, 2]], dtype=int)
    
    # Create a LineCollection with this segment
    collection = mcollections.LineCollection([segment])
    
    # Check that the segment was converted to float
    assert collection._paths[0].vertices.dtype == np.float64, \
        "Segment vertices should be converted to float"

def create_test_figure():
    """Create a test figure showing the issue with LineCollection."""
    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # Create data for the first subplot - working case
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    
    # Create line segments
    points1 = np.column_stack([x, y1])
    points2 = np.column_stack([x, y2])
    
    # Create a masked array with some points masked
    mask = np.zeros_like(x, dtype=bool)
    mask[30:40] = True  # Mask some points
    masked_points = np.ma.MaskedArray(
        np.column_stack([x, y1 + 2]), 
        mask=np.column_stack([mask, mask])
    )
    
    # Add an empty segment
    empty_segment = np.array([])
    
    # Create a LineCollection with these segments
    segments = [points1, points2, masked_points, empty_segment]
    lc1 = mcollections.LineCollection(segments, colors=['blue', 'green', 'red', 'black'])
    ax1.add_collection(lc1)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(-3, 3)
    ax1.set_title('Expected Behavior')
    
    # Create the same plot for the second subplot - this will show the bug
    lc2 = mcollections.LineCollection(segments, colors=['blue', 'green', 'red', 'black'])
    ax2.add_collection(lc2)
    ax2.set_xlim(0, 10)
    ax2.set_ylim(-3, 3)
    ax2.set_title('Buggy Behavior')
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    test_empty_segments()
    test_masked_array_segments()
    test_float_conversion()
    fig = create_test_figure()
    plt.show()