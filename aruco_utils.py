"""
ArUco Utility Functions
Common operations for ArUco marker tracking shared across multiple modules
"""

import cv2
import numpy as np
import csv
from pathlib import Path


class ArucoInitializer:
    """Centralized ArUco dictionary and detector initialization"""

    @staticmethod
    def initialize_detector(aruco_dict_type):
        """
        Initialize ArUco detector with specified dictionary

        Args:
            aruco_dict_type: String name of dictionary (e.g., 'DICT_4X4_50')

        Returns:
            (aruco_dict, aruco_params, detector): Initialized ArUco components
        """
        aruco_dict = cv2.aruco.getPredefinedDictionary(
            getattr(cv2.aruco, aruco_dict_type)
        )
        aruco_params = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)
        return aruco_dict, aruco_params, detector

    @staticmethod
    def initialize_params_only(aruco_dict_type):
        """
        Initialize only the dictionary and params (not detector)
        Useful when detector will be created later

        Args:
            aruco_dict_type: String name of dictionary

        Returns:
            (aruco_dict, aruco_params): Initialized ArUco components
        """
        aruco_dict = cv2.aruco.getPredefinedDictionary(
            getattr(cv2.aruco, aruco_dict_type)
        )
        aruco_params = cv2.aruco.DetectorParameters()
        return aruco_dict, aruco_params


class CameraConfig:
    """Camera configuration loader with defaults"""

    @staticmethod
    def load_camera_params(marker_size=None, camera_matrix=None, dist_coeffs=None, config_module=None):
        """
        Load camera parameters with fallback to config defaults

        Args:
            marker_size: Marker size in meters (optional)
            camera_matrix: 3x3 camera intrinsic matrix (optional)
            dist_coeffs: Distortion coefficients (optional)
            config_module: Config module to use for defaults

        Returns:
            (marker_size, camera_matrix, dist_coeffs): Processed parameters as numpy arrays
        """
        if config_module is None:
            import config
            config_module = config

        # Process marker size
        if marker_size is None:
            marker_size = config_module.MARKER_SIZE

        # Process camera matrix
        if camera_matrix is not None:
            camera_matrix = np.array(camera_matrix, dtype=np.float32)
        else:
            camera_matrix = np.array(config_module.CAMERA_MATRIX, dtype=np.float32)

        # Process distortion coefficients
        if dist_coeffs is not None:
            dist_coeffs = np.array(dist_coeffs, dtype=np.float32)
        else:
            dist_coeffs = np.array(config_module.DIST_COEFFS, dtype=np.float32)

        return marker_size, camera_matrix, dist_coeffs


class VisualizationUtils:
    """3D visualization helper functions"""

    @staticmethod
    def draw_axis(frame, rvec, tvec, camera_matrix, dist_coeffs, length=0.03):
        """
        Draw 3D coordinate axes on frame

        Args:
            frame: Input image frame
            rvec: Rotation vector
            tvec: Translation vector
            camera_matrix: Camera intrinsic matrix
            dist_coeffs: Distortion coefficients
            length: Length of axes in meters

        Returns:
            Annotated frame with axes drawn
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
            axis_points, rvec, tvec, camera_matrix, dist_coeffs
        )

        img_points = img_points.astype(int)

        # Draw axes
        origin = tuple(img_points[0].ravel())
        frame = cv2.line(frame, origin, tuple(img_points[1].ravel()), (0, 0, 255), 3)  # X (red)
        frame = cv2.line(frame, origin, tuple(img_points[2].ravel()), (0, 255, 0), 3)  # Y (green)
        frame = cv2.line(frame, origin, tuple(img_points[3].ravel()), (255, 0, 0), 3)  # Z (blue)

        return frame

    @staticmethod
    def annotate_marker_frame(frame, corners, ids, rvecs, tvecs,
                            camera_matrix, dist_coeffs, marker_size):
        """
        Annotate frame with marker detections and 3D coordinates

        Args:
            frame: Input image frame
            corners: Detected marker corners
            ids: Detected marker IDs
            rvecs: Rotation vectors
            tvecs: Translation vectors
            camera_matrix: Camera intrinsic matrix
            dist_coeffs: Distortion coefficients
            marker_size: Marker size in meters

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
            frame = VisualizationUtils.draw_axis(
                frame, rvec, tvec, camera_matrix, dist_coeffs,
                length=marker_size * 0.6
            )

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


class TrajectoryIO:
    """Trajectory data I/O operations"""

    FIELDNAMES = ['timestamp', 'frame', 'marker_id', 'x', 'y', 'z', 'rx', 'ry', 'rz']

    @staticmethod
    def save_trajectory(trajectory_data, output_path):
        """
        Save trajectory data to CSV file

        Args:
            trajectory_data: List of trajectory data dictionaries
            output_path: Path to output CSV file

        Returns:
            Boolean indicating success
        """
        if not trajectory_data:
            print("Warning: No trajectory data to save")
            return False

        try:
            with open(output_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=TrajectoryIO.FIELDNAMES)
                writer.writeheader()
                for data_point in trajectory_data:
                    writer.writerow(data_point)

            return True
        except Exception as e:
            print(f"Error saving trajectory: {e}")
            return False

    @staticmethod
    def create_trajectory_point(timestamp, frame, marker_id, tvec, rvec):
        """
        Create a single trajectory data point

        Args:
            timestamp: Timestamp value
            frame: Frame number
            marker_id: Marker ID
            tvec: Translation vector
            rvec: Rotation vector

        Returns:
            Dictionary with trajectory point data
        """
        return {
            'timestamp': float(timestamp),
            'frame': int(frame),
            'marker_id': int(marker_id[0]) if hasattr(marker_id, '__getitem__') else int(marker_id),
            'x': float(tvec[0]),
            'y': float(tvec[1]),
            'z': float(tvec[2]),
            'rx': float(rvec[0]),
            'ry': float(rvec[1]),
            'rz': float(rvec[2])
        }
