"""
Trajectory Analysis Script
Analyzes ArUco marker trajectory data from CSV files
Calculates speed, velocity, distance, angular changes, and generates graphs
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse
from pathlib import Path
from scipy.signal import savgol_filter


class TrajectoryAnalyzer:
    def __init__(self, csv_path):
        """
        Initialize trajectory analyzer

        Args:
            csv_path: Path to CSV file with trajectory data
        """
        self.csv_path = csv_path
        self.df = None
        self.markers = {}
        self.load_data()

    def load_data(self):
        """Load and preprocess trajectory data"""
        print(f"Loading trajectory data from: {self.csv_path}")

        self.df = pd.read_csv(self.csv_path)

        # Check required columns
        required_cols = ['timestamp', 'marker_id', 'x', 'y', 'z', 'rx', 'ry', 'rz']
        missing_cols = [col for col in required_cols if col not in self.df.columns]

        if missing_cols:
            print(f"Warning: Missing columns: {missing_cols}")
            return

        # Group by marker ID
        for marker_id in self.df['marker_id'].unique():
            marker_data = self.df[self.df['marker_id'] == marker_id].copy()
            marker_data = marker_data.sort_values('timestamp').reset_index(drop=True)
            self.markers[marker_id] = marker_data

        print(f"Loaded data for {len(self.markers)} marker(s)")
        for marker_id, data in self.markers.items():
            print(f"  Marker {marker_id}: {len(data)} data points")

    def calculate_metrics(self, marker_id=None, smooth=True, window=5):
        """
        Calculate motion metrics for trajectory

        Args:
            marker_id: Specific marker ID (None = all markers)
            smooth: Apply smoothing filter
            window: Smoothing window size

        Returns:
            Dictionary of metrics by marker ID
        """
        marker_ids = [marker_id] if marker_id is not None else self.markers.keys()
        results = {}

        for mid in marker_ids:
            if mid not in self.markers:
                print(f"Warning: Marker {mid} not found")
                continue

            df = self.markers[mid].copy()

            # Time differences
            df['dt'] = df['timestamp'].diff()

            # Position differences
            df['dx'] = df['x'].diff()
            df['dy'] = df['y'].diff()
            df['dz'] = df['z'].diff()

            # Distance (3D Euclidean distance)
            df['distance'] = np.sqrt(df['dx']**2 + df['dy']**2 + df['dz']**2)
            df['cumulative_distance'] = df['distance'].cumsum()

            # Velocity components (m/s)
            df['vx'] = df['dx'] / df['dt']
            df['vy'] = df['dy'] / df['dt']
            df['vz'] = df['dz'] / df['dt']

            # Speed (magnitude of velocity)
            df['speed'] = np.sqrt(df['vx']**2 + df['vy']**2 + df['vz']**2)

            # Acceleration components
            df['ax'] = df['vx'].diff() / df['dt']
            df['ay'] = df['vy'].diff() / df['dt']
            df['az'] = df['vz'].diff() / df['dt']

            # Acceleration magnitude
            df['acceleration'] = np.sqrt(df['ax']**2 + df['ay']**2 + df['az']**2)

            # Angular velocity (rad/s)
            df['drx'] = df['rx'].diff()
            df['dry'] = df['ry'].diff()
            df['drz'] = df['rz'].diff()

            df['omega_x'] = df['drx'] / df['dt']
            df['omega_y'] = df['dry'] / df['dt']
            df['omega_z'] = df['drz'] / df['dt']

            # Angular speed (magnitude)
            df['angular_speed'] = np.sqrt(df['omega_x']**2 + df['omega_y']**2 + df['omega_z']**2)

            # Convert rotation to degrees for easier interpretation
            df['rx_deg'] = np.degrees(df['rx'])
            df['ry_deg'] = np.degrees(df['ry'])
            df['rz_deg'] = np.degrees(df['rz'])

            # Smooth data if requested
            if smooth and len(df) > window:
                smooth_cols = ['speed', 'acceleration', 'angular_speed',
                              'rx_deg', 'ry_deg', 'rz_deg']
                for col in smooth_cols:
                    if col in df.columns:
                        df[f'{col}_raw'] = df[col].copy()
                        df[col] = savgol_filter(df[col].fillna(0), window, 2)

            results[mid] = df

        return results

    def print_summary(self, marker_id=None):
        """
        Print summary statistics

        Args:
            marker_id: Specific marker ID (None = all markers)
        """
        metrics = self.calculate_metrics(marker_id)

        print("\n" + "="*70)
        print("TRAJECTORY ANALYSIS SUMMARY")
        print("="*70)

        for mid, df in metrics.items():
            print(f"\nMarker {mid}:")
            print("-" * 70)

            # Time statistics
            duration = df['timestamp'].max() - df['timestamp'].min()
            print(f"\nTime Statistics:")
            print(f"  Duration: {duration:.2f} seconds")
            print(f"  Data points: {len(df)}")
            print(f"  Sample rate: {len(df)/duration:.1f} Hz")

            # Position statistics
            print(f"\nPosition Range:")
            print(f"  X: [{df['x'].min():.4f}, {df['x'].max():.4f}] m (range: {df['x'].max()-df['x'].min():.4f} m)")
            print(f"  Y: [{df['y'].min():.4f}, {df['y'].max():.4f}] m (range: {df['y'].max()-df['y'].min():.4f} m)")
            print(f"  Z: [{df['z'].min():.4f}, {df['z'].max():.4f}] m (range: {df['z'].max()-df['z'].min():.4f} m)")

            # Distance statistics
            total_dist = df['cumulative_distance'].max()
            print(f"\nDistance Statistics:")
            print(f"  Total distance traveled: {total_dist:.4f} m")
            print(f"  Average distance per move: {df['distance'].mean():.6f} m")

            # Speed statistics (filter out NaN and inf)
            speed_valid = df['speed'].replace([np.inf, -np.inf], np.nan).dropna()
            if len(speed_valid) > 0:
                print(f"\nSpeed Statistics:")
                print(f"  Average speed: {speed_valid.mean():.4f} m/s")
                print(f"  Maximum speed: {speed_valid.max():.4f} m/s")
                print(f"  Minimum speed: {speed_valid.min():.4f} m/s")
                print(f"  Std deviation: {speed_valid.std():.4f} m/s")

            # Acceleration statistics
            accel_valid = df['acceleration'].replace([np.inf, -np.inf], np.nan).dropna()
            if len(accel_valid) > 0:
                print(f"\nAcceleration Statistics:")
                print(f"  Average: {accel_valid.mean():.4f} m/s²")
                print(f"  Maximum: {accel_valid.max():.4f} m/s²")

            # Angular statistics
            print(f"\nRotation Range (degrees):")
            print(f"  RX: [{df['rx_deg'].min():.2f}, {df['rx_deg'].max():.2f}]° (range: {df['rx_deg'].max()-df['rx_deg'].min():.2f}°)")
            print(f"  RY: [{df['ry_deg'].min():.2f}, {df['ry_deg'].max():.2f}]° (range: {df['ry_deg'].max()-df['ry_deg'].min():.2f}°)")
            print(f"  RZ: [{df['rz_deg'].min():.2f}, {df['rz_deg'].max():.2f}]° (range: {df['rz_deg'].max()-df['rz_deg'].min():.2f}°)")

            # Angular velocity
            omega_valid = df['angular_speed'].replace([np.inf, -np.inf], np.nan).dropna()
            if len(omega_valid) > 0:
                print(f"\nAngular Speed Statistics:")
                print(f"  Average: {omega_valid.mean():.4f} rad/s ({np.degrees(omega_valid.mean()):.2f}°/s)")
                print(f"  Maximum: {omega_valid.max():.4f} rad/s ({np.degrees(omega_valid.max()):.2f}°/s)")

        print("="*70 + "\n")

    def plot_position_vs_time(self, marker_id=None, save_path=None, show=True):
        """
        Plot X, Y, Z positions vs time

        Args:
            marker_id: Specific marker ID (None = all markers)
            save_path: Path to save plot
            show: Whether to display plot
        """
        metrics = self.calculate_metrics(marker_id)

        fig, axes = plt.subplots(3, 1, figsize=(12, 10))
        colors = plt.cm.rainbow(np.linspace(0, 1, len(metrics)))

        for idx, (mid, df) in enumerate(metrics.items()):
            axes[0].plot(df['timestamp'], df['x'], '-', color=colors[idx],
                        linewidth=2, label=f'Marker {mid}', alpha=0.7)
            axes[1].plot(df['timestamp'], df['y'], '-', color=colors[idx],
                        linewidth=2, label=f'Marker {mid}', alpha=0.7)
            axes[2].plot(df['timestamp'], df['z'], '-', color=colors[idx],
                        linewidth=2, label=f'Marker {mid}', alpha=0.7)

        axes[0].set_ylabel('X Position (m)', fontsize=11, fontweight='bold')
        axes[0].set_title('Position vs Time', fontsize=14, fontweight='bold')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        axes[1].set_ylabel('Y Position (m)', fontsize=11, fontweight='bold')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

        axes[2].set_ylabel('Z Position (m)', fontsize=11, fontweight='bold')
        axes[2].set_xlabel('Time (seconds)', fontsize=11, fontweight='bold')
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved position plot: {save_path}")

        if show:
            plt.show()
        else:
            plt.close()

    def plot_velocity_analysis(self, marker_id=None, save_path=None, show=True):
        """
        Plot velocity and speed analysis

        Args:
            marker_id: Specific marker ID (None = all markers)
            save_path: Path to save plot
            show: Whether to display plot
        """
        metrics = self.calculate_metrics(marker_id)

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        colors = plt.cm.rainbow(np.linspace(0, 1, len(metrics)))

        for idx, (mid, df) in enumerate(metrics.items()):
            # Velocity components
            axes[0, 0].plot(df['timestamp'], df['vx'], '-', color=colors[idx],
                           linewidth=1.5, label=f'Marker {mid}', alpha=0.7)
            axes[0, 1].plot(df['timestamp'], df['vy'], '-', color=colors[idx],
                           linewidth=1.5, label=f'Marker {mid}', alpha=0.7)
            axes[1, 0].plot(df['timestamp'], df['vz'], '-', color=colors[idx],
                           linewidth=1.5, label=f'Marker {mid}', alpha=0.7)

            # Speed (magnitude)
            axes[1, 1].plot(df['timestamp'], df['speed'], '-', color=colors[idx],
                           linewidth=2, label=f'Marker {mid}', alpha=0.7)

        axes[0, 0].set_ylabel('Vx (m/s)', fontsize=10, fontweight='bold')
        axes[0, 0].set_title('Velocity Components', fontsize=12, fontweight='bold')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)

        axes[0, 1].set_ylabel('Vy (m/s)', fontsize=10, fontweight='bold')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)

        axes[1, 0].set_ylabel('Vz (m/s)', fontsize=10, fontweight='bold')
        axes[1, 0].set_xlabel('Time (seconds)', fontsize=10, fontweight='bold')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)

        axes[1, 1].set_ylabel('Speed (m/s)', fontsize=10, fontweight='bold')
        axes[1, 1].set_xlabel('Time (seconds)', fontsize=10, fontweight='bold')
        axes[1, 1].set_title('Speed Magnitude', fontsize=12, fontweight='bold')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved velocity plot: {save_path}")

        if show:
            plt.show()
        else:
            plt.close()

    def plot_distance_analysis(self, marker_id=None, save_path=None, show=True):
        """
        Plot distance traveled over time

        Args:
            marker_id: Specific marker ID (None = all markers)
            save_path: Path to save plot
            show: Whether to display plot
        """
        metrics = self.calculate_metrics(marker_id)

        fig, axes = plt.subplots(2, 1, figsize=(12, 8))
        colors = plt.cm.rainbow(np.linspace(0, 1, len(metrics)))

        for idx, (mid, df) in enumerate(metrics.items()):
            # Cumulative distance
            axes[0].plot(df['timestamp'], df['cumulative_distance'], '-',
                        color=colors[idx], linewidth=2, label=f'Marker {mid}', alpha=0.7)

            # Instantaneous distance (per time step)
            axes[1].plot(df['timestamp'], df['distance'], '-',
                        color=colors[idx], linewidth=1.5, label=f'Marker {mid}', alpha=0.7)

        axes[0].set_ylabel('Cumulative Distance (m)', fontsize=11, fontweight='bold')
        axes[0].set_title('Distance Analysis', fontsize=14, fontweight='bold')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        axes[1].set_ylabel('Instantaneous Distance (m)', fontsize=11, fontweight='bold')
        axes[1].set_xlabel('Time (seconds)', fontsize=11, fontweight='bold')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved distance plot: {save_path}")

        if show:
            plt.show()
        else:
            plt.close()

    def plot_angular_analysis(self, marker_id=None, save_path=None, show=True):
        """
        Plot angular rotation and angular velocity over time

        Args:
            marker_id: Specific marker ID (None = all markers)
            save_path: Path to save plot
            show: Whether to display plot
        """
        metrics = self.calculate_metrics(marker_id)

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        colors = plt.cm.rainbow(np.linspace(0, 1, len(metrics)))

        for idx, (mid, df) in enumerate(metrics.items()):
            # Rotation angles (degrees)
            axes[0, 0].plot(df['timestamp'], df['rx_deg'], '-', color=colors[idx],
                           linewidth=1.5, label=f'Marker {mid}', alpha=0.7)
            axes[0, 1].plot(df['timestamp'], df['ry_deg'], '-', color=colors[idx],
                           linewidth=1.5, label=f'Marker {mid}', alpha=0.7)
            axes[1, 0].plot(df['timestamp'], df['rz_deg'], '-', color=colors[idx],
                           linewidth=1.5, label=f'Marker {mid}', alpha=0.7)

            # Angular speed
            axes[1, 1].plot(df['timestamp'], np.degrees(df['angular_speed']), '-',
                           color=colors[idx], linewidth=2, label=f'Marker {mid}', alpha=0.7)

        axes[0, 0].set_ylabel('Rotation X (degrees)', fontsize=10, fontweight='bold')
        axes[0, 0].set_title('Angular Rotation Over Time', fontsize=12, fontweight='bold')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)

        axes[0, 1].set_ylabel('Rotation Y (degrees)', fontsize=10, fontweight='bold')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)

        axes[1, 0].set_ylabel('Rotation Z (degrees)', fontsize=10, fontweight='bold')
        axes[1, 0].set_xlabel('Time (seconds)', fontsize=10, fontweight='bold')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)

        axes[1, 1].set_ylabel('Angular Speed (deg/s)', fontsize=10, fontweight='bold')
        axes[1, 1].set_xlabel('Time (seconds)', fontsize=10, fontweight='bold')
        axes[1, 1].set_title('Angular Speed Magnitude', fontsize=12, fontweight='bold')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved angular plot: {save_path}")

        if show:
            plt.show()
        else:
            plt.close()

    def plot_acceleration_analysis(self, marker_id=None, save_path=None, show=True):
        """
        Plot acceleration analysis

        Args:
            marker_id: Specific marker ID (None = all markers)
            save_path: Path to save plot
            show: Whether to display plot
        """
        metrics = self.calculate_metrics(marker_id)

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        colors = plt.cm.rainbow(np.linspace(0, 1, len(metrics)))

        for idx, (mid, df) in enumerate(metrics.items()):
            # Acceleration components
            axes[0, 0].plot(df['timestamp'], df['ax'], '-', color=colors[idx],
                           linewidth=1.5, label=f'Marker {mid}', alpha=0.7)
            axes[0, 1].plot(df['timestamp'], df['ay'], '-', color=colors[idx],
                           linewidth=1.5, label=f'Marker {mid}', alpha=0.7)
            axes[1, 0].plot(df['timestamp'], df['az'], '-', color=colors[idx],
                           linewidth=1.5, label=f'Marker {mid}', alpha=0.7)

            # Acceleration magnitude
            axes[1, 1].plot(df['timestamp'], df['acceleration'], '-',
                           color=colors[idx], linewidth=2, label=f'Marker {mid}', alpha=0.7)

        axes[0, 0].set_ylabel('Ax (m/s²)', fontsize=10, fontweight='bold')
        axes[0, 0].set_title('Acceleration Components', fontsize=12, fontweight='bold')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)

        axes[0, 1].set_ylabel('Ay (m/s²)', fontsize=10, fontweight='bold')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)

        axes[1, 0].set_ylabel('Az (m/s²)', fontsize=10, fontweight='bold')
        axes[1, 0].set_xlabel('Time (seconds)', fontsize=10, fontweight='bold')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)

        axes[1, 1].set_ylabel('Acceleration (m/s²)', fontsize=10, fontweight='bold')
        axes[1, 1].set_xlabel('Time (seconds)', fontsize=10, fontweight='bold')
        axes[1, 1].set_title('Acceleration Magnitude', fontsize=12, fontweight='bold')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Saved acceleration plot: {save_path}")

        if show:
            plt.show()
        else:
            plt.close()

    def export_analysis(self, marker_id=None, output_path='analysis_results.csv'):
        """
        Export calculated metrics to CSV

        Args:
            marker_id: Specific marker ID (None = all markers)
            output_path: Output CSV file path
        """
        metrics = self.calculate_metrics(marker_id)

        # Combine all marker data
        all_data = []
        for mid, df in metrics.items():
            df_export = df.copy()
            df_export['marker_id'] = mid
            all_data.append(df_export)

        combined_df = pd.concat(all_data, ignore_index=True)

        # Select columns to export
        export_cols = ['timestamp', 'marker_id', 'x', 'y', 'z',
                      'vx', 'vy', 'vz', 'speed',
                      'ax', 'ay', 'az', 'acceleration',
                      'distance', 'cumulative_distance',
                      'rx_deg', 'ry_deg', 'rz_deg',
                      'omega_x', 'omega_y', 'omega_z', 'angular_speed']

        # Export only existing columns
        export_cols = [col for col in export_cols if col in combined_df.columns]
        combined_df[export_cols].to_csv(output_path, index=False)

        print(f"Exported analysis results to: {output_path}")

    def generate_full_report(self, marker_id=None, output_dir='analysis_output'):
        """
        Generate complete analysis report with all plots

        Args:
            marker_id: Specific marker ID (None = all markers)
            output_dir: Output directory for plots
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        print(f"\nGenerating full analysis report in: {output_dir}")
        print("-" * 70)

        # Print summary
        self.print_summary(marker_id)

        # Generate all plots
        self.plot_position_vs_time(marker_id,
                                   save_path=output_path / 'position_vs_time.png',
                                   show=False)

        self.plot_velocity_analysis(marker_id,
                                    save_path=output_path / 'velocity_analysis.png',
                                    show=False)

        self.plot_distance_analysis(marker_id,
                                    save_path=output_path / 'distance_analysis.png',
                                    show=False)

        self.plot_angular_analysis(marker_id,
                                   save_path=output_path / 'angular_analysis.png',
                                   show=False)

        self.plot_acceleration_analysis(marker_id,
                                       save_path=output_path / 'acceleration_analysis.png',
                                       show=False)

        # Export metrics
        self.export_analysis(marker_id, output_path / 'analysis_metrics.csv')

        print(f"\n[OK] Full report generated successfully!")
        print(f"\nGenerated files:")
        print(f"  - position_vs_time.png")
        print(f"  - velocity_analysis.png")
        print(f"  - distance_analysis.png")
        print(f"  - angular_analysis.png")
        print(f"  - acceleration_analysis.png")
        print(f"  - analysis_metrics.csv")


def main():
    parser = argparse.ArgumentParser(
        description='Analyze ArUco marker trajectory data'
    )
    parser.add_argument('csv_path', type=str, help='Path to trajectory CSV file')
    parser.add_argument('--marker-id', type=int, default=None,
                        help='Specific marker ID to analyze')
    parser.add_argument('--summary', action='store_true',
                        help='Print summary statistics only')
    parser.add_argument('--plot', type=str, choices=['position', 'velocity', 'distance',
                                                     'angular', 'acceleration', 'all'],
                        help='Generate specific plot')
    parser.add_argument('--output-dir', type=str, default='analysis_output',
                        help='Output directory for full report')
    parser.add_argument('--export', type=str, help='Export metrics to CSV file')
    parser.add_argument('--no-show', action='store_true',
                        help='Do not display plots')
    parser.add_argument('--full-report', action='store_true',
                        help='Generate full analysis report')

    args = parser.parse_args()

    # Check if file exists
    if not Path(args.csv_path).exists():
        print(f"Error: File not found: {args.csv_path}")
        return

    # Create analyzer
    analyzer = TrajectoryAnalyzer(args.csv_path)

    # Generate full report
    if args.full_report:
        analyzer.generate_full_report(args.marker_id, args.output_dir)
        return

    # Print summary
    if args.summary or args.plot is None:
        analyzer.print_summary(args.marker_id)

    # Generate plots
    if args.plot:
        show = not args.no_show

        if args.plot == 'position':
            analyzer.plot_position_vs_time(args.marker_id, show=show)
        elif args.plot == 'velocity':
            analyzer.plot_velocity_analysis(args.marker_id, show=show)
        elif args.plot == 'distance':
            analyzer.plot_distance_analysis(args.marker_id, show=show)
        elif args.plot == 'angular':
            analyzer.plot_angular_analysis(args.marker_id, show=show)
        elif args.plot == 'acceleration':
            analyzer.plot_acceleration_analysis(args.marker_id, show=show)
        elif args.plot == 'all':
            analyzer.plot_position_vs_time(args.marker_id, show=show)
            analyzer.plot_velocity_analysis(args.marker_id, show=show)
            analyzer.plot_distance_analysis(args.marker_id, show=show)
            analyzer.plot_angular_analysis(args.marker_id, show=show)
            analyzer.plot_acceleration_analysis(args.marker_id, show=show)

    # Export metrics
    if args.export:
        analyzer.export_analysis(args.marker_id, args.export)


if __name__ == '__main__':
    main()
