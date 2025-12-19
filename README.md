# ArUco Marker 3D Trajectory Tracker

A comprehensive Python application for detecting, tracking, and analyzing ArUco markers in 3D space. Features real-time camera tracking, automatic camera calibration, trajectory analysis with speed/velocity/angular metrics, and advanced visualization tools.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Setup and Calibration](#setup-and-calibration)
  - [Generate Checkerboard Pattern](#generate-checkerboard-pattern)
  - [Camera Calibration Methods](#camera-calibration-methods)
  - [Calibration Best Practices](#calibration-best-practices)
  - [Understanding Calibration Results](#understanding-calibration-results)
- [Live Tracking](#live-tracking)
  - [Live Tracker Controls](#live-tracker-controls)
  - [Recording Workflow](#recording-workflow)
  - [Command-Line Options](#live-tracker-command-line-options)
  - [Tips for Best Results](#tips-for-best-results)
- [Video Processing](#video-processing)
  - [Processing Pre-Recorded Videos](#processing-pre-recorded-videos)
  - [Video Overlay and Annotation](#video-overlay-and-annotation)
- [Trajectory Analysis](#trajectory-analysis)
  - [Analysis Commands](#analysis-commands)
  - [Metrics Calculated](#metrics-calculated)
  - [Understanding the Plots](#understanding-the-plots)
  - [Data Export and Integration](#data-export-and-integration)
- [Timestamp Features](#timestamp-features)
  - [CSV Format with Timestamps](#csv-format-with-timestamps)
  - [Temporal Analysis](#temporal-analysis)
- [CSV Data Format](#csv-data-format)
- [Configuration Reference](#configuration-reference)
- [Troubleshooting](#troubleshooting)
  - [Camera Calibration Issues](#camera-calibration-issues)
  - [Tracking Issues](#tracking-issues)
  - [Analysis Issues](#analysis-issues)
- [Best Practices](#best-practices)
  - [Calibration Best Practices](#calibration-best-practices-1)
  - [Tracking Best Practices](#tracking-best-practices)
  - [Analysis Best Practices](#analysis-best-practices)
- [Advanced Features](#advanced-features)
  - [Multi-Marker Tracking](#multi-marker-tracking)
  - [Custom Checkerboard Patterns](#custom-checkerboard-patterns)
  - [Multi-Camera Systems](#multi-camera-systems)
  - [Batch Processing](#batch-processing)
- [Python Integration Examples](#python-integration-examples)
- [File Structure](#file-structure)
- [Dependencies](#dependencies)

---

## Overview

This application provides a complete workflow for 3D ArUco marker tracking:

1. **Camera Calibration** - Ensure accurate 3D measurements
2. **Live Tracking** - Real-time marker detection and recording
3. **Video Processing** - Track markers from pre-recorded videos
4. **Trajectory Analysis** - Calculate motion metrics and generate visualizations
5. **Data Export** - Export results for further analysis in Excel, Python, or R

---

## Features

### Core Tracking
- **3D Pose Estimation**: Detect ArUco markers and estimate their 3D position and orientation
- **Live Camera Tracking**: Real-time ArUco detection from webcam with interactive recording
- **Video Processing**: Track markers from pre-recorded video files
- **Trajectory Tracking**: Track marker movement through 3D space over time
- **Timestamp Data**: All trajectories include precise timestamps for temporal analysis
- **Multi-Marker Support**: Track multiple markers simultaneously

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
- **Configurable Parameters**: Easy configuration of marker size and camera settings

---

## Prerequisites

**Python 3.7 or higher** required

**IMPORTANT: Camera calibration is required for accurate 3D measurements!**

Without proper calibration, 3D position measurements may be significantly inaccurate. See the [Setup and Calibration](#setup-and-calibration) section for complete instructions.

---

## Installation

### 1. Clone or Download Repository

Download the project files to your local machine.

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- opencv-contrib-python (ArUco detection and calibration)
- numpy (numerical operations)
- matplotlib (plotting and visualization)
- pandas (data analysis and manipulation)
- scipy (signal processing and smoothing)

---

## Quick Start

### Complete Workflow (First Time Users)

```bash
# 1. Activate environment
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. Generate and print checkerboard
python generate_checkerboard.py --output checkerboard.png
# Print at 100% scale on rigid surface

# 3. Camera Calibration (REQUIRED - first time only)
python camera_calibration.py --mode live

# 4. Live Tracking
python live_tracker.py --marker-size 0.05

# 5. Analyze Trajectory
python trajectory_analysis.py live_trajectory.csv --full-report

# 6. View results in analysis_output/ folder
```

---

## Setup and Calibration

Camera calibration is **essential** for accurate 3D ArUco marker tracking. This section provides complete calibration instructions.

### Generate Checkerboard Pattern

The checkerboard pattern is used to calibrate your camera's intrinsic parameters.

#### Standard Pattern (Recommended)

```bash
# Generate standard 9x6 checkerboard (25mm squares)
python generate_checkerboard.py --output checkerboard.png
```

#### Custom Patterns

```bash
# Large pattern for distant calibration
python generate_checkerboard.py --width 11 --height 8 --square-size 30

# Small pattern for closeup
python generate_checkerboard.py --width 7 --height 5 --square-size 20

# High-DPI printing
python generate_checkerboard.py --dpi 600
```

#### Standard Sizes Reference

| Pattern | Inner Corners | Square Size | Total Size | Use Case |
|---------|---------------|-------------|------------|----------|
| Small | 7x5 | 20mm | 160x120mm | Webcam, close range |
| Medium | 9x6 | 25mm | 250x175mm | Standard (recommended) |
| Large | 11x8 | 30mm | 360x270mm | High-res camera, far range |

#### Printing Instructions

**Critical steps for accurate calibration:**

1. **Print Settings:**
   - Use high-quality printer
   - Print at **100% scale** (Actual Size)
   - **DO NOT** resize or fit to page
   - Check "Actual Size" or "Do not scale" option

2. **Paper and Mounting:**
   - Use thick paper or cardstock
   - Mount on rigid, flat surface (foam board recommended)
   - Ensure perfectly flat (no curves or wrinkles)
   - Keep surface clean

3. **Verification:**
   - **Measure squares with ruler** (in millimeters)
   - Verify size matches expected value
   - If incorrect, adjust printer settings and reprint

---

### Camera Calibration Methods

Three calibration methods are available. Choose the one that best fits your workflow.

#### Method 1: Live Camera Calibration (Recommended)

**Advantages:**
- Real-time feedback
- Interactive capture control
- Best for beginners
- Immediate quality check

**Command:**
```bash
python camera_calibration.py --mode live --checkerboard 9x6 --square-size 0.025
```

**Optional parameters:**
```bash
python camera_calibration.py --mode live \
    --camera 0 \
    --num-images 25 \
    --interval 2.0 \
    --checkerboard 9x6 \
    --square-size 0.025
```

**Interactive Controls:**

| Key | Action |
|-----|--------|
| **C** | Toggle auto-capture ON/OFF |
| **SPACE** | Manual capture |
| **Q** | Quit and calibrate |

**Calibration Workflow:**

1. **Position checkerboard** in camera view
2. **Press C** to start auto-capture (captures every 2 seconds)
3. **Move checkerboard** slowly through different:
   - Distances (near/far from camera)
   - Angles (tilted left/right/up/down)
   - Positions (center/corners/edges of frame)
4. **Press SPACE** to manually capture particularly good frames
5. **Collect 20-30 images** with variety
6. **Press Q** when enough images collected
7. Script automatically calibrates and updates config.py

**Tips for Best Results:**
- Keep checkerboard flat and rigid
- Use good, even lighting (avoid shadows and glare)
- Move slowly and smoothly
- Cover entire camera view area
- Capture at least 20-30 images
- Vary both distance and angles significantly

---

#### Method 2: Video File Calibration

**Advantages:**
- Use pre-recorded video
- Process offline
- Can review video quality before calibration

**Recording the Video:**
```bash
# Record 30-60 seconds of video showing checkerboard
# Move checkerboard around during recording
# Keep checkerboard in frame and in focus
```

**Run Calibration:**
```bash
python camera_calibration.py --mode video \
    --input my_calibration.mp4 \
    --checkerboard 9x6 \
    --square-size 0.025 \
    --sample-interval 30
```

**Recording Tips:**
- Record 30-60 seconds total
- Move checkerboard slowly and smoothly
- Cover all areas of camera frame
- Vary distance and angles significantly
- Keep entire checkerboard visible
- Avoid motion blur (move slowly)
- Use good lighting

---

#### Method 3: Image Files Calibration

**Advantages:**
- Full control over each image
- Can verify quality before calibration
- Easy to retake poor images

**Capture Images:**
1. Take 20-30 photos of checkerboard
2. Use any camera or webcam software
3. Save as: calib_001.jpg, calib_002.jpg, etc.
4. Store in folder: `calib_images/`

**Run Calibration:**
```bash
python camera_calibration.py --mode images \
    --input "calib_images/*.jpg" \
    --checkerboard 9x6 \
    --square-size 0.025
```

**Image Requirements:**
- Checkerboard clearly visible and in focus
- Entire checkerboard pattern in frame
- Good lighting (no shadows or glare)
- Variety of positions and angles
- At least 20-30 quality images

---

### Calibration Best Practices

#### Checkerboard Quality

**Do:**
- Print on thick, rigid paper or cardstock
- Use high-quality printer
- Mount on foam board or rigid surface
- Keep perfectly flat
- Measure squares accurately with ruler
- Store flat when not in use

**Don't:**
- Use wrinkled or curved paper
- Print at wrong scale
- Fold or bend the pattern
- Guess square size measurements
- Use glossy paper (causes glare)

#### Image Collection Strategy

**Do:**
- Collect 20-30 images minimum (30-40 for high precision)
- Vary angles significantly (tilt in all directions)
- Vary distances (near and far from camera)
- Cover all frame areas (center, corners, edges)
- Use consistent, good lighting
- Keep checkerboard steady during capture
- Ensure entire pattern is visible in each frame

**Don't:**
- Rush the calibration process
- Use blurry or out-of-focus images
- Keep same angle for all captures
- Keep same distance for all captures
- Use poor or inconsistent lighting
- Move too quickly (causes blur)
- Capture with partial pattern visibility

#### Camera Setup

**Do:**
- Use fixed focus if available
- Disable auto-exposure during capture
- Use good, even lighting
- Keep camera stable (use tripod if possible)
- Use native camera resolution
- Calibrate at the resolution you'll use for tracking

**Don't:**
- Change camera settings mid-calibration
- Use digital zoom
- Mix different cameras or resolutions
- Use very low resolution
- Change lighting during calibration

---

### Understanding Calibration Results

After calibration, you'll see output like this:

```
CALIBRATION RESULTS
============================================================

Camera Matrix (Intrinsic Parameters):
  fx = 1234.56 (focal length x)
  fy = 1235.78 (focal length y)
  cx = 639.50 (principal point x)
  cy = 479.50 (principal point y)

Distortion Coefficients:
  k1 = -0.123456 (radial distortion)
  k2 = 0.234567 (radial distortion)
  p1 = -0.001234 (tangential distortion)
  p2 = 0.002345 (tangential distortion)
  k3 = -0.012345 (radial distortion)

Calibration Quality:
  Reprojection Error: 0.42 pixels
  Quality: Excellent
```

#### Reprojection Error Interpretation

| Error (pixels) | Quality | Action |
|----------------|---------|--------|
| < 0.5 | Excellent | Perfect! Use it |
| 0.5 - 1.0 | Good | Acceptable for most uses |
| 1.0 - 2.0 | Acceptable | Consider recalibrating for better accuracy |
| > 2.0 | Poor | Recalibrate required |

**High error causes:**
- Insufficient images (need 20+ with variety)
- Inaccurate checkerboard measurements
- Motion blur in images
- Checkerboard not perfectly flat
- Poor image variety (same angles/distances)
- Printer scaled the pattern incorrectly

#### What Gets Saved

After successful calibration:
- ✅ `config.py` automatically updated with camera parameters
- ✅ `calibration_data.npz` saved as backup
- ✅ Reprojection error displayed
- ✅ Ready to use for ArUco tracking immediately

---

### Calibration Command-Line Reference

```bash
python camera_calibration.py --mode <MODE> [OPTIONS]
```

#### Required Arguments:
- `--mode {live,video,images}` - Calibration mode

#### Common Options:
- `--checkerboard WxH` - Pattern size (e.g., 9x6) [default: 9x6]
- `--square-size SIZE` - Square size in meters [default: 0.025]
- `--output FILE` - Save calibration to file [default: calibration_data.npz]
- `--no-update-config` - Don't update config.py automatically

#### Live Mode Options:
- `--camera ID` - Camera device ID [default: 0]
- `--num-images N` - Target number of images [default: 20]
- `--interval SECONDS` - Auto-capture interval [default: 2.0]

#### Video Mode Options:
- `--input VIDEO` - Input video file (required)
- `--sample-interval N` - Sample every Nth frame [default: 30]

#### Images Mode Options:
- `--input PATTERN` - Image file pattern (required)
  - Examples: `"images/*.jpg"`, `"calib*.png"`, `"C:/photos/*.bmp"`

---

### Calibration Validation

After calibration, test accuracy by tracking a known-size marker:

```bash
# Track a marker with known size (e.g., 5cm)
python live_tracker.py --marker-size 0.05

# Move marker to known distance (e.g., 0.5m from camera)
# Check if reported Z position ≈ 0.5m
# Error should be < 5% for good calibration
```

---

## Live Tracking

The Live Tracker allows real-time ArUco marker detection from your webcam with interactive recording controls.

### Live Tracker Controls

**Start Live Tracker:**
```bash
python live_tracker.py
```

**Keyboard Controls:**

| Key | Action |
|-----|--------|
| **SPACE** | Start/Stop recording trajectory data |
| **Q** | Quit and generate 3D animation |

### On-Screen Display

The live view shows real-time information:

- **Status**: RECORDING (green) or STANDBY (orange)
- **Time**: Elapsed time since program start
- **Rec Time**: Recording timestamp (only during recording)
- **Frames**: Current frame count
- **Data points**: Number of trajectory points recorded
- **Detection**: Whether marker is currently detected
- **3D Axes**: Red (X), Green (Y), Blue (Z) overlaid on marker
- **Position**: Real-time X, Y, Z coordinates in meters

### Recording Workflow

#### 1. Marker Setup

Before starting:
- Print an ArUco marker (DICT_4X4_50 recommended)
- Measure the marker size accurately with ruler (in millimeters)
- Convert to meters (e.g., 50mm = 0.05m)

Update config.py or use command-line option:
```python
# In config.py
MARKER_SIZE = 0.05  # 5cm marker
```

Or:
```bash
python live_tracker.py --marker-size 0.05
```

#### 2. Start Tracking

```bash
python live_tracker.py --marker-size 0.05
```

#### 3. Recording Session

1. **Camera window opens** showing live feed
2. **Position marker in view** - ensure good lighting and focus
3. **Press SPACE** to start recording (status turns green, "RECORDING" appears)
4. **Move the marker** through 3D space as desired
5. **Press SPACE** to stop recording (data saved, status returns to standby)
6. Can start new recording by pressing SPACE again (clears previous data)

#### 4. Exit and Process

- **Press Q** to quit
- Script automatically saves:
  - `live_trajectory.csv` - trajectory data with timestamps
  - `live_animation.mp4` - 3D animation video (unless `--no-animation`)

**Note:** Live webcam video is NOT saved (saves disk space). Only trajectory data and 3D animation are generated.

---

### Live Tracker Command-Line Options

```bash
python live_tracker.py [options]
```

#### Options:

| Option | Description | Default |
|--------|-------------|---------|
| `--camera ID` | Camera device ID (0, 1, 2, etc.) | 0 |
| `--marker-size SIZE` | Marker size in meters | From config.py |
| `--output FILE` | CSV output file | live_trajectory.csv |
| `--animation FILE` | Animation output file | live_animation.mp4 |
| `--no-animation` | Skip animation generation | False |

#### Examples:

```bash
# Use specific camera and marker size
python live_tracker.py --camera 1 --marker-size 0.08

# Custom output files
python live_tracker.py --output my_data.csv --animation my_video.mp4

# Skip animation generation (faster)
python live_tracker.py --no-animation

# Multiple sessions with different outputs
python live_tracker.py --output session1.csv
python live_tracker.py --output session2.csv
python live_tracker.py --output session3.csv
```

---

### Tips for Best Results

#### Camera Setup
- Use good, even lighting (avoid shadows)
- Position camera at comfortable working distance
- Ensure stable camera mounting (tripod recommended)
- Use high-quality webcam if possible
- Close other applications using the camera

#### Marker Setup
- Print marker on flat, rigid surface
- Use high-quality printer (avoid smudges and blur)
- Measure marker size accurately with ruler
- Keep marker clean and unwrinkled
- Use matte paper (avoid glossy to prevent glare)

#### Recording Technique
- Start with marker clearly visible
- Move slowly and smoothly
- Keep marker in frame at all times
- Avoid rapid rotations (causes blur)
- Record for at least 5-10 seconds
- Maintain consistent lighting
- Avoid occlusions

#### Multiple Recording Sessions

You can press SPACE multiple times during one session:
- **First SPACE**: Start recording
- **Second SPACE**: Stop recording (data kept)
- **Third SPACE**: Start new recording (clears previous data)
- **Q**: Quit and process last recording

---

### Live Tracker Output Files

#### 1. Trajectory CSV (live_trajectory.csv)

Contains timestamped trajectory data:
- `timestamp` - Time in seconds since recording started
- `frame` - Frame number
- `marker_id` - ArUco marker ID
- `x, y, z` - 3D position in meters
- `rx, ry, rz` - Rotation in radians

#### 2. Animation Video (live_animation.mp4)

Automatically generated 3D visualization featuring:
- 3D trajectory path
- Rotating camera view
- Building trajectory animation
- Coordinate axes at origin
- Current position highlighted
- 10 seconds duration at 30 FPS

---

### Example Session Output

After running the live tracker, you'll see:

```
TRACKING SUMMARY
============================================================
Total frames processed: 450
Frames with detections: 387
Detection rate: 86.0%
Trajectory data points: 387
============================================================

[RECORDING STOPPED]
Captured 245 data points
Recording duration: 12.45 seconds

Trajectory saved: live_trajectory.csv

Generating 3D animation video...
Creating 3D animation video: live_animation.mp4
Duration: 10s, FPS: 30
Generating frames...
Saving video (this may take a while)...
Video saved successfully: live_animation.mp4
```

---

## Video Processing

Process ArUco markers from pre-recorded video files.

### Processing Pre-Recorded Videos

**Basic Usage:**
```bash
python aruco_tracker.py video.mp4 --marker-size 0.05
```

**Features:**
- Process any video format (mp4, avi, mov, etc.)
- Automatic timestamp calculation from FPS
- Frame-by-frame detection with progress tracking
- Handles multiple markers automatically

**Options:**
```bash
python aruco_tracker.py video.mp4 \
    --marker-size 0.05 \
    --output trajectory.csv
```

**How Timestamps Work:**
- Calculated from frame number and video FPS
- Formula: `timestamp = frame_number / fps`
- Example at 30 FPS: frame 30 = 1.0 second, frame 60 = 2.0 seconds

---

### Video Overlay and Annotation

Add 3D coordinate visualization to videos:

```bash
python visualize_on_video.py video.mp4 --output annotated.mp4
```

**Features:**
- 3D coordinate axes overlaid on markers
- Real-time position display (X, Y, Z)
- Frame numbers
- Detection status indicators
- Marker ID labels

**Use Cases:**
- Create presentation videos
- Verify tracking accuracy
- Debug tracking issues
- Educational demonstrations

---

### Test ArUco Dictionaries

If you don't know which ArUco dictionary your markers use:

```bash
python test_aruco_dictionaries.py video.mp4
```

**Output Example:**
```
Testing dictionary: DICT_4X4_50
  Marker IDs detected: [0, 1, 3]
  Total detections: 245
  Detection rate: 73.3%

Testing dictionary: DICT_5X5_100
  No markers detected

RECOMMENDATION: Use 'DICT_4X4_50' in config.py
```

Update config.py with recommended dictionary:
```python
ARUCO_DICT_TYPE = 'DICT_4X4_50'
```

---

## Trajectory Analysis

Comprehensive analysis of ArUco marker trajectory data with statistics, visualizations, and data export.

### Analysis Commands

#### Quick Analysis

```bash
# Print summary statistics only
python trajectory_analysis.py data.csv --summary

# Generate specific plot
python trajectory_analysis.py data.csv --plot velocity

# Generate all plots
python trajectory_analysis.py data.csv --plot all

# Full report (all plots + summary + CSV export)
python trajectory_analysis.py data.csv --full-report
```

#### Advanced Options

```bash
# Analyze specific marker
python trajectory_analysis.py data.csv --marker-id 0 --full-report

# Custom output directory
python trajectory_analysis.py data.csv --full-report --output-dir my_analysis

# Export metrics without showing plots
python trajectory_analysis.py data.csv --export metrics.csv --no-show

# Generate report without displaying plots
python trajectory_analysis.py data.csv --full-report --no-show
```

---

### Metrics Calculated

The analysis script calculates comprehensive motion metrics across six categories:

#### Position Metrics

| Metric | Description | Unit |
|--------|-------------|------|
| x, y, z | 3D position coordinates | meters (m) |
| Position range | Min/max values for each axis | meters (m) |

#### Velocity Metrics

| Metric | Description | Unit | Formula |
|--------|-------------|------|---------|
| vx, vy, vz | Velocity components | m/s | Δx/Δt, Δy/Δt, Δz/Δt |
| speed | Velocity magnitude | m/s | √(vx² + vy² + vz²) |

**Statistics provided:**
- Average speed
- Maximum speed
- Minimum speed

#### Distance Metrics

| Metric | Description | Unit | Formula |
|--------|-------------|------|---------|
| distance | Instantaneous distance | m | √(Δx² + Δy² + Δz²) |
| cumulative_distance | Total distance traveled | m | Σ distance |

#### Acceleration Metrics

| Metric | Description | Unit | Formula |
|--------|-------------|------|---------|
| ax, ay, az | Acceleration components | m/s² | Δvx/Δt, Δvy/Δt, Δvz/Δt |
| acceleration | Acceleration magnitude | m/s² | √(ax² + ay² + az²) |

#### Angular Metrics

| Metric | Description | Unit | Formula |
|--------|-------------|------|---------|
| rx, ry, rz | Rotation angles | radians | From pose estimation |
| rx_deg, ry_deg, rz_deg | Rotation angles | degrees | radians × 180/π |
| omega_x, omega_y, omega_z | Angular velocity components | rad/s | Δrx/Δt, etc. |
| angular_speed | Angular velocity magnitude | rad/s | √(ωx² + ωy² + ωz²) |

#### Time Metrics

- Duration (total time)
- Sample rate (Hz)
- Data points count

---

### Analysis Output Files

**Full Report Generates:**

```
analysis_output/
├── position_vs_time.png       # X, Y, Z coordinates over time
├── velocity_analysis.png      # Velocity components and speed magnitude
├── distance_analysis.png      # Cumulative and instantaneous distance
├── angular_analysis.png       # Rotation angles and angular speed
├── acceleration_analysis.png  # Acceleration components and magnitude
└── analysis_metrics.csv       # All calculated metrics (exportable)
```

All plots are saved at 300 DPI for high-quality presentations.

---

### Understanding the Plots

#### 1. Position vs Time

**Shows:** X, Y, Z coordinates over time

**Use for:**
- Track movement path through 3D space
- Identify position changes and patterns
- Detect stationary periods

**Interpretation:**
- Flat lines = stationary in that axis
- Slope = velocity in that direction
- Curves = acceleration/deceleration

---

#### 2. Velocity Analysis

**Shows:** Velocity components (Vx, Vy, Vz) and speed magnitude

**Use for:**
- Measure movement speed
- Identify direction changes
- Analyze velocity patterns and consistency

**Interpretation:**
- Positive/negative values = direction of movement
- Magnitude = speed of movement
- Spikes = sudden movements or jerks
- Zero crossings = direction reversals

---

#### 3. Distance Analysis

**Shows:** Cumulative distance and per-step distance

**Use for:**
- Calculate total path length
- Analyze movement efficiency
- Identify consistent vs variable movement

**Interpretation:**
- Cumulative line = total distance traveled
- Instantaneous distance = step-by-step movement size
- Slope of cumulative = average speed
- Flat cumulative = stationary period

---

#### 4. Angular Analysis

**Shows:** Rotation angles (RX, RY, RZ) and angular speed

**Use for:**
- Track orientation changes over time
- Measure rotation rates
- Identify spin patterns and stability

**Interpretation:**
- Angles shown in degrees
- Angular speed in degrees/second
- Wrapping at ±180°
- High angular speed = rapid rotation

---

#### 5. Acceleration Analysis

**Shows:** Acceleration components (Ax, Ay, Az) and magnitude

**Use for:**
- Detect sudden movements or impacts
- Measure forces and jerks
- Identify smooth vs jerky motion

**Interpretation:**
- High values = rapid velocity changes
- Zero = constant velocity (smooth motion)
- Spikes = impacts, jerks, or sudden direction changes
- Smoothing filter applied to reduce noise

---

### Data Smoothing

The analysis automatically applies Savitzky-Golay smoothing to reduce measurement noise:

- **Window size:** 5 points
- **Polynomial order:** 2
- **Applied to:** Speed, acceleration, angular speed calculations

**Raw data is preserved** with `_raw` suffix in exported CSV for comparison.

---

### Data Export and Integration

#### CSV Export

All calculated metrics can be exported to CSV:

```bash
python trajectory_analysis.py data.csv --export metrics.csv
```

**Exported columns include:**
- timestamp, frame, marker_id
- x, y, z (position)
- vx, vy, vz, speed (velocity)
- ax, ay, az, acceleration
- distance, cumulative_distance
- rx_deg, ry_deg, rz_deg (rotation in degrees)
- omega_x, omega_y, omega_z, angular_speed
- Raw versions: speed_raw, acceleration_raw, angular_speed_raw

---

#### Excel/Spreadsheet Integration

**Import CSV to Excel:**
1. Open Excel/LibreOffice Calc
2. File → Open → Select `analysis_metrics.csv`
3. Use "Text Import Wizard" if prompted (comma-delimited)

**Useful Columns for Charts:**

| Column | What to Plot |
|--------|--------------|
| timestamp | X-axis for all time-series plots |
| x, y, z | Position over time (3 line charts) |
| speed | Speed over time |
| cumulative_distance | Total distance traveled |
| rx_deg, ry_deg, rz_deg | Rotation angles over time |
| angular_speed | Rotation rate |
| acceleration | Acceleration magnitude |

**Create Custom Charts:**
1. Select timestamp column (A)
2. Hold Ctrl, select metric column (e.g., speed)
3. Insert → Chart → Line Chart
4. Customize axes labels, title, gridlines

---

### Summary Statistics Example

```bash
python trajectory_analysis.py data.csv --summary
```

**Output:**
```
Time Statistics:
  Duration: 12.45 seconds
  Data points: 245
  Sample rate: 19.7 Hz

Position Range:
  X: [0.0234, 0.4567] m (range: 0.4333 m)
  Y: [-0.0123, 0.2890] m (range: 0.3013 m)
  Z: [0.3500, 0.7800] m (range: 0.4300 m)

Distance Statistics:
  Total distance traveled: 2.1234 m
  Average distance per move: 0.008668 m

Speed Statistics:
  Average speed: 0.1705 m/s
  Maximum speed: 0.8234 m/s
  Minimum speed: 0.0012 m/s

Acceleration Statistics:
  Average acceleration: 0.0523 m/s²
  Maximum acceleration: 0.4521 m/s²

Angular Statistics:
  RX range: [-25.3°, 48.2°]
  RY range: [-12.1°, 15.6°]
  RZ range: [-180.0°, 179.8°]
  Average angular speed: 15.3 °/s
```

---

## Timestamp Features

All tracking modules include precise timestamp functionality for temporal analysis.

### CSV Format with Timestamps

**New CSV Format:**
```csv
timestamp,frame,marker_id,x,y,z,rx,ry,rz
0.000,0,0,0.1135,0.0684,0.3697,3.1131,-0.0130,0.0598
0.039,1,0,0.1141,0.0694,0.3723,3.1244,-0.0276,0.0516
0.078,2,0,0.1150,0.0705,0.3755,3.1076,-0.0110,0.0294
```

**Column Descriptions:**

| Column | Type | Unit | Description |
|--------|------|------|-------------|
| **timestamp** | float | seconds | Time since recording start (live) or video start |
| frame | int | - | Frame number |
| marker_id | int | - | ArUco marker ID |
| x, y, z | float | meters | 3D position |
| rx, ry, rz | float | radians | 3D rotation |

---

### Timestamp Behavior by Module

#### Live Tracker
- Timestamp starts at **0.0** when you press SPACE to start recording
- Independent of when program started
- Each new recording session resets to 0.0
- Reflects actual capture time (not frame-perfect)
- **On-screen display:** "Rec Time: X.XXs" during recording
- **Console output:** Shows recording duration when stopped

#### Video Processor
- Timestamp starts at **0.0** at first video frame
- Calculated from frame number and FPS
- Formula: `timestamp = frame_number / fps`
- Accurate for constant frame rate videos
- May drift slightly for variable frame rate videos

---

### Temporal Analysis

**Benefits of timestamps:**

1. **Time-Series Analysis:**
   - Track how position changes over time
   - Calculate velocities and accelerations
   - Identify time-specific events
   - Measure movement durations

2. **Data Synchronization:**
   - Sync with external sensors
   - Correlate with other time-series data
   - Match with video playback time
   - Align multiple recording sessions

3. **Performance Metrics:**
   - Calculate average speeds over intervals
   - Measure task completion times
   - Analyze motion patterns temporally
   - Compare timing across sessions

4. **Debugging:**
   - Identify when markers were lost
   - Check frame timing issues
   - Verify recording intervals
   - Analyze detection rates over time

---

### Python Examples with Timestamps

#### Plot Position Over Time

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load trajectory data
df = pd.read_csv('live_trajectory.csv')

# Plot X position over time
plt.plot(df['timestamp'], df['x'])
plt.xlabel('Time (seconds)')
plt.ylabel('X Position (meters)')
plt.title('X Position vs Time')
plt.grid(True)
plt.show()
```

#### Calculate Velocity

```python
import pandas as pd
import numpy as np

df = pd.read_csv('trajectory.csv')

# Calculate velocity components
df['vx'] = df['x'].diff() / df['timestamp'].diff()
df['vy'] = df['y'].diff() / df['timestamp'].diff()
df['vz'] = df['z'].diff() / df['timestamp'].diff()

# Calculate speed magnitude
df['speed'] = np.sqrt(df['vx']**2 + df['vy']**2 + df['vz']**2)

print(f"Average speed: {df['speed'].mean():.3f} m/s")
print(f"Max speed: {df['speed'].max():.3f} m/s")
```

#### Time-Based Filtering

```python
# Extract data from specific time range
start_time = 2.0  # Start at 2 seconds
end_time = 5.0    # End at 5 seconds

segment = df[(df['timestamp'] >= start_time) & (df['timestamp'] <= end_time)]

# Calculate statistics for segment
avg_position = segment[['x', 'y', 'z']].mean()
print(f"Average position (2-5s): {avg_position}")
```

#### Calculate Distance Traveled

```python
import numpy as np

df = pd.read_csv('trajectory.csv')

# Calculate distance between consecutive points
df['distance'] = np.sqrt(
    df['x'].diff()**2 +
    df['y'].diff()**2 +
    df['z'].diff()**2
)

# Cumulative distance
df['cumulative_distance'] = df['distance'].cumsum()

# Plot distance vs time
plt.plot(df['timestamp'], df['cumulative_distance'])
plt.xlabel('Time (s)')
plt.ylabel('Distance Traveled (m)')
plt.title('Cumulative Distance vs Time')
plt.grid(True)
plt.show()

print(f"Total distance: {df['cumulative_distance'].iloc[-1]:.3f} m")
```

---

## CSV Data Format

All trajectory CSV files follow a consistent format with timestamps as the first column.

**Standard CSV Format:**
```csv
timestamp,frame,marker_id,x,y,z,rx,ry,rz
0.000,0,0,0.1135,0.0684,0.3697,3.1131,-0.0130,0.0598
0.039,1,0,0.1141,0.0694,0.3723,3.1244,-0.0276,0.0516
```

**Column Reference:**

| Column | Type | Unit | Range | Description |
|--------|------|------|-------|-------------|
| timestamp | float | seconds | ≥ 0.0 | Time since start |
| frame | int | - | ≥ 0 | Frame number |
| marker_id | int | - | 0-999 | ArUco marker ID |
| x | float | meters | any | Horizontal position (right is positive) |
| y | float | meters | any | Vertical position (down is positive) |
| z | float | meters | > 0 | Depth/distance from camera |
| rx | float | radians | -π to π | Rotation around X-axis |
| ry | float | radians | -π to π | Rotation around Y-axis |
| rz | float | radians | -π to π | Rotation around Z-axis |

**Coordinate System:**
- **X-axis (Red)**: Right of the marker
- **Y-axis (Green)**: Down from the marker
- **Z-axis (Blue)**: Away from camera (depth)
- **Origin (0,0,0)**: Top-left corner of ArUco marker

---

## Configuration Reference

### config.py Settings

```python
# ArUco marker parameters
ARUCO_DICT_TYPE = 'DICT_4X4_50'  # Dictionary type
MARKER_SIZE = 0.05               # Marker size in meters (5cm)

# Camera calibration parameters (AUTO-UPDATED by camera_calibration.py)
CAMERA_MATRIX = [
    [fx, 0, cx],   # fx = focal length X, cx = principal point X
    [0, fy, cy],   # fy = focal length Y, cy = principal point Y
    [0, 0, 1]
]

DIST_COEFFS = [k1, k2, p1, p2, k3]  # Distortion coefficients

# Output file settings
OUTPUT_TRAJECTORY_FILE = 'trajectory_data.csv'
OUTPUT_VIDEO_FILE = 'output_with_3d_coords.mp4'
PLOT_OUTPUT_FILE = 'trajectory_3d.png'

# Processing settings
FRAME_SKIP = 1  # Process every Nth frame (1 = all frames)
```

**IMPORTANT:**
- Run `camera_calibration.py` to automatically update CAMERA_MATRIX and DIST_COEFFS
- Do not manually edit calibration parameters unless you know the exact values
- MARKER_SIZE must match your physical marker size (measure with ruler!)
- ARUCO_DICT_TYPE must match your printed markers (use `test_aruco_dictionaries.py` to verify)

---

## Troubleshooting

### Camera Calibration Issues

#### Problem: No checkerboard detected

**Solutions:**
- Ensure checkerboard size matches command: `--checkerboard 9x6`
- Verify checkerboard is completely flat (not curved or bent)
- Improve lighting (even, no shadows or glare)
- Move closer to camera
- Ensure entire pattern is visible in frame
- Check if checkerboard is in focus
- Verify pattern was printed correctly (9x6 = 9 corners wide, 6 tall)
- Try different checkerboard size (7x5 or 11x8)

---

#### Problem: "Need at least 10 images for calibration"

**Solutions:**
- Capture more images with checkerboard clearly visible
- Move checkerboard more slowly (avoid motion blur)
- Improve lighting conditions
- Ensure checkerboard is always in focus
- Verify checkerboard is completely in frame
- Check that checkerboard corners are detectable (high contrast)

---

#### Problem: High reprojection error (> 1.0 pixels)

**Causes:**
- Insufficient or poor quality images
- Incorrect square size measurement
- Checkerboard not flat or rigid
- Motion blur in images
- Poor image variety

**Solutions:**
- Recalibrate with more images (25-30 recommended, 30-40 for high precision)
- **Measure square size accurately with ruler** (critical!)
- Ensure checkerboard is mounted on rigid, flat surface
- Use better quality images (no blur)
- Vary angles and positions more significantly
- Verify printer settings (must be 100% scale, not fit to page)
- Remount checkerboard if warped
- Use thicker backing material

---

#### Problem: Camera not found

**Solutions:**
- Try different camera ID: `--camera 1` or `--camera 2`
- Check camera permissions (Windows Privacy Settings / Linux permissions)
- Close other applications using the camera (Zoom, Skype, etc.)
- Reconnect USB camera
- Restart computer if camera driver issues
- Verify camera works in other applications first

---

#### Problem: Wrong square size / measurements inaccurate

**Solutions:**
- **Measure squares with ruler in millimeters**
- Convert to meters: 25mm = 0.025m, 30mm = 0.030m
- Update command: `--square-size 0.025`
- Verify printer didn't scale the pattern
- Check print settings: must be "Actual Size" not "Fit to page"
- Reprint checkerboard if scaled incorrectly
- Measure multiple squares and average

---

### Tracking Issues

#### Problem: No markers detected

**Solutions:**
- Run `test_aruco_dictionaries.py video.mp4` to find correct dictionary
- Update `ARUCO_DICT_TYPE` in config.py with detected dictionary
- Verify marker size setting matches physical marker
- Improve lighting (even, diffuse light)
- Ensure marker is in focus
- Check that marker is not damaged or smudged
- Move marker closer to camera
- Verify marker quality (high-contrast print)
- Ensure marker is not too reflective (use matte paper)

---

#### Problem: Inaccurate 3D measurements

**Solutions:**
- **Calibrate camera** with `camera_calibration.py` (most common cause!)
- Verify marker size is correct (measure with ruler in millimeters)
- Check camera calibration quality (reprojection error should be < 1.0)
- Ensure marker is flat and rigid (not bent or curved)
- Use larger marker for better accuracy
- Reduce distance to marker
- Ensure good lighting
- Recalibrate if camera settings changed

---

#### Problem: Jittery or unstable tracking

**Solutions:**
- Improve camera calibration (recalibrate with more images)
- Use better lighting (even, no flickering)
- Use larger marker size
- Use better quality camera (higher resolution)
- Mount camera on stable surface (tripod)
- Move marker more slowly
- Use trajectory analysis smoothing filters
- Ensure marker is flat and rigid

---

#### Problem: Marker detection rate low

**Solutions:**
- Improve lighting conditions
- Use higher quality marker print
- Increase marker size
- Move marker closer to camera
- Ensure marker stays in frame
- Reduce motion blur (move slower)
- Use higher quality camera
- Verify correct ArUco dictionary
- Clean marker surface (no smudges)

---

### Analysis Issues

#### Problem: "Missing columns: ['timestamp']"

**Cause:** CSV file doesn't have timestamp column (old format)

**Solutions:**
- Re-record trajectory with updated scripts (all now include timestamps)
- Use `live_tracker.py` or `aruco_tracker.py` for new recordings
- Migrate old CSV files:

```python
import pandas as pd

# Load old CSV
df = pd.read_csv('old_trajectory.csv')

# Assume 30 FPS (adjust as needed)
fps = 30.0
df.insert(0, 'timestamp', df['frame'] / fps)

# Save with timestamps
df.to_csv('new_trajectory.csv', index=False)
```

---

#### Problem: Very high acceleration or velocity values (unrealistic)

**Causes:**
- Tracking noise or errors
- Poor camera calibration
- Marker detection jumps
- Frame drops

**Solutions:**
- Improve camera calibration quality
- Use better lighting and camera setup
- Increase marker size
- Ensure stable camera mount
- Move marker more slowly
- Analysis script already applies automatic smoothing
- Use exported CSV to apply custom smoothing:

```python
from scipy.signal import savgol_filter

df['speed_smooth'] = savgol_filter(df['speed'], window_length=11, polyorder=3)
```

---

#### Problem: NaN or inf values in calculated metrics

**Causes:**
- Division by zero (Δt = 0)
- Duplicate timestamps
- Single data point for marker

**Solutions:**
- Check for duplicate timestamps in CSV
- Ensure multiple data points exist
- Filter out invalid values:

```python
df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna()
```

---

#### Problem: Plots don't display

**Cause:** Running on headless server, or `--no-show` flag used

**Solutions:**
```bash
# Save plots without displaying
python trajectory_analysis.py data.csv --plot all --no-show

# Generate full report (automatically saves to files)
python trajectory_analysis.py data.csv --full-report

# Then open PNG files manually
```

---

#### Problem: Animation generation fails

**Causes:**
- FFmpeg not installed
- Insufficient data points
- File permissions

**Solutions:**
- Install FFmpeg for video generation
- Script will fallback to GIF format if FFmpeg unavailable
- Use `--no-animation` to skip animation generation
- Check file write permissions in output directory
- Ensure at least 10 data points exist

---

### Performance Issues

#### Problem: Slow video processing

**Solutions:**
- Increase `FRAME_SKIP` in config.py (process every Nth frame)
- Process smaller video segments
- Use lower resolution video
- Close other CPU-intensive applications

#### Problem: Analysis takes too long

**Solutions:**
- Use `--summary` for quick statistics only
- Generate specific plots instead of `--plot all`
- Process smaller data files
- Use `--no-show` to skip plot display

---

## Best Practices

### Calibration Best Practices

#### Checkerboard Preparation

✅ **Do:**
- Print on thick, rigid paper or cardstock
- Use high-quality printer (600+ DPI)
- Mount on foam board or rigid backing
- Keep perfectly flat at all times
- Measure square size accurately with ruler
- Use matte paper (no gloss)
- Store flat when not in use
- Verify print scale with ruler before use

❌ **Don't:**
- Use wrinkled, bent, or curved paper
- Print at wrong scale (must be 100% / actual size)
- Fold, bend, or damage the pattern
- Guess square size measurements
- Use glossy paper (causes glare)
- Leave in humid conditions (can warp)

---

#### Image Collection Strategy

✅ **Do:**
- Collect 20-30 images minimum (30-40 for high precision)
- Vary angles significantly (tilt in all directions)
- Vary distances (near and far)
- Cover all frame areas (center, corners, edges)
- Use consistent, good lighting
- Keep checkerboard steady during each capture
- Ensure entire pattern visible in every frame
- Use auto-capture for consistency

❌ **Don't:**
- Rush the calibration process
- Use blurry or out-of-focus images
- Keep same angle for all images
- Keep same distance for all images
- Use poor or inconsistent lighting
- Move too quickly (causes motion blur)
- Partially occlude the pattern
- Change camera settings mid-calibration

---

#### Camera Setup

✅ **Do:**
- Use fixed focus if available (disable autofocus)
- Disable auto-exposure during calibration
- Use good, even lighting
- Mount camera on stable surface or tripod
- Use native camera resolution
- Calibrate at the resolution you'll use for tracking
- Note camera settings for future reference

❌ **Don't:**
- Change camera settings during calibration
- Use digital zoom
- Mix different cameras or resolutions
- Use very low resolution
- Change lighting mid-calibration
- Use auto-focus (can shift between frames)

---

### Tracking Best Practices

#### Marker Preparation

✅ **Do:**
- Print markers on rigid, flat surface
- Use high-quality printer (600+ DPI minimum)
- Use high-contrast print (pure black on white)
- Measure marker size precisely with ruler
- Use matte paper or laminate
- Keep markers clean
- Verify dictionary type matches config
- Use larger markers for greater distances

❌ **Don't:**
- Use wrinkled or bent surfaces
- Print on glossy paper (causes glare)
- Guess marker size
- Use damaged or smudged markers
- Print too small (reduces detection range)
- Use low-quality or faded prints

---

#### Recording Environment

✅ **Do:**
- Use good, even lighting (diffuse light best)
- Mount camera on stable surface (tripod ideal)
- Ensure clear field of view
- Test detection before recording
- Keep marker in frame at all times
- Move smoothly and deliberately
- Record for adequate duration (5-10+ seconds)

❌ **Don't:**
- Use flickering lights
- Allow strong backlighting or glare
- Move camera during recording
- Move marker too quickly
- Occlude marker during recording
- Rush movements
- Record in very low light

---

#### Calibration Requirement

✅ **Do:**
- **Always calibrate camera before tracking**
- Verify calibration quality (error < 1.0 pixels)
- Recalibrate if camera settings change
- Test calibration with known distances
- Keep calibration backups

❌ **Don't:**
- Skip calibration (accuracy will suffer!)
- Use default/placeholder calibration values
- Mix calibrations from different cameras
- Change camera resolution after calibration

---

### Analysis Best Practices

#### Data Quality

✅ **Do:**
- Review summary statistics first
- Check for outliers in plots
- Verify values are physically plausible
- Ensure adequate data points (100+ recommended)
- Check timestamp consistency
- Verify marker was detected consistently

❌ **Don't:**
- Ignore obvious outliers
- Trust unrealistic values
- Analyze very short recordings (< 2 seconds)
- Skip summary review before detailed analysis

---

#### Analysis Workflow

✅ **Do:**
- Start with `--summary` to understand data
- Generate full report for comprehensive analysis
- Export metrics to CSV for detailed work
- Compare results across multiple sessions
- Use appropriate smoothing for noisy data
- Document analysis parameters and assumptions
- Include units in all reports

❌ **Don't:**
- Jump directly to specific plots without overview
- Over-smooth data (loses real variations)
- Mix data from different markers without identifying
- Forget to note recording conditions
- Omit units from presentations

---

#### Interpretation

✅ **Do:**
- Consider measurement uncertainty
- Compare with expected physical behavior
- Cross-validate with multiple analysis methods
- Note any filtering or smoothing applied
- Document outliers and anomalies
- Use statistical significance tests where appropriate

❌ **Don't:**
- Over-interpret noise as real signal
- Ignore physical constraints (e.g., speed limits)
- Trust single outlier measurements
- Report excessive precision (beyond measurement capability)

---

## Advanced Features

### Multi-Marker Tracking

All scripts automatically support tracking multiple markers simultaneously.

**Setup:**
```bash
# Print multiple markers with different IDs
# Place in scene together
```

**Track all markers:**
```bash
python live_tracker.py
# All detected markers tracked automatically
```

**Analyze specific marker:**
```bash
# Analyze marker ID 0
python trajectory_analysis.py data.csv --marker-id 0 --full-report --output-dir marker_0

# Analyze marker ID 1
python trajectory_analysis.py data.csv --marker-id 1 --full-report --output-dir marker_1

# Compare results from different folders
```

**CSV format with multiple markers:**
```csv
timestamp,frame,marker_id,x,y,z,rx,ry,rz
0.000,0,0,0.1135,0.0684,0.3697,3.1131,-0.0130,0.0598
0.000,0,1,0.2234,0.1123,0.4512,3.0987,-0.0245,0.0634
0.039,1,0,0.1141,0.0694,0.3723,3.1244,-0.0276,0.0516
0.039,1,1,0.2241,0.1134,0.4535,3.1098,-0.0198,0.0612
```

---

### Custom Checkerboard Patterns

Generate custom calibration patterns for different scenarios:

```bash
# Large pattern for distant calibration or large camera FOV
python generate_checkerboard.py --width 11 --height 8 --square-size 30 --output large_pattern.png

# Small pattern for close-up work or small camera FOV
python generate_checkerboard.py --width 7 --height 5 --square-size 20 --output small_pattern.png

# High-DPI printing (for very high quality)
python generate_checkerboard.py --dpi 600 --output hq_pattern.png

# Custom size for specific needs
python generate_checkerboard.py --width 10 --height 7 --square-size 25 --output custom.png
```

**Pattern selection guide:**
- **Small (7x5, 20mm)**: Webcams, close range (< 0.5m), small FOV
- **Medium (9x6, 25mm)**: Standard cameras, normal range (0.3-1m), recommended default
- **Large (11x8, 30mm)**: High-res cameras, far range (> 1m), large FOV

---

### Multi-Camera Systems

Calibrate each camera separately and use distinct calibration files:

```bash
# Calibrate camera 0
python camera_calibration.py --mode live --camera 0 --output camera0_calib.npz --no-update-config

# Calibrate camera 1
python camera_calibration.py --mode live --camera 1 --output camera1_calib.npz --no-update-config

# Then manually update config.py for each camera's tracking script
# Or maintain separate config files for each camera
```

**For synchronized multi-camera tracking**, you'll need to:
1. Calibrate each camera separately
2. Load appropriate calibration for each camera in your code
3. Synchronize timestamps across cameras
4. Consider stereo calibration for precise 3D from multiple views

---

### High-Precision Calibration

For applications requiring maximum accuracy:

```bash
python camera_calibration.py --mode live \
    --num-images 40 \
    --interval 1.5 \
    --checkerboard 11x8 \
    --square-size 0.030
```

**High-precision tips:**
- Collect 40+ images
- Use larger checkerboard (11x8 or larger)
- Vary angles and distances extensively
- Use professional printer for checkerboard
- Verify square size with precision ruler
- Target reprojection error < 0.3 pixels
- Use camera with minimal distortion (high-quality lens)

---

### Batch Processing

Process multiple videos or sessions automatically:

**Windows (PowerShell):**
```powershell
# Process all MP4 files in directory
Get-ChildItem *.mp4 | ForEach-Object {
    $basename = $_.BaseName
    python aruco_tracker.py $_.Name --output "$basename.csv"
    python trajectory_analysis.py "$basename.csv" --full-report --output-dir "${basename}_analysis"
}
```

**Linux/Mac (Bash):**
```bash
# Process multiple videos
for video in *.mp4; do
    basename="${video%.mp4}"
    python aruco_tracker.py "$video" --output "${basename}.csv"
    python trajectory_analysis.py "${basename}.csv" --full-report --output-dir "${basename}_analysis"
done
```

**Python script for batch processing:**
```python
import os
import subprocess
import glob

# Find all CSV files
csv_files = glob.glob('*.csv')

for csv_file in csv_files:
    basename = os.path.splitext(csv_file)[0]
    output_dir = f"{basename}_analysis"

    # Run analysis
    subprocess.run([
        'python', 'trajectory_analysis.py',
        csv_file,
        '--full-report',
        '--output-dir', output_dir
    ])

    print(f"Processed: {csv_file} -> {output_dir}/")
```

---

### Loading Saved Calibration

Load previously saved calibration data:

```python
import numpy as np

# Load calibration from .npz file
data = np.load('calibration_data.npz')
camera_matrix = data['camera_matrix']
dist_coeffs = data['dist_coeffs']
calibration_error = data['calibration_error']

print(f"Loaded calibration with error: {calibration_error:.4f} pixels")
print(f"Camera matrix:\n{camera_matrix}")
print(f"Distortion coefficients: {dist_coeffs}")
```

---

### Custom Visualization

Create custom 3D trajectory visualizations:

```bash
# Static 3D plot
python visualize_trajectory.py data.csv --save trajectory_3d.png

# Animated video with custom settings
python visualize_trajectory.py data.csv \
    --animate \
    --video-output custom_animation.mp4 \
    --duration 15 \
    --fps 60 \
    --rotation-speed 2.0
```

**Animation options:**
- `--duration` - Video duration in seconds
- `--fps` - Frames per second (30, 60, etc.)
- `--rotation-speed` - Camera rotation speed multiplier
- Trajectory builds up over time with rotating view

---

## Python Integration Examples

### Compare Multiple Trajectories

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load multiple recording sessions
traj1 = pd.read_csv('analysis_output/session1/analysis_metrics.csv')
traj2 = pd.read_csv('analysis_output/session2/analysis_metrics.csv')
traj3 = pd.read_csv('analysis_output/session3/analysis_metrics.csv')

# Plot speed comparison
plt.figure(figsize=(12, 6))
plt.plot(traj1['timestamp'], traj1['speed'], label='Session 1', alpha=0.7)
plt.plot(traj2['timestamp'], traj2['speed'], label='Session 2', alpha=0.7)
plt.plot(traj3['timestamp'], traj3['speed'], label='Session 3', alpha=0.7)
plt.xlabel('Time (s)')
plt.ylabel('Speed (m/s)')
plt.title('Speed Comparison Across Sessions')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Compare statistics
print("Average speeds:")
print(f"  Session 1: {traj1['speed'].mean():.3f} m/s")
print(f"  Session 2: {traj2['speed'].mean():.3f} m/s")
print(f"  Session 3: {traj3['speed'].mean():.3f} m/s")

print("\nTotal distances:")
print(f"  Session 1: {traj1['cumulative_distance'].iloc[-1]:.3f} m")
print(f"  Session 2: {traj2['cumulative_distance'].iloc[-1]:.3f} m")
print(f"  Session 3: {traj3['cumulative_distance'].iloc[-1]:.3f} m")
```

---

### Custom Metric Calculation

```python
import pandas as pd
import numpy as np

# Load trajectory data
df = pd.read_csv('live_trajectory.csv')

# Calculate custom metrics
df['distance_from_origin'] = np.sqrt(df['x']**2 + df['y']**2 + df['z']**2)
df['horizontal_distance'] = np.sqrt(df['x']**2 + df['y']**2)

# Calculate time in zones
close_zone = df[df['z'] < 0.5]
mid_zone = df[(df['z'] >= 0.5) & (df['z'] < 1.0)]
far_zone = df[df['z'] >= 1.0]

print(f"Time in close zone (< 0.5m): {close_zone['timestamp'].count() / 30:.2f}s")
print(f"Time in mid zone (0.5-1.0m): {mid_zone['timestamp'].count() / 30:.2f}s")
print(f"Time in far zone (> 1.0m): {far_zone['timestamp'].count() / 30:.2f}s")

# Find peak speed and location
peak_idx = df['speed'].idxmax()
peak_speed = df.loc[peak_idx, 'speed']
peak_location = df.loc[peak_idx, ['x', 'y', 'z']].values

print(f"\nPeak speed: {peak_speed:.3f} m/s")
print(f"Location at peak: x={peak_location[0]:.3f}, y={peak_location[1]:.3f}, z={peak_location[2]:.3f}")
```

---

### Advanced Filtering and Smoothing

```python
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter, butter, filtfilt

df = pd.read_csv('trajectory.csv')

# Apply Savitzky-Golay smoothing
window_length = 11  # Must be odd
polyorder = 3
df['x_smooth'] = savgol_filter(df['x'], window_length, polyorder)
df['y_smooth'] = savgol_filter(df['y'], window_length, polyorder)
df['z_smooth'] = savgol_filter(df['z'], window_length, polyorder)

# Apply Butterworth low-pass filter
def butter_lowpass_filter(data, cutoff_freq, sampling_rate, order=4):
    nyquist = 0.5 * sampling_rate
    normal_cutoff = cutoff_freq / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)

sampling_rate = 1.0 / df['timestamp'].diff().mean()  # Hz
cutoff_frequency = 5.0  # Hz

df['x_filtered'] = butter_lowpass_filter(df['x'], cutoff_frequency, sampling_rate)
df['y_filtered'] = butter_lowpass_filter(df['y'], cutoff_frequency, sampling_rate)
df['z_filtered'] = butter_lowpass_filter(df['z'], cutoff_frequency, sampling_rate)

# Save filtered data
df.to_csv('trajectory_filtered.csv', index=False)
```

---

### Statistical Analysis

```python
import pandas as pd
import numpy as np
from scipy import stats

# Load data
df = pd.read_csv('analysis_output/analysis_metrics.csv')

# Calculate statistical measures
print("Position Statistics (X-axis):")
print(f"  Mean: {df['x'].mean():.3f} m")
print(f"  Std Dev: {df['x'].std():.3f} m")
print(f"  Median: {df['x'].median():.3f} m")
print(f"  IQR: {stats.iqr(df['x']):.3f} m")

# Test for normality (important for some statistical tests)
statistic, p_value = stats.shapiro(df['speed'].dropna())
print(f"\nSpeed normality test: p-value = {p_value:.4f}")
if p_value > 0.05:
    print("  Speed distribution is approximately normal")
else:
    print("  Speed distribution is not normal")

# Calculate confidence intervals
confidence_level = 0.95
speed_mean = df['speed'].mean()
speed_sem = stats.sem(df['speed'].dropna())
confidence_interval = stats.t.interval(confidence_level,
                                       len(df['speed'].dropna())-1,
                                       loc=speed_mean,
                                       scale=speed_sem)
print(f"\n95% Confidence Interval for speed:")
print(f"  {confidence_interval[0]:.3f} to {confidence_interval[1]:.3f} m/s")

# Detect outliers using IQR method
Q1 = df['speed'].quantile(0.25)
Q3 = df['speed'].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df['speed'] < Q1 - 1.5*IQR) | (df['speed'] > Q3 + 1.5*IQR)]
print(f"\nOutliers detected: {len(outliers)} points ({len(outliers)/len(df)*100:.1f}%)")
```

---

## File Structure

```
tagCalibration/
├── venv/                           # Virtual environment
├── config.py                       # Configuration parameters
│
├── # Tracking Scripts
├── live_tracker.py                 # Live camera tracking with recording controls
├── aruco_tracker.py                # Video file processing
│
├── # Calibration Scripts
├── camera_calibration.py           # Camera calibration (live/video/images)
├── generate_checkerboard.py        # Checkerboard pattern generator
│
├── # Analysis Scripts
├── trajectory_analysis.py          # Comprehensive motion analysis
├── visualize_trajectory.py         # 3D plots and animations
├── visualize_on_video.py           # Video overlay with 3D coords
│
├── # Utility Scripts
├── test_aruco_dictionaries.py      # ArUco dictionary detection
│
├── # Documentation
├── README.md                       # This comprehensive guide
│
├── # Dependencies
├── requirements.txt                # Python package requirements
│
└── # Generated Files (examples)
    ├── calibration_data.npz        # Camera calibration backup
    ├── camera0_calib.npz           # Multi-camera calibrations
    ├── checkerboard.png            # Generated calibration pattern
    ├── live_trajectory.csv         # Live tracking trajectory data
    ├── live_animation.mp4          # 3D trajectory animation
    ├── trajectory_data.csv         # Video processing output
    ├── output_with_3d_coords.mp4   # Annotated video
    └── analysis_output/            # Analysis results directory
        ├── position_vs_time.png    # Position plot
        ├── velocity_analysis.png   # Velocity plot
        ├── distance_analysis.png   # Distance plot
        ├── angular_analysis.png    # Angular plot
        ├── acceleration_analysis.png # Acceleration plot
        └── analysis_metrics.csv    # Exported metrics
```

---

## Dependencies

All dependencies are listed in `requirements.txt`:

```
opencv-contrib-python>=4.5.0  # ArUco detection, camera calibration
numpy>=1.19.0                 # Numerical operations, arrays
matplotlib>=3.3.0             # Plotting, visualization, animations
pandas>=1.1.0                 # Data analysis, CSV handling
scipy>=1.5.0                  # Signal processing, smoothing filters
```

**Install all dependencies:**
```bash
pip install -r requirements.txt
```

**Individual installation:**
```bash
pip install opencv-contrib-python numpy matplotlib pandas scipy
```

---

## Example Workflows

### Workflow 1: First-Time Setup and Live Tracking

```bash
# 1. Setup environment
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Generate checkerboard
python generate_checkerboard.py --output checkerboard.png
# Print at 100% scale, mount on rigid board

# 3. Calibrate camera (REQUIRED)
python camera_calibration.py --mode live
# Follow on-screen instructions, collect 20-30 images

# 4. Track live
python live_tracker.py --marker-size 0.05
# Press SPACE to record, Q to quit

# 5. Analyze trajectory
python trajectory_analysis.py live_trajectory.csv --full-report

# 6. Review results
# - Check analysis_output/ folder for plots
# - Open analysis_metrics.csv in Excel
# - Watch live_animation.mp4
```

---

### Workflow 2: Video Processing and Analysis

```bash
# 1. Detect dictionary type (if unknown)
python test_aruco_dictionaries.py video.mp4
# Update config.py with recommended dictionary

# 2. Process video
python aruco_tracker.py video.mp4 --marker-size 0.05 --output trajectory.csv

# 3. Full analysis
python trajectory_analysis.py trajectory.csv --full-report

# 4. Create annotated video
python visualize_on_video.py video.mp4 --output annotated.mp4

# 5. Custom 3D animation
python visualize_trajectory.py trajectory.csv --animate --duration 15 --video-output custom_anim.mp4
```

---

### Workflow 3: Research Study with Multiple Trials

```bash
# 1. One-time camera calibration
python camera_calibration.py --mode live --num-images 30

# 2. Record multiple trials
python live_tracker.py --output trial1.csv --animation trial1_anim.mp4
python live_tracker.py --output trial2.csv --animation trial2_anim.mp4
python live_tracker.py --output trial3.csv --animation trial3_anim.mp4

# 3. Analyze each trial separately
python trajectory_analysis.py trial1.csv --full-report --output-dir trial1_analysis
python trajectory_analysis.py trial2.csv --full-report --output-dir trial2_analysis
python trajectory_analysis.py trial3.csv --full-report --output-dir trial3_analysis

# 4. Compare in Excel or Python
# - Open trial*_analysis/analysis_metrics.csv
# - Create comparison charts
# - Calculate statistics across trials
```

---

### Workflow 4: Multi-Marker Tracking

```bash
# 1. Print multiple markers (IDs 0, 1, 2, etc.)
# 2. Place all markers in scene

# 3. Track all markers
python live_tracker.py --output multi_marker_session.csv

# 4. Analyze each marker separately
python trajectory_analysis.py multi_marker_session.csv --marker-id 0 --full-report --output-dir marker_0
python trajectory_analysis.py multi_marker_session.csv --marker-id 1 --full-report --output-dir marker_1
python trajectory_analysis.py multi_marker_session.csv --marker-id 2 --full-report --output-dir marker_2

# 5. Compare marker behaviors
# Use Python to load and compare analysis_metrics.csv from each folder
```

---

## License

This project is open source and available for educational and research purposes.

---

## Support and Contributing

For issues, questions, or feature requests:

1. **Check this documentation first** - Most common questions are answered here
2. **Review troubleshooting section** - Common problems and solutions
3. **Verify your setup** - Ensure calibration is done correctly
4. **Test with known configurations** - Use recommended settings first

**Common support topics:**
- **Calibration problems**: See [Camera Calibration Issues](#camera-calibration-issues)
- **Tracking problems**: See [Tracking Issues](#tracking-issues)
- **Analysis questions**: See [Analysis Issues](#analysis-issues)
- **Python integration**: See [Python Integration Examples](#python-integration-examples)

---

**Version:** 3.0 (Consolidated Documentation)

**Features:**
- ✅ Camera Calibration (Live/Video/Images)
- ✅ Live Tracking with Interactive Controls
- ✅ Video Processing with Timestamps
- ✅ Comprehensive Trajectory Analysis (5 plot types)
- ✅ 3D Visualization and Animation
- ✅ Multi-Marker Support
- ✅ Data Export (CSV)
- ✅ Full Timestamp Support

**Documentation Status:** Complete and Consolidated
