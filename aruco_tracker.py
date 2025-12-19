"""
ArUco Marker 3D Trajectory Tracker
Detects ArUco markers in a video and tracks their 3D position over time
"""

import cv2
import numpy as np
import csv
import argparse
from pathlib import Path
import config
from aruco_utils import ArucoInitializer, CameraConfig, TrajectoryIO


class ArucoTracker:
    def __init__(self, marker_size=None, camera_matrix=None, dist_coeffs=None):
        """
        Initialize the ArUco tracker

        Args:
            marker_size: Size of the ArUco marker in meters
            camera_matrix: Camera intrinsic matrix (3x3)
            dist_coeffs: Camera distortion coefficients
        """
        # Use config values if not provided
        self.marker_size, self.camera_matrix, self.dist_coeffs = CameraConfig.load_camera_params(
            marker_size, camera_matrix, dist_coeffs
        )

        # Get ArUco dictionary
        self.aruco_dict, self.aruco_params = ArucoInitializer.initialize_params_only(
            config.ARUCO_DICT_TYPE
        )

        # Storage for trajectory data
        self.trajectory_data = []

    def detect_and_estimate_pose(self, frame, frame_number):
        """
        Detect ArUco markers and estimate their 3D pose

        Args:
            frame: Input image frame
            frame_number: Current frame number

        Returns:
            corners, ids, rvecs, tvecs: Detection and pose estimation results
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect markers
        detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.aruco_params)
        corners, ids, rejected = detector.detectMarkers(gray)

        rvecs, tvecs = None, None

        if ids is not None and len(ids) > 0:
            # Estimate pose for each marker
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
                corners, self.marker_size, self.camera_matrix, self.dist_coeffs
            )

            # Store trajectory data
            for i, marker_id in enumerate(ids):
                tvec = tvecs[i][0]  # Translation vector (x, y, z)
                rvec = rvecs[i][0]  # Rotation vector

                # Convert rotation vector to rotation matrix
                rmat, _ = cv2.Rodrigues(rvec)

                # Calculate timestamp from frame number and FPS
                timestamp = frame_number / self.fps if hasattr(self, 'fps') and self.fps > 0 else 0.0

                # Store data: timestamp, frame, marker_id, x, y, z, rx, ry, rz
                self.trajectory_data.append({
                    'timestamp': float(timestamp),
                    'frame': frame_number,
                    'marker_id': int(marker_id[0]),
                    'x': float(tvec[0]),
                    'y': float(tvec[1]),
                    'z': float(tvec[2]),
                    'rx': float(rvec[0]),
                    'ry': float(rvec[1]),
                    'rz': float(rvec[2])
                })

        return corners, ids, rvecs, tvecs

    def process_video(self, video_path, output_csv=None):
        """
        Process a video file and track ArUco markers

        Args:
            video_path: Path to input video file
            output_csv: Path to output CSV file (optional)
        """
        if output_csv is None:
            output_csv = config.OUTPUT_TRAJECTORY_FILE

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(f"Cannot open video file: {video_path}")

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = cap.get(cv2.CAP_PROP_FPS)

        print(f"Processing video: {video_path}")
        print(f"Total frames: {total_frames}")
        print(f"FPS: {self.fps}")
        print(f"Marker size: {self.marker_size}m")

        frame_number = 0

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            # Process frame
            if frame_number % config.FRAME_SKIP == 0:
                corners, ids, rvecs, tvecs = self.detect_and_estimate_pose(frame, frame_number)

                if ids is not None:
                    print(f"Frame {frame_number}/{total_frames}: Detected {len(ids)} marker(s)")

            frame_number += 1

        cap.release()

        # Save trajectory data to CSV
        self.save_trajectory(output_csv)

        print(f"\nProcessing complete!")
        print(f"Total data points: {len(self.trajectory_data)}")
        print(f"Trajectory saved to: {output_csv}")

        return self.trajectory_data

    def save_trajectory(self, output_path):
        """
        Save trajectory data to CSV file

        Args:
            output_path: Path to output CSV file
        """
        TrajectoryIO.save_trajectory(self.trajectory_data, output_path)


def main():
    parser = argparse.ArgumentParser(description='Track ArUco markers in 3D from video')
    parser.add_argument('video_path', type=str, help='Path to input video file')
    parser.add_argument('--marker-size', type=float, default=None,
                        help=f'Size of ArUco marker in meters (default: {config.MARKER_SIZE})')
    parser.add_argument('--output', type=str, default=None,
                        help=f'Output CSV file path (default: {config.OUTPUT_TRAJECTORY_FILE})')

    args = parser.parse_args()

    # Check if video file exists
    if not Path(args.video_path).exists():
        print(f"Error: Video file not found: {args.video_path}")
        return

    # Create tracker
    tracker = ArucoTracker(marker_size=args.marker_size)

    # Process video
    tracker.process_video(args.video_path, args.output)


if __name__ == '__main__':
    main()
