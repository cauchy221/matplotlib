# Affine2D.rotate_deg_around method produces incorrect rotations

## Description
I've discovered several issues with the `Affine2D.rotate_deg_around` method in matplotlib's transforms module:

1. When rotating around a point with large or negative angle values, the rotation is sometimes incorrect. The method doesn't properly normalize the angle, leading to unexpected results.

2. When the rotation center is provided as a numpy array or other non-scalar type, the method fails to properly convert the values, leading to incorrect transformations or errors.

3. When chaining multiple `rotate_deg_around` calls, the transformations don't compose correctly, resulting in unexpected final positions.

4. The method sometimes applies the rotation in the wrong direction (clockwise instead of counterclockwise or vice versa) when the angle is processed incorrectly.

5. In some cases, the method seems to use radians instead of degrees for the rotation, resulting in much larger rotations than expected.

These issues make it difficult to create reliable rotations around specific points, which is a common need in many visualization tasks.

## Steps to Reproduce
1. Rotate around a point with a large angle:
```python
import matplotlib.transforms as mtransforms
import numpy as np

t = mtransforms.Affine2D()
t.rotate_deg_around(1.0, 2.0, 450.0)  # Should be equivalent to 90 degrees

# Test with a point
point = np.array([2.0, 2.0])
transformed_point = t.transform_point(point)
print(transformed_point)  # Should be [1.0, 3.0] but isn't
```

2. Rotate around a point defined as a numpy array:
```python
center = np.array([1.0, 2.0])
t = mtransforms.Affine2D()
t.rotate_deg_around(center[0], center[1], 90.0)  # This can fail
```

3. Chain multiple rotations:
```python
t = mtransforms.Affine2D()
t.rotate_deg_around(1.0, 2.0, 90.0).rotate_deg_around(3.0, 4.0, 45.0)
# The result is not the expected composition of the two rotations
```

## Expected Behavior
1. Rotating around a point with any angle value (positive, negative, or larger than 360 degrees) should produce the correct rotation.
2. The method should handle any valid numeric type for the center coordinates, including numpy arrays.
3. Chaining multiple `rotate_deg_around` calls should correctly compose the transformations.
4. The rotation direction should always be consistent (counterclockwise for positive angles).
5. The method should always use degrees, not radians, for the rotation angle.

## Actual Behavior
1. Rotating with large or negative angles sometimes produces incorrect results.
2. Using numpy arrays for the center coordinates can cause errors or incorrect transformations.
3. Chained rotations don't always compose correctly.
4. The rotation direction is sometimes reversed.
5. In some cases, the method seems to use radians instead of degrees.

## Environment
- Matplotlib version: 3.7.0
- Python version: 3.9.7
- Operating system: Ubuntu 20.04

## Additional Context
This issue is particularly important for scientific visualization where precise control over transformations is required. The current behavior can lead to misleading visualizations or unexpected errors.

I've attached a test script that demonstrates the issues with visual examples.