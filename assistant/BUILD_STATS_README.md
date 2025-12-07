# Build Time Statistics System

This system automatically tracks build times and maintains statistics when commits are pushed to Git.

## Features

- **Automatic build time measurement** on every push (GitHub Actions) or commit (Git hook)
- **Statistics tracking**:
  - Current build time
  - Average build time
  - Fastest build time
  - Slowest build time
  - Total number of builds
- **Performance comparison**: Shows how the current build compares to the average
- **Build history**: View recent builds with timestamps and commit information

## Components

### 1. `build_stats.py`
Python script that manages the build statistics database.

**Usage:**
```bash
# Record a new build
python3 build_stats.py <duration_seconds> [commit_hash] [branch]

# Show current statistics
python3 build_stats.py --show

# Show build history
python3 build_stats.py --history
```

### 2. `measure_build.sh`
Shell script that measures build time and updates statistics.

**Usage:**
```bash
./measure_build.sh
```

This script:
1. Gets current Git commit and branch information
2. Runs the Gradle build
3. Measures the build duration
4. Updates the statistics
5. Displays the current statistics

### 3. GitHub Actions Workflow (`.github/workflows/build-stats.yml`)
Automatically runs on every push to main branches:
- Compiles the build
- Measures build time
- Updates statistics
- Shows summary in GitHub Actions output
- Uploads statistics as artifacts

### 4. Git Post-Commit Hook (optional)
Runs locally after each commit to track build times on your machine.

**Setup:**
```bash
./setup_git_hook.sh
```

## Installation

### Option 1: GitHub Actions (Recommended for CI/CD)

The GitHub Actions workflow is already configured in `.github/workflows/build-stats.yml`.

It will automatically run on pushes to:
- `main`
- `master`
- `develop`
- `sketch`
- `lesson_*` branches

**No setup required** - just push to one of these branches!

### Option 2: Local Git Hook

To track build times locally after each commit:

```bash
cd assistant
./setup_git_hook.sh
```

This installs a post-commit hook that automatically:
1. Builds the project after each commit
2. Measures the build time
3. Updates local statistics

**Note:** This will run a full build after every commit, which may slow down your workflow.

## Viewing Statistics

### Show current statistics:
```bash
python3 assistant/build_stats.py --show
```

Output example:
```
============================================================
📊 BUILD TIME STATISTICS
============================================================

📈 Total builds:     15
⏱️  Current build:    2m 34.5s
📊 Average build:    2m 28.3s
🚀 Fastest build:    1m 45.2s
🐌 Slowest build:    3m 12.1s

⚠️  Current build is 6.2s (4.2%) SLOWER than average

============================================================
```

### View build history:
```bash
python3 assistant/build_stats.py --history
```

Output example:
```
============================================================
📜 RECENT BUILDS (last 10)
============================================================

1. ✅ 2025-12-08 | 2m 34.5s
   Commit: a1b2c3d4 | Branch: lesson_23

2. ✅ 2025-12-07 | 2m 15.8s
   Commit: e5f6g7h8 | Branch: sketch

3. ✅ 2025-12-07 | 2m 42.1s
   Commit: i9j0k1l2 | Branch: lesson_22
...
============================================================
```

## Statistics File

Statistics are stored in `assistant/build_stats.json`:

```json
{
  "builds": [
    {
      "timestamp": "2025-12-08T10:30:45Z",
      "duration_seconds": 154.5,
      "success": true,
      "commit_hash": "a1b2c3d4",
      "branch": "lesson_23"
    }
  ],
  "summary": {
    "total_builds": 15,
    "average_time": 148.3,
    "fastest_time": 105.2,
    "slowest_time": 192.1,
    "current_time": 154.5
  }
}
```

## GitHub Actions Integration

### Viewing in GitHub Actions

1. Go to your repository on GitHub
2. Click on **Actions** tab
3. Select **Build Time Statistics** workflow
4. Click on any workflow run
5. View the statistics in:
   - Job summary (at the bottom of the run page)
   - Step outputs (in "Display statistics" step)

### Downloading Statistics

Statistics are uploaded as artifacts and retained for 90 days:

1. Go to workflow run page
2. Scroll to **Artifacts** section
3. Download `build-statistics`

## Integration with Existing Workflows

The build statistics workflow runs independently and doesn't interfere with other workflows like code review.

You can also integrate build time measurement into existing workflows:

```yaml
- name: Measure build time
  run: |
    cd assistant
    ./measure_build.sh
```

## Troubleshooting

### Statistics not updating

**Check:**
1. Is the workflow enabled in GitHub Actions?
2. Are you pushing to a tracked branch?
3. Check workflow logs for errors

### Local hook not working

**Check:**
1. Is the hook executable? `ls -la .git/hooks/post-commit`
2. Run `chmod +x .git/hooks/post-commit`
3. Ensure `measure_build.sh` is executable

### Build fails in workflow

**Check:**
1. Review GitHub Actions logs
2. Ensure all dependencies are available
3. Check Android SDK setup

## Customization

### Change tracked branches

Edit `.github/workflows/build-stats.yml`:

```yaml
on:
  push:
    branches:
      - your-branch-name
      - another-branch
```

### Change statistics file location

Edit `build_stats.py`:

```python
tracker = BuildStatsTracker(stats_file="custom_location.json")
```

### Exclude certain builds

Modify `measure_build.sh` to add conditions:

```bash
# Only track on main branch
if [ "$BRANCH" != "main" ]; then
    echo "Skipping stats for branch $BRANCH"
    exit 0
fi
```

## Best Practices

1. **Don't commit `build_stats.json`** - Keep it local or in artifacts only
2. **Use GitHub Actions for team statistics** - Consistent build environment
3. **Use local hook for personal tracking** - Monitor your development machine performance
4. **Review trends regularly** - Identify build performance degradation early
5. **Archive old statistics** - Keep the stats file manageable

## Future Enhancements

Possible improvements:
- Build time trending graphs
- Performance alerts when builds are significantly slower
- Build time breakdown by module
- Integration with Slack/Discord notifications
- Historical data visualization
- Comparison across different branches
