"""
3D Trajectory Visualization
Reads trajectory data from CSV and creates 3D plots
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
import argparse
from pathlib import Path
import config


class TrajectoryVisualizer:
    def __init__(self, csv_path):
        """
        Initialize the trajectory visualizer

        Args:
            csv_path: Path to CSV file containing trajectory data
        """
        self.csv_path = csv_path
        self.data = self.load_trajectory_data()

    def load_trajectory_data(self):
        """
        Load trajectory data from CSV file

        Returns:
            Dictionary with marker IDs as keys and trajectory arrays as values
        """
        data = {}

        with open(self.csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                marker_id = int(row['marker_id'])

                if marker_id not in data:
                    data[marker_id] = {
                        'frames': [],
                        'x': [],
                        'y': [],
                        'z': [],
                        'rx': [],
                        'ry': [],
                        'rz': []
                    }

                data[marker_id]['frames'].append(int(row['frame']))
                data[marker_id]['x'].append(float(row['x']))
                data[marker_id]['y'].append(float(row['y']))
                data[marker_id]['z'].append(float(row['z']))
                data[marker_id]['rx'].append(float(row['rx']))
                data[marker_id]['ry'].append(float(row['ry']))
                data[marker_id]['rz'].append(float(row['rz']))

        # Convert lists to numpy arrays
        for marker_id in data:
            for key in ['frames', 'x', 'y', 'z', 'rx', 'ry', 'rz']:
                data[marker_id][key] = np.array(data[marker_id][key])

        return data

    def plot_3d_trajectory(self, marker_id=None, save_path=None, show=True):
        """
        Create 3D plot of marker trajectory

        Args:
            marker_id: Specific marker ID to plot (None = plot all)
            save_path: Path to save the plot (optional)
            show: Whether to display the plot
        """
        if not self.data:
            print("No trajectory data to plot")
            return

        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111, projection='3d')

        # Plot trajectory for each marker
        marker_ids = [marker_id] if marker_id is not None else self.data.keys()

        colors = plt.cm.rainbow(np.linspace(0, 1, len(marker_ids)))

        for idx, mid in enumerate(marker_ids):
            if mid not in self.data:
                print(f"Warning: Marker ID {mid} not found in data")
                continue

            traj = self.data[mid]
            x, y, z = traj['x'], traj['y'], traj['z']

            # Plot trajectory line
            ax.plot(x, y, z, '-', color=colors[idx], linewidth=2,
                    label=f'Marker {mid}', alpha=0.7)

            # Mark start and end points
            ax.scatter(x[0], y[0], z[0], color=colors[idx], s=100,
                      marker='o', edgecolors='black', linewidths=2,
                      label=f'Start {mid}')
            ax.scatter(x[-1], y[-1], z[-1], color=colors[idx], s=100,
                      marker='s', edgecolors='black', linewidths=2,
                      label=f'End {mid}')

            # Print statistics
            print(f"\nMarker {mid} Statistics:")
            print(f"  Total points: {len(x)}")
            print(f"  X range: [{x.min():.4f}, {x.max():.4f}] m")
            print(f"  Y range: [{y.min():.4f}, {y.max():.4f}] m")
            print(f"  Z range: [{z.min():.4f}, {z.max():.4f}] m")

            # Calculate total distance traveled
            distances = np.sqrt(np.diff(x)**2 + np.diff(y)**2 + np.diff(z)**2)
            total_distance = np.sum(distances)
            print(f"  Total distance: {total_distance:.4f} m")

        ax.set_xlabel('X (m)', fontsize=12)
        ax.set_ylabel('Y (m)', fontsize=12)
        ax.set_zlabel('Z (m)', fontsize=12)
        ax.set_title('ArUco Marker 3D Trajectory', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)

        # Set equal aspect ratio for better visualization
        max_range = np.array([
            max([self.data[m]['x'].max() - self.data[m]['x'].min() for m in marker_ids]),
            max([self.data[m]['y'].max() - self.data[m]['y'].min() for m in marker_ids]),
            max([self.data[m]['z'].max() - self.data[m]['z'].min() for m in marker_ids])
        ]).max() / 2.0

        mid_x = np.mean([self.data[m]['x'].mean() for m in marker_ids])
        mid_y = np.mean([self.data[m]['y'].mean() for m in marker_ids])
        mid_z = np.mean([self.data[m]['z'].mean() for m in marker_ids])

        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"\nPlot saved to: {save_path}")

        if show:
            plt.show()

    def plot_position_vs_time(self, marker_id=None, save_path=None, show=True):
        """
        Create 2D plots of X, Y, Z positions vs frame number

        Args:
            marker_id: Specific marker ID to plot (None = plot all)
            save_path: Path to save the plot (optional)
            show: Whether to display the plot
        """
        if not self.data:
            print("No trajectory data to plot")
            return

        marker_ids = [marker_id] if marker_id is not None else self.data.keys()

        fig, axes = plt.subplots(3, 1, figsize=(12, 10))
        colors = plt.cm.rainbow(np.linspace(0, 1, len(marker_ids)))

        for idx, mid in enumerate(marker_ids):
            if mid not in self.data:
                continue

            traj = self.data[mid]
            frames = traj['frames']

            axes[0].plot(frames, traj['x'], '-', color=colors[idx],
                        linewidth=2, label=f'Marker {mid}')
            axes[1].plot(frames, traj['y'], '-', color=colors[idx],
                        linewidth=2, label=f'Marker {mid}')
            axes[2].plot(frames, traj['z'], '-', color=colors[idx],
                        linewidth=2, label=f'Marker {mid}')

        axes[0].set_ylabel('X Position (m)', fontsize=11)
        axes[0].set_title('Position vs Frame', fontsize=14, fontweight='bold')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        axes[1].set_ylabel('Y Position (m)', fontsize=11)
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

        axes[2].set_ylabel('Z Position (m)', fontsize=11)
        axes[2].set_xlabel('Frame Number', fontsize=11)
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            base_path = Path(save_path)
            time_plot_path = base_path.parent / f"{base_path.stem}_vs_time{base_path.suffix}"
            plt.savefig(time_plot_path, dpi=300, bbox_inches='tight')
            print(f"Time plot saved to: {time_plot_path}")

        if show:
            plt.show()

    def create_3d_animation_video(self, marker_id=None, output_path='trajectory_animation.mp4',
                                   fps=30, duration=10, rotation_speed=1.0):
        """
        Create an animated 3D video showing trajectory with rotating view

        Args:
            marker_id: Specific marker ID to animate (None = all markers)
            output_path: Path to save the video file
            fps: Frames per second for the video
            duration: Duration of video in seconds
            rotation_speed: Speed of rotation (1.0 = one full rotation per video)
        """
        if not self.data:
            print("No trajectory data to animate")
            return

        print(f"Creating 3D animation video: {output_path}")
        print(f"Duration: {duration}s, FPS: {fps}")

        # Setup figure and 3D axis
        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111, projection='3d')

        # Get marker IDs to plot
        marker_ids = [marker_id] if marker_id is not None else self.data.keys()
        colors = plt.cm.rainbow(np.linspace(0, 1, len(marker_ids)))

        # Collect all trajectory data
        all_trajectories = []
        for idx, mid in enumerate(marker_ids):
            if mid not in self.data:
                continue

            traj = self.data[mid]
            x, y, z = traj['x'], traj['y'], traj['z']
            all_trajectories.append({
                'x': x, 'y': y, 'z': z,
                'color': colors[idx],
                'marker_id': mid
            })

        if not all_trajectories:
            print("No valid trajectory data found")
            return

        # Calculate axis limits
        all_x = np.concatenate([t['x'] for t in all_trajectories])
        all_y = np.concatenate([t['y'] for t in all_trajectories])
        all_z = np.concatenate([t['z'] for t in all_trajectories])

        max_range = np.array([
            all_x.max() - all_x.min(),
            all_y.max() - all_y.min(),
            all_z.max() - all_z.min()
        ]).max() / 2.0

        mid_x = (all_x.max() + all_x.min()) * 0.5
        mid_y = (all_y.max() + all_y.min()) * 0.5
        mid_z = (all_z.max() + all_z.min()) * 0.5

        # Set axis limits
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)

        # Labels
        ax.set_xlabel('X (m)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Y (m)', fontsize=12, fontweight='bold')
        ax.set_zlabel('Z (m)', fontsize=12, fontweight='bold')
        ax.set_title('3D Trajectory Animation', fontsize=14, fontweight='bold')

        # Draw 3D coordinate axes at origin
        axis_length = max_range * 0.3
        ax.quiver(0, 0, 0, axis_length, 0, 0, color='red', arrow_length_ratio=0.2, linewidth=2, label='X-axis')
        ax.quiver(0, 0, 0, 0, axis_length, 0, color='green', arrow_length_ratio=0.2, linewidth=2, label='Y-axis')
        ax.quiver(0, 0, 0, 0, 0, axis_length, color='blue', arrow_length_ratio=0.2, linewidth=2, label='Z-axis')

        # Initialize plot elements
        lines = []
        points = []
        trails = []

        for traj in all_trajectories:
            # Trail line (accumulates over time)
            line, = ax.plot([], [], [], '-', color=traj['color'], linewidth=2,
                           alpha=0.6, label=f"Marker {traj['marker_id']}")
            lines.append(line)

            # Current position point
            point = ax.scatter([], [], [], color=traj['color'], s=150,
                              marker='o', edgecolors='black', linewidths=2)
            points.append(point)

            trails.append({'x': [], 'y': [], 'z': []})

        ax.legend(loc='upper right', fontsize=10)
        ax.grid(True, alpha=0.3)

        total_frames = int(fps * duration)

        # Calculate total points across all trajectories
        max_points = max([len(t['x']) for t in all_trajectories])

        def init():
            """Initialize animation"""
            for line in lines:
                line.set_data([], [])
                line.set_3d_properties([])
            return lines + points

        def animate(frame):
            """Animation function called for each frame"""
            # Calculate progress (0 to 1)
            progress = frame / total_frames

            # Rotate view
            angle = progress * 360 * rotation_speed
            ax.view_init(elev=20 + 10 * np.sin(progress * 2 * np.pi), azim=angle)

            # Update trajectories
            for i, traj in enumerate(all_trajectories):
                # Calculate how many points to show based on progress
                num_points = len(traj['x'])
                show_points = int(progress * num_points)

                if show_points > 0:
                    # Update trail
                    x_data = traj['x'][:show_points]
                    y_data = traj['y'][:show_points]
                    z_data = traj['z'][:show_points]

                    lines[i].set_data(x_data, y_data)
                    lines[i].set_3d_properties(z_data)

                    # Update current position point
                    points[i]._offsets3d = ([x_data[-1]], [y_data[-1]], [z_data[-1]])
                else:
                    lines[i].set_data([], [])
                    lines[i].set_3d_properties([])

            # Update title with progress
            ax.set_title(f'3D Trajectory Animation - {progress*100:.1f}% Complete',
                        fontsize=14, fontweight='bold')

            return lines + points

        # Create animation
        print("Generating frames...")
        anim = FuncAnimation(fig, animate, init_func=init, frames=total_frames,
                           interval=1000/fps, blit=False)

        # Save animation
        print("Saving video (this may take a while)...")
        try:
            # Try to use FFMpegWriter first
            writer = FFMpegWriter(fps=fps, bitrate=2000, codec='libx264')
            anim.save(output_path, writer=writer, dpi=100)
            print(f"Video saved successfully: {output_path}")
        except Exception as e:
            print(f"FFMpeg not available, trying Pillow (GIF format)...")
            try:
                # Fallback to GIF using Pillow
                gif_path = output_path.replace('.mp4', '.gif')
                writer = PillowWriter(fps=fps)
                anim.save(gif_path, writer=writer, dpi=100)
                print(f"Animation saved as GIF: {gif_path}")
            except Exception as e2:
                print(f"Error saving animation: {e2}")
                print("Please install ffmpeg: https://ffmpeg.org/download.html")

        plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description='Visualize 3D trajectory of ArUco markers')
    parser.add_argument('csv_path', type=str, nargs='?',
                        default=config.OUTPUT_TRAJECTORY_FILE,
                        help='Path to trajectory CSV file')
    parser.add_argument('--marker-id', type=int, default=None,
                        help='Specific marker ID to visualize (default: all markers)')
    parser.add_argument('--save', type=str, default=None,
                        help=f'Save plot to file (default: {config.PLOT_OUTPUT_FILE})')
    parser.add_argument('--no-show', action='store_true',
                        help='Do not display the plot')
    parser.add_argument('--animate', action='store_true',
                        help='Create 3D animation video')
    parser.add_argument('--video-output', type=str, default='trajectory_animation.mp4',
                        help='Output path for animation video (default: trajectory_animation.mp4)')
    parser.add_argument('--fps', type=int, default=30,
                        help='Frames per second for animation (default: 30)')
    parser.add_argument('--duration', type=int, default=10,
                        help='Duration of animation in seconds (default: 10)')
    parser.add_argument('--rotation-speed', type=float, default=1.0,
                        help='Rotation speed for animation (default: 1.0)')

    args = parser.parse_args()

    # Check if CSV file exists
    if not Path(args.csv_path).exists():
        print(f"Error: CSV file not found: {args.csv_path}")
        return

    # Create visualizer
    visualizer = TrajectoryVisualizer(args.csv_path)

    # Create animation video if requested
    if args.animate:
        print(f"Loading trajectory data from: {args.csv_path}")
        visualizer.create_3d_animation_video(
            marker_id=args.marker_id,
            output_path=args.video_output,
            fps=args.fps,
            duration=args.duration,
            rotation_speed=args.rotation_speed
        )
    else:
        # Determine save path
        save_path = args.save if args.save else (config.PLOT_OUTPUT_FILE if config.SAVE_PLOT else None)

        # Create plots
        print(f"Loading trajectory data from: {args.csv_path}")
        visualizer.plot_3d_trajectory(marker_id=args.marker_id, save_path=save_path,
                                       show=not args.no_show)
        visualizer.plot_position_vs_time(marker_id=args.marker_id, save_path=save_path,
                                         show=not args.no_show)


if __name__ == '__main__':
    main()
