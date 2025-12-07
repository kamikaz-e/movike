#!/usr/bin/env python3
"""
Build statistics tracker for the Movike project.
Tracks build times and maintains statistics: average, current, maximum, and fastest.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any


class BuildStatsTracker:
    """Tracks and maintains build time statistics."""

    def __init__(self, stats_file: str = "build_stats.json"):
        """
        Initialize the build stats tracker.

        Args:
            stats_file: Path to the JSON file storing statistics
        """
        self.stats_file = Path(__file__).parent / stats_file
        self.stats = self._load_stats()

    def _load_stats(self) -> Dict[str, Any]:
        """Load existing statistics from file or create new structure."""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load stats file: {e}", file=sys.stderr)
                return self._create_empty_stats()
        return self._create_empty_stats()

    def _create_empty_stats(self) -> Dict[str, Any]:
        """Create an empty statistics structure."""
        return {
            "builds": [],
            "summary": {
                "total_builds": 0,
                "average_time": 0.0,
                "fastest_time": None,
                "slowest_time": None,
                "current_time": None
            }
        }

    def _save_stats(self) -> None:
        """Save statistics to file."""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except IOError as e:
            print(f"Error: Could not save stats file: {e}", file=sys.stderr)
            sys.exit(1)

    def _update_summary(self) -> None:
        """Update summary statistics based on all builds."""
        builds = self.stats["builds"]

        if not builds:
            return

        build_times = [b["duration_seconds"] for b in builds]

        self.stats["summary"] = {
            "total_builds": len(builds),
            "average_time": sum(build_times) / len(build_times),
            "fastest_time": min(build_times),
            "slowest_time": max(build_times),
            "current_time": builds[-1]["duration_seconds"]
        }

    def add_build(self, duration_seconds: float, commit_hash: str = None,
                  branch: str = None, success: bool = True) -> None:
        """
        Add a new build record and update statistics.

        Args:
            duration_seconds: Build duration in seconds
            commit_hash: Git commit hash (optional)
            branch: Git branch name (optional)
            success: Whether the build was successful
        """
        build_record = {
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "duration_seconds": round(duration_seconds, 2),
            "success": success,
            "commit_hash": commit_hash,
            "branch": branch
        }

        self.stats["builds"].append(build_record)
        self._update_summary()
        self._save_stats()

    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics."""
        return self.stats["summary"]

    def print_summary(self) -> None:
        """Print formatted summary statistics."""
        summary = self.stats["summary"]

        print("\n" + "="*60)
        print("📊 BUILD TIME STATISTICS")
        print("="*60)

        if summary["total_builds"] == 0:
            print("No builds recorded yet.")
            return

        print(f"\n📈 Total builds:     {summary['total_builds']}")
        print(f"⏱️  Current build:    {self._format_duration(summary['current_time'])}")
        print(f"📊 Average build:    {self._format_duration(summary['average_time'])}")
        print(f"🚀 Fastest build:    {self._format_duration(summary['fastest_time'])}")
        print(f"🐌 Slowest build:    {self._format_duration(summary['slowest_time'])}")

        if summary["current_time"] and summary["average_time"]:
            diff = summary["current_time"] - summary["average_time"]
            diff_percent = (diff / summary["average_time"]) * 100

            if diff > 0:
                print(f"\n⚠️  Current build is {self._format_duration(abs(diff))} "
                      f"({abs(diff_percent):.1f}%) SLOWER than average")
            else:
                print(f"\n✅ Current build is {self._format_duration(abs(diff))} "
                      f"({abs(diff_percent):.1f}%) FASTER than average")

        print("\n" + "="*60 + "\n")

    def _format_duration(self, seconds: float) -> str:
        """Format duration in a human-readable way."""
        if seconds is None:
            return "N/A"

        minutes = int(seconds // 60)
        secs = seconds % 60

        if minutes > 0:
            return f"{minutes}m {secs:.1f}s"
        return f"{secs:.1f}s"

    def get_recent_builds(self, count: int = 10) -> list:
        """Get the most recent builds."""
        return self.stats["builds"][-count:]

    def print_recent_builds(self, count: int = 10) -> None:
        """Print recent build history."""
        recent = self.get_recent_builds(count)

        if not recent:
            print("No build history available.")
            return

        print("\n" + "="*60)
        print(f"📜 RECENT BUILDS (last {len(recent)})")
        print("="*60)

        for i, build in enumerate(reversed(recent), 1):
            status = "✅" if build["success"] else "❌"
            timestamp = build["timestamp"].split("T")[0]
            duration = self._format_duration(build["duration_seconds"])
            commit = build.get("commit_hash", "N/A")[:8] if build.get("commit_hash") else "N/A"
            branch = build.get("branch", "N/A")

            print(f"\n{i}. {status} {timestamp} | {duration}")
            print(f"   Commit: {commit} | Branch: {branch}")

        print("\n" + "="*60 + "\n")


def main():
    """Main entry point for the build stats tracker."""
    if len(sys.argv) < 2:
        print("Usage: python3 build_stats.py <duration_seconds> [commit_hash] [branch]")
        print("   or: python3 build_stats.py --show")
        print("   or: python3 build_stats.py --history")
        sys.exit(1)

    tracker = BuildStatsTracker()

    if sys.argv[1] == "--show":
        tracker.print_summary()
    elif sys.argv[1] == "--history":
        tracker.print_recent_builds(20)
    else:
        try:
            duration = float(sys.argv[1])
            commit_hash = sys.argv[2] if len(sys.argv) > 2 else None
            branch = sys.argv[3] if len(sys.argv) > 3 else None

            tracker.add_build(duration, commit_hash, branch)
            tracker.print_summary()

        except ValueError:
            print(f"Error: Invalid duration '{sys.argv[1]}'. Must be a number.",
                  file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
