# API Reference - Movike

## Обзор

Справочник по основным API и классам проекта Movike.

## Модули

### app

Основное приложение.

#### MainActivity
```kotlin
class MainActivity : ComponentActivity()
```

Главная активность приложения.

**Методы:**
- `onCreate(savedInstanceState: Bundle?)` - инициализация приложения

### feature-snack

Feature модуль с функциональностью snack.

#### SnackViewModel
```kotlin
class SnackViewModel : ViewModel()
```

ViewModel для управления состоянием snack feature.

**State:**
```kotlin
data class SnackUiState(
    val items: List<SnackItem>,
    val isLoading: Boolean,
    val error: String?
)
```

**Методы:**
- `loadSnacks()` - загрузка списка snacks
- `selectSnack(id: String)` - выбор snack

### shared-utils

Утилитные функции и расширения.

#### Extension Functions

##### String Extensions
```kotlin
fun String.isValidEmail(): Boolean
```
Проверяет, является ли строка валидным email.

```kotlin
fun String.capitalize(): String
```
Делает первую букву заглавной.

##### Collection Extensions
```kotlin
fun <T> List<T>.safeGet(index: Int): T?
```
Безопасное получение элемента по индексу.

#### Helper Classes

##### DateUtils
```kotlin
object DateUtils {
    fun formatDate(timestamp: Long): String
    fun getCurrentTimestamp(): Long
}
```

**Методы:**
- `formatDate(timestamp: Long)` - форматирование даты
- `getCurrentTimestamp()` - получение текущего timestamp

##### StringUtils
```kotlin
object StringUtils {
    fun isNullOrEmpty(str: String?): Boolean
    fun truncate(str: String, maxLength: Int): String
}
```

**Методы:**
- `isNullOrEmpty(str: String?)` - проверка на null или пустоту
- `truncate(str: String, maxLength: Int)` - обрезка строки

### shared-error

Обработка ошибок.

#### AppError
```kotlin
sealed class AppError {
    data class NetworkError(val message: String) : AppError()
    data class ValidationError(val message: String) : AppError()
    data class UnknownError(val throwable: Throwable) : AppError()
}
```

Sealed class для типизированных ошибок.

#### ErrorHandler
```kotlin
interface ErrorHandler {
    fun handleError(error: AppError)
}
```

Интерфейс для обработки ошибок.

#### Logger
```kotlin
object Logger {
    fun d(tag: String, message: String)
    fun e(tag: String, message: String, throwable: Throwable? = null)
    fun i(tag: String, message: String)
    fun w(tag: String, message: String)
}
```

**Методы:**
- `d(tag: String, message: String)` - debug логирование
- `e(tag: String, message: String, throwable: Throwable?)` - error логирование
- `i(tag: String, message: String)` - info логирование
- `w(tag: String, message: String)` - warning логирование

### shared-resources

Общие ресурсы проекта.

#### Цвета
Определены в `colors.xml`:
- `primary` - основной цвет
- `secondary` - вторичный цвет
- `background` - цвет фона
- `surface` - цвет поверхностей

#### Темы
Определены в `themes.xml`:
- `Theme.Movike` - основная тема приложения

## Data Classes

### SnackItem (пример)
```kotlin
data class SnackItem(
    val id: String,
    val name: String,
    val description: String,
    val price: Double,
    val imageUrl: String?
)
```

## Константы

### App Constants
```kotlin
object AppConstants {
    const val BASE_URL = "https://api.example.com"
    const val TIMEOUT = 30_000L // 30 seconds
    const val MAX_RETRIES = 3
}
```

## ViewModel Pattern

### Базовая структура
```kotlin
class MyViewModel : ViewModel() {
    // Private mutable state
    private val _uiState = MutableStateFlow(UiState())
    // Public read-only state
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    fun loadData() {
        viewModelScope.launch {
            try {
                // Load data
                _uiState.update { it.copy(isLoading = true) }
                val data = repository.getData()
                _uiState.update { it.copy(data = data, isLoading = false) }
            } catch (e: Exception) {
                _uiState.update { it.copy(error = e.message, isLoading = false) }
            }
        }
    }
}
```

## Composable Functions

### Именование
Composable функции должны быть в PascalCase:
```kotlin
@Composable
fun SnackCard(item: SnackItem, modifier: Modifier = Modifier) {
    Card(modifier = modifier) {
        // UI implementation
    }
}
```

### Параметры
Порядок параметров:
1. Обязательные параметры
2. Callbacks
3. `modifier: Modifier = Modifier`
4. Опциональные параметры

```kotlin
@Composable
fun CustomButton(
    text: String,              // Обязательный
    onClick: () -> Unit,       // Callback
    modifier: Modifier = Modifier,  // Modifier
    enabled: Boolean = true    // Опциональный
) { }
```

## Примеры использования

### Работа с ViewModel
```kotlin
@Composable
fun MyScreen(viewModel: MyViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()

    when {
        uiState.isLoading -> LoadingIndicator()
        uiState.error != null -> ErrorMessage(uiState.error!!)
        else -> ContentView(uiState.data)
    }
}
```

### Обработка ошибок
```kotlin
try {
    val result = repository.getData()
    processResult(result)
} catch (e: Exception) {
    val error = when (e) {
        is IOException -> AppError.NetworkError(e.message ?: "Network error")
        is IllegalArgumentException -> AppError.ValidationError(e.message ?: "Validation error")
        else -> AppError.UnknownError(e)
    }
    errorHandler.handleError(error)
}
```

### Использование утилит
```kotlin
// String extensions
val email = "test@example.com"
if (email.isValidEmail()) {
    // Process email
}

// Date utils
val timestamp = DateUtils.getCurrentTimestamp()
val formattedDate = DateUtils.formatDate(timestamp)

// Logger
Logger.d(TAG, "Processing data: $data")
Logger.e(TAG, "Error occurred", exception)
```

## Gradle Dependencies

### Добавление зависимости между модулями
В `build.gradle` модуля:
```groovy
dependencies {
    implementation project(':shared-utils')
    implementation project(':shared-resources')
    implementation project(':shared-error')
}
```

### Версии библиотек
Рекомендуется использовать version catalog или `buildSrc` для управления версиями.

## Тестирование

### Unit тесты
```kotlin
class MyViewModelTest {
    @Test
    fun `loadData updates state correctly`() {
        // Given
        val viewModel = MyViewModel()

        // When
        viewModel.loadData()

        // Then
        assertEquals(expectedState, viewModel.uiState.value)
    }
}
```

## Дополнительная информация

Для получения справки используйте команду `/help` в Claude Code.
