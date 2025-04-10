import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import numpy as np
import pytest
import math

def test_rotate_deg_around_scalar():
    """Test rotate_deg_around with scalar inputs."""
    # Create a transform
    t = mtransforms.Affine2D()
    
    # Apply a rotation around a point
    t.rotate_deg_around(1.0, 2.0, 90.0)
    
    # Test that the transform works correctly
    point = np.array([1.0, 2.0])  # This point should not move
    transformed_point = t.transform_point(point)
    np.testing.assert_allclose(transformed_point, point, atol=1e-10)
    
    # Test another point
    point = np.array([2.0, 2.0])  # This point should move to [1.0, 3.0]
    transformed_point = t.transform_point(point)
    np.testing.assert_allclose(transformed_point, [1.0, 3.0], atol=1e-10)

def test_rotate_deg_around_array():
    """Test rotate_deg_around with array inputs."""
    # Create a transform
    t = mtransforms.Affine2D()
    
    # Apply a rotation around a point defined as a numpy array
    center = np.array([1.0, 2.0])
    t.rotate_deg_around(center[0], center[1], 90.0)
    
    # Test that the transform works correctly
    point = np.array([1.0, 2.0])  # This point should not move
    transformed_point = t.transform_point(point)
    np.testing.assert_allclose(transformed_point, point, atol=1e-10)
    
    # Test another point
    point = np.array([2.0, 2.0])  # This point should move to [1.0, 3.0]
    transformed_point = t.transform_point(point)
    np.testing.assert_allclose(transformed_point, [1.0, 3.0], atol=1e-10)

def test_rotate_deg_around_large_angle():
    """Test rotate_deg_around with large angle values."""
    # Create a transform
    t1 = mtransforms.Affine2D()
    t2 = mtransforms.Affine2D()
    
    # Apply rotations with equivalent angles
    t1.rotate_deg_around(1.0, 2.0, 90.0)
    t2.rotate_deg_around(1.0, 2.0, 450.0)  # 450 = 90 + 360
    
    # Test that both transforms produce the same result
    point = np.array([2.0, 2.0])
    transformed_point1 = t1.transform_point(point)
    transformed_point2 = t2.transform_point(point)
    np.testing.assert_allclose(transformed_point1, transformed_point2, atol=1e-10)

def test_rotate_deg_around_negative_angle():
    """Test rotate_deg_around with negative angle values."""
    # Create a transform
    t1 = mtransforms.Affine2D()
    t2 = mtransforms.Affine2D()
    
    # Apply rotations with equivalent angles
    t1.rotate_deg_around(1.0, 2.0, 90.0)
    t2.rotate_deg_around(1.0, 2.0, -270.0)  # -270 = 90 - 360
    
    # Test that both transforms produce the same result
    point = np.array([2.0, 2.0])
    transformed_point1 = t1.transform_point(point)
    transformed_point2 = t2.transform_point(point)
    np.testing.assert_allclose(transformed_point1, transformed_point2, atol=1e-10)

def test_rotate_deg_around_chained():
    """Test chaining multiple rotate_deg_around calls."""
    # Create a transform
    t = mtransforms.Affine2D()
    
    # Apply multiple rotations
    t.rotate_deg_around(1.0, 2.0, 90.0).rotate_deg_around(3.0, 4.0, 45.0)
    
    # Test that the transform works correctly
    # The exact values aren't important, just that the method returns self
    # and can be chained
    assert isinstance(t, mtransforms.Affine2D)

def create_test_figure():
    """Create a test figure showing the issue with rotate_deg_around."""
    # Create a figure with 2x2 subplots
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    
    # Test case 1: Correct rotation around a point
    ax = axs[0, 0]
    center = (1.0, 1.0)
    t = mtransforms.Affine2D().rotate_deg_around(center[0], center[1], 45.0)
    
    # Draw the center point
    ax.plot(center[0], center[1], 'ro', markersize=10)
    
    # Draw a square before rotation
    square = np.array([[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]])
    ax.plot(square[:, 0], square[:, 1], 'b-', label='Original')
    
    # Draw the square after rotation
    rotated_square = t.transform(square)
    ax.plot(rotated_square[:, 0], rotated_square[:, 1], 'g-', label='Rotated')
    
    ax.set_title('Correct Rotation')
    ax.legend()
    ax.set_aspect('equal')
    ax.grid(True)
    
    # Test case 2: Incorrect rotation (wrong direction)
    ax = axs[0, 1]
    center = (1.0, 1.0)
    
    # Create a transform with the bug (wrong direction)
    t_buggy = mtransforms.Affine2D()
    # Simulate the bug by using a negative angle
    t_buggy.translate(-center[0], -center[1])
    t_buggy.rotate_deg(-45.0)
    t_buggy.translate(center[0], center[1])
    
    # Draw the center point
    ax.plot(center[0], center[1], 'ro', markersize=10)
    
    # Draw a square before rotation
    ax.plot(square[:, 0], square[:, 1], 'b-', label='Original')
    
    # Draw the square after incorrect rotation
    rotated_square_buggy = t_buggy.transform(square)
    ax.plot(rotated_square_buggy[:, 0], rotated_square_buggy[:, 1], 'r-', label='Buggy')
    
    ax.set_title('Incorrect Rotation (Wrong Direction)')
    ax.legend()
    ax.set_aspect('equal')
    ax.grid(True)
    
    # Test case 3: Incorrect rotation (wrong angle)
    ax = axs[1, 0]
    center = (1.0, 1.0)
    
    # Create a transform with the bug (wrong angle)
    t_buggy = mtransforms.Affine2D()
    # Simulate the bug by using radians instead of degrees
    t_buggy.translate(-center[0], -center[1])
    t_buggy.rotate(45.0)  # Using radians instead of degrees
    t_buggy.translate(center[0], center[1])
    
    # Draw the center point
    ax.plot(center[0], center[1], 'ro', markersize=10)
    
    # Draw a square before rotation
    ax.plot(square[:, 0], square[:, 1], 'b-', label='Original')
    
    # Draw the square after incorrect rotation
    rotated_square_buggy = t_buggy.transform(square)
    ax.plot(rotated_square_buggy[:, 0], rotated_square_buggy[:, 1], 'r-', label='Buggy')
    
    ax.set_title('Incorrect Rotation (Wrong Angle)')
    ax.legend()
    ax.set_aspect('equal')
    ax.grid(True)
    
    # Test case 4: Chained rotations
    ax = axs[1, 1]
    center1 = (1.0, 1.0)
    center2 = (0.0, 0.0)
    
    # Create a transform with chained rotations
    t = mtransforms.Affine2D()
    t.rotate_deg_around(center1[0], center1[1], 45.0)
    t.rotate_deg_around(center2[0], center2[1], 45.0)
    
    # Draw the center points
    ax.plot(center1[0], center1[1], 'ro', markersize=10, label='Center 1')
    ax.plot(center2[0], center2[1], 'go', markersize=10, label='Center 2')
    
    # Draw a square before rotation
    ax.plot(square[:, 0], square[:, 1], 'b-', label='Original')
    
    # Draw the square after chained rotations
    rotated_square = t.transform(square)
    ax.plot(rotated_square[:, 0], rotated_square[:, 1], 'g-', label='Rotated')
    
    ax.set_title('Chained Rotations')
    ax.legend()
    ax.set_aspect('equal')
    ax.grid(True)
    
    fig.suptitle('Affine2D.rotate_deg_around Issues', fontsize=16)
    fig.tight_layout()
    
    return fig

if __name__ == "__main__":
    test_rotate_deg_around_scalar()
    test_rotate_deg_around_array()
    test_rotate_deg_around_large_angle()
    test_rotate_deg_around_negative_angle()
    test_rotate_deg_around_chained()
    
    fig = create_test_figure()
    plt.show()