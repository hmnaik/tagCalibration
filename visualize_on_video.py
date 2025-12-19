"""
Video Overlay Visualization
Displays ArUco marker detection and 3D coordinates on video frames
"""

import cv2
import numpy as np
import argparse
from pathlib import Path
import config
from aruco_utils import ArucoInitializer, CameraConfig, VisualizationUtils


class VideoOverlay:
    def __init__(self, marker_size=None, camera_matrix=None, dist_coeffs=None):
        """
        Initialize the video overlay visualizer

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

    def draw_axis(self, frame, rvec, tvec, length=0.03):
        """
        Draw 3D coordinate axes on the frame

        Args:
            frame: Input image frame
            rvec: Rotation vector
            tvec: Translation vector
            length: Length of the axes in meters
        """
        return VisualizationUtils.draw_axis(
            frame, rvec, tvec, self.camera_matrix, self.dist_coeffs, length
        )

    def draw_cube(self, frame, rvec, tvec, size=None):
        """
        Draw a 3D cube on the marker

        Args:
            frame: Input image frame
            rvec: Rotation vector
            tvec: Translation vector
            size: Size of the cube (default: marker size)
        """
        if size is None:
            size = self.marker_size

        # Define 3D points for the cube
        cube_points = np.float32([
            [0, 0, 0],
            [size, 0, 0],
            [size, size, 0],
            [0, size, 0],
            [0, 0, size],
            [size, 0, size],
            [size, size, size],
            [0, size, size]
        ])

        # Project 3D points to 2D image plane
        img_points, _ = cv2.projectPoints(
            cube_points, rvec, tvec, self.camera_matrix, self.dist_coeffs
        )

        img_points = img_points.astype(int)

        # Draw cube edges
        # Base (z=0)
        for i in range(4):
            pt1 = tuple(img_points[i].ravel())
            pt2 = tuple(img_points[(i + 1) % 4].ravel())
            frame = cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

        # Top (z=size)
        for i in range(4, 8):
            pt1 = tuple(img_points[i].ravel())
            pt2 = tuple(img_points[4 + (i + 1) % 4].ravel())
            frame = cv2.line(frame, pt1, pt2, (255, 0, 255), 2)

        # Vertical edges
        for i in range(4):
            pt1 = tuple(img_points[i].ravel())
            pt2 = tuple(img_points[i + 4].ravel())
            frame = cv2.line(frame, pt1, pt2, (255, 255, 0), 2)

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
        return VisualizationUtils.annotate_marker_frame(
            frame, corners, ids, rvecs, tvecs,
            self.camera_matrix, self.dist_coeffs, self.marker_size
        )

    def process_video(self, input_video, output_video=None, show_live=False):
        """
        Process video and overlay 3D coordinates

        Args:
            input_video: Path to input video file
            output_video: Path to output video file (optional)
            show_live: Display frames in real-time
        """
        if output_video is None:
            output_video = config.OUTPUT_VIDEO_FILE

        cap = cv2.VideoCapture(input_video)

        if not cap.isOpened():
            raise ValueError(f"Cannot open video file: {input_video}")

        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        print(f"Processing video: {input_video}")
        print(f"Resolution: {width}x{height}")
        print(f"FPS: {fps}")
        print(f"Total frames: {total_frames}")

        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

        frame_number = 0
        detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.aruco_params)

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            # Detect markers
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, rejected = detector.detectMarkers(gray)

            rvecs, tvecs = None, None

            if ids is not None and len(ids) > 0:
                # Estimate pose
                rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(
                    corners, self.marker_size, self.camera_matrix, self.dist_coeffs
                )

                # Annotate frame
                frame = self.annotate_frame(frame, corners, ids, rvecs, tvecs)

            # Add frame number
            cv2.putText(
                frame, f"Frame: {frame_number}/{total_frames}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2
            )

            # Write frame
            out.write(frame)

            # Display frame
            if show_live:
                cv2.imshow('ArUco Tracking', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            frame_number += 1

            # Print progress
            if frame_number % 30 == 0:
                progress = (frame_number / total_frames) * 100
                print(f"Progress: {progress:.1f}%")

        cap.release()
        out.release()
        cv2.destroyAllWindows()

        print(f"\nVideo processing complete!")
        print(f"Output saved to: {output_video}")


def main():
    parser = argparse.ArgumentParser(
        description='Overlay 3D coordinates on video with ArUco marker detection'
    )
    parser.add_argument('video_path', type=str, help='Path to input video file')
    parser.add_argument('--marker-size', type=float, default=None,
                        help=f'Size of ArUco marker in meters (default: {config.MARKER_SIZE})')
    parser.add_argument('--output', type=str, default=None,
                        help=f'Output video file path (default: {config.OUTPUT_VIDEO_FILE})')
    parser.add_argument('--show', action='store_true',
                        help='Display video in real-time')

    args = parser.parse_args()

    # Check if video file exists
    if not Path(args.video_path).exists():
        print(f"Error: Video file not found: {args.video_path}")
        return

    # Create visualizer
    visualizer = VideoOverlay(marker_size=args.marker_size)

    # Process video
    visualizer.process_video(args.video_path, args.output, args.show)


if __name__ == '__main__':
    main()
