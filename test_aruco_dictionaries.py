"""
ArUco Dictionary Test Script
Tests different ArUco dictionaries to find which one detects markers in your video
"""

import cv2
import numpy as np
import argparse
from pathlib import Path


def test_all_dictionaries(video_path, num_frames=50):
    """
    Test all ArUco dictionary types on a video

    Args:
        video_path: Path to video file
        num_frames: Number of frames to sample
    """
    # List of all available ArUco dictionaries
    aruco_dicts = [
        'DICT_4X4_50',
        'DICT_4X4_100',
        'DICT_4X4_250',
        'DICT_4X4_1000',
        'DICT_5X5_50',
        'DICT_5X5_100',
        'DICT_5X5_250',
        'DICT_5X5_1000',
        'DICT_6X6_50',
        'DICT_6X6_100',
        'DICT_6X6_250',
        'DICT_6X6_1000',
        'DICT_7X7_50',
        'DICT_7X7_100',
        'DICT_7X7_250',
        'DICT_7X7_1000',
        'DICT_ARUCO_ORIGINAL',
    ]

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Cannot open video file: {video_path}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Testing video: {video_path}")
    print(f"Total frames: {total_frames}")
    print(f"Sampling {min(num_frames, total_frames)} frames\n")

    # Sample frames evenly distributed through the video
    frame_indices = np.linspace(0, total_frames - 1, min(num_frames, total_frames), dtype=int)

    results = {}

    for dict_name in aruco_dicts:
        try:
            aruco_dict = cv2.aruco.getPredefinedDictionary(getattr(cv2.aruco, dict_name))
            aruco_params = cv2.aruco.DetectorParameters()
            detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

            detected_markers = set()
            frames_with_detection = 0

            for frame_idx in frame_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()

                if not ret:
                    continue

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                corners, ids, rejected = detector.detectMarkers(gray)

                if ids is not None and len(ids) > 0:
                    frames_with_detection += 1
                    for marker_id in ids:
                        detected_markers.add(int(marker_id[0]))

            if detected_markers:
                results[dict_name] = {
                    'marker_ids': sorted(list(detected_markers)),
                    'frames_detected': frames_with_detection,
                    'detection_rate': frames_with_detection / len(frame_indices) * 100
                }

        except Exception as e:
            print(f"Error testing {dict_name}: {e}")

    cap.release()

    # Print results
    print("\n" + "=" * 70)
    print("DETECTION RESULTS")
    print("=" * 70 + "\n")

    if not results:
        print("[X] No ArUco markers detected with any dictionary type!")
        print("\nPossible reasons:")
        print("  1. The video does not contain ArUco markers")
        print("  2. The markers are too small or unclear")
        print("  3. The markers are obstructed or out of focus")
        print("  4. The lighting conditions are poor")
        print("\nSuggestions:")
        print("  - Verify your video contains ArUco markers")
        print("  - Ensure markers are clearly visible and well-lit")
        print("  - Try recording closer to the markers")
    else:
        print("[OK] Found ArUco markers!\n")

        # Sort by detection rate
        sorted_results = sorted(results.items(), key=lambda x: x[1]['detection_rate'], reverse=True)

        for dict_name, data in sorted_results:
            print(f"Dictionary: {dict_name}")
            print(f"  Marker IDs detected: {data['marker_ids']}")
            print(f"  Frames with detection: {data['frames_detected']}/{len(frame_indices)}")
            print(f"  Detection rate: {data['detection_rate']:.1f}%")
            print()

        best_dict = sorted_results[0][0]
        print("=" * 70)
        print(f"RECOMMENDATION: Use '{best_dict}' in config.py")
        print("=" * 70)
        print(f"\nUpdate config.py:")
        print(f"  ARUCO_DICT_TYPE = '{best_dict}'")


def main():
    parser = argparse.ArgumentParser(
        description='Test different ArUco dictionaries on a video to find the correct type'
    )
    parser.add_argument('video_path', type=str, help='Path to input video file')
    parser.add_argument('--frames', type=int, default=50,
                        help='Number of frames to sample (default: 50)')

    args = parser.parse_args()

    if not Path(args.video_path).exists():
        print(f"Error: Video file not found: {args.video_path}")
        return

    test_all_dictionaries(args.video_path, args.frames)


if __name__ == '__main__':
    main()
