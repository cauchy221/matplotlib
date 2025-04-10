# Annotation arrows fail or display incorrectly in certain edge cases

## Description
I've encountered several issues with the `Annotation` class in matplotlib when working with certain edge cases:

1. When creating an annotation with empty text, the arrow sometimes points to the wrong location or disappears entirely.

2. When the annotation text has zero size (e.g., `set_size(0)`), the code crashes with a division by zero error instead of handling this case gracefully.

3. When the annotation's `xy` and `xytext` positions are the same, the arrow should either be hidden or drawn with a minimal length, but instead it sometimes appears as a dot or causes rendering artifacts.

4. When using custom `patchA` in `arrowprops`, the arrow sometimes doesn't connect properly to the patch.

5. The calculation of the closest point on the text bbox to the annotated point seems incorrect in some cases, especially when the text is rotated or when the annotated point is equidistant from multiple corners.

These issues make it difficult to create reliable annotations, especially in automated plotting scenarios where the text or positions might be dynamically generated.

## Steps to Reproduce
1. Create an annotation with empty text:
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ann = ax.annotate("", xy=(0.7, 0.7), xytext=(0.2, 0.2),
                 arrowprops=dict(arrowstyle="->"))
fig.canvas.draw()
```

2. Create an annotation with zero size text:
```python
ann = ax.annotate("Test", xy=(0.7, 0.7), xytext=(0.2, 0.2),
                 arrowprops=dict(arrowstyle="->"))
ann.set_size(0)
fig.canvas.draw()  # This crashes
```

3. Create an annotation with same xy and xytext:
```python
ann = ax.annotate("Same Points", xy=(0.5, 0.5), xytext=(0.5, 0.5),
                 arrowprops=dict(arrowstyle="->"))
fig.canvas.draw()  # Arrow appears as a dot or causes artifacts
```

4. Create an annotation with custom patchA:
```python
rect = plt.Rectangle((0.1, 0.1), 0.1, 0.1, fc="0.8")
ann = ax.annotate("Test", xy=(0.7, 0.7), xytext=(0.2, 0.2),
                 arrowprops=dict(arrowstyle="->", patchA=rect))
fig.canvas.draw()  # Arrow doesn't connect properly to the patch
```

## Expected Behavior
1. Annotations with empty text should still display the arrow correctly.
2. Annotations with zero size text should either be handled gracefully or raise a clear error.
3. Annotations with same xy and xytext should either hide the arrow or draw it with a minimal length.
4. Annotations with custom patchA should connect the arrow properly to the patch.
5. The calculation of the closest point on the text bbox should be correct in all cases.

## Actual Behavior
1. Annotations with empty text sometimes display the arrow incorrectly or not at all.
2. Annotations with zero size text crash with a division by zero error.
3. Annotations with same xy and xytext display the arrow as a dot or cause rendering artifacts.
4. Annotations with custom patchA sometimes don't connect the arrow properly to the patch.
5. The calculation of the closest point on the text bbox is incorrect in some cases.

## Environment
- Matplotlib version: 3.7.0
- Python version: 3.9.7
- Operating system: Ubuntu 20.04

## Additional Context
This issue is particularly important for scientific visualization where annotations are used to highlight specific features in plots. The current behavior can lead to misleading visualizations or unexpected errors.

I've attached a test script that demonstrates the issues with visual examples.