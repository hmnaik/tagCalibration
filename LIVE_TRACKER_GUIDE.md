# Live ArUco Tracker - Quick Start Guide

## Overview

The Live Tracker allows you to record ArUco marker trajectories in real-time from your webcam and automatically generate 3D animation videos.

## Quick Start

```bash
# Activate virtual environment
venv\Scripts\activate

# Run live tracker
python live_tracker.py
```

## Controls

| Key | Action |
|-----|--------|
| **SPACE** | Start/Stop recording trajectory data |
| **Q** | Quit and generate 3D animation |

## On-Screen Display

The live view shows:
- **Status**: RECORDING (green) or STANDBY (orange)
- **Time**: Elapsed time since start
- **Frames**: Current frame count
- **Data points**: Number of trajectory points recorded
- **Detection**: Whether marker is currently detected
- **3D Axes**: Red (X), Green (Y), Blue (Z)
- **Position**: Real-time X, Y, Z coordinates in meters

## Workflow

### 1. Setup
- Print an ArUco marker (4x4_50 dictionary recommended)
- Measure the marker size in meters
- Update `config.py` with marker size:
  ```python
  MARKER_SIZE = 0.05  # 5cm marker
  ```

### 2. Run
```bash
python live_tracker.py --marker-size 0.05
```

### 3. Record
1. Camera window opens showing live feed
2. Position ArUco marker in view
3. Press **SPACE** to start recording (status turns green)
4. Move the marker through 3D space
5. Press **SPACE** to stop recording

### 4. Exit
- Press **Q** to quit
- Script automatically saves:
  - `live_trajectory.csv` - trajectory data
  - `live_animation.mp4` - 3D animation video

## Command Line Options

```bash
python live_tracker.py [options]
```

### Options:

| Option | Description | Default |
|--------|-------------|---------|
| `--camera ID` | Camera device ID | 0 |
| `--marker-size SIZE` | Marker size in meters | From config.py |
| `--output FILE` | CSV output file | live_trajectory.csv |
| `--animation FILE` | Animation output file | live_animation.mp4 |
| `--no-animation` | Skip animation generation | False |

### Examples:

```bash
# Use specific camera and marker size
python live_tracker.py --camera 1 --marker-size 0.08

# Custom output files
python live_tracker.py --output my_data.csv --animation my_video.mp4

# Skip animation generation
python live_tracker.py --no-animation
```

## Output Files

### 1. Trajectory CSV (`live_trajectory.csv`)
Contains:
- `frame`: Frame number
- `marker_id`: ArUco marker ID
- `x, y, z`: 3D position in meters
- `rx, ry, rz`: Rotation in radians

### 2. Animation Video (`live_animation.mp4`)
Features:
- 3D trajectory visualization
- Rotating camera view
- Building trajectory animation
- Coordinate axes display
- 10 seconds duration at 30 FPS

## Tips for Best Results

### Camera Setup
- Use good lighting (avoid shadows)
- Position camera at comfortable distance
- Ensure stable camera mounting
- Use high-quality webcam if possible

### Marker Setup
- Print marker on flat, rigid surface
- Use high-quality printer (avoid smudges)
- Measure marker size accurately
- Keep marker clean and unwrinkled

### Recording
- Start with marker clearly visible
- Move slowly and smoothly
- Keep marker in frame
- Avoid rapid rotations
- Record for at least 5-10 seconds

### Troubleshooting

**No marker detected:**
- Check marker is in focus
- Verify marker dictionary matches config
- Improve lighting
- Run `test_aruco_dictionaries.py` to verify dictionary type

**Jittery tracking:**
- Improve lighting
- Use larger marker
- Calibrate camera properly
- Move marker more slowly

**No camera found:**
- Check camera permissions
- Try different `--camera` ID (0, 1, 2, etc.)
- Ensure camera is not in use by another app

**Animation not generated:**
- Check for error messages
- Ensure FFmpeg is installed
- Will fallback to GIF if FFmpeg unavailable
- Use `--no-animation` to skip

## Camera Calibration

For accurate 3D measurements, calibrate your camera:

1. Print a checkerboard pattern
2. Record video of checkerboard from different angles
3. Use OpenCV calibration tools
4. Update `config.py` with results:

```python
CAMERA_MATRIX = [
    [fx, 0, cx],
    [0, fy, cy],
    [0, 0, 1]
]

DIST_COEFFS = [k1, k2, p1, p2, k3]
```

## Advanced Usage

### Multiple Recording Sessions

Press SPACE multiple times during one session:
- First SPACE: Start recording
- Second SPACE: Stop recording (keeps data)
- Third SPACE: Start new recording (clears previous data)
- Q: Quit and process last recording

### Integration with Other Scripts

```bash
# 1. Record live trajectory
python live_tracker.py --output session1.csv

# 2. Create custom visualization
python visualize_trajectory.py session1.csv --animate --duration 15

# 3. Analyze specific marker
python visualize_trajectory.py session1.csv --marker-id 0 --save analysis.png
```

## Keyboard Shortcuts Summary

```
┌─────────────────────────────────────┐
│  LIVE ARUCO TRACKER CONTROLS        │
├─────────────────────────────────────┤
│  SPACE  │ Toggle Recording          │
│  Q      │ Quit & Generate Animation │
└─────────────────────────────────────┘
```

## What Gets Saved vs Not Saved

✅ **SAVED:**
- Trajectory data (CSV file)
- 3D animation video
- Statistics and logs

❌ **NOT SAVED:**
- Live webcam video
- Individual frames
- Temporary data

This saves disk space while keeping the important trajectory data and visualization!

## Example Output

After running the live tracker, you'll see:

```
TRACKING SUMMARY
============================================================
Total frames processed: 450
Frames with detections: 387
Detection rate: 86.0%
Trajectory data points: 387
============================================================

Trajectory saved: live_trajectory.csv

Generating 3D animation video...
Creating 3D animation video: live_animation.mp4
Duration: 10s, FPS: 30
Generating frames...
Saving video (this may take a while)...
Video saved successfully: live_animation.mp4
```

## Next Steps

After recording, you can:
1. View the 3D animation video
2. Analyze the CSV data in Excel/Python
3. Create custom visualizations
4. Compare multiple recordings
5. Export data for further processing

Enjoy tracking! 🎥📊
