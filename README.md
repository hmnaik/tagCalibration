# ArUco Marker 3D Trajectory Tracker

A Python application for detecting and tracking ArUco markers in 3D space from video files. The application estimates the 3D pose of ArUco markers, tracks their trajectory over time, and provides visualization tools for both the trajectory data and video overlay.

## Features

- **3D Pose Estimation**: Detect ArUco markers and estimate their 3D position and orientation
- **Trajectory Tracking**: Track marker movement through 3D space over time
- **Live Camera Tracking**: Real-time ArUco detection and tracking from webcam (NEW!)
- **Data Export**: Save trajectory data to CSV format
- **3D Visualization**: Generate interactive 3D plots of marker trajectories
- **3D Animation Videos**: Create animated 3D trajectory videos with rotating views (NEW!)
- **Video Overlay**: Create annotated videos with 3D coordinates and axes overlaid
- **Configurable Parameters**: Easy configuration of marker size and camera calibration
- **Dictionary Detection**: Automatic detection of ArUco dictionary type

## Installation

### 1. Activate Virtual Environment

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

Before processing videos, update the `config.py` file with your specific parameters:

### Camera Calibration

**Important**: For accurate 3D measurements, you must calibrate your camera and update these values:

```python
# Example camera matrix (replace with your calibration data)
CAMERA_MATRIX = [
    [fx, 0, cx],
    [0, fy, cy],
    [0, 0, 1]
]

# Distortion coefficients [k1, k2, p1, p2, k3]
DIST_COEFFS = [k1, k2, p1, p2, k3]
```

To calibrate your camera, you can use OpenCV's camera calibration tools or online tutorials.

### Marker Settings

```python
# Size of your ArUco marker in meters
MARKER_SIZE = 0.05  # Example: 5cm marker

# ArUco dictionary type
ARUCO_DICT_TYPE = 'DICT_4X4_50'  # Options: DICT_4X4_50, DICT_5X5_100, etc.
```

## Usage

### 1. Live Camera Tracking (NEW!)

Track ArUco markers in real-time from your webcam with automatic 3D animation generation:

```bash
python live_tracker.py
```

**Controls:**
- **SPACE** - Start/Stop recording trajectory
- **Q** - Quit and generate 3D animation

**Features:**
- Real-time ArUco marker detection and 3D pose estimation
- Live video display with 3D coordinate axes overlay
- Records trajectory data only when you press SPACE
- Automatically generates 3D animation video when done
- Does NOT save the webcam video (only trajectory and animation)

Options:
- `--camera`: Camera device ID (default: 0)
- `--marker-size`: Marker size in meters
- `--output`: CSV output file (default: live_trajectory.csv)
- `--animation`: Animation output file (default: live_animation.mp4)
- `--no-animation`: Skip 3D animation generation

Example:
```bash
# Use camera 0, marker size 5cm, custom output files
python live_tracker.py --camera 0 --marker-size 0.05 --output my_data.csv --animation my_anim.mp4
```

**Workflow:**
1. Run the script - live camera feed opens
2. Position ArUco marker in view
3. Press SPACE to start recording trajectory
4. Move the marker around
5. Press SPACE to stop recording
6. Press Q to quit
7. 3D animation video is automatically generated!

### 2. Track ArUco Markers from Video File

Process a video file to detect ArUco markers and save trajectory data:

```bash
python aruco_tracker.py path/to/video.mp4
```

Options:
- `--marker-size`: Specify marker size in meters (overrides config.py)
- `--output`: Specify output CSV file path

Example:
```bash
python aruco_tracker.py my_video.mp4 --marker-size 0.05 --output trajectory.csv
```

This will create a CSV file with columns:
- `frame`: Frame number
- `marker_id`: ArUco marker ID
- `x, y, z`: 3D position in meters
- `rx, ry, rz`: Rotation angles in radians

### 3. Visualize 3D Trajectory

Create 3D plots and animated videos from trajectory data:

```bash
python visualize_trajectory.py trajectory_data.csv
```

Options:
- `--marker-id`: Visualize specific marker ID only
- `--save`: Save plot to file
- `--no-show`: Don't display the plot window

Example:
```bash
python visualize_trajectory.py trajectory_data.csv --marker-id 0 --save output_plot.png
```

This generates:
- Interactive 3D trajectory plot
- Position vs. time plots for X, Y, Z coordinates
- Statistics (range, distance traveled, etc.)

**Create 3D Animation Video:**
```bash
python visualize_trajectory.py trajectory_data.csv --animate --video-output my_animation.mp4
```

Animation options:
- `--animate`: Enable animation mode
- `--video-output`: Output filename (default: trajectory_animation.mp4)
- `--duration`: Video duration in seconds (default: 10)
- `--fps`: Frames per second (default: 30)
- `--rotation-speed`: Rotation speed multiplier (default: 1.0)

The animation shows:
- 3D trajectory building up over time
- Rotating camera view for depth perception
- Coordinate axes at origin (X=red, Y=green, Z=blue)
- Current marker position highlighted

### 4. Create Annotated Video

Overlay 3D coordinates and axes on the video:

```bash
python visualize_on_video.py path/to/video.mp4
```

Options:
- `--marker-size`: Specify marker size in meters
- `--output`: Specify output video file path
- `--show`: Display video in real-time while processing

Example:
```bash
python visualize_on_video.py my_video.mp4 --output annotated.mp4 --show
```

The output video will show:
- Detected marker boundaries
- 3D coordinate axes (X=red, Y=green, Z=blue)
- Real-time 3D position coordinates
- Frame numbers

## Complete Workflow Example

```bash
# 1. Activate virtual environment
venv\Scripts\activate

# 2. Track markers and save trajectory
python aruco_tracker.py sample_video.mp4 --marker-size 0.05

# 3. Visualize trajectory in 3D
python visualize_trajectory.py trajectory_data.csv --save trajectory_plot.png

# 4. Create annotated video
python visualize_on_video.py sample_video.mp4 --output output_annotated.mp4
```

## Understanding the Coordinate System

The 3D coordinate system used:
- **X-axis (Red)**: Points to the right of the marker
- **Y-axis (Green)**: Points downward from the marker
- **Z-axis (Blue)**: Points away from the camera (depth)

The origin (0,0,0) is at the top-left corner of the ArUco marker.

## Troubleshooting

### No markers detected
- Ensure the marker is clearly visible in the video
- Check that `ARUCO_DICT_TYPE` matches your marker's dictionary
- Verify marker size is set correctly

### Inaccurate 3D measurements
- Calibrate your camera properly
- Ensure marker size in config matches physical marker size
- Check that markers are not too close or too far from camera

### Video processing is slow
- Increase `FRAME_SKIP` in config.py to process every Nth frame
- Use a lower resolution video
- Close other applications to free up CPU

## File Structure

```
tagCalibration/
├── venv/                          # Virtual environment
├── config.py                      # Configuration parameters
├── aruco_tracker.py              # Main tracking script
├── visualize_trajectory.py       # 3D trajectory visualization
├── visualize_on_video.py         # Video overlay script
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── trajectory_data.csv           # Generated trajectory data
└── output_with_3d_coords.mp4     # Generated annotated video
```

## Dependencies

- **opencv-contrib-python**: ArUco marker detection and pose estimation
- **numpy**: Numerical operations
- **matplotlib**: 3D plotting and visualization

## Camera Calibration Guide

For accurate 3D pose estimation, proper camera calibration is essential:

1. Print a checkerboard calibration pattern
2. Record a video moving the checkerboard in different positions
3. Use OpenCV's calibration tools to extract camera matrix and distortion coefficients
4. Update `config.py` with your calibration data

Alternatively, you can use online camera calibration tools or follow OpenCV tutorials.

## Tips for Best Results

1. **Lighting**: Ensure good, even lighting on the marker
2. **Marker Quality**: Use high-quality printed markers with clear borders
3. **Camera Stability**: Use a stable camera or tripod for consistent results
4. **Marker Size**: Larger markers are easier to detect from greater distances
5. **Frame Rate**: Higher frame rate videos provide smoother trajectories
6. **Calibration**: Always calibrate your camera for accurate measurements

## License

This project is open source and available for educational and research purposes.
