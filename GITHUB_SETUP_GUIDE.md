# 🚀 GitHub Actions Setup Guide - AI Code Review

This guide will help you set up automated code review in your GitHub repository.

## 📋 Prerequisites

- GitHub repository with the code
- Push access to the repository
- GitHub Actions enabled (enabled by default)

## ✅ What's Already Done

All necessary files are already created:

1. ✅ `.github/workflows/code-review.yml` - GitHub Actions workflow
2. ✅ `assistant/code_reviewer.py` - Main review script
3. ✅ `assistant/mcp_git_server.py` - MCP server for git operations
4. ✅ `assistant/simple_rag.py` - RAG system for documentation
5. ✅ `assistant/requirements.txt` - Dependencies (none needed!)

## 🔧 Step-by-Step Setup

### Step 1: Push the Code to GitHub

```bash
# Make sure you're on the test branch
git branch
# Should show: test-code-review-demo

# Push the branch to GitHub
git push origin test-code-review-demo
```

**Expected output:**
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
...
To github.com:yourusername/movike.git
 * [new branch]      test-code-review-demo -> test-code-review-demo
```

### Step 2: Create a Pull Request

#### Option A: Using GitHub CLI (gh)

```bash
gh pr create \
  --base sketch \
  --head test-code-review-demo \
  --title "Test: AI Code Review Demo" \
  --body "Testing automated code review system"
```

#### Option B: Using GitHub Web UI

1. Go to your repository on GitHub
2. Click "Pull requests" tab
3. Click "New pull request"
4. Set:
   - **Base:** `sketch` (or `main`/`master`)
   - **Compare:** `test-code-review-demo`
5. Click "Create pull request"
6. Add title: "Test: AI Code Review Demo"
7. Click "Create pull request"

### Step 3: Verify GitHub Actions is Running

1. Go to the PR you just created
2. Scroll down to "Checks" section
3. You should see: **"AI Code Review"** workflow running
4. Click on it to see live logs

**Expected workflow steps:**
```
✓ Checkout code
✓ Fetch base branch
✓ Setup Python
✓ Install dependencies
✓ Index documentation with RAG
✓ Run AI Code Review
✓ Post review as comment
✓ Upload review artifact
```

### Step 4: Wait for Review Comment

After ~1-2 minutes, you'll see a new comment on the PR:

```markdown
# 🤖 AI Code Review

**Base branch:** `sketch`
**Head branch:** `test-code-review-demo`
**Files changed:** 10

---

## 📄 `app/src/main/java/com/example/TestCodeReview.kt`
...
```

## 🎯 What Happens Automatically?

Every time you push new commits to a PR:

1. **GitHub Actions triggers** the workflow
2. **Code is checked out** with full git history
3. **Python environment** is set up
4. **RAG indexes** your documentation
5. **Code reviewer analyzes** all changed files
6. **Review comment** is posted or updated on PR
7. **Artifact** is uploaded (review report saved for 30 days)

## 🔍 Verify Setup is Working

### Check 1: Workflow File Exists

```bash
ls -la .github/workflows/code-review.yml
```

Should show the file exists.

### Check 2: Test Locally First

```bash
# From project root
python3 assistant/code_reviewer.py sketch

# Check output
cat assistant/review_output.md
```

If this works, GitHub Actions will work too!

### Check 3: Check GitHub Actions Tab

1. Go to your repository on GitHub
2. Click "Actions" tab
3. You should see "AI Code Review" workflow listed

## 🐛 Troubleshooting

### Issue: Workflow doesn't trigger

**Check:**
- Is the branch you're merging **TO** one of: `main`, `master`, `develop`, `sketch`?
- Is GitHub Actions enabled in your repository?
- Did you push the `.github/workflows/code-review.yml` file?

**Fix:**
```bash
# Verify the workflow file is in git
git ls-files .github/workflows/code-review.yml

# If not, add it
git add .github/workflows/code-review.yml
git commit -m "Add code review workflow"
git push
```

### Issue: Workflow fails at "Run AI Code Review"

**Check logs in GitHub Actions:**
1. Click on the failed workflow
2. Click on "Run AI Code Review" step
3. Read the error message

**Common fixes:**
- Make sure `assistant/code_reviewer.py` is executable
- Verify all Python files are pushed
- Check that base branch exists

### Issue: No comment appears on PR

**Check:**
1. Did workflow complete successfully?
2. Check "Post review as comment" step logs
3. Verify repository has "pull-requests: write" permission

**Permission issue fix:**
Go to repository Settings → Actions → General → Workflow permissions:
- Select "Read and write permissions"
- Check "Allow GitHub Actions to create and approve pull requests"

### Issue: "Review file not found"

This means the review script didn't create output. Check:

```bash
# Test locally
python3 assistant/code_reviewer.py sketch
ls -la assistant/review_output.md
```

## 🎨 Customization

### Change Target Branches

Edit `.github/workflows/code-review.yml`:

```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened]
    branches:
      - main          # Add or remove branches
      - develop
      - your-branch
```

### Change Review Rules

Edit `assistant/code_reviewer.py` to add your own checks:

```python
def _check_kotlin_issues(self, content: str, file_path: str) -> List[str]:
    issues = []

    # Add your custom check
    if 'your_pattern' in content:
        issues.append("Custom issue: found your_pattern")

    return issues
```

### Add Support for Other Languages

In `assistant/code_reviewer.py`:

```python
def analyze_file_changes(self, file_path: str, status: str) -> Dict[str, Any]:
    # ...existing code...

    # Add Java support
    if file_path.endswith('.java'):
        analysis['issues'].extend(self._check_java_issues(content, file_path))

    # Add XML support
    elif file_path.endswith('.xml'):
        analysis['issues'].extend(self._check_xml_issues(content, file_path))
```

## 📊 Monitoring

### View Workflow Runs

1. Go to repository → Actions tab
2. See all workflow runs with status
3. Click on any run to see detailed logs

### Download Review Reports

1. Go to completed workflow run
2. Scroll to "Artifacts" section
3. Download "code-review-report"
4. Reports are kept for 30 days

### Workflow Statistics

GitHub shows:
- Success rate
- Average run time
- Failed runs

## 🔐 Permissions Required

The workflow needs these permissions (already configured):

```yaml
permissions:
  contents: read          # Read repository code
  pull-requests: write    # Post comments on PR
```

These are automatically granted by `GITHUB_TOKEN`.

## 💡 Best Practices

### 1. Test Changes Locally First

```bash
# Before pushing
python3 assistant/code_reviewer.py sketch
```

### 2. Keep Branches Clean

Workflow runs on these events:
- `opened` - New PR created
- `synchronize` - New commits pushed
- `reopened` - Closed PR reopened

### 3. Review Bot Comments

- Read all issues and bugs
- Fix critical problems before merging
- Use suggestions to improve code quality

### 4. Update Documentation

When you update README or docs:
```bash
# RAG will auto-index on next PR
# Or manually:
cd assistant
python3 -c "from simple_rag import SimpleRAG; rag = SimpleRAG(); rag.index_all()"
```

## 📝 Complete Example Flow

```bash
# 1. Create feature branch
git checkout sketch
git pull origin sketch
git checkout -b feature/new-screen

# 2. Make changes
# Edit some Kotlin files...

# 3. Test locally
python3 assistant/code_reviewer.py sketch
cat assistant/review_output.md

# 4. Commit and push
git add .
git commit -m "feat: add new screen"
git push origin feature/new-screen

# 5. Create PR (using gh CLI or web UI)
gh pr create --base sketch --head feature/new-screen \
  --title "Add new screen" \
  --body "Description of changes"

# 6. Wait for automatic review comment
# GitHub Actions will post review within 1-2 minutes

# 7. Fix issues if found
# Edit code based on review...
git add .
git commit -m "fix: address review comments"
git push

# 8. Review is automatically updated!
```

## ✅ Verification Checklist

Before creating your first real PR, verify:

- [ ] Workflow file exists: `.github/workflows/code-review.yml`
- [ ] All assistant scripts are committed
- [ ] Local test works: `python3 assistant/code_reviewer.py sketch`
- [ ] Test branch is pushed to GitHub
- [ ] Test PR is created
- [ ] GitHub Actions runs successfully
- [ ] Review comment appears on PR
- [ ] Artifact is uploaded

## 🎉 You're All Set!

Your automated code review system is now active!

Every PR will automatically get:
- ⚠️ Problem detection
- 🐛 Bug identification
- 💡 Improvement suggestions
- 📚 Related documentation

---

**Questions?** Check the full documentation:
- `assistant/CODE_REVIEW_README.md` - Detailed documentation
- `QUICK_START_CODE_REVIEW.md` - Quick start guide

**Need help?** Create an issue in the repository.
