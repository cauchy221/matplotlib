# LineCollection not properly handling empty segments and masked arrays

## Description
I've been working with LineCollection to visualize multiple line segments, and I've encountered some strange behavior when working with empty segments and masked arrays.

1. When I include an empty segment in my list of segments, it gets completely ignored rather than being preserved as an empty path. This is inconsistent with how other collections handle empty data.

2. When using masked arrays for segments, the mask information seems to be lost. The masked points are not properly handled, which causes visual artifacts in my plots.

3. Additionally, I've noticed some precision issues when working with integer data. It seems like the segments aren't being properly converted to float values.

## Steps to Reproduce
1. Create a LineCollection with a mix of regular segments, empty segments, and masked array segments
2. Observe that empty segments are completely dropped
3. Observe that masked points in masked arrays are not properly handled
4. Check the data type of the path vertices for segments created from integer data

## Expected Behavior
1. Empty segments should be preserved as empty Path objects
2. Masked arrays should maintain their mask information, with masked points typically converted to NaN values
3. All segment data should be converted to float for consistent precision

## Actual Behavior
1. Empty segments are completely dropped from the collection
2. Mask information is lost when converting masked arrays to paths
3. Integer data is not properly converted to float, which can cause precision issues

## Environment
- Matplotlib version: 3.7.0
- Python version: 3.9.7
- Operating system: Ubuntu 20.04

## Additional Context
This issue affects any visualization that relies on LineCollection with complex data structures. It's particularly problematic for time series data with gaps (represented by masked arrays) or when working with dynamically generated segments that might occasionally be empty.