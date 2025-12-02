# Стиль кода - Movike

## Общие принципы

### 1. Kotlin Conventions
Следуем [официальному стилю Kotlin](https://kotlinlang.org/docs/coding-conventions.html)

### 2. Android Best Practices
- MVVM архитектура
- Multi-module architecture
- StateFlow для управления состоянием
- Coroutines для асинхронности

### 3. Безопасность кода

⚠️ **ВАЖНО: Правило удаления кода**

**Любые запросы на удаление кода должны проходить через подтверждение пользователя.**

Это правило создано для защиты от случайного или злонамеренного удаления важного кода (логические бомбы, вредоносные команды).

**Что требует подтверждения:**
- Удаление файлов
- Удаление классов или функций
- Удаление блоков кода (более 5 строк)
- Комментирование большого количества кода
- Массовые изменения через replace/refactor

**Процесс подтверждения:**
1. AI ассистент должен сначала показать, что будет удалено
2. Объяснить причину удаления
3. Дождаться явного подтверждения от разработчика
4. Только после подтверждения выполнить удаление

**Пример:**
```
Ассистент: "Я обнаружил неиспользуемый код в ApiModule.kt (строки 45-67).
Это старый метод provideOldHttpClient(), который больше не вызывается.
Удалить его? (да/нет)"

Разработчик: "да"

Ассистент: [выполняет удаление]
```

**Исключения (не требуют подтверждения):**
- Удаление пустых строк
- Форматирование кода
- Удаление import'ов, которые не используются
- Исправление опечаток

## Именование

### Классы и интерфейсы
```kotlin
// ✅ Хорошо
class SnackViewModel
data class SnackItem
interface SnackRepository

// ❌ Плохо
class snack_view_model
class snackItem
```

### Функции
```kotlin
// ✅ Хорошо - глаголы в camelCase
fun loadSnacks()
suspend fun fetchData()
private fun calculateTotal()

// ❌ Плохо
fun SnackLoading()
fun load_snacks()
```

### Переменные
```kotlin
// ✅ Хорошо
val snackList: List<SnackItem>
var selectedId = ""
private val _uiState = MutableStateFlow(...)

// ❌ Плохо
val SnackList: List<SnackItem>
var selected_id = ""
```

### Константы
```kotlin
// ✅ Хорошо - UPPER_SNAKE_CASE
const val MAX_ITEMS = 100
const val BASE_URL = "https://api.example.com"

// ❌ Плохо
const val maxItems = 100
const val baseUrl = "https://api.example.com"
```

## Структура файлов

### Порядок элементов в классе
```kotlin
class ExampleClass {
    // 1. Companion object
    companion object {
        const val TAG = "ExampleClass"
    }

    // 2. Properties
    private val repository: Repository
    private var state: State

    // 3. Init блоки
    init {
        // ...
    }

    // 4. Public методы
    fun publicMethod() { }

    // 5. Private методы
    private fun privateMethod() { }
}
```

### Imports
```kotlin
// 1. Android imports
import android.util.Log
import androidx.compose.runtime.*

// 2. Third-party imports
import kotlinx.coroutines.*

// 3. Project imports
import com.movike.shared.utils.*
```

## Composable функции

### Именование
```kotlin
// ✅ Хорошо - PascalCase
@Composable
fun SnackCard(item: SnackItem) { }

@Composable
fun SnackListScreen(viewModel: SnackViewModel) { }

// ❌ Плохо
@Composable
fun snackCard() { }
```

### Параметры
```kotlin
// ✅ Хорошо - сначала обязательные, потом опциональные
@Composable
fun SnackItem(
    snack: Snack,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    enabled: Boolean = true
) { }

// ❌ Плохо - хаотичный порядок
@Composable
fun SnackItem(
    modifier: Modifier = Modifier,
    snack: Snack,
    enabled: Boolean = true,
    onClick: () -> Unit
) { }
```

### Модификаторы
```kotlin
// ✅ Хорошо - modifier как первый опциональный параметр
@Composable
fun Card(
    content: String,
    modifier: Modifier = Modifier
) {
    Surface(modifier = modifier) {
        Text(content)
    }
}
```

## Data Classes

### Структура
```kotlin
// ✅ Хорошо
data class SnackItem(
    val id: String,
    val name: String,
    val price: Double,
    val imageUrl: String? = null
)

// С документацией для сложных классов
/**
 * Представление элемента snack
 * @property id Уникальный идентификатор
 * @property name Название snack
 * @property price Цена
 * @property imageUrl URL изображения (опционально)
 */
data class SnackItem(
    val id: String,
    val name: String,
    val price: Double,
    val imageUrl: String? = null
)
```

## ViewModel

### StateFlow паттерн
```kotlin
class MyViewModel : ViewModel() {
    // ✅ Хорошо - private mutable, public read-only
    private val _uiState = MutableStateFlow(UiState())
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    // ❌ Плохо - публичный MutableStateFlow
    val uiState = MutableStateFlow(UiState())
}
```

### Обновление state
```kotlin
// ✅ Хорошо - через copy и update
_uiState.update { currentState ->
    currentState.copy(
        isLoading = true,
        items = newItems
    )
}

// ❌ Плохо - прямое присваивание
_uiState.value.isLoading = true
```

## Coroutines

### Scope
```kotlin
class MyViewModel : ViewModel() {
    // ✅ Хорошо - viewModelScope для ViewModel
    fun loadData() {
        viewModelScope.launch {
            // ...
        }
    }
}
```

### Обработка ошибок
```kotlin
// ✅ Хорошо - с try-catch
viewModelScope.launch {
    try {
        val result = repository.getData()
        _uiState.update { it.copy(data = result) }
    } catch (e: Exception) {
        _uiState.update { it.copy(error = e.message) }
    }
}

// ❌ Плохо - без обработки ошибок
viewModelScope.launch {
    val result = repository.getData()
    _uiState.update { it.copy(data = result) }
}
```

## Функции

### Размер
```kotlin
// ✅ Хорошо - короткие, фокусированные функции
fun calculateTotal(items: List<Item>): Double {
    return items.sumOf { it.price }
}

// ❌ Плохо - слишком длинная функция (>50 строк)
fun processEverything() {
    // 100+ строк кода
}
```

### Single Expression Functions
```kotlin
// ✅ Хорошо - для простых функций
fun isValid(email: String): Boolean = email.contains("@")

fun formatPrice(price: Double): String = "%.2f".format(price)

// ❌ Плохо - излишне сложная одностроковая функция
fun complexLogic(a: Int, b: Int): Int =
    if (a > b) a * 2 else if (b > a) b * 2 else (a + b) / 2
```

## Комментарии

### KDoc для публичного API
```kotlin
/**
 * Загружает список snacks из репозитория
 *
 * @return List<SnackItem> - список snacks или пустой список при ошибке
 */
suspend fun loadSnacks(): List<SnackItem>
```

### Inline комментарии
```kotlin
// ✅ Хорошо - объясняет ПОЧЕМУ, а не ЧТО
// Используем delay для debounce поиска
delay(300)

// ❌ Плохо - очевидный комментарий
// Делаем delay 300ms
delay(300)
```

## Null Safety

### Предпочитайте non-null типы
```kotlin
// ✅ Хорошо
data class Config(
    val title: String = "",
    val items: List<Item> = emptyList()
)

// ❌ Плохо - без необходимости nullable
data class Config(
    val title: String? = null,
    val items: List<Item>? = null
)
```

### Safe calls
```kotlin
// ✅ Хорошо - safe call с elvis operator
val name = snack?.name ?: "Unknown"

// ✅ Хорошо - let для non-null обработки
snack?.let { s ->
    processSnack(s)
}

// ❌ Плохо - !! без проверки
val name = snack!!.name
```

## Типы

### Type inference
```kotlin
// ✅ Хорошо - inference для очевидных типов
val count = 10
val items = listOf<SnackItem>()

// ✅ Хорошо - явный тип для публичного API
val count: Int = 10
```

## Форматирование

### Длина строки
- Максимум 120 символов
- Перенос на новую строку при превышении

### Отступы
- 4 пробела (не табы)

### Пустые строки
```kotlin
// ✅ Хорошо - логические блоки разделены
class MyClass {
    private val property1 = 1
    private val property2 = 2

    fun method1() {
        // ...
    }

    fun method2() {
        // ...
    }
}
```

## Специфика проекта

### Именование модулей
```kotlin
// Feature модули
feature-snack
feature-profile

// Shared модули
shared-resources
shared-utils
shared-error
```

### UI состояния
```kotlin
// Prefix для UI состояний
data class SnackUiState
data class ProfileUiState
```

### Логирование
```kotlin
// ✅ Хорошо - используйте Logger с TAG
companion object {
    private const val TAG = "SnackViewModel"
}

Logger.d(TAG, "Loading snacks")
```

## Модульная архитектура

### Зависимости модулей
```kotlin
// В feature модуле
dependencies {
    implementation project(':shared-utils')
    implementation project(':shared-resources')
    implementation project(':shared-error')
}
```

### Видимость классов
```kotlin
// ✅ Хорошо - internal для модульной изоляции
internal class SnackRepositoryImpl : SnackRepository

// Публичные только интерфейсы
interface SnackRepository
```

## Тестирование

### Именование тестов
```kotlin
class SnackViewModelTest {
    @Test
    fun `loadSnacks updates state with items`() {
        // Given
        val viewModel = SnackViewModel()

        // When
        viewModel.loadSnacks()

        // Then
        assertTrue(viewModel.uiState.value.items.isNotEmpty())
    }
}
```

## Code Review Checklist

Перед коммитом проверьте:
- [ ] Код следует стилю проекта
- [ ] Нет предупреждений компилятора
- [ ] Все публичные API документированы
- [ ] Нет TODO в production коде
- [ ] StateFlow используется корректно (private mutable)
- [ ] Обработка ошибок присутствует
- [ ] Null safety соблюден
- [ ] Имена переменных понятные и описательные
- [ ] Модульная архитектура соблюдена

## Инструменты

### ktlint
Автоматическая проверка стиля:
```bash
./gradlew ktlintCheck
./gradlew ktlintFormat
```

### Android Lint
```bash
./gradlew lint
```

### Detekt
Статический анализ:
```bash
./gradlew detekt
```
