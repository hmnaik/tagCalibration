"""
Live ArUco Marker Tracker
Records from webcam, displays real-time 3D tracking, saves trajectory, and generates 3D animation
"""

import cv2
import numpy as np
import csv
import argparse
import time
from pathlib import Path
import config
from visualize_trajectory import TrajectoryVisualizer


class LiveArucoTracker:
    def __init__(self, marker_size=None, camera_matrix=None, dist_coeffs=None, camera_id=0):
        """
        Initialize the live ArUco tracker

        Args:
            marker_size: Size of the ArUco marker in meters
            camera_matrix: Camera intrinsic matrix (3x3)
            dist_coeffs: Camera distortion coefficients
            camera_id: Camera device ID (default: 0)
        """
        # Use config values if not provided
        self.marker_size = marker_size if marker_size is not None else config.MARKER_SIZE

        if camera_matrix is not None:
            self.camera_matrix = np.array(camera_matrix, dtype=np.float32)
        else:
            self.camera_matrix = np.array(config.CAMERA_MATRIX, dtype=np.float32)

        if dist_coeffs is not None:
            self.dist_coeffs = np.array(dist_coeffs, dtype=np.float32)
        else:
            self.dist_coeffs = np.array(config.DIST_COEFFS, dtype=np.float32)

        # Get ArUco dictionary
        aruco_dict_name = config.ARUCO_DICT_TYPE
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(
            getattr(cv2.aruco, aruco_dict_name)
        )
        self.aruco_params = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.aruco_params)

        # Camera
        self.camera_id = camera_id
        self.cap = None

        # Storage for trajectory data
        self.trajectory_data = []
        self.frame_count = 0
        self.start_time = None
        self.recording = False
        self.recording_start_time = None

    def draw_axis(self, frame, rvec, tvec, length=0.03):
        """
        Draw 3D coordinate axes on the frame

        Args:
            frame: Input image frame
            rvec: Rotation vector
            tvec: Translation vector
            length: Length of the axes in meters
        """
        # Define 3D points for the axes
        axis_points = np.float32([
            [0, 0, 0],
            [length, 0, 0],  # X-axis (red)
            [0, length, 0],  # Y-axis (green)
            [0, 0, length]   # Z-axis (blue)
        ]).reshape(-1, 3)

        # Project 3D points to 2D image plane
        img_points, _ = cv2.projectPoints(
            axis_points, rvec, tvec, self.camera_matrix, self.dist_coeffs
        )

        img_points = img_points.astype(int)

        # Draw axes
        origin = tuple(img_points[0].ravel())
        frame = cv2.line(frame, origin, tuple(img_points[1].ravel()), (0, 0, 255), 3)  # X (red)
        frame = cv2.line(frame, origin, tuple(img_points[2].ravel()), (0, 255, 0), 3)  # Y (green)
        frame = cv2.line(frame, origin, tuple(img_points[3].ravel()), (255, 0, 0), 3)  # Z (blue)

        return frame

    def annotate_frame(self, frame, corners, ids, rvecs, tvecs):
        """
        Annotate frame with marker information and 3D coordinates

        Args:
            frame: Input image frame
            corners: Detected marker corners
            ids: Detected marker IDs
            rvecs: Rotation vectors
            tvecs: Translation vectors

        Returns:
            Annotated frame
        """
        if ids is None:
            return frame

        # Draw detected markers
        frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        for i, marker_id in enumerate(ids):
            rvec = rvecs[i][0]
            tvec = tvecs[i][0]

            # Draw 3D axes
            frame = self.draw_axis(frame, rvec, tvec, length=self.marker_size * 0.6)

            # Get marker corner for text placement
            corner = corners[i][0][0]  # Top-left corner
            text_pos = (int(corner[0]), int(corner[1]) - 10)

            # Display 3D position
            pos_text = f"ID:{marker_id[0]} X:{tvec[0]:.3f} Y:{tvec[1]:.3f} Z:{tvec[2]:.3f}m"

            # Add background rectangle for better text visibility
            (text_width, text_height), _ = cv2.getTextSize(
                pos_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2
            )
            cv2.rectangle(
                frame,
                (text_pos[0] - 5, text_pos[1] - text_height - 5),
                (text_pos[0] + text_width + 5, text_pos[1] + 5),
                (0, 0, 0),
                -1
            )

            # Draw text
            cv2.putText(
                frame, pos_text, text_pos,
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2
            )

        return frame

    def process_frame(self, frame):
        """
        Process a single frame for ArUco detection

        Args:
            frame: Input frame from camera

        Returns:
            Annotated frame, detection status
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect markers
        corners, ids, rejected = self.detector.detectMarkers(gray)

        rvecs, tvecs = None, None
        detected = False

        if ids is not None and len(ids) > 0:
            detected = True
            # Estimate pose
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
                corners, self.marker_size, self.camera_matrix, self.dist_coeffs
            )

            # Store trajectory data if recording
            if self.recording:
                # Calculate timestamp relative to recording start
                current_time = time.time()
                timestamp = current_time - self.recording_start_time

                for i, marker_id in enumerate(ids):
                    tvec = tvecs[i][0]
                    rvec = rvecs[i][0]

                    self.trajectory_data.append({
                        'timestamp': float(timestamp),
                        'frame': self.frame_count,
                        'marker_id': int(marker_id[0]),
                        'x': float(tvec[0]),
                        'y': float(tvec[1]),
                        'z': float(tvec[2]),
                        'rx': float(rvec[0]),
                        'ry': float(rvec[1]),
                        'rz': float(rvec[2])
                    })

            # Annotate frame
            frame = self.annotate_frame(frame, corners, ids, rvecs, tvecs)

        return frame, detected

    def save_trajectory(self, output_path):
        """
        Save trajectory data to CSV file

        Args:
            output_path: Path to output CSV file
        """
        if not self.trajectory_data:
            print("Warning: No trajectory data to save")
            return False

        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'frame', 'marker_id', 'x', 'y', 'z', 'rx', 'ry', 'rz']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for data_point in self.trajectory_data:
                writer.writerow(data_point)

        print(f"Trajectory saved: {output_path}")
        return True

    def run_live_tracking(self, output_csv='live_trajectory.csv',
                         generate_animation=True, animation_output='live_animation.mp4'):
        """
        Run live tracking from webcam

        Args:
            output_csv: Path to save trajectory CSV
            generate_animation: Whether to generate 3D animation after tracking
            animation_output: Path for animation video
        """
        # Open camera
        self.cap = cv2.VideoCapture(self.camera_id)

        if not self.cap.isOpened():
            print(f"Error: Cannot open camera {self.camera_id}")
            return

        # Get camera properties
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)

        print("\n" + "="*60)
        print("LIVE ARUCO TRACKER")
        print("="*60)
        print(f"Camera: {self.camera_id}")
        print(f"Resolution: {width}x{height}")
        print(f"FPS: {fps}")
        print(f"Marker size: {self.marker_size}m")
        print(f"ArUco dictionary: {config.ARUCO_DICT_TYPE}")
        print("\nControls:")
        print("  SPACE - Start/Stop recording")
        print("  Q     - Quit")
        print("="*60 + "\n")

        self.start_time = time.time()
        markers_detected_count = 0
        total_frames = 0

        while True:
            ret, frame = self.cap.read()

            if not ret:
                print("Error: Cannot read frame from camera")
                break

            total_frames += 1
            self.frame_count += 1

            # Process frame
            annotated_frame, detected = self.process_frame(frame)

            if detected:
                markers_detected_count += 1

            # Add status information
            elapsed_time = time.time() - self.start_time
            status_color = (0, 255, 0) if self.recording else (0, 165, 255)
            status_text = "RECORDING" if self.recording else "STANDBY"

            # Status bar background
            cv2.rectangle(annotated_frame, (0, 0), (width, 80), (0, 0, 0), -1)

            # Status text
            cv2.putText(annotated_frame, status_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)

            # Time and frame info
            info_text = f"Time: {elapsed_time:.1f}s | Frames: {self.frame_count}"
            cv2.putText(annotated_frame, info_text, (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # Data points count and recording timestamp
            if self.recording:
                data_text = f"Data points: {len(self.trajectory_data)}"
                cv2.putText(annotated_frame, data_text, (width - 250, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                # Recording timestamp
                rec_time = time.time() - self.recording_start_time
                timestamp_text = f"Rec Time: {rec_time:.2f}s"
                cv2.putText(annotated_frame, timestamp_text, (width - 250, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            # Detection indicator
            detection_text = "Marker Detected" if detected else "No Marker"
            detection_color = (0, 255, 0) if detected else (0, 0, 255)
            cv2.putText(annotated_frame, detection_text, (width - 250, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, detection_color, 2)

            # Display frame
            cv2.imshow('Live ArUco Tracker', annotated_frame)

            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                print("\nQuitting...")
                break
            elif key == ord(' '):
                self.recording = not self.recording
                if self.recording:
                    print("\n[RECORDING STARTED]")
                    self.trajectory_data = []  # Clear previous data
                    self.frame_count = 0
                    self.recording_start_time = time.time()  # Record start timestamp
                else:
                    print(f"\n[RECORDING STOPPED]")
                    print(f"Captured {len(self.trajectory_data)} data points")
                    if self.trajectory_data:
                        duration = self.trajectory_data[-1]['timestamp']
                        print(f"Recording duration: {duration:.2f} seconds")

        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()

        # Print summary
        print("\n" + "="*60)
        print("TRACKING SUMMARY")
        print("="*60)
        print(f"Total frames processed: {total_frames}")
        print(f"Frames with detections: {markers_detected_count}")
        print(f"Detection rate: {markers_detected_count/total_frames*100:.1f}%")
        print(f"Trajectory data points: {len(self.trajectory_data)}")
        print("="*60 + "\n")

        # Save trajectory
        if self.trajectory_data:
            saved = self.save_trajectory(output_csv)

            # Generate 3D animation
            if saved and generate_animation:
                print("\nGenerating 3D animation video...")
                try:
                    visualizer = TrajectoryVisualizer(output_csv)
                    visualizer.create_3d_animation_video(
                        output_path=animation_output,
                        fps=30,
                        duration=10,
                        rotation_speed=1.0
                    )
                    print(f"3D animation saved: {animation_output}")
                except Exception as e:
                    print(f"Error generating animation: {e}")
        else:
            print("No trajectory data recorded")


def main():
    parser = argparse.ArgumentParser(
        description='Live ArUco tracking with real-time display and 3D animation'
    )
    parser.add_argument('--camera', type=int, default=0,
                        help='Camera device ID (default: 0)')
    parser.add_argument('--marker-size', type=float, default=None,
                        help=f'Size of ArUco marker in meters (default: {config.MARKER_SIZE})')
    parser.add_argument('--output', type=str, default='live_trajectory.csv',
                        help='Output CSV file path (default: live_trajectory.csv)')
    parser.add_argument('--animation', type=str, default='live_animation.mp4',
                        help='Output animation file path (default: live_animation.mp4)')
    parser.add_argument('--no-animation', action='store_true',
                        help='Do not generate 3D animation')

    args = parser.parse_args()

    # Create tracker
    tracker = LiveArucoTracker(
        marker_size=args.marker_size,
        camera_id=args.camera
    )

    # Run live tracking
    tracker.run_live_tracking(
        output_csv=args.output,
        generate_animation=not args.no_animation,
        animation_output=args.animation
    )


if __name__ == '__main__':
    main()
