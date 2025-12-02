# 🤖 AI Code Review

**Mode:** Проверка всех файлов (sketch)
**Files analyzed:** 120

---

## 📄 `app/src/main/java/dev/kamikaze/movike/api/ApiModule.kt`

**Status:** M

### 💡 Советы по улучшению:

- Line 126: Для констант на уровне файла используйте const val
- Line 128: Для констант на уровне файла используйте const val

### 📚 Связанная документация:

- `project/docs/API_REFERENCE.md` (релевантность: 11)
- `app/src/main/java/dev/kamikaze/movike/api/ApiModule.kt:21` (релевантность: 11)

---

## 📄 `app/src/main/java/dev/kamikaze/movike/common/base/BaseFragment.kt`

**Status:** M

### ⚠️ Проблемы:

- Line 18: Использование !! (force unwrap) может привести к NPE
- Line 21: Использование !! (force unwrap) может привести к NPE

### 🐛 Потенциальные баги:

- Line 42: Убедитесь, что listener очищается в onDestroy/onDestroyView

### 📚 Связанная документация:

- `app/src/main/java/dev/kamikaze/movike/common/AutoDestroyValue.kt:10` (релевантность: 12)
- `app/src/main/java/dev/kamikaze/movike/common/base/BaseDialog.kt:6` (релевантность: 12)

---

## 📄 `app/src/main/java/dev/kamikaze/movike/common/base/BaseViewModel.kt`

**Status:** M

### 🐛 Потенциальные баги:

- Line 32: Корутина без явного Dispatcher - может выполняться на UI потоке
- Line 55: Корутина без явного Dispatcher - может выполняться на UI потоке
- Line 64: Корутина без явного Dispatcher - может выполняться на UI потоке

### 📚 Связанная документация:

- `app/src/main/java/dev/kamikaze/movike/common/base/BaseViewModel.kt:13` (релевантность: 12)
- `app/src/main/java/dev/kamikaze/movike/common/AutoDestroyValue.kt:10` (релевантность: 11)

---

## 📄 `app/src/main/java/dev/kamikaze/movike/di/modules/DBModule.kt`

**Status:** M

### 💡 Советы по улучшению:

- Line 26: Рассмотрите использование ?.let { } вместо if != null

### 📚 Связанная документация:

- `app/src/main/java/dev/kamikaze/movike/di/modules/DBModule.kt:14` (релевантность: 12)
- `app/src/main/java/dev/kamikaze/movike/di/modules/DataModule.kt:12` (релевантность: 11)

---

## 📄 `app/src/main/java/dev/kamikaze/movike/presentation/adapters/viewholders/LoadStateViewHolder.kt`

**Status:** M

### 🐛 Потенциальные баги:

- Line 16: Убедитесь, что listener очищается в onDestroy/onDestroyView

### 📚 Связанная документация:

- `app/src/main/java/dev/kamikaze/movike/presentation/adapters/viewholders/LoadStateViewHolder.kt:10` (релевантность: 13)
- `app/src/main/java/dev/kamikaze/movike/presentation/adapters/LoadingStateAdapter.kt:12` (релевантность: 12)

---

## 📄 `app/src/main/java/dev/kamikaze/movike/presentation/adapters/viewholders/MovieHolder.kt`

**Status:** M

### 🐛 Потенциальные баги:

- Line 24: Убедитесь, что listener очищается в onDestroy/onDestroyView

### 📚 Связанная документация:

- `app/src/main/java/dev/kamikaze/movike/presentation/adapters/viewholders/MovieHolder.kt:9` (релевантность: 13)
- `app/src/main/java/dev/kamikaze/movike/presentation/adapters/viewholders/SearchMovieHolder.kt:9` (релевантность: 13)

---

## 📄 `app/src/main/java/dev/kamikaze/movike/presentation/adapters/viewholders/SearchMovieHolder.kt`

**Status:** M

### 🐛 Потенциальные баги:

- Line 24: Убедитесь, что listener очищается в onDestroy/onDestroyView
- Line 25: Убедитесь, что listener очищается в onDestroy/onDestroyView
- Line 26: Убедитесь, что listener очищается в onDestroy/onDestroyView

### 📚 Связанная документация:

- `app/src/main/java/dev/kamikaze/movike/presentation/adapters/viewholders/SearchMovieHolder.kt:9` (релевантность: 13)
- `app/src/main/java/dev/kamikaze/movike/presentation/adapters/SearchMovieAdapter.kt:13` (релевантность: 12)

---

## 📄 `app/src/main/java/dev/kamikaze/movike/presentation/customviews/WatchMovieBtn.kt`

**Status:** M

### 🐛 Потенциальные баги:

- Line 35: Убедитесь, что listener очищается в onDestroy/onDestroyView

### 📚 Связанная документация:

- `app/src/main/java/dev/kamikaze/movike/presentation/customviews/WatchMovieBtn.kt:12` (релевантность: 12)
- `app/src/main/java/dev/kamikaze/movike/presentation/customviews/WatchMovieBtn.kt:47` (релевантность: 12)

---

## 📄 `app/src/main/java/dev/kamikaze/movike/presentation/customviews/error/ErrorView.kt`

**Status:** M

### ⚠️ Проблемы:

- Line 16: Использование !! (force unwrap) может привести к NPE

### 🐛 Потенциальные баги:

- Line 22: Убедитесь, что listener очищается в onDestroy/onDestroyView

### 📚 Связанная документация:

- `app/src/main/java/dev/kamikaze/movike/presentation/customviews/error/ErrorView.kt:12` (релевантность: 13)
- `app/src/main/java/dev/kamikaze/movike/presentation/customviews/error/ErrorCallback.kt:3` (релевантность: 12)

---

## 📄 `app/src/main/java/dev/kamikaze/movike/presentation/customviews/search/SearchView.kt`

**Status:** M

### ⚠️ Проблемы:

- Line 22: Использование !! (force unwrap) может привести к NPE

### 🐛 Потенциальные баги:

- Line 33: Убедитесь, что listener очищается в onDestroy/onDestroyView

### 💡 Советы по улучшению:

- Line 83: Для констант на уровне файла используйте const val

### 📚 Связанная документация:

- `app/src/main/java/dev/kamikaze/movike/presentation/customviews/search/SearchView.kt:19` (релевантность: 13)
- `app/src/main/java/dev/kamikaze/movike/presentation/customviews/search/SearchCallback.kt:3` (релевантность: 12)

---

## 📄 `app/src/main/java/dev/kamikaze/movike/presentation/navigation/Navigator.kt`

**Status:** M

### 💡 Советы по улучшению:

- Line 47: Для констант на уровне файла используйте const val

### 📚 Связанная документация:

- `app/src/main/java/dev/kamikaze/movike/presentation/navigation/Navigator.kt:20` (релевантность: 12)
- `app/src/main/java/dev/kamikaze/movike/presentation/navigation/navigators/SearchNavigator.kt:5` (релевантность: 12)

---

## 📄 `app/src/main/java/dev/kamikaze/movike/presentation/ui/fragments/DetailsFragment.kt`

**Status:** M

### ⚠️ Проблемы:

- Line 29: Использование !! (force unwrap) может привести к NPE

### 🐛 Потенциальные баги:

- Line 42: Корутина без явного Dispatcher - может выполняться на UI потоке
- Line 44: Корутина без явного Dispatcher - может выполняться на UI потоке
- Line 52: Корутина без явного Dispatcher - может выполняться на UI потоке

### 📚 Связанная документация:

- `app/src/main/java/dev/kamikaze/movike/presentation/ui/fragments/DetailsFragment.kt:26` (релевантность: 13)
- `app/src/main/java/dev/kamikaze/movike/presentation/ui/fragments/SearchFragment.kt:27` (релевантность: 12)

---

## 📄 `app/src/main/java/dev/kamikaze/movike/presentation/ui/fragments/FeedFragment.kt`

**Status:** M

### ⚠️ Проблемы:

- Line 33: Использование !! (force unwrap) может привести к NPE
- Line 107: Использование !! (force unwrap) может привести к NPE

### 🐛 Потенциальные баги:

- Line 97: Корутина без явного Dispatcher - может выполняться на UI потоке
- Line 104: Корутина без явного Dispatcher - может выполняться на UI потоке
- Line 159: Корутина без явного Dispatcher - может выполняться на UI потоке
- Line 178: Корутина без явного Dispatcher - может выполняться на UI потоке

### 💡 Советы по улучшению:

- Line 106: Рассмотрите использование ?.let { } вместо if != null
- Line 108: Рассмотрите использование ?.let { } вместо if != null
- Line 154: Для констант на уровне файла используйте const val

### 📚 Связанная документация:

- `app/src/main/java/dev/kamikaze/movike/presentation/ui/fragments/FeedFragment.kt:28` (релевантность: 13)
- `app/src/main/java/dev/kamikaze/movike/presentation/navigation/Navigator.kt:20` (релевантность: 12)

---

## 📄 `app/src/main/java/dev/kamikaze/movike/presentation/ui/fragments/ProfileFragment.kt`

**Status:** M

### ⚠️ Проблемы:

- Line 22: Использование !! (force unwrap) может привести к NPE

### 📚 Связанная документация:

- `app/src/main/java/dev/kamikaze/movike/presentation/ui/fragments/ProfileFragment.kt:15` (релевантность: 13)
- `app/src/main/java/dev/kamikaze/movike/presentation/ui/fragments/SearchFragment.kt:27` (релевантность: 12)

---

## 📄 `app/src/main/java/dev/kamikaze/movike/presentation/ui/fragments/SearchFragment.kt`

**Status:** M

### ⚠️ Проблемы:

- Line 31: Использование !! (force unwrap) может привести к NPE

### 🐛 Потенциальные баги:

- Line 116: Корутина без явного Dispatcher - может выполняться на UI потоке

### 📚 Связанная документация:

- `app/src/main/java/dev/kamikaze/movike/presentation/ui/fragments/SearchFragment.kt:27` (релевантность: 13)
- `app/src/main/java/dev/kamikaze/movike/presentation/ui/fragments/FeedFragment.kt:28` (релевантность: 12)

---

## 📄 `app/src/main/java/dev/kamikaze/movike/presentation/ui/viewmodel/FeedViewModel.kt`

**Status:** M

### 🐛 Потенциальные баги:

- Line 40: Использование GlobalScope - рассмотрите lifecycleScope или viewModelScope
- Line 40: Корутина без явного Dispatcher - может выполняться на UI потоке
- Line 58: Корутина без явного Dispatcher - может выполняться на UI потоке
- Line 84: Корутина без явного Dispatcher - может выполняться на UI потоке

### 📚 Связанная документация:

- `app/src/main/java/dev/kamikaze/movike/presentation/ui/viewmodel/FeedViewModel.kt:13` (релевантность: 13)
- `app/src/main/java/dev/kamikaze/movike/presentation/ui/fragments/FeedFragment.kt:28` (релевантность: 13)

---

## 📄 `app/src/main/java/dev/kamikaze/movike/repository/RepositoryImpl.kt`

**Status:** M

### ⚠️ Проблемы:

- Line 91: Найден TODO/FIXME комментарий
- Line 95: Найден TODO/FIXME комментарий

### 🐛 Потенциальные баги:

- Line 67: Использование GlobalScope - рассмотрите lifecycleScope или viewModelScope
- Line 67: Корутина без явного Dispatcher - может выполняться на UI потоке
- Line 120: Использование GlobalScope - рассмотрите lifecycleScope или viewModelScope

### 📚 Связанная документация:

- `app/src/main/java/dev/kamikaze/movike/repository/RepositoryImpl.kt:18` (релевантность: 11)
- `app/src/main/java/dev/kamikaze/movike/presentation/ui/viewmodel/SearchViewModel.kt:12` (релевантность: 11)

---

## 📄 `app/src/main/java/dev/kamikaze/movike/utils/DateUtil.kt`

**Status:** M

### 💡 Советы по улучшению:

- Line 11: Для констант на уровне файла используйте const val
- Line 12: Для констант на уровне файла используйте const val
- Line 13: Для констант на уровне файла используйте const val

### 📚 Связанная документация:

- `app/src/main/java/dev/kamikaze/movike/utils/DateUtil.kt:6` (релевантность: 11)
- `app/src/main/java/dev/kamikaze/movike/utils/KeyboardUtil.kt:14` (релевантность: 10)

---

## 📄 `app/src/main/java/dev/kamikaze/movike/utils/KeyboardUtil.kt`

**Status:** M

### 💡 Советы по улучшению:

- Line 34: Рассмотрите использование ?.let { } вместо if != null

### 📚 Связанная документация:

- `app/src/main/java/dev/kamikaze/movike/utils/KeyboardUtil.kt:14` (релевантность: 11)
- `app/src/main/java/dev/kamikaze/movike/utils/DateUtil.kt:6` (релевантность: 10)

---

## 📄 `app/src/main/java/dev/kamikaze/movike/utils/StringUtil.kt`

**Status:** M

### 💡 Советы по улучшению:

- Line 38: Для констант на уровне файла используйте const val

### 📚 Связанная документация:

- `app/src/main/java/dev/kamikaze/movike/utils/StringUtil.kt:5` (релевантность: 11)
- `app/src/main/java/dev/kamikaze/movike/utils/KeyboardUtil.kt:14` (релевантность: 10)

---

## 📄 `feature-snack/src/main/java/dev/kamikaze/feature_snack/insets/InsetsExtensions.kt`

**Status:** M

### 💡 Советы по улучшению:

- Line 25: Для констант на уровне файла используйте const val

### 📚 Связанная документация:

- `app/src/main/java/dev/kamikaze/movike/AppController.kt:8` (релевантность: 7)
- `app/src/main/java/dev/kamikaze/movike/repository/Repository.kt:7` (релевантность: 7)

---

## 📄 `feature-snack/src/main/java/dev/kamikaze/feature_snack/view/SnackCallbackView.kt`

**Status:** M

### 🐛 Потенциальные баги:

- Line 38: Убедитесь, что listener очищается в onDestroy/onDestroyView

### 📚 Связанная документация:

- `app/src/main/java/dev/kamikaze/movike/utils/KeyboardUtil.kt:14` (релевантность: 8)
- `app/src/main/java/dev/kamikaze/movike/utils/AppConstants.kt:3` (релевантность: 8)

---

## 📄 `shared-utils/src/main/java/dev/kamikaze/shared_utils/extensions/InsetsExtensions.kt`

**Status:** M

### 💡 Советы по улучшению:

- Line 27: Для констант на уровне файла используйте const val
- Line 36: Для констант на уровне файла используйте const val

### 📚 Связанная документация:

- `app/src/main/java/dev/kamikaze/movike/utils/UIHelper.kt:13` (релевантность: 9)
- `app/src/main/java/dev/kamikaze/movike/utils/KeyboardUtil.kt:14` (релевантность: 8)

---

## 📊 Сводка

- **Всего проблем:** 11
- **Потенциальных багов:** 28
- **Предложений по улучшению:** 16

### ❗ Рекомендация: Критические проблемы требуют внимания!

---
*Автоматическое ревью сгенерировано AI Code Reviewer*