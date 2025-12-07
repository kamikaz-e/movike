# Quick Reference - Code Review

## Run the Check

```bash
cd /Users/admin/StudioProjects/movike
python3 assistant/code_reviewer.py sketch
```

## View Results

```bash
cat assistant/review_output.md
```

## Files with Intentional Errors

| File | Issues | Location |
|------|--------|----------|
| **ApiService.kt** | Blocking calls, hardcoded API key | `app/src/main/java/dev/kamikaze/movike/api/ApiService.kt:14-36` |
| **RepositoryImpl.kt** | Memory leaks, GlobalScope, unclosed resources | `app/src/main/java/dev/kamikaze/movike/repository/RepositoryImpl.kt:29-116` |
| **FeedViewModel.kt** | Public LiveData, Activity refs, no error handling | `app/src/main/java/dev/kamikaze/movike/presentation/ui/viewmodel/FeedViewModel.kt:35-89` |
| **ApiModule.kt** | Logging secrets, HTTP, no cert pinning | `app/src/main/java/dev/kamikaze/movike/api/ApiModule.kt:25-140` |
| **FeedFragment.kt** | Naming, magic numbers, dead code | `app/src/main/java/dev/kamikaze/movike/presentation/ui/fragments/FeedFragment.kt:45-182` |

## Error Categories

- 🔴 **Security** (7 issues): Hardcoded keys, HTTP, logging secrets
- 🟠 **Memory Leaks** (6 issues): GlobalScope, unclosed streams, Activity refs
- 🟡 **Architecture** (5 issues): Blocking calls, wrong dispatchers
- 🔵 **Code Style** (10+ issues): Naming, magic numbers, formatting

## Expected Detection

The code reviewer should detect approximately **28+ issues** total:

- ApiService.kt: ~4 issues
- RepositoryImpl.kt: ~7 issues  
- FeedViewModel.kt: ~7 issues
- ApiModule.kt: ~6 issues
- FeedFragment.kt: ~10 issues

All issues are marked with `// BAD:` comments for easy verification.
