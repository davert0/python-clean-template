# uv - Современный пакетный менеджер

## 🚀 Что такое uv?

**uv** - это сверхбыстрый пакетный менеджер для Python от [Astral](https://astral.sh/) (создатели ruff).

### Преимущества

- ⚡ **В 10-100 раз быстрее** pip
- 🦀 Написан на Rust
- 📦 Совместим с pip
- 🔒 Генерирует lock файл
- 🎯 Один инструмент для всего (venv + pip + pip-tools)

---

## 📦 Установка uv

### macOS/Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Через pip
```bash
pip install uv
```

### Через Homebrew (macOS)
```bash
brew install uv
```

Проверка:
```bash
uv --version
```

---

## 🎯 Основные команды

### Создать виртуальное окружение
```bash
uv venv
```

Активировать:
```bash
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### Установить зависимости
```bash
uv pip install -e .
```

Это установит всё из `pyproject.toml`.

### Установить dev зависимости
```bash
uv pip install -e ".[dev]"
```

### Добавить новую зависимость
```bash
# Редактируй pyproject.toml, добавь в dependencies
uv pip install <package>
```

### Обновить зависимости
```bash
uv pip install -e . --upgrade
```

### Синхронизировать окружение
```bash
uv pip sync requirements.txt  # если есть requirements.txt
# или
uv pip install -e .
```

---

## 📝 pyproject.toml vs requirements.txt

Проект использует **pyproject.toml** (современный стандарт):

```toml
[project]
dependencies = [
    "fastapi>=0.104.1",
    "uvicorn[standard]>=0.24.0",
    ...
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.3",
    ...
]
```

**Преимущества pyproject.toml:**
- ✅ Стандарт PEP 621
- ✅ Метаданные проекта в одном месте
- ✅ Разделение dev/prod зависимостей
- ✅ Конфигурация инструментов (ruff, pytest)

**requirements.txt** оставлен для совместимости.

---

## 🔄 Workflow разработки

### 1. Клонировать проект
```bash
git clone <repo>
cd python-clean-template
```

### 2. Создать окружение
```bash
uv venv
source .venv/bin/activate
```

### 3. Установить зависимости
```bash
uv pip install -e ".[dev]"
```

### 4. Запустить приложение
```bash
python main.py
```

---

## 🐳 Docker + uv

Dockerfile обновлён для использования uv:

```dockerfile
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
RUN uv pip install -e .
```

Это **значительно ускоряет** сборку образа!

---

## 📊 Сравнение скорости

| Операция | pip | uv | Ускорение |
|----------|-----|----|-----------| 
| Установка зависимостей | 30s | 1s | **30x** |
| Создание venv | 3s | 0.1s | **30x** |
| Разрешение зависимостей | 20s | 0.5s | **40x** |

---

## 🔧 Часто используемые команды

### Создать и активировать окружение
```bash
uv venv && source .venv/bin/activate
```

### Установить всё одной командой
```bash
uv pip install -e ".[dev]"
```

### Обновить одну зависимость
```bash
uv pip install --upgrade fastapi
```

### Показать установленные пакеты
```bash
uv pip list
```

### Удалить пакет
```bash
uv pip uninstall <package>
```

### Заморозить зависимости
```bash
uv pip freeze > requirements.txt
```

---

## 🆚 Сравнение с другими инструментами

### uv vs pip
- ⚡ uv в **10-100 раз быстрее**
- 🔒 uv лучше разрешает зависимости
- 📦 uv совместим с pip

### uv vs Poetry
- ⚡ uv **намного быстрее**
- 📝 Poetry имеет встроенный lock файл
- 🎯 Poetry - полноценный менеджер проектов
- 🔧 uv - замена pip, проще в использовании

### uv vs PDM
- ⚡ uv быстрее
- 📦 PDM следует PEP 582
- 🎯 uv проще и легче

---

## 💡 Почему uv?

1. **Скорость** - главное преимущество
2. **Простота** - работает как pip, но быстрее
3. **Совместимость** - можно использовать с существующими проектами
4. **Активное развитие** - от создателей ruff
5. **Современность** - поддержка pyproject.toml

---

## 📚 Полезные ссылки

- [Официальная документация](https://github.com/astral-sh/uv)
- [Сравнение с pip](https://github.com/astral-sh/uv#benchmarks)
- [pyproject.toml спецификация](https://peps.python.org/pep-0621/)

---

## 🔄 Миграция с pip

Если у вас есть `requirements.txt`:

```bash
# Создать pyproject.toml на основе requirements.txt
# (сделано вручную в проекте)

# Установить через uv
uv pip install -r requirements.txt
```

Проект уже мигрирован! 🎉

---

## ⚙️ Конфигурация

### .python-version
Указывает версию Python:
```
3.11
```

### pyproject.toml
Основной файл конфигурации:
```toml
[project]
requires-python = ">=3.11"
dependencies = [...]
```

---

## 🎯 Быстрые команды

```bash
uv venv                           # создать окружение
uv pip install -e .               # установить проект
uv pip install -e ".[dev]"        # + dev зависимости
uv pip install <package>          # добавить пакет
uv pip list                       # список пакетов
uv pip freeze > requirements.txt  # заморозить
```

---

Готово! uv настроен и готов к использованию! ⚡

