# ScalarFormatter fails to properly format certain numeric values

## Description
I've discovered several issues with the `ScalarFormatter.format_data` method that cause incorrect formatting for certain numeric values:

1. When formatting zero (0), the formatter raises a math domain error because it tries to compute `log10(0)`.

2. Very small values (close to the floating-point limit) cause overflow errors or incorrect formatting.

3. The significand rounding is inconsistent, sometimes causing precision loss or incorrect display.

4. When using math text formatting, the special case for when the significand equals 1 (which should display just "10^{n}" without the "1 ×") doesn't work correctly.

5. Integer significands sometimes display unnecessary decimal points.

These issues affect data cursor readouts, annotations, and any other feature that uses the formatter's `format_data` method.

## Steps to Reproduce
1. Create a ScalarFormatter instance
2. Try to format various edge cases:
   - Zero: `formatter.format_data(0)`
   - Very small values: `formatter.format_data(1e-323)`
   - Values with integer significands: `formatter.format_data(2000)`
   - Values that should round to integer significands: `formatter.format_data(1.9999999999e5)`
   - Values with significand = 1 when using math text: `formatter.format_data(1e5)` with `_useMathText=True`

## Expected Behavior
1. Zero should format as "0" without errors
2. Very small values should format with appropriate scientific notation
3. Significands should be rounded consistently to an appropriate precision
4. When significand = 1 and using math text, only "10^{n}" should be displayed (not "1 × 10^{n}")
5. Integer significands should not show decimal points

## Actual Behavior
1. Formatting zero raises a math domain error
2. Very small values cause overflow errors or incorrect formatting
3. Significand rounding is inconsistent
4. With math text, "1 × 10^{n}" is always displayed even when significand = 1
5. Integer significands sometimes show unnecessary decimal points

## Environment
- Matplotlib version: 3.7.0
- Python version: 3.9.7
- Operating system: macOS 12.6

## Additional Context
This issue affects data exploration workflows where precise numeric formatting is important, especially when working with data that spans multiple orders of magnitude or includes very small values.