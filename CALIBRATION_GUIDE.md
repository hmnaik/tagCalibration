# Camera Calibration Guide

## Overview

Camera calibration is **essential** for accurate 3D ArUco marker tracking. This module provides three calibration methods:

1. **Live Camera** - Interactive real-time calibration
2. **Video File** - Calibrate from pre-recorded video
3. **Image Files** - Calibrate from multiple images

## Quick Start

### 1. Generate Checkerboard Pattern

```bash
# Generate standard 9x6 checkerboard (25mm squares)
python generate_checkerboard.py --output checkerboard.png

# Custom size (e.g., 7x5 with 30mm squares)
python generate_checkerboard.py --width 7 --height 5 --square-size 30 --output my_checkerboard.png
```

**Print the checkerboard:**
- Use high-quality printer
- Print at 100% scale (Actual Size)
- DO NOT resize or fit to page
- Use thick paper or cardstock
- Mount on rigid, flat surface
- Verify square size with ruler

### 2. Run Calibration

**Live Camera (Recommended):**
```bash
python camera_calibration.py --mode live --checkerboard 9x6 --square-size 0.025
```

**From Video:**
```bash
python camera_calibration.py --mode video --input calibration_video.mp4 --checkerboard 9x6 --square-size 0.025
```

**From Images:**
```bash
python camera_calibration.py --mode images --input "calib_images/*.jpg" --checkerboard 9x6 --square-size 0.025
```

### 3. Results

After calibration:
- ✅ `config.py` automatically updated
- ✅ `calibration_data.npz` saved (backup)
- ✅ Reprojection error displayed
- ✅ Ready to use for ArUco tracking!

## Detailed Instructions

### Method 1: Live Camera Calibration (Interactive)

**Advantages:**
- Real-time feedback
- Interactive capture control
- Best for beginners
- Immediate quality check

**Steps:**

```bash
python camera_calibration.py --mode live --num-images 25 --interval 2.0
```

**In the live window:**

1. **Position checkerboard** in camera view
2. **Press C** to start auto-capture (captures every 2 seconds)
3. **Move checkerboard** slowly:
   - Different distances (near/far)
   - Different angles (tilted left/right/up/down)
   - Different positions (center/corners/edges)
4. **Press SPACE** to manually capture good frames
5. **Press Q** when enough images collected

**Controls:**
| Key | Action |
|-----|--------|
| **C** | Toggle auto-capture ON/OFF |
| **SPACE** | Manual capture |
| **Q** | Quit and calibrate |

**Tips for Best Results:**
- Keep checkerboard flat and rigid
- Use good, even lighting
- Avoid glare and shadows
- Move slowly and smoothly
- Cover entire camera view
- Capture 20-30 images minimum
- Vary distance and angles

### Method 2: Video File Calibration

**Advantages:**
- Use pre-recorded video
- Process offline
- Can review video first

**Steps:**

1. Record video with checkerboard:
   ```bash
   # Move checkerboard around while recording
   # 30-60 seconds is enough
   ```

2. Run calibration:
   ```bash
   python camera_calibration.py --mode video \
       --input my_calibration.mp4 \
       --checkerboard 9x6 \
       --square-size 0.025 \
       --sample-interval 30
   ```

**Recording Tips:**
- Record 30-60 seconds
- Move checkerboard slowly
- Cover all areas of frame
- Vary distance and angles
- Keep checkerboard in frame
- Avoid motion blur

### Method 3: Image Files Calibration

**Advantages:**
- Full control over images
- Can verify each image
- Easy to retake bad images

**Steps:**

1. Capture images (use any camera or webcam software):
   - Save 20-30 images
   - Name them: calib_001.jpg, calib_002.jpg, etc.
   - Put in folder: `calib_images/`

2. Run calibration:
   ```bash
   python camera_calibration.py --mode images \
       --input "calib_images/*.jpg" \
       --checkerboard 9x6 \
       --square-size 0.025
   ```

**Image Requirements:**
- Checkerboard clearly visible
- Good focus (not blurry)
- Entire checkerboard in frame
- Variety of positions/angles
- Good lighting

## Checkerboard Patterns

### Standard Sizes

| Pattern | Inner Corners | Square Size | Total Size | Use Case |
|---------|---------------|-------------|------------|----------|
| Small | 7x5 | 20mm | 160x120mm | Webcam, close range |
| Medium | 9x6 | 25mm | 250x175mm | Standard (recommended) |
| Large | 11x8 | 30mm | 360x270mm | High-res camera, far range |

### Generate Custom Pattern

```bash
# Large pattern for distant calibration
python generate_checkerboard.py --width 11 --height 8 --square-size 30

# Small pattern for closeup
python generate_checkerboard.py --width 7 --height 5 --square-size 20

# High-DPI printing
python generate_checkerboard.py --dpi 600
```

## Command-Line Reference

```bash
python camera_calibration.py --mode <MODE> [OPTIONS]
```

### Required Arguments:
- `--mode {live,video,images}` - Calibration mode

### Common Options:
- `--checkerboard WxH` - Pattern size (e.g., 9x6) [default: 9x6]
- `--square-size SIZE` - Square size in meters [default: 0.025]
- `--output FILE` - Save calibration to file [default: calibration_data.npz]
- `--no-update-config` - Don't update config.py

### Live Mode Options:
- `--camera ID` - Camera device ID [default: 0]
- `--num-images N` - Target number of images [default: 20]
- `--interval SECONDS` - Auto-capture interval [default: 2.0]

### Video Mode Options:
- `--input VIDEO` - Input video file (required)
- `--sample-interval N` - Sample every Nth frame [default: 30]

### Images Mode Options:
- `--input PATTERN` - Image file pattern (required)
  - Examples: `"images/*.jpg"`, `"calib*.png"`, `"C:/photos/*.bmp"`

## Understanding Results

### Calibration Output

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

### Reprojection Error Interpretation

| Error (pixels) | Quality | Action |
|----------------|---------|--------|
| < 0.5 | Excellent | Perfect! Use it |
| 0.5 - 1.0 | Good | Acceptable for most uses |
| 1.0 - 2.0 | Acceptable | Consider recalibrating |
| > 2.0 | Poor | Recalibrate required |

**High error causes:**
- Not enough images (need 20+)
- Inaccurate checkerboard measurements
- Motion blur in images
- Checkerboard not flat
- Poor image variety

## Troubleshooting

### Problem: "No checkerboard detected"

**Solutions:**
- Ensure pattern size matches (`--checkerboard 9x6`)
- Check checkerboard is flat, not curved
- Improve lighting
- Move closer to camera
- Ensure entire pattern is visible
- Check if checkerboard is in focus

### Problem: "Need at least 10 images"

**Solutions:**
- Capture more images with checkerboard visible
- Move checkerboard more slowly
- Improve lighting
- Ensure checkerboard is in focus

### Problem: High reprojection error (> 1.0)

**Solutions:**
- Recalibrate with more images (25-30)
- Verify square size measurement
- Ensure checkerboard is rigid and flat
- Use better quality images
- Vary angles and positions more
- Check printer settings (100% scale)

### Problem: Camera not found

**Solutions:**
- Try different camera ID: `--camera 1` or `--camera 2`
- Check camera permissions
- Close other apps using camera
- Reconnect USB camera

### Problem: Wrong square size

**Solutions:**
- Measure with ruler (in millimeters)
- Convert to meters: 25mm = 0.025m
- Update command: `--square-size 0.025`
- Reprint checkerboard if needed

## Best Practices

### 1. Checkerboard Quality
✅ **Do:**
- Print on thick, rigid paper
- Use high-quality printer
- Mount on foam board
- Keep perfectly flat
- Measure squares accurately

❌ **Don't:**
- Use wrinkled paper
- Print at wrong scale
- Use curved surface
- Fold or bend
- Guess square size

### 2. Image Collection
✅ **Do:**
- Collect 20-30 images
- Vary angles (tilted)
- Vary distances (near/far)
- Cover all frame areas
- Use good lighting
- Keep checkerboard steady

❌ **Don't:**
- Rush the process
- Use blurry images
- Keep same angle
- Keep same distance
- Use poor lighting
- Move too fast

### 3. Camera Setup
✅ **Do:**
- Use fixed focus if available
- Disable auto-exposure during capture
- Use good, even lighting
- Keep camera stable
- Use native resolution

❌ **Don't:**
- Change camera settings mid-calibration
- Use digital zoom
- Mix different cameras
- Use low resolution

## Advanced Usage

### Multi-Camera System

Calibrate each camera separately:

```bash
# Camera 0
python camera_calibration.py --mode live --camera 0 --output camera0_calib.npz --no-update-config

# Camera 1
python camera_calibration.py --mode live --camera 1 --output camera1_calib.npz --no-update-config
```

### High-Precision Calibration

```bash
python camera_calibration.py --mode live \
    --num-images 40 \
    --interval 1.5 \
    --checkerboard 11x8 \
    --square-size 0.030
```

### Loading Saved Calibration

```python
import numpy as np

# Load calibration
data = np.load('calibration_data.npz')
camera_matrix = data['camera_matrix']
dist_coeffs = data['dist_coeffs']
error = data['calibration_error']

print(f"Loaded calibration with error: {error:.4f} pixels")
```

### Manual config.py Update

If you need to manually update config.py:

```python
CAMERA_MATRIX = [
    [fx, 0, cx],
    [0, fy, cy],
    [0, 0, 1]
]

DIST_COEFFS = [k1, k2, p1, p2, k3]
```

Replace values from calibration output.

## Integration with ArUco Tracking

After calibration, the scripts automatically use the new calibration:

```bash
# Live tracking (uses updated config.py)
python live_tracker.py

# Video processing (uses updated config.py)
python aruco_tracker.py video.mp4

# All scripts now use accurate calibration!
```

## Validation

Test calibration accuracy:

```bash
# Track a known-size ArUco marker
python live_tracker.py --marker-size 0.05

# Move marker to known distance (e.g., 0.5m)
# Check if reported Z position ≈ 0.5m
# Error should be < 5%
```

## Summary

### Checklist

- [ ] Generate checkerboard pattern
- [ ] Print at 100% scale
- [ ] Mount on rigid surface
- [ ] Measure square size
- [ ] Run calibration (20+ images)
- [ ] Check reprojection error < 1.0
- [ ] Verify config.py updated
- [ ] Test with ArUco tracking

### Quick Commands

```bash
# 1. Generate pattern
python generate_checkerboard.py

# 2. Calibrate
python camera_calibration.py --mode live

# 3. Test
python live_tracker.py
```

Done! Your camera is now calibrated for accurate 3D tracking! 🎯
