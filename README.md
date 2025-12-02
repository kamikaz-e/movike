# Movike - Android Application

Android приложение Movike с модульной архитектурой.

## Возможности

- Модульная архитектура приложения
- Feature модули для разделения функциональности
- Shared библиотеки для переиспользования кода

## Технологии

- **Kotlin** - основной язык разработки
- **Jetpack Compose** - современный UI toolkit
- **Gradle** - система сборки
- **Multi-module** - модульная архитектура

## Быстрый старт

### Требования

- Android Studio Hedgehog+
- JDK 17+
- Android SDK 34+

### Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd Movike
```

2. Откройте проект в Android Studio

3. Синхронизируйте Gradle:
```bash
./gradlew build
```

4. Запустите приложение на эмуляторе или устройстве

### AI Ассистент

Для получения справки о проекте используйте простую команду:
```bash
run_assistant help 'ваш вопрос'
```

Примеры:
```bash
run_assistant help 'Какие модули есть в проекте?'
run_assistant help 'структура проекта'
run_assistant /help 'API'
```

Подробнее см. раздел [Использование команды /help](#использование-команды-help)

## Структура проекта

```
Movike/
├── app/                    # Основное приложение
├── feature-snack/          # Feature модуль
├── shared-resources/       # Общие ресурсы
├── shared-utils/           # Утилиты
├── shared-error/           # Обработка ошибок
├── project/docs/           # Документация проекта
│   ├── PROJECT_STRUCTURE.md
│   ├── API_REFERENCE.md
│   └── CODE_STYLE.md
├── build.gradle            # Корневая конфигурация Gradle
└── settings.gradle         # Настройки проекта
```

## Модули

### app
Основное приложение с точкой входа и навигацией.

### feature-snack
Feature модуль с функциональностью snack.

### shared-resources
Общие ресурсы: строки, цвета, темы, drawable.

### shared-utils
Утилитные классы и расширения.

### shared-error
Обработка ошибок и логирование.

## Сборка

### Debug сборка
```bash
./gradlew assembleDebug
```

### Release сборка
```bash
./gradlew assembleRelease
```

### Запуск тестов
```bash
./gradlew test
```

## Документация

- [PROJECT_STRUCTURE.md](project/docs/PROJECT_STRUCTURE.md) - архитектура проекта
- [API_REFERENCE.md](project/docs/API_REFERENCE.md) - справка по API
- [CODE_STYLE.md](project/docs/CODE_STYLE.md) - стиль кода

## Использование команды /help

### В Claude Code

Для получения справки о проекте используйте:
```
/help
```

### В терминале

**Простая команда (рекомендуется):**
```bash
# Используйте простую команду run_assistant
run_assistant help 'Какие модули есть в проекте?'

# Также поддерживается /help как синоним
run_assistant /help 'Какие модули есть в проекте?'

# Без знака вопроса тоже работает
run_assistant help 'Какие модули есть в проекте'
```

**Альтернативный способ (полный путь):**
```bash
# Используйте одинарные кавычки для вопросов со знаками препинания (особенно в zsh)
python3 assistant/assistant.py help 'Какие модули есть в проекте?'

# Также поддерживается /help как синоним
python3 assistant/assistant.py /help 'вопрос'
```

**Важно для zsh:** Используйте одинарные кавычки `'...'` вместо двойных `"..."`, чтобы избежать проблем с glob-паттернами (знаки `?`, `*` и т.д.).

Команда поддерживает вопросы о:
- Структуре проекта
- API и методах
- Стиле кода
- Архитектурных решениях
- Примерах использования

## Примеры вопросов для /help

- "Какая структура проекта?"
- "Какие модули есть в проекте?"
- "Как добавить новый feature модуль?"
- "Какой стиль именования для классов?"
- "Как запустить сборку проекта?"

## Git workflow

Проверить текущую ветку:
```bash
git branch
```

Создать новую ветку:
```bash
git checkout -b feature/my-feature
```

## Архитектура

### Multi-module
```
app → feature modules → shared libraries
```

### Зависимости модулей
- app зависит от feature модулей
- feature модули зависят от shared библиотек
- shared библиотеки независимы друг от друга

## Требования к системе

- minSdk: 24 (Android 7.0)
- targetSdk: 34 (Android 14)
- compileSdk: 34

## Лицензия

TODO: Указать лицензию

## Авторы

- Разработка: 2024-2025
- Текущая версия: 1.0

## Поддержка

Для вопросов и обратной связи:
- Issues: создайте issue в репозитории
- Документация: см. project/docs/

---

Для подробной информации см. [документацию](project/docs/).
