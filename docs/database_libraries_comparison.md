# Сравнение библиотек для работы с PostgreSQL (без ORM)

## 1. asyncpg ⭐⭐⭐⭐⭐

**GitHub:** https://github.com/MagicStack/asyncpg  
**Stars:** ~6.8k  
**Статус:** Активно развивается

### Особенности:
- Самая быстрая библиотека для PostgreSQL в Python
- Написана на Cython, нативный протокол PostgreSQL
- Async-first, connection pool из коробки
- Автоматические prepared statements
- Типизация PostgreSQL типов

### Плюсы:
✅ Максимальная производительность (в 3-5 раз быстрее psycopg2)  
✅ Настоящий async/await  
✅ Connection pool встроен  
✅ Отличная документация  
✅ Активное сообщество  
✅ Идеально для FastAPI/Starlette  

### Минусы:
❌ Только PostgreSQL (не универсальная)  
❌ Синтаксис $1, $2 вместо привычного %s  
❌ Нет поддержки psycopg2 extensions  

### Производительность:
- ~50,000-100,000 queries/sec (простые SELECT)
- ~10,000-30,000 inserts/sec

### Пример:
```python
import asyncpg

pool = await asyncpg.create_pool(dsn='postgresql://...')
row = await pool.fetchrow('select * from users where id = $1', 1)
```

### Рекомендация: 
🏆 **ЛУЧШИЙ ВЫБОР для FastAPI + PostgreSQL**

---

## 2. psycopg3 (psycopg) ⭐⭐⭐⭐

**GitHub:** https://github.com/psycopg/psycopg  
**Stars:** ~1.6k  
**Статус:** Активно развивается (новое поколение)

### Особенности:
- Современная замена psycopg2
- Поддержка sync И async
- Connection pool (pgpool)
- Лучшая типизация
- Prepared statements

### Плюсы:
✅ Sync и async в одной библиотеке  
✅ Знакомый API (похож на psycopg2)  
✅ Современный код (type hints)  
✅ Активное развитие  
✅ Connection pool (pgpool)  
✅ Привычный синтаксис %s  

### Минусы:
❌ Async медленнее asyncpg (написан на чистом Python)  
❌ Меньше adoption в сообществе (пока)  
❌ Некоторые фичи ещё в разработке  

### Производительность:
- Sync: ~как psycopg2
- Async: медленнее asyncpg на 30-50%

### Пример:
```python
import psycopg
from psycopg_pool import AsyncConnectionPool

pool = AsyncConnectionPool('postgresql://...')
async with pool.connection() as conn:
    async with conn.cursor() as cur:
        await cur.execute('select * from users where id = %s', (1,))
        row = await cur.fetchone()
```

### Рекомендация:
💡 **Хороший выбор, если нужна гибкость sync/async**

---

## 3. encode/databases ⭐⭐⭐⭐

**GitHub:** https://github.com/encode/databases  
**Stars:** ~3.8k  
**Статус:** Maintenance mode (не добавляют новые фичи)

### Особенности:
- Универсальная async абстракция
- Поддержка PostgreSQL, MySQL, SQLite
- Под капотом использует asyncpg/aiomysql/aiosqlite
- Core queries (как в SQLAlchemy Core)

### Плюсы:
✅ Простой и чистый API  
✅ Поддержка разных БД (универсальность)  
✅ Query builder встроен  
✅ Хорошая интеграция с FastAPI  
✅ Использует asyncpg под капотом (для Postgres)  

### Минусы:
❌ Maintenance mode (мало апдейтов)  
❌ Дополнительный слой абстракции (overhead)  
❌ Привязка к SQLAlchemy Core для query builder  
❌ Менее гибкий чем чистый asyncpg  

### Производительность:
- Близка к asyncpg (небольшой overhead на абстракцию)

### Пример:
```python
from databases import Database

database = Database('postgresql://...')
await database.connect()

query = "select * from users where id = :id"
row = await database.fetch_one(query=query, values={"id": 1})
```

### Рекомендация:
⚠️ **Был популярен, но сейчас в maintenance mode. Лучше чистый asyncpg**

---

## 4. aiopg ⭐⭐⭐

**GitHub:** https://github.com/aio-libs/aiopg  
**Stars:** ~1.4k  
**Статус:** Поддерживается, но медленное развитие

### Особенности:
- Async wrapper вокруг psycopg2
- Connection pool
- Поддержка SA Core (опционально)

### Плюсы:
✅ Знакомый API psycopg2  
✅ Connection pool  
✅ Поддержка всех фич psycopg2  

### Минусы:
❌ Медленнее asyncpg (wrapper вокруг синхронного кода)  
❌ Устаревает (лучше psycopg3)  
❌ Меньше оптимизаций  

### Производительность:
- Медленнее asyncpg в ~2 раза

### Рекомендация:
🚫 **Не рекомендуется для новых проектов. Используйте asyncpg или psycopg3**

---

## 5. psycopg2 ⭐⭐⭐

**Классика, уже рассмотрели**

### Плюсы:
✅ Проверено временем  
✅ Огромное сообщество  
✅ Все знают как использовать  

### Минусы:
❌ Только sync  
❌ Блокирует event loop в async приложениях  
❌ Нет встроенного pool (нужен pgbouncer или свой)  

### Рекомендация:
⚠️ **Только для sync приложений. Для FastAPI - плохой выбор**

---

## Специальные упоминания

### 6. SQLAlchemy Core (без ORM)

```python
from sqlalchemy import create_engine, text

engine = create_engine('postgresql://...')
with engine.connect() as conn:
    result = conn.execute(text('select * from users where id = :id'), {'id': 1})
    row = result.fetchone()
```

**Плюсы:**
- Query builder
- Миграции через Alembic
- Можно без ORM (Core only)

**Минусы:**
- Тяжеловесная библиотека
- Сложнее чистого SQL

### 7. PonyORM / Tortoise ORM
❌ Это ORM - не подходит по требованию

---

## 🏆 Итоговая таблица

| Библиотека | Async | Скорость | Популярность | Sync/Async | Рекомендация |
|------------|-------|----------|--------------|------------|--------------|
| **asyncpg** | ✅ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Async only | 🏆 Лучший |
| **psycopg3** | ✅ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Оба | 💡 Перспективный |
| **databases** | ✅ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Async only | ⚠️ Maintenance |
| **aiopg** | ✅ | ⭐⭐⭐ | ⭐⭐ | Async only | 🚫 Устарел |
| **psycopg2** | ❌ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Sync only | ⚠️ Sync only |

---

## 🎯 Финальные рекомендации

### Для FastAPI production:
```
1. asyncpg          (если только PostgreSQL)
2. psycopg3         (если нужна гибкость sync/async)
3. databases        (если нужна поддержка разных БД, но осторожно - maintenance)
```

### Для sync Django/Flask:
```
1. psycopg2         (проверено временем)
2. psycopg3 sync    (современная альтернатива)
```

### Для микросервисов:
```
1. asyncpg          (максимальная производительность)
```

---

## 💡 Мой вердикт для вашего проекта

**Рекомендую остаться на asyncpg**, потому что:

1. ✅ Это FastAPI проект → нужен настоящий async
2. ✅ PostgreSQL → asyncpg оптимизирован именно под него
3. ✅ Максимальная производительность
4. ✅ Огромное комьюнити в FastAPI экосистеме
5. ✅ Стабильная и проверенная библиотека

**Альтернатива:** psycopg3 - если нужна гибкость, но производительность немного ниже.

**НЕ рекомендую:**
- ❌ databases - в maintenance mode
- ❌ aiopg - устарел
- ❌ psycopg2 - блокирующий, плохо для async

