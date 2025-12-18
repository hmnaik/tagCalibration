"""
Generate Checkerboard Pattern for Camera Calibration
Creates a high-quality checkerboard pattern image for printing
"""

import cv2
import numpy as np
import argparse


def generate_checkerboard(width=9, height=6, square_size_mm=25, dpi=300, border_squares=2):
    """
    Generate a checkerboard pattern

    Args:
        width: Number of inner corners horizontally
        height: Number of inner corners vertically
        square_size_mm: Size of each square in millimeters
        dpi: Dots per inch for output image
        border_squares: Number of border squares around the pattern

    Returns:
        checkerboard image
    """
    # Calculate pixels per mm
    pixels_per_mm = dpi / 25.4

    # Calculate square size in pixels
    square_size_px = int(square_size_mm * pixels_per_mm)

    # Total squares (add 1 for checkerboard and borders)
    total_width = width + 1 + (2 * border_squares)
    total_height = height + 1 + (2 * border_squares)

    # Image dimensions
    img_width = total_width * square_size_px
    img_height = total_height * square_size_px

    # Create white image
    checkerboard = np.ones((img_height, img_width), dtype=np.uint8) * 255

    # Draw checkerboard pattern
    for i in range(total_height):
        for j in range(total_width):
            # Determine if square should be black
            if (i + j) % 2 == 0:
                y1 = i * square_size_px
                y2 = (i + 1) * square_size_px
                x1 = j * square_size_px
                x2 = (j + 1) * square_size_px
                checkerboard[y1:y2, x1:x2] = 0

    return checkerboard


def add_labels(image, width, height, square_size_mm, dpi):
    """
    Add labels and information to the checkerboard

    Args:
        image: Checkerboard image
        width, height: Inner corners
        square_size_mm: Square size
        dpi: DPI

    Returns:
        Labeled image
    """
    # Convert to color for labels
    labeled = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # Add white border at top for text
    border_height = 200
    bordered = np.ones((image.shape[0] + border_height, image.shape[1], 3),
                       dtype=np.uint8) * 255
    bordered[border_height:, :] = labeled

    # Add text information
    font = cv2.FONT_HERSHEY_SIMPLEX
    y_pos = 40

    texts = [
        f"Camera Calibration Checkerboard",
        f"Inner Corners: {width} x {height}",
        f"Square Size: {square_size_mm}mm",
        f"Print at: {dpi} DPI (100% scale)",
        f"DO NOT RESIZE - Print at actual size"
    ]

    for i, text in enumerate(texts):
        font_scale = 1.2 if i == 0 else 0.8
        thickness = 3 if i == 0 else 2
        cv2.putText(bordered, text, (20, y_pos + i*35),
                   font, font_scale, (0, 0, 0), thickness)

    return bordered


def main():
    parser = argparse.ArgumentParser(
        description='Generate checkerboard pattern for camera calibration'
    )
    parser.add_argument('--width', type=int, default=9,
                        help='Number of inner corners horizontally (default: 9)')
    parser.add_argument('--height', type=int, default=6,
                        help='Number of inner corners vertically (default: 6)')
    parser.add_argument('--square-size', type=int, default=25,
                        help='Square size in millimeters (default: 25)')
    parser.add_argument('--dpi', type=int, default=300,
                        help='DPI for output image (default: 300)')
    parser.add_argument('--output', type=str, default='checkerboard.png',
                        help='Output filename (default: checkerboard.png)')
    parser.add_argument('--no-labels', action='store_true',
                        help='Do not add labels')

    args = parser.parse_args()

    print("Generating checkerboard pattern...")
    print(f"  Inner corners: {args.width} x {args.height}")
    print(f"  Square size: {args.square_size}mm")
    print(f"  DPI: {args.dpi}")

    # Generate checkerboard
    checkerboard = generate_checkerboard(
        width=args.width,
        height=args.height,
        square_size_mm=args.square_size,
        dpi=args.dpi
    )

    # Add labels
    if not args.no_labels:
        checkerboard = add_labels(
            checkerboard,
            args.width,
            args.height,
            args.square_size,
            args.dpi
        )

    # Save image
    cv2.imwrite(args.output, checkerboard)

    # Calculate physical dimensions
    total_width_mm = (args.width + 1) * args.square_size
    total_height_mm = (args.height + 1) * args.square_size

    print(f"\n[OK] Checkerboard saved to: {args.output}")
    print(f"\nPhysical dimensions:")
    print(f"  Width: {total_width_mm}mm ({total_width_mm/10:.1f}cm)")
    print(f"  Height: {total_height_mm}mm ({total_height_mm/10:.1f}cm)")
    print(f"\nPrinting instructions:")
    print(f"  1. Print at {args.dpi} DPI")
    print(f"  2. Use 'Actual Size' or '100% scale' in print settings")
    print(f"  3. DO NOT use 'Fit to Page'")
    print(f"  4. Print on rigid, flat paper")
    print(f"  5. Measure a square to verify size: {args.square_size}mm")
    print(f"\nRecommended:")
    print(f"  - Use high-quality printer")
    print(f"  - Print on thick paper or cardstock")
    print(f"  - Mount on rigid board (foam board, cardboard)")
    print(f"  - Ensure pattern is perfectly flat")


if __name__ == '__main__':
    main()
