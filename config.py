"""
Configuration file for ArUco marker tracking
Adjust these parameters according to your setup
"""

# ArUco marker parameters
ARUCO_DICT_TYPE = 'DICT_4X4_50'  # Options: DICT_4X4_50, DICT_5X5_100, DICT_6X6_250, etc.
MARKER_SIZE = 0.05  # Marker size in meters (e.g., 0.05 = 5cm)

# Camera calibration parameters
# You should calibrate your camera and update these values
# These are example values - replace with your actual calibration data
CAMERA_MATRIX = [
    [636.295497, 0.000000, 322.817517],
    [0.000000, 636.712497, 255.982381],
    [0.000000, 0.000000, 1.000000],
]
]

DIST_COEFFS = [0.02806658, -0.80382847, 0.00310489, -0.00080338, 1.75826186]

# Output settings
OUTPUT_TRAJECTORY_FILE = 'trajectory_data.csv'
OUTPUT_VIDEO_FILE = 'output_with_3d_coords.mp4'

# Visualization settings
PLOT_3D = True  # Show 3D plot after processing
SAVE_PLOT = True  # Save 3D plot as image
PLOT_OUTPUT_FILE = 'trajectory_3d.png'

# Video processing settings
FRAME_SKIP = 1  # Process every Nth frame (1 = process all frames)
