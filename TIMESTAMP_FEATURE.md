# Timestamp Feature - Documentation

## Overview

Both the **live tracker** and **video processor** now include timestamp functionality in CSV output and video display.

## Changes Made

### 1. Live Tracker (`live_tracker.py`)

#### CSV Output
- **New Column**: `timestamp` (first column)
- **Format**: Seconds since recording started (relative time)
- **Precision**: Float with millisecond accuracy
- **Example**: `0.0, 0.125, 0.250, 0.375...`

#### Video Display
- **New Overlay**: "Rec Time: X.XXs" shown during recording
- **Location**: Top-right corner (cyan color)
- **Updates**: Real-time during recording

#### Console Output
When stopping recording:
```
[RECORDING STOPPED]
Captured 245 data points
Recording duration: 12.45 seconds
```

### 2. Video Processor (`aruco_tracker.py`)

#### CSV Output
- **New Column**: `timestamp` (first column)
- **Format**: Seconds calculated from frame number and FPS
- **Formula**: `timestamp = frame_number / fps`
- **Example**: At 30 FPS: frame 30 = 1.0 second

## CSV File Format

### New Format (with timestamps):
```csv
timestamp,frame,marker_id,x,y,z,rx,ry,rz
0.000,0,0,0.1135,0.0684,0.3697,3.1131,-0.0130,0.0598
0.039,1,0,0.1141,0.0694,0.3723,3.1244,-0.0276,0.0516
0.078,2,0,0.1150,0.0705,0.3755,3.1076,-0.0110,0.0294
```

### Column Descriptions:
| Column | Type | Unit | Description |
|--------|------|------|-------------|
| **timestamp** | float | seconds | Time since start (live) or from video start |
| frame | int | - | Frame number |
| marker_id | int | - | ArUco marker ID |
| x, y, z | float | meters | 3D position |
| rx, ry, rz | float | radians | 3D rotation |

## Usage Examples

### Live Tracker with Timestamps

```bash
# Run live tracker
python live_tracker.py --output my_data.csv

# During recording, you'll see:
# - "Rec Time: 5.23s" on screen
# - Timestamp in CSV starts at 0.0 when you press SPACE
```

### Video Processor with Timestamps

```bash
# Process video
python aruco_tracker.py video.mp4 --output trajectory.csv

# Timestamps calculated from FPS:
# - Frame 0 at 30 FPS = 0.000s
# - Frame 30 at 30 FPS = 1.000s
# - Frame 60 at 30 FPS = 2.000s
```

## Data Analysis with Timestamps

### Python Example

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
plt.show()

# Calculate velocity
df['velocity_x'] = df['x'].diff() / df['timestamp'].diff()

# Find average position over time period
start_time = 2.0  # seconds
end_time = 5.0
subset = df[(df['timestamp'] >= start_time) & (df['timestamp'] <= end_time)]
avg_position = subset[['x', 'y', 'z']].mean()
print(f"Average position: {avg_position}")
```

### Excel/Spreadsheet Usage

1. Open CSV in Excel/Google Sheets
2. Create charts using timestamp as X-axis
3. Calculate time differences: `=B2-B1` (for consecutive rows)
4. Filter by time range: Use AutoFilter on timestamp column
5. Calculate statistics over time periods

## Time Synchronization

### Live Tracker
- Timestamp starts at **0.0** when you press SPACE to start recording
- Independent of when you start the program
- Multiple recordings in one session each start at 0.0

### Video Processor
- Timestamp starts at **0.0** at first frame of video
- Calculated based on video FPS
- Accurate for constant frame rate videos
- May drift for variable frame rate videos

## Benefits

### 1. Temporal Analysis
- Track how position changes over time
- Calculate velocities and accelerations
- Identify time-specific events

### 2. Data Synchronization
- Sync with external sensors
- Correlate with other time-series data
- Match with video playback time

### 3. Performance Metrics
- Measure movement duration
- Calculate average speeds
- Analyze motion patterns

### 4. Debugging
- Identify when markers were lost
- Check frame timing issues
- Verify recording intervals

## Video Display Features

### Live Tracker Display

```
┌─────────────────────────────────────────┐
│ RECORDING                               │
│ Time: 15.3s | Frames: 458              │
│                                         │
│      [Live Camera Feed]                 │
│      with ArUco markers                 │
│                                         │
│ Data points: 245        Rec Time: 5.67s│
│ Marker Detected                         │
└─────────────────────────────────────────┘
```

### Display Elements:
- **Time**: Total elapsed time since program start
- **Frames**: Total frames processed
- **Rec Time**: Recording timestamp (only when recording)
- **Data points**: Number of trajectory points saved

## Backward Compatibility

⚠️ **Note**: The CSV format has changed!

### Old Format:
```csv
frame,marker_id,x,y,z,rx,ry,rz
```

### New Format:
```csv
timestamp,frame,marker_id,x,y,z,rx,ry,rz
```

### Migration:
If you have old CSV files without timestamps, you can add them:

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

## Example Use Cases

### 1. Motion Analysis
```python
# Calculate distance traveled over time
import numpy as np

df = pd.read_csv('trajectory.csv')
df['distance'] = np.sqrt(
    df['x'].diff()**2 +
    df['y'].diff()**2 +
    df['z'].diff()**2
)
df['cumulative_distance'] = df['distance'].cumsum()

# Plot distance vs time
plt.plot(df['timestamp'], df['cumulative_distance'])
plt.xlabel('Time (s)')
plt.ylabel('Distance Traveled (m)')
plt.show()
```

### 2. Speed Calculation
```python
# Calculate instantaneous speed
df['dt'] = df['timestamp'].diff()
df['dx'] = df['x'].diff()
df['dy'] = df['y'].diff()
df['dz'] = df['z'].diff()

df['speed'] = np.sqrt(df['dx']**2 + df['dy']**2 + df['dz']**2) / df['dt']
print(f"Average speed: {df['speed'].mean():.3f} m/s")
print(f"Max speed: {df['speed'].max():.3f} m/s")
```

### 3. Time-Based Filtering
```python
# Extract data from specific time range
start = 5.0  # Start at 5 seconds
end = 10.0   # End at 10 seconds

segment = df[(df['timestamp'] >= start) & (df['timestamp'] <= end)]
print(f"Found {len(segment)} points in time range")
```

## Troubleshooting

### Issue: Timestamps all zero
**Cause**: Recording wasn't started (SPACE not pressed in live tracker)
**Solution**: Press SPACE to start recording

### Issue: Irregular timestamps in live tracker
**Cause**: Frame rate drops due to processing load
**Solution**: This is normal - timestamps reflect actual capture time

### Issue: Timestamps don't match video playback
**Cause**: Variable frame rate video
**Solution**: Use live tracker for accurate timestamps, or re-encode video to constant frame rate

## Summary

✅ **Timestamp column added to CSV** (first column)
✅ **Live tracker** - Real-time recording timestamp
✅ **Video processor** - Calculated from FPS
✅ **On-screen display** - Shows recording time
✅ **Console output** - Shows recording duration
✅ **Full precision** - Float values with milliseconds

All scripts now provide temporal data for comprehensive motion analysis!
