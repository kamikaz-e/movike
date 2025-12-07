# 📋 Руководство по созданию задач через чат

## Быстрый старт

Просто напишите в чате одну из следующих команд:

### ✅ Рабочие примеры:

1. **Простая задача:**
   ```
   Create task: Fix memory leak with high priority. Description: Images not released properly
   ```

2. **Задача с низким приоритетом:**
   ```
   Create task: Update README with low priority. Description: Add installation instructions
   ```

3. **Критическая задача:**
   ```
   Create task: Fix security bug with critical priority. Description: SQL injection vulnerability
   ```

4. **Без указания приоритета (будет MEDIUM):**
   ```
   Create task: Add new feature. Description: Implement user profile page
   ```

### 🇷🇺 На русском:

1. **Создать задачу:**
   ```
   Создать задачу: Исправить утечку памяти с высоким приоритетом. Описание: Изображения не освобождаются правильно
   ```

2. **Добавить задачу:**
   ```
   Добавить задачу: Обновить документацию. Описание: Добавить примеры кода
   ```

## 📝 Формат команды

```
Create task: [Название] with [приоритет] priority. Description: [Описание]
```

Где:
- **[Название]** - название задачи (обязательно)
- **[приоритет]** - low, medium, high, critical (опционально, по умолчанию medium)
- **[Описание]** - подробное описание (опционально, если не указано, используется название)

## 🎯 Что происходит после создания

После успешного создания задачи вы получите сообщение:

```
✅ Task created successfully!

ID: 1
Title: Fix memory leak
Description: Images not released properly
Priority: HIGH
Status: TODO
```

## 💡 Полезные советы

1. Всегда начинайте с "Create task:" или "Создать задачу:"
2. Указывайте приоритет для важных задач
3. Используйте "Description:" для более подробного описания
4. Можно создавать задачи на русском и английском языках

## 🔧 Технические детали

- Сервер автоматически парсит текст и извлекает детали задачи
- Задачи сохраняются в памяти сервера
- Приоритет определяется по ключевым словам: low, medium, high, critical
- Если приоритет не указан, используется MEDIUM

