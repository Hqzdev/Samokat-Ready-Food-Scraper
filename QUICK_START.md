# 🚀 Быстрый старт

## 1. Установка

```bash
# Клонирование репозитория
git clone <repository-url>
cd Samokat-Ready-Food-Scraper

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt

# Установка браузеров Playwright
playwright install chromium
```

## 2. Настройка

Отредактируйте `config.yaml`:

```yaml
# Включите все источники
sources:
  - samokat
  - lavka
  - vkusvill

# Укажите ваш город
city: "Москва"

# Для отладки отключите headless режим
headless: false
```

## 3. Тестирование

### Тест всех источников
```bash
python test_all_sources.py
```

### Тест отдельных источников
```bash
# Самокат
make test-samokat-only

# Яндекс.Лавка
make test-lavka-only

# ВкусВилл
make test-vkusvill-only
```

## 4. Запуск Telegram бота

```bash
# Укажите токен в config.yaml
telegram_bot_token: "ваш_токен_от_botfather"

# Запуск бота
python run_bot.py

# Или через make
make run-bot
```

## 5. Использование бота

В Telegram используйте команды:
- `/start` - Главное меню
- `/scrape_all` - Парсинг всех источников (рекомендуется)
- `/test_samokat` - Тест Самоката
- `/test_lavka` - Тест Лавки
- `/test_vkusvill` - Тест ВкусВилла

## 6. Командная строка

```bash
# Парсинг всех источников
python -m src.main --source all --city "Москва" --out data.csv

# Парсинг с лимитом
python -m src.main --source all --limit 100 --out data.sqlite

# Парсинг с изображениями
python -m src.main --source all --download-images --out data.sqlite
```

## 🆘 Решение проблем

### Бот не находит товары (0 продуктов)

1. **Проверьте интернет-соединение**
2. **Запустите тест отдельных источников**
3. **Проверьте логи в `data/out/scraper.log`**
4. **Убедитесь, что браузер не заблокирован**

### Ошибки инициализации скрейперов

1. **Проверьте версию Python (3.11+)**
2. **Переустановите зависимости: `pip install -r requirements.txt`**
3. **Переустановите браузеры: `playwright install chromium`**

### Бот зависает

1. **Используйте команду `/scrape_all` - она показывает прогресс**
2. **Проверьте логи бота**
3. **Перезапустите бота**

## 📊 Ожидаемые результаты

- **Самокат**: 50-200 продуктов на категорию
- **Яндекс.Лавка**: 30-150 продуктов на категорию  
- **ВкусВилл**: 40-180 продуктов на категорию

**Общее время парсинга**: 10-15 минут для всех источников
