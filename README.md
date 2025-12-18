# ArUco Marker 3D Trajectory Tracker

A comprehensive Python application for detecting, tracking, and analyzing ArUco markers in 3D space. Features real-time camera tracking, automatic camera calibration, trajectory analysis with speed/velocity/angular metrics, and advanced visualization tools.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start Guide](#quick-start-guide)
- [Documentation](#documentation)
- [Module Documentation](#module-documentation)
- [Example Workflows](#example-workflows)
- [Troubleshooting](#troubleshooting)

## Prerequisites

**IMPORTANT: Camera calibration is required for accurate 3D measurements!**

Before tracking markers, you must calibrate your camera:
1. Generate and print a checkerboard pattern
2. Run the calibration module
3. The calibration will automatically update your config.py

**See [CALIBRATION_GUIDE.md](CALIBRATION_GUIDE.md) for complete step-by-step instructions.**

Quick calibration command:
```bash
python camera_calibration.py --mode live
```

Without proper calibration, 3D position measurements may be significantly inaccurate.

## Features

### Core Tracking
- **3D Pose Estimation**: Detect ArUco markers and estimate their 3D position and orientation
- **Live Camera Tracking**: Real-time ArUco detection from webcam with interactive recording
- **Video Processing**: Track markers from pre-recorded video files
- **Trajectory Tracking**: Track marker movement through 3D space over time
- **Timestamp Data**: All trajectories include precise timestamps for temporal analysis

### Calibration
- **Automatic Camera Calibration**: Interactive calibration with checkerboard pattern
- **Multiple Calibration Modes**: Live camera, video file, or image sequence
- **Quality Metrics**: Reprojection error analysis and quality assessment
- **Auto-Config Update**: Automatically updates config.py with calibration results
- **Checkerboard Generator**: Create custom calibration patterns for printing

### Analysis & Visualization
- **Comprehensive Analysis**: Calculate speed, velocity, distance, acceleration, and angular metrics
- **5 Analysis Plot Types**: Position, velocity, distance, angular rotation, and acceleration
- **3D Animation Videos**: Create animated trajectory videos with rotating camera views
- **Video Overlay**: Annotate videos with 3D coordinates and axes
- **Data Export**: Export analysis results to CSV for Excel/Python integration
- **Statistical Reports**: Detailed summary statistics with all motion metrics

### Utilities
- **Dictionary Detection**: Automatically detect ArUco dictionary type
- **Multi-Marker Support**: Track multiple markers simultaneously
- **Configurable Parameters**: Easy configuration of marker size and camera settings

## Installation

### 1. Create Virtual Environment (if not already created)

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**
- opencv-contrib-python (ArUco detection)
- numpy (numerical operations)
- matplotlib (plotting and visualization)
- pandas (data analysis)
- scipy (signal processing)

## Documentation

This README provides an overview. For detailed instructions, see:

| Document | Purpose |
|----------|---------|
| **[CALIBRATION_GUIDE.md](CALIBRATION_GUIDE.md)** | Complete camera calibration instructions with troubleshooting |
| **[LIVE_TRACKER_GUIDE.md](LIVE_TRACKER_GUIDE.md)** | Live tracking detailed usage and controls |
| **[ANALYSIS_GUIDE.md](ANALYSIS_GUIDE.md)** | Comprehensive trajectory analysis guide with examples |
| **[TIMESTAMP_FEATURE.md](TIMESTAMP_FEATURE.md)** | Timestamp feature technical documentation |

## Quick Start Guide

### Complete Workflow (Recommended)

```bash
# 1. Activate environment
venv\Scripts\activate

# 2. Camera Calibration (REQUIRED - first time only)
#    See CALIBRATION_GUIDE.md for detailed instructions
python camera_calibration.py --mode live

# 3. Live Tracking
python live_tracker.py --marker-size 0.05

# 4. Analyze Trajectory
python trajectory_analysis.py live_trajectory.csv --full-report

# 5. View results in analysis_output/ folder
```

**Note:** For detailed instructions on each step, refer to the [Documentation](#documentation) section below.

## Module Documentation

### 1. Camera Calibration Module

**Purpose:** Calibrate your camera for accurate 3D measurements

#### Generate Checkerboard Pattern

```bash
# Generate standard 9x6 checkerboard (25mm squares)
python generate_checkerboard.py --output checkerboard.png

# Print at 100% scale, mount on rigid board
```

#### Run Calibration

**Live Camera (Recommended):**
```bash
python camera_calibration.py --mode live --checkerboard 9x6 --square-size 0.025
```

Controls:
- **C** - Toggle auto-capture ON/OFF
- **SPACE** - Manual capture
- **Q** - Quit and calibrate

**From Video:**
```bash
python camera_calibration.py --mode video --input calibration_video.mp4
```

**From Images:**
```bash
python camera_calibration.py --mode images --input "calib_images/*.jpg"
```

**Features:**
- Real-time checkerboard detection
- Interactive auto/manual capture
- Quality metrics (reprojection error)
- Automatic config.py update
- Calibration data backup (.npz file)

**📖 Detailed Guide:** [CALIBRATION_GUIDE.md](CALIBRATION_GUIDE.md) - Complete instructions, best practices, and troubleshooting

---

### 2. Live Tracker Module

**Purpose:** Real-time ArUco tracking from webcam

```bash
python live_tracker.py
```

**Controls:**
- **SPACE** - Start/Stop recording trajectory
- **Q** - Quit and generate 3D animation

**Features:**
- Real-time marker detection and 3D pose display
- Live video with coordinate axes overlay
- Selective recording (only when you press SPACE)
- Timestamp tracking (starts at 0.0 when recording begins)
- Automatic 3D animation generation
- Does NOT save webcam video (saves space)

**Options:**
```bash
python live_tracker.py \
    --camera 0 \
    --marker-size 0.05 \
    --output my_data.csv \
    --animation my_anim.mp4 \
    --no-animation  # Skip animation
```

**Output:**
- `live_trajectory.csv` - Trajectory data with timestamps
- `live_animation.mp4` - 3D animated visualization

**📖 Detailed Guide:** [LIVE_TRACKER_GUIDE.md](LIVE_TRACKER_GUIDE.md) - Controls, tips, and advanced usage

---

### 3. Video Processor Module

**Purpose:** Track ArUco markers from video files

```bash
python aruco_tracker.py video.mp4 --marker-size 0.05
```

**Features:**
- Process pre-recorded videos
- Automatic timestamp calculation (from FPS)
- Frame-by-frame detection
- Progress tracking

**Options:**
```bash
python aruco_tracker.py video.mp4 \
    --marker-size 0.05 \
    --output trajectory.csv
```

**Output CSV Columns:**
- `timestamp` - Time in seconds (from video start)
- `frame` - Frame number
- `marker_id` - ArUco marker ID
- `x, y, z` - 3D position (meters)
- `rx, ry, rz` - 3D rotation (radians)

---

### 4. Trajectory Analysis Module

**Purpose:** Comprehensive motion analysis with graphs and statistics

#### Quick Analysis

```bash
# Summary statistics
python trajectory_analysis.py data.csv --summary

# Full report (all plots + CSV export)
python trajectory_analysis.py data.csv --full-report
```

#### Specific Plots

```bash
# Position over time
python trajectory_analysis.py data.csv --plot position

# Velocity analysis
python trajectory_analysis.py data.csv --plot velocity

# Distance traveled
python trajectory_analysis.py data.csv --plot distance

# Angular rotation (rotation angles over time)
python trajectory_analysis.py data.csv --plot angular

# Acceleration analysis
python trajectory_analysis.py data.csv --plot acceleration

# All plots
python trajectory_analysis.py data.csv --plot all
```

**Metrics Calculated:**

| Category | Metrics |
|----------|---------|
| **Position** | X, Y, Z coordinates, position ranges |
| **Velocity** | Vx, Vy, Vz components, speed magnitude, avg/max/min |
| **Distance** | Total distance, cumulative distance, per-step distance |
| **Acceleration** | Ax, Ay, Az components, acceleration magnitude |
| **Angular** | RX, RY, RZ angles (degrees), angular velocity, angular speed |
| **Time** | Duration, sample rate, timestamps |

**Output (Full Report):**
```
analysis_output/
├── position_vs_time.png       # X, Y, Z over time
├── velocity_analysis.png      # Velocity components + speed
├── distance_analysis.png      # Distance traveled
├── angular_analysis.png       # Rotation angles + angular speed
├── acceleration_analysis.png  # Acceleration components
└── analysis_metrics.csv       # All calculated metrics
```

**Options:**
```bash
python trajectory_analysis.py data.csv \
    --marker-id 0 \              # Specific marker
    --output-dir my_analysis \   # Custom output folder
    --export metrics.csv \       # Export to custom CSV
    --no-show                    # Don't display plots
```

**📖 Detailed Guide:** [ANALYSIS_GUIDE.md](ANALYSIS_GUIDE.md) - All metrics explained, formulas, and Python examples

---

### 5. Visualization Modules

#### 3D Trajectory Plots & Animation

```bash
# Static 3D plots
python visualize_trajectory.py data.csv --save plot.png

# Animated 3D video
python visualize_trajectory.py data.csv --animate --video-output anim.mp4
```

**Animation Features:**
- Trajectory builds up over time
- Rotating 3D camera view
- Coordinate axes at origin
- Current position highlighted
- Customizable duration and FPS

**Options:**
```bash
python visualize_trajectory.py data.csv \
    --animate \
    --video-output animation.mp4 \
    --duration 10 \
    --fps 30 \
    --rotation-speed 1.0
```

#### Video Overlay

```bash
python visualize_on_video.py video.mp4 --output annotated.mp4
```

**Features:**
- 3D coordinate axes on markers
- Real-time position display
- Frame numbers
- Detection status

---

### 6. Utility Modules

#### Test ArUco Dictionaries

Automatically detect which ArUco dictionary your markers use:

```bash
python test_aruco_dictionaries.py video.mp4
```

**Output:**
```
Dictionary: DICT_4X4_50
  Marker IDs detected: [0]
  Detection rate: 73.3%

RECOMMENDATION: Use 'DICT_4X4_50' in config.py
```

## Configuration

### config.py Settings

```python
# ArUco marker parameters
ARUCO_DICT_TYPE = 'DICT_4X4_50'
MARKER_SIZE = 0.05  # meters (5cm)

# Camera calibration (AUTOMATICALLY updated by camera_calibration.py)
CAMERA_MATRIX = [
    [fx, 0, cx],
    [0, fy, cy],
    [0, 0, 1]
]

DIST_COEFFS = [k1, k2, p1, p2, k3]

# Output settings
OUTPUT_TRAJECTORY_FILE = 'trajectory_data.csv'
OUTPUT_VIDEO_FILE = 'output_with_3d_coords.mp4'
PLOT_OUTPUT_FILE = 'trajectory_3d.png'
```

**IMPORTANT:** Run `camera_calibration.py` to automatically update camera parameters!
**See:** [CALIBRATION_GUIDE.md](CALIBRATION_GUIDE.md) for complete calibration instructions.

## Coordinate System

The 3D coordinate system:
- **X-axis (Red)**: Right of the marker
- **Y-axis (Green)**: Down from the marker
- **Z-axis (Blue)**: Away from camera (depth)
- **Origin (0,0,0)**: Top-left corner of ArUco marker

## CSV Data Format

All trajectory CSV files include:

```csv
timestamp,frame,marker_id,x,y,z,rx,ry,rz
0.000,0,0,0.1135,0.0684,0.3697,3.1131,-0.0130,0.0598
0.039,1,0,0.1141,0.0694,0.3723,3.1244,-0.0276,0.0516
...
```

| Column | Description | Unit |
|--------|-------------|------|
| timestamp | Time since start | seconds |
| frame | Frame number | - |
| marker_id | ArUco marker ID | - |
| x, y, z | 3D position | meters |
| rx, ry, rz | 3D rotation | radians |

## Example Workflows

### Workflow 1: Live Tracking & Analysis

For complete beginner-friendly instructions, see [CALIBRATION_GUIDE.md](CALIBRATION_GUIDE.md) and [LIVE_TRACKER_GUIDE.md](LIVE_TRACKER_GUIDE.md).

```bash
# 1. Calibrate (first time only) - See CALIBRATION_GUIDE.md
python camera_calibration.py --mode live

# 2. Track live - See LIVE_TRACKER_GUIDE.md
python live_tracker.py --marker-size 0.05

# 3. Analyze - See ANALYSIS_GUIDE.md
python trajectory_analysis.py live_trajectory.csv --full-report
```

### Workflow 2: Video Processing & Analysis

```bash
# 1. Detect dictionary type
python test_aruco_dictionaries.py video.mp4

# 2. Process video
python aruco_tracker.py video.mp4 --marker-size 0.05

# 3. Analyze trajectory
python trajectory_analysis.py trajectory_data.csv --full-report

# 4. Create annotated video
python visualize_on_video.py video.mp4 --output annotated.mp4
```

### Workflow 3: Research Study

```bash
# 1. Calibrate camera
python camera_calibration.py --mode live --num-images 30

# 2. Multiple recordings
python live_tracker.py --output trial1.csv
python live_tracker.py --output trial2.csv
python live_tracker.py --output trial3.csv

# 3. Analyze each trial
python trajectory_analysis.py trial1.csv --full-report --output-dir trial1_analysis
python trajectory_analysis.py trial2.csv --full-report --output-dir trial2_analysis
python trajectory_analysis.py trial3.csv --full-report --output-dir trial3_analysis

# 4. Compare in Excel/Python using exported CSV files
```

## File Structure

```
tagCalibration/
├── venv/                           # Virtual environment
├── config.py                       # Configuration parameters
│
├── # Tracking Scripts
├── live_tracker.py                 # Live camera tracking
├── aruco_tracker.py                # Video file processing
│
├── # Calibration Scripts
├── camera_calibration.py           # Camera calibration module
├── generate_checkerboard.py        # Checkerboard pattern generator
│
├── # Analysis Scripts
├── trajectory_analysis.py          # Comprehensive motion analysis
├── visualize_trajectory.py         # 3D plots and animations
├── visualize_on_video.py           # Video overlay
│
├── # Utility Scripts
├── test_aruco_dictionaries.py      # Dictionary detection
│
├── # Documentation
├── README.md                       # This file
├── CALIBRATION_GUIDE.md            # Camera calibration guide
├── LIVE_TRACKER_GUIDE.md           # Live tracker guide
├── ANALYSIS_GUIDE.md               # Trajectory analysis guide
├── TIMESTAMP_FEATURE.md            # Timestamp documentation
│
├── # Dependencies
├── requirements.txt                # Python packages
│
└── # Generated Files (examples)
    ├── calibration_data.npz        # Camera calibration backup
    ├── checkerboard.png            # Calibration pattern
    ├── live_trajectory.csv         # Trajectory data
    ├── live_animation.mp4          # 3D animation
    └── analysis_output/            # Analysis results
        ├── *.png                   # Analysis plots
        └── analysis_metrics.csv    # Calculated metrics
```

## Troubleshooting

For complete troubleshooting guides, see the detailed documentation files linked below.

### Camera Calibration Issues

**See [CALIBRATION_GUIDE.md](CALIBRATION_GUIDE.md) for complete calibration troubleshooting.**

**Problem:** No checkerboard detected

**Solutions:**
- Ensure checkerboard size matches (`--checkerboard 9x6`)
- Print at 100% scale (not fit to page)
- Verify checkerboard is flat and rigid
- Improve lighting
- Check focus

**Problem:** High reprojection error (> 1.0)

**Solutions:**
- Collect more images (25-30 recommended)
- Verify square size measurement (use ruler)
- Ensure varied angles and positions
- Check printer settings (actual size)

### Tracking Issues

**Problem:** No markers detected

**Solutions:**
- Run `test_aruco_dictionaries.py` to find correct dictionary
- Update `ARUCO_DICT_TYPE` in config.py
- Verify marker size setting
- Improve lighting
- Ensure marker is in focus

**Problem:** Inaccurate 3D measurements

**Solutions:**
- Calibrate camera with `camera_calibration.py`
- Verify marker size is correct (measure with ruler)
- Check camera calibration quality (reprojection error < 1.0)
- Ensure marker is flat and rigid

### Analysis Issues

**See [ANALYSIS_GUIDE.md](ANALYSIS_GUIDE.md) for detailed analysis troubleshooting and examples.**

**Problem:** Missing timestamp column

**Solutions:**
- Re-record with updated scripts (all now include timestamps)
- Use `live_tracker.py` or `aruco_tracker.py`

**Problem:** High noise in velocity/acceleration

**Solutions:**
- Analysis script applies automatic smoothing
- Improve camera calibration
- Use stable camera mount
- Increase marker size
- Better lighting

## Performance Tips

1. **Fast Processing**: Increase `FRAME_SKIP` in config.py
2. **Better Accuracy**: Use larger markers and closer distances
3. **Smooth Data**: Analysis script automatically applies smoothing
4. **Multiple Markers**: Script handles multiple markers automatically
5. **Large Videos**: Process in segments or increase sample interval

## Best Practices

For detailed best practices and tips, see the individual guide documents.

### For Calibration:
✅ Use rigid, flat checkerboard
✅ Collect 20-30 images
✅ Vary angles and distances
✅ Cover entire camera view
✅ Measure square size accurately

**See [CALIBRATION_GUIDE.md](CALIBRATION_GUIDE.md) for detailed calibration best practices.**

### For Tracking:
✅ Calibrate camera first
✅ Use good, even lighting
✅ Print high-quality markers
✅ Keep marker flat and rigid
✅ Measure marker size precisely

**See [LIVE_TRACKER_GUIDE.md](LIVE_TRACKER_GUIDE.md) for tracking tips and techniques.**

### For Analysis:
✅ Review summary statistics first
✅ Check for outliers in plots
✅ Verify physical plausibility
✅ Export to CSV for detailed analysis
✅ Compare multiple trials

**See [ANALYSIS_GUIDE.md](ANALYSIS_GUIDE.md) for analysis workflows and Python examples.**

## Integration Examples

### Python Analysis

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load analysis results
df = pd.read_csv('analysis_output/analysis_metrics.csv')

# Calculate average speed
avg_speed = df['speed'].mean()
print(f"Average speed: {avg_speed:.3f} m/s")

# Plot custom analysis
plt.plot(df['timestamp'], df['speed'])
plt.xlabel('Time (s)')
plt.ylabel('Speed (m/s)')
plt.title('Speed Over Time')
plt.grid(True)
plt.show()

# Angular analysis
total_rotation_x = df['rx_deg'].max() - df['rx_deg'].min()
print(f"Total X rotation: {total_rotation_x:.1f}°")
```

### Excel Integration

1. Open `analysis_metrics.csv` in Excel
2. Create pivot tables for statistics
3. Generate custom charts
4. Use formulas for calculations
5. Export to other formats

## Advanced Features

### Multi-Marker Tracking

All scripts support multiple markers automatically:

```bash
# Track multiple markers
python live_tracker.py

# Analyze specific marker
python trajectory_analysis.py data.csv --marker-id 0

# Or analyze all markers together
python trajectory_analysis.py data.csv --full-report
```

### Custom Checkerboard Patterns

```bash
# Large pattern for distant calibration
python generate_checkerboard.py --width 11 --height 8 --square-size 30

# Small pattern for close-up
python generate_checkerboard.py --width 7 --height 5 --square-size 20
```

### Batch Processing

```bash
# Process multiple videos
for video in *.mp4; do
    python aruco_tracker.py "$video" --output "${video%.mp4}.csv"
    python trajectory_analysis.py "${video%.mp4}.csv" --full-report --output-dir "${video%.mp4}_analysis"
done
```

## Complete Documentation Index

| Document | Description |
|----------|-------------|
| `README.md` | Main documentation (this file) - Overview and quick reference |
| **[CALIBRATION_GUIDE.md](CALIBRATION_GUIDE.md)** | Complete camera calibration instructions with troubleshooting |
| **[LIVE_TRACKER_GUIDE.md](LIVE_TRACKER_GUIDE.md)** | Live tracking detailed guide with controls and tips |
| **[ANALYSIS_GUIDE.md](ANALYSIS_GUIDE.md)** | Trajectory analysis guide with formulas and examples |
| **[TIMESTAMP_FEATURE.md](TIMESTAMP_FEATURE.md)** | Technical documentation for timestamp feature |

## Dependencies

All dependencies are listed in `requirements.txt`:

```
opencv-contrib-python  # ArUco detection and calibration
numpy                  # Numerical operations
matplotlib             # Plotting and visualization
pandas                 # Data analysis and manipulation
scipy                  # Signal processing and smoothing
```

## License

This project is open source and available for educational and research purposes.

## Support

For issues, questions, or feature requests, please refer to the documentation files:
- **Calibration issues:** See [CALIBRATION_GUIDE.md](CALIBRATION_GUIDE.md)
- **Tracking issues:** See [LIVE_TRACKER_GUIDE.md](LIVE_TRACKER_GUIDE.md)
- **Analysis questions:** See [ANALYSIS_GUIDE.md](ANALYSIS_GUIDE.md)
- **Timestamp questions:** See [TIMESTAMP_FEATURE.md](TIMESTAMP_FEATURE.md)

---

**Version:** 2.0
**Features:** Camera Calibration | Live Tracking | Video Processing | Trajectory Analysis | 3D Visualization
**Timestamp Support:** ✅ All modules
**Multi-Marker Support:** ✅ All modules
**Automatic Calibration:** ✅ Included
