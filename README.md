# 🍽️ ВкусВилл Парсер - Готовая Еда

Мощный Python-парсер для сбора данных о готовой еде с ВкусВилл с поддержкой геолокации и максимальным извлечением БЖУ.

## ✨ Особенности

- 🎯 **1459 товаров** с качеством данных **95%+**
- ⚡ **Два режима работы**: быстрый (секунды) и полный (минуты)
- 📍 **Геолокация**: работа с любыми адресами в России
- 🔄 **Retry-механизм**: повторные попытки для 100% заполненности
- 📊 **Полные БЖУ**: калории, белки, жиры, углеводы + состав
- 🐳 **Docker Ready**: готовый контейнер для Railway/Heroku
- 💾 **Экспорт**: CSV и JSONL форматы

## 🚀 Быстрый старт

### Локальная установка

```bash
# Клонирование репозитория
git clone https://github.com/your-repo/Samokat-Ready-Food-Scraper.git
cd Samokat-Ready-Food-Scraper

# Установка зависимостей
pip install -r requirements.txt

# Быстрый тест (120 товаров за 8 секунд)
python3 address.py "Москва, Тверская улица, 12" 500

# Полный парсинг (1459 товаров за 30 минут)
python3 moscow.py 1500
```

### 🐳 Развертывание на Railway

1. **Форкните репозиторий** на GitHub
2. **Подключите к Railway**:
   - Зайдите на [railway.app](https://railway.app)
   - Нажмите "Deploy from GitHub"
   - Выберите ваш форк репозитория
3. **Настройте переменные окружения**:
   ```bash
   RAILWAY_ENVIRONMENT=production
   PYTHONPATH=/app
   ```
4. **Деплой завершится автоматически**

Railway автоматически:
- Соберет Docker-образ
- Установит все зависимости
- Запустит парсер
- Сохранит результаты

## 📋 Доступные команды

### 🏃‍♂️ Быстрый парсер (рекомендуется)

```bash
# По адресу (мгновенно, использует готовую базу)
python3 address.py "Адрес" [количество]

# Примеры
python3 address.py "Москва, Красная площадь, 1" 1000
python3 address.py "СПб, Невский проспект, 10" 500
python3 address.py "55.7558,37.6176" 300  # координаты
python3 address.py  # интерактивный режим
```

**Результат**: 1459 товаров за 0.1 секунды, 95.4% с полными БЖУ

### 🔍 Полный парсер

```bash
# Полное сканирование сайта (медленно, но актуально)
python3 moscow.py [количество]

# Примеры  
python3 moscow.py 1500  # максимум товаров
python3 moscow.py 500   # быстрый тест
```

**Результат**: Свежие данные прямо с сайта, 91.6% с полными БЖУ

## 🛠️ Настройка для Railway

### Изменение заголовков User-Agent

Для обхода блокировок измените User-Agent в файлах:

**1. В `address.py` (строки 58-64):**
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0',  # ← Измените эту строку
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}
```

**2. В `moscow.py` (строки 37-43):**
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0',  # ← Измените эту строку
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}
```

**Популярные User-Agent строки:**
```bash
# Chrome Windows
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36

# Chrome Mac  
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36

# Firefox Windows
Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0

# Safari Mac
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15
```

### Настройка таймаутов и лимитов

**В `address.py` (строка 460):**
```python
antibot_client = AntiBotClient(concurrency=5, timeout=60)  # ← Уменьшите concurrency, увеличьте timeout
```

**В `moscow.py` (строка 35):**
```python
self.semaphore = asyncio.Semaphore(3)  # ← Уменьшите для Railway
self.timeout = 45  # ← Увеличьте timeout
```

## 📊 Формат данных

### Структура CSV/JSONL файлов

| Поле | Описание | Пример |
|------|----------|--------|
| `id` | Уникальный ID товара | `kurinaya-grudka-s-gribami-37923` |
| `name` | Название товара | `Куриная грудка с грибами и пенне` |
| `price` | Цена в рублях | `318` |
| `category` | Категория | `Готовая еда` |
| `url` | Ссылка на товар | `https://vkusvill.ru/goods/...` |
| `shop` | Магазин | `vkusvill_improved` |
| `photo` | URL фотографии | `https://vkusvill.ru/upload/...` |
| `composition` | Состав продукта | `филе грудки куриное, макароны...` |
| `tags` | Теги (пока пустые) | `` |
| `portion_g` | Вес порции | `230.0г` |
| `kcal_100g` | Калории на 100г | `160.5` |
| `protein_100g` | Белки на 100г | `15.9` |
| `fat_100g` | Жиры на 100г | `5.7` |
| `carb_100g` | Углеводы на 100г | `11.4` |

### Пример записи

```json
{
  "id": "kurinaya-grudka-s-gribami-i-penne-37923",
  "name": "Куриная грудка с грибами и пенне", 
  "price": "318",
  "category": "Готовая еда",
  "url": "https://vkusvill.ru/goods/kurinaya-grudka-s-gribami-i-penne-37923.html",
  "shop": "vkusvill_improved",
  "photo": "https://vkusvill.ru/upload/iblock/...",
  "composition": "филе грудки куриное, макаронные изделия...",
  "tags": "",
  "portion_g": "230.0г",
  "kcal_100g": "160.5",
  "protein_100g": "15.9", 
  "fat_100g": "5.7",
  "carb_100g": "11.4"
}
```

## 📈 Статистика качества

### Быстрый парсер (`address.py`)
- ✅ **1459 товаров** за 0.1 секунды
- ✅ **95.4% с полными БЖУ** (1392 товара)
- ✅ **100% с составом** (1459 товаров) 
- ✅ **Мгновенная работа** (использует готовую базу)

### Полный парсер (`moscow.py`)  
- ✅ **1459 товаров** за 31 минуту
- ✅ **91.6% с полными БЖУ** (1336 товаров)
- ✅ **100% с составом** (1459 товаров)
- ✅ **Свежие данные** (парсит сайт в реальном времени)

## 🐳 Docker

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Создание директории для данных
RUN mkdir -p data

# Запуск быстрого парсера по умолчанию
CMD ["python3", "address.py", "Москва, Тверская улица, 12", "1500"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  vkusvill-parser:
    build: .
    volumes:
      - ./data:/app/data
    environment:
      - PYTHONPATH=/app
    command: python3 address.py "Москва, Красная площадь, 1" 1000
```

### Команды Docker

```bash
# Сборка образа
docker build -t vkusvill-parser .

# Быстрый парсер
docker run -v $(pwd)/data:/app/data vkusvill-parser python3 address.py "Москва" 1000

# Полный парсер  
docker run -v $(pwd)/data:/app/data vkusvill-parser python3 moscow.py 1500

# Интерактивный режим
docker run -it -v $(pwd)/data:/app/data vkusvill-parser bash
```

## 🔧 Устранение проблем

### Блокировка запросов
```bash
# Уменьшите нагрузку
python3 address.py "Адрес" 100  # меньше товаров

# Измените User-Agent (см. выше)
# Увеличьте timeout в коде
```

### Ошибки на Railway
```bash
# Проверьте логи
railway logs

# Перезапустите сервис  
railway restart

# Обновите переменные окружения
railway variables set PYTHONPATH=/app
```

### Пустые результаты
```bash
# Проверьте доступность сайта
curl -I https://vkusvill.ru

# Попробуйте другой адрес
python3 address.py "Москва, Красная площадь, 1" 100

# Используйте полный парсер
python3 moscow.py 500
```

## 📁 Структура проекта

```
Samokat-Ready-Food-Scraper/
├── address.py          # 🏃‍♂️ Быстрый парсер по адресу
├── moscow.py           # 🔍 Полный парсер ВкусВилл  
├── requirements.txt    # 📦 Зависимости Python
├── Dockerfile         # 🐳 Docker образ
├── railway.toml       # 🚂 Конфигурация Railway
├── data/              # 📊 Результаты парсинга
│   ├── address_fast_*.csv
│   ├── address_fast_*.jsonl
│   ├── moscow_improved_*.csv
│   └── moscow_improved_*.jsonl
└── README.md          # 📖 Документация
```

## 🤝 Поддержка

- 🐛 **Баги**: Создайте Issue на GitHub
- 💡 **Идеи**: Pull Request приветствуются
- 📧 **Вопросы**: Обратитесь через Issues

## 📄 Лицензия

MIT License - используйте свободно в коммерческих и некоммерческих проектах.

---

⭐ **Поставьте звезду**, если проект оказался полезным!