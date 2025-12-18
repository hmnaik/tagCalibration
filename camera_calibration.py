"""
Camera Calibration Module
Calibrate camera using checkerboard pattern from images, video, or live feed
Automatically updates config.py with calibration results
"""

import cv2
import numpy as np
import glob
import argparse
import time
from pathlib import Path


class CameraCalibrator:
    def __init__(self, checkerboard_size=(9, 6), square_size=0.025):
        """
        Initialize camera calibrator

        Args:
            checkerboard_size: (width, height) number of inner corners
            square_size: Size of checkerboard square in meters
        """
        self.checkerboard_size = checkerboard_size
        self.square_size = square_size

        # Termination criteria for corner refinement
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # Prepare object points (0,0,0), (1,0,0), (2,0,0) ....,(8,5,0)
        self.objp = np.zeros((checkerboard_size[0] * checkerboard_size[1], 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:checkerboard_size[0],
                                     0:checkerboard_size[1]].T.reshape(-1, 2)
        self.objp *= square_size

        # Arrays to store object points and image points
        self.objpoints = []  # 3D points in real world space
        self.imgpoints = []  # 2D points in image plane

        # Calibration results
        self.camera_matrix = None
        self.dist_coeffs = None
        self.calibration_error = None

    def find_checkerboard(self, image, refine=True):
        """
        Find checkerboard corners in image

        Args:
            image: Input image
            refine: Whether to refine corner positions

        Returns:
            success, corners
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, self.checkerboard_size, None)

        if ret and refine:
            # Refine corner positions
            corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)

        return ret, corners

    def add_calibration_image(self, image):
        """
        Add image to calibration dataset

        Args:
            image: Input image with checkerboard

        Returns:
            success, annotated_image
        """
        ret, corners = self.find_checkerboard(image)

        if ret:
            self.objpoints.append(self.objp)
            self.imgpoints.append(corners)

            # Draw corners for visualization
            annotated = image.copy()
            cv2.drawChessboardCorners(annotated, self.checkerboard_size, corners, ret)
            return True, annotated
        else:
            return False, image

    def calibrate(self, image_size):
        """
        Perform camera calibration

        Args:
            image_size: (width, height) of images

        Returns:
            success
        """
        if len(self.objpoints) < 10:
            print(f"Warning: Only {len(self.objpoints)} calibration images. Recommended: 20+")

        print(f"\nCalibrating camera with {len(self.objpoints)} images...")

        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            self.objpoints, self.imgpoints, image_size, None, None
        )

        if ret:
            self.camera_matrix = mtx
            self.dist_coeffs = dist

            # Calculate reprojection error
            mean_error = 0
            for i in range(len(self.objpoints)):
                imgpoints2, _ = cv2.projectPoints(
                    self.objpoints[i], rvecs[i], tvecs[i], mtx, dist
                )
                error = cv2.norm(self.imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
                mean_error += error

            self.calibration_error = mean_error / len(self.objpoints)

            print(f"[OK] Calibration successful!")
            print(f"  Reprojection error: {self.calibration_error:.4f} pixels")
            print(f"  (Lower is better, <0.5 is excellent, <1.0 is good)")

            return True
        else:
            print("[ERROR] Calibration failed!")
            return False

    def calibrate_from_images(self, image_paths):
        """
        Calibrate from image files

        Args:
            image_paths: List of image file paths or glob pattern

        Returns:
            success
        """
        if isinstance(image_paths, str):
            # Glob pattern
            images = glob.glob(image_paths)
        else:
            images = image_paths

        if not images:
            print("Error: No images found!")
            return False

        print(f"Found {len(images)} images")
        print(f"Checkerboard size: {self.checkerboard_size[0]}x{self.checkerboard_size[1]}")
        print(f"Square size: {self.square_size}m\n")

        image_size = None
        successful = 0

        for idx, fname in enumerate(images):
            img = cv2.imread(fname)
            if img is None:
                print(f"[{idx+1}/{len(images)}] [X] Failed to load: {fname}")
                continue

            if image_size is None:
                image_size = (img.shape[1], img.shape[0])

            ret, annotated = self.add_calibration_image(img)

            if ret:
                successful += 1
                print(f"[{idx+1}/{len(images)}] [OK] {Path(fname).name}")
            else:
                print(f"[{idx+1}/{len(images)}] [X] No checkerboard: {Path(fname).name}")

        print(f"\nSuccessfully detected checkerboard in {successful}/{len(images)} images")

        if successful < 10:
            print("Error: Need at least 10 good images for calibration")
            return False

        return self.calibrate(image_size)

    def calibrate_from_video(self, video_path, sample_interval=30):
        """
        Calibrate from video file

        Args:
            video_path: Path to video file
            sample_interval: Sample every Nth frame

        Returns:
            success
        """
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"Error: Cannot open video: {video_path}")
            return False

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        image_size = (width, height)

        print(f"Processing video: {video_path}")
        print(f"Total frames: {total_frames}, FPS: {fps}")
        print(f"Resolution: {width}x{height}")
        print(f"Checkerboard size: {self.checkerboard_size[0]}x{self.checkerboard_size[1]}")
        print(f"Sampling every {sample_interval} frames\n")

        frame_idx = 0
        successful = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % sample_interval == 0:
                success, annotated = self.add_calibration_image(frame)
                if success:
                    successful += 1
                    print(f"Frame {frame_idx}: [OK] ({successful} images collected)")

            frame_idx += 1

        cap.release()

        print(f"\nCollected {successful} calibration images from video")

        if successful < 10:
            print("Error: Need at least 10 good frames for calibration")
            return False

        return self.calibrate(image_size)

    def calibrate_live(self, camera_id=0, num_images=20, capture_interval=2.0):
        """
        Calibrate from live camera feed

        Args:
            camera_id: Camera device ID
            num_images: Target number of calibration images
            capture_interval: Seconds between auto-capture

        Returns:
            success
        """
        cap = cv2.VideoCapture(camera_id)

        if not cap.isOpened():
            print(f"Error: Cannot open camera {camera_id}")
            return False

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        image_size = (width, height)

        print("\n" + "="*60)
        print("LIVE CAMERA CALIBRATION")
        print("="*60)
        print(f"Camera: {camera_id}")
        print(f"Resolution: {width}x{height}")
        print(f"Checkerboard size: {self.checkerboard_size[0]}x{self.checkerboard_size[1]}")
        print(f"Square size: {self.square_size}m")
        print(f"Target images: {num_images}")
        print("\nControls:")
        print("  SPACE - Capture image manually")
        print("  C     - Start/Stop auto-capture")
        print("  Q     - Quit and calibrate")
        print("="*60 + "\n")

        last_capture_time = time.time()
        auto_capture = False
        captured_count = 0

        while captured_count < num_images:
            ret, frame = cap.read()
            if not ret:
                print("Error reading frame")
                break

            # Check for checkerboard
            found, corners = self.find_checkerboard(frame, refine=False)

            # Create display frame
            display = frame.copy()

            # Draw corners if found
            if found:
                cv2.drawChessboardCorners(display, self.checkerboard_size, corners, found)

            # Status information
            status_color = (0, 255, 0) if found else (0, 0, 255)
            status_text = "CHECKERBOARD FOUND" if found else "NO CHECKERBOARD"

            # Background for status
            cv2.rectangle(display, (0, 0), (width, 120), (0, 0, 0), -1)

            # Status
            cv2.putText(display, status_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)

            # Progress
            progress_text = f"Images: {captured_count}/{num_images}"
            cv2.putText(display, progress_text, (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Auto-capture status
            mode_text = "AUTO-CAPTURE ON" if auto_capture else "MANUAL MODE"
            mode_color = (0, 255, 255) if auto_capture else (255, 255, 255)
            cv2.putText(display, mode_text, (10, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, mode_color, 2)

            # Quality indicator
            if found:
                quality_text = "QUALITY: GOOD - HOLD STEADY"
                cv2.putText(display, quality_text, (10, 110),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Auto-capture logic
            current_time = time.time()
            if auto_capture and found and (current_time - last_capture_time) >= capture_interval:
                success, _ = self.add_calibration_image(frame)
                if success:
                    captured_count += 1
                    last_capture_time = current_time
                    print(f"Auto-captured image {captured_count}/{num_images}")

                    # Flash effect
                    flash = np.ones_like(display) * 255
                    cv2.addWeighted(display, 0.5, flash, 0.5, 0, display)

            cv2.imshow('Camera Calibration', display)

            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                print("\nStopping capture...")
                break
            elif key == ord(' ') and found:
                # Manual capture
                success, _ = self.add_calibration_image(frame)
                if success:
                    captured_count += 1
                    print(f"Manually captured image {captured_count}/{num_images}")
            elif key == ord('c'):
                # Toggle auto-capture
                auto_capture = not auto_capture
                status = "ON" if auto_capture else "OFF"
                print(f"Auto-capture: {status}")

        cap.release()
        cv2.destroyAllWindows()

        print(f"\nCollected {captured_count} calibration images")

        if captured_count < 10:
            print("Error: Need at least 10 images for calibration")
            return False

        return self.calibrate(image_size)

    def save_calibration(self, output_file='calibration_data.npz'):
        """
        Save calibration to numpy file

        Args:
            output_file: Output file path
        """
        if self.camera_matrix is None:
            print("Error: No calibration data to save")
            return False

        np.savez(output_file,
                 camera_matrix=self.camera_matrix,
                 dist_coeffs=self.dist_coeffs,
                 calibration_error=self.calibration_error,
                 checkerboard_size=self.checkerboard_size,
                 square_size=self.square_size)

        print(f"\nCalibration data saved to: {output_file}")
        return True

    def update_config_file(self, config_path='config.py'):
        """
        Update config.py with calibration results

        Args:
            config_path: Path to config.py file
        """
        if self.camera_matrix is None:
            print("Error: No calibration data to save")
            return False

        # Read current config
        with open(config_path, 'r') as f:
            lines = f.readlines()

        # Format calibration data
        camera_matrix_str = "[\n"
        for row in self.camera_matrix:
            camera_matrix_str += f"    [{row[0]:.6f}, {row[1]:.6f}, {row[2]:.6f}],\n"
        camera_matrix_str += "]"

        dist_coeffs_str = f"[{', '.join([f'{x:.8f}' for x in self.dist_coeffs[0]])}]"

        # Update lines
        new_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]

            if line.startswith('CAMERA_MATRIX'):
                # Replace camera matrix
                new_lines.append(f"CAMERA_MATRIX = {camera_matrix_str}\n")
                # Skip old matrix lines
                while i < len(lines) and not lines[i].strip().endswith(']'):
                    i += 1
            elif line.startswith('DIST_COEFFS'):
                # Replace distortion coefficients
                new_lines.append(f"DIST_COEFFS = {dist_coeffs_str}\n")
            else:
                new_lines.append(line)

            i += 1

        # Write updated config
        with open(config_path, 'w') as f:
            f.writelines(new_lines)

        print(f"\n[OK] Updated {config_path} with calibration data")
        print("\nCalibration Results:")
        print("="*60)
        print("Camera Matrix:")
        print(self.camera_matrix)
        print("\nDistortion Coefficients:")
        print(self.dist_coeffs)
        print(f"\nReprojection Error: {self.calibration_error:.4f} pixels")
        print("="*60)

        return True

    def print_results(self):
        """Print calibration results"""
        if self.camera_matrix is None:
            print("No calibration data available")
            return

        print("\n" + "="*60)
        print("CALIBRATION RESULTS")
        print("="*60)
        print(f"\nCamera Matrix (Intrinsic Parameters):")
        print(f"  fx = {self.camera_matrix[0, 0]:.2f} (focal length x)")
        print(f"  fy = {self.camera_matrix[1, 1]:.2f} (focal length y)")
        print(f"  cx = {self.camera_matrix[0, 2]:.2f} (principal point x)")
        print(f"  cy = {self.camera_matrix[1, 2]:.2f} (principal point y)")

        print(f"\nDistortion Coefficients:")
        print(f"  k1 = {self.dist_coeffs[0, 0]:.6f} (radial distortion)")
        print(f"  k2 = {self.dist_coeffs[0, 1]:.6f} (radial distortion)")
        print(f"  p1 = {self.dist_coeffs[0, 2]:.6f} (tangential distortion)")
        print(f"  p2 = {self.dist_coeffs[0, 3]:.6f} (tangential distortion)")
        print(f"  k3 = {self.dist_coeffs[0, 4]:.6f} (radial distortion)")

        print(f"\nCalibration Quality:")
        print(f"  Reprojection Error: {self.calibration_error:.4f} pixels")
        if self.calibration_error < 0.5:
            quality = "Excellent"
        elif self.calibration_error < 1.0:
            quality = "Good"
        elif self.calibration_error < 2.0:
            quality = "Acceptable"
        else:
            quality = "Poor - Consider recalibrating"
        print(f"  Quality: {quality}")

        print(f"\nCalibration Dataset:")
        print(f"  Number of images: {len(self.objpoints)}")
        print(f"  Checkerboard: {self.checkerboard_size[0]}x{self.checkerboard_size[1]}")
        print(f"  Square size: {self.square_size}m")
        print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description='Camera calibration using checkerboard pattern'
    )
    parser.add_argument('--mode', type=str, choices=['live', 'images', 'video'],
                        required=True, help='Calibration mode')
    parser.add_argument('--input', type=str, help='Input images path (glob) or video file')
    parser.add_argument('--camera', type=int, default=0, help='Camera ID for live mode')
    parser.add_argument('--checkerboard', type=str, default='9x6',
                        help='Checkerboard size (e.g., 9x6)')
    parser.add_argument('--square-size', type=float, default=0.025,
                        help='Checkerboard square size in meters (default: 0.025 = 25mm)')
    parser.add_argument('--num-images', type=int, default=20,
                        help='Number of images to collect in live mode')
    parser.add_argument('--interval', type=float, default=2.0,
                        help='Auto-capture interval in seconds for live mode')
    parser.add_argument('--sample-interval', type=int, default=30,
                        help='Frame sampling interval for video mode')
    parser.add_argument('--output', type=str, default='calibration_data.npz',
                        help='Output calibration file')
    parser.add_argument('--no-update-config', action='store_true',
                        help='Do not update config.py')

    args = parser.parse_args()

    # Parse checkerboard size
    try:
        width, height = map(int, args.checkerboard.split('x'))
        checkerboard_size = (width, height)
    except:
        print(f"Error: Invalid checkerboard size format: {args.checkerboard}")
        print("Use format: WIDTHxHEIGHT (e.g., 9x6)")
        return

    # Create calibrator
    calibrator = CameraCalibrator(
        checkerboard_size=checkerboard_size,
        square_size=args.square_size
    )

    # Run calibration based on mode
    success = False

    if args.mode == 'live':
        success = calibrator.calibrate_live(
            camera_id=args.camera,
            num_images=args.num_images,
            capture_interval=args.interval
        )

    elif args.mode == 'images':
        if not args.input:
            print("Error: --input required for images mode")
            return
        success = calibrator.calibrate_from_images(args.input)

    elif args.mode == 'video':
        if not args.input:
            print("Error: --input required for video mode")
            return
        success = calibrator.calibrate_from_video(
            args.input,
            sample_interval=args.sample_interval
        )

    if success:
        # Print results
        calibrator.print_results()

        # Save calibration data
        calibrator.save_calibration(args.output)

        # Update config.py
        if not args.no_update_config:
            calibrator.update_config_file('config.py')
        else:
            print("\nSkipped updating config.py (--no-update-config flag)")

        print("\n[OK] Calibration complete!")
    else:
        print("\n[ERROR] Calibration failed!")


if __name__ == '__main__':
    main()
