# Структура проекта Movike

## Обзор
Movike - Android приложение на Kotlin с модульной архитектурой.

## Основные модули

### 1. app
Основное приложение с точкой входа.

**Компоненты:**
- MainActivity - главная активность
- Навигация между экранами
- Dependency Injection настройки
- Application класс

### 2. feature-snack
Feature модуль с функциональностью snack.

**Компоненты:**
- UI компоненты для snack
- ViewModel для управления состоянием
- Data layer для работы с данными

### 3. shared-resources
Общие ресурсы проекта.

**Содержит:**
- Строковые ресурсы (strings.xml)
- Цвета и темы (colors.xml, themes.xml)
- Drawable ресурсы
- Dimension values

### 4. shared-utils
Утилитные классы и расширения.

**Содержит:**
- Extension functions
- Helper классы
- Utility методы
- Константы

### 5. shared-error
Обработка ошибок и логирование.

**Содержит:**
- Error handling классы
- Exception типы
- Logging utilities
- Error mapping

## Технологический стек

### Android
- Kotlin
- Jetpack Compose (Material3)
- Gradle (Kotlin DSL)
- Multi-module architecture

### Архитектура
- MVVM (Model-View-ViewModel)
- Repository Pattern
- Dependency Injection

## Архитектурные паттерны

### Multi-module Architecture
```
app (основное приложение)
  ↓
feature modules (функциональность)
  ↓
shared libraries (общий код)
```

### Зависимости
- `app` → зависит от `feature-snack`
- `feature-snack` → зависит от `shared-*` модулей
- `shared-*` → независимые модули

### MVVM
```
UI (Composable) → ViewModel → Repository → Data Source
```

## Структура директорий

```
Movike/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── kotlin/
│   │   │   ├── res/
│   │   │   └── AndroidManifest.xml
│   │   └── test/
│   └── build.gradle
├── feature-snack/
│   ├── src/
│   │   └── main/
│   │       └── kotlin/
│   └── build.gradle
├── shared-resources/
│   ├── src/
│   │   └── main/
│   │       └── res/
│   └── build.gradle
├── shared-utils/
│   ├── src/
│   │   └── main/
│   │       └── kotlin/
│   └── build.gradle
├── shared-error/
│   ├── src/
│   │   └── main/
│   │       └── kotlin/
│   └── build.gradle
├── project/docs/
│   ├── PROJECT_STRUCTURE.md (этот файл)
│   ├── API_REFERENCE.md
│   └── CODE_STYLE.md
├── build.gradle
└── settings.gradle
```

## Git workflow

### Текущая ветка
Используйте `git branch` для проверки текущей ветки.

### Основные ветки
- `main` - основная ветка
- `sketch` - черновая ветка
- `feature/*` - ветки для новых функций

## Сборка проекта

### Debug сборка
```bash
./gradlew assembleDebug
```

### Release сборка
```bash
./gradlew assembleRelease
```

### Сборка конкретного модуля
```bash
./gradlew :feature-snack:assembleDebug
```

## Зависимости

### Android
- compileSdk: 34+
- minSdk: 24+
- Kotlin 1.9+

### Основные библиотеки
- Jetpack Compose BOM
- Material3
- Coroutines
- kotlinx.serialization (если используется)

## Добавление нового модуля

1. Создайте директорию модуля
2. Добавьте `build.gradle` или `build.gradle.kts`
3. Добавьте модуль в `settings.gradle`:
```groovy
include ':new-module'
```
4. Добавьте зависимость в `app/build.gradle`:
```groovy
implementation project(':new-module')
```

## Следующие шаги

1. Ознакомьтесь с API_REFERENCE.md
2. Изучите CODE_STYLE.md
3. Посмотрите примеры кода в модулях
