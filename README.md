# Ready Food Scraper

Готовый Python 3.11 скрипт/пакет для веб-скрейпинга готовой еды из сервисов доставки: **Самокат**, **Яндекс Лавка**, **ВкусВилл**.

## 🎯 Возможности

- ✅ **Полная автоматизация**: установка города/адреса, пагинация, извлечение данных
- ✅ **Модульная архитектура**: отдельные скрейперы для каждого магазина
- ✅ **Нормализация данных**: единый формат БЖУ (на 100г), очистка названий
- ✅ **Множественные форматы**: CSV, JSON, Parquet
- ✅ **Загрузка изображений**: опционально с сохранением локально
- ✅ **Валидация качества**: проверка полноты нутриентов ≥99%
- ✅ **CLI интерфейс**: удобное управление через командную строку
- ✅ **Docker поддержка**: готовые образы и docker-compose
- ✅ **Логирование**: структурированные логи с отчетами
- ✅ **Конфигурация**: YAML/ENV настройки для всех параметров

## 📋 Собираемые данные

### Обязательные поля
- `id` - стабильный ID ({shop}:{native_id})
- `name` - название товара (очищенное)
- `category` - нормализованная категория
- `kcal_100g`, `protein_100g`, `fat_100g`, `carb_100g` - БЖУ на 100г
- `portion_g` - вес порции в граммах
- `price` - актуальная цена
- `shop` - магазин (samokat|lavka|vkusvill)
- `url` - ссылка на товар
- `photo_url` - ссылка на изображение

### Дополнительные поля
- `tags` - теги товара (острое, вегетарианское, ПП и т.д.)
- `composition` - состав/ингредиенты
- `allergens`, `shelf_life`, `storage`, `brand` - дополнительная информация
- `price_per_100g`, `rating`, `reviews_count` - расчетные и метрические данные

## 🚀 Быстрый старт

### Установка

```bash
# Клонирование репозитория
git clone https://github.com/your-repo/ready-food-scraper.git
cd ready-food-scraper

# Установка зависимостей
make setup
# или вручную:
pip3 install -r requirements.txt
pip3 install pyarrow  # для поддержки Parquet
python3 -m playwright install firefox
```

### Демонстрация

```bash
# Главное меню парсера
python3 run_scraper.py

# Готовые данные (275 товаров ВкусВилл)
head data/FINAL_real_foods.csv

# Диагностика магазинов
python3 debug_samokat.py    # Самокат
python3 debug_lavka_real.py # Лавка
```

### Базовое использование

```bash
# Скрейпинг всех магазинов
python -m app scrape --shop all --city "Москва" --address "Красная площадь, 1" --out data/foods.csv

# Конкретный магазин
python -m app scrape --shop samokat --city "Москва" --out data/samokat.csv

# С загрузкой изображений
python -m app scrape --shop all --download-images --out data/foods.csv

# Множественные форматы
python -m app scrape --shop all --format csv json parquet --out data/foods.csv
```

## 📖 Подробная документация

### CLI команды

#### Основная команда скрейпинга
```bash
python -m app scrape [OPTIONS]
```

**Параметры:**
- `--shop` - Магазин: `samokat`, `lavka`, `vkusvill`, `all` (по умолчанию: `all`)
- `--city` - Город (по умолчанию: `Москва`)
- `--address` - Адрес доставки
- `--out` - Выходной файл (по умолчанию: `data/foods.csv`)
- `--format` - Форматы вывода: `csv`, `json`, `jsonl`, `parquet` (можно несколько)
- `--download-images/--no-download-images` - Скачивать изображения
- `--parallel` - Количество параллельных процессов (по умолчанию: 3)
- `--headless/--no-headless` - Режим браузера (по умолчанию: headless)
- `--log-level` - Уровень логирования: `DEBUG`, `INFO`, `WARNING`, `ERROR`
- `--proxy` - Прокси серверы (можно несколько)
- `--max-retries` - Максимальное количество повторных попыток
- `--delay-min/--delay-max` - Задержки между запросами

#### Примеры использования

```bash
# Санкт-Петербург с изображениями
python -m app scrape --shop all --city "Санкт-Петербург" --address "Невский проспект, 1" --download-images --out data/spb_foods.csv

# Только Лавка с прокси
python -m app scrape --shop lavka --city "Москва" --proxy "http://proxy:8080" --out data/lavka.csv

# Высокая параллельность
python -m app scrape --shop all --parallel 6 --delay-min 0.5 --delay-max 1.5 --out data/foods.csv

# Все форматы экспорта
python -m app scrape --shop all --format csv json parquet --out data/foods.csv

# Режим разработки (с GUI браузера)
python -m app scrape --shop samokat --no-headless --log-level DEBUG --out data/debug.csv
```

#### Дополнительные команды

```bash
# Валидация конфигурации
python -m app validate-config --config config.yaml

# Очистка старых изображений
python -m app cleanup-images --days 7 --images-dir images

# Установка браузера
python -m app install-browser
```

### Конфигурация

#### config.yaml
```yaml
# Настройки браузера
browser:
  headless: true
  timeout: 30000

# Настройки скрейпинга  
scraping:
  parallel_workers: 3
  request_delay_min: 1.0
  request_delay_max: 3.0
  max_retries: 3

# Город и адрес по умолчанию
defaults:
  city: "Москва"
  address: "Красная площадь, 1"

# Прокси (опционально)
proxy:
  enabled: false
  servers: []

# Экспорт данных
export:
  formats: ["csv"]
  download_images: false
  images_dir: "images"
```

#### Переменные окружения (.env)
```bash
BROWSER_HEADLESS=true
PARALLEL_WORKERS=3
DEFAULT_CITY=Москва
DEFAULT_ADDRESS=Красная площадь, 1
DOWNLOAD_IMAGES=false
LOG_LEVEL=INFO
```

## 🐳 Docker

### Быстрый запуск
```bash
# Сборка и запуск
make docker-run

# Или через docker-compose
docker-compose up scraper
```

### Кастомные команды
```bash
# Конкретный магазин
docker-compose run --rm scraper-task scrape --shop samokat --city "Москва" --out data/samokat.csv

# С изображениями
docker-compose run --rm scraper-task scrape --shop all --download-images --out data/foods.csv

# Другой город
docker-compose run --rm scraper-task scrape --shop all --city "Санкт-Петербург" --address "Невский проспект, 1" --out data/spb.csv
```

### Периодический запуск (cron)
```bash
# Запуск cron сервиса
docker-compose --profile cron up -d scraper-cron
```

## 📊 Качество данных

### Валидация
- ✅ **Полнота нутриентов**: ≥99% товаров с БЖУ и калориями
- ✅ **Корректность названий**: не числовые, длина ≥3 символов
- ✅ **Валидные цены**: > 0, корректный формат
- ✅ **Стабильные ID**: одинаковые при повторных запусках
- ✅ **Дедупликация**: по ID и name+portion_g

### Отчетность
После каждого запуска создается:
- 📄 `{filename}_report.md` - подробный отчет
- 📄 `{filename}_issues.csv` - проблемы валидации
- 📊 Статистика в логах: покрытие, время, ошибки

### Пример отчета
```
# Отчет о скрейпинге готовой еды

## Общая статистика
- Всего найдено товаров: 1,247
- Успешно обработано: 1,235
- Процент успеха: 99.0%
- Общее время выполнения: 180.5 сек

## Качество данных
- Товаров с полными нутриентами: 1,223 из 1,235 (99.0%)
- Товаров с фото: 1,235 из 1,235
- Товаров с составом: 1,198 из 1,235
```

## 🛠 Разработка

### Установка для разработки
```bash
make install-dev
```

### Тестирование
```bash
# Все тесты
make test

# Конкретный тест
pytest tests/test_models.py -v

# С покрытием
pytest --cov=app --cov-report=html
```

### Линтинг и форматирование
```bash
make lint    # Проверка кода
make format  # Форматирование
```

### Структура проекта
```
ready-food-scraper/
├── app/                    # Основной код
│   ├── scrapers/          # Скрейперы магазинов
│   │   ├── base.py       # Базовый класс
│   │   ├── samokat.py    # Самокат
│   │   ├── lavka.py      # Яндекс Лавка
│   │   └── vkusvill.py   # ВкусВилл
│   ├── utils/            # Утилиты
│   │   ├── normalizer.py # Нормализация данных
│   │   ├── storage.py    # Экспорт данных
│   │   └── logger.py     # Логирование
│   ├── models.py         # Модели данных
│   └── cli.py           # CLI интерфейс
├── tests/               # Тесты
├── data/               # Выходные данные
├── images/             # Изображения товаров
├── logs/               # Логи
├── config.yaml         # Конфигурация
├── Dockerfile         # Docker образ
├── docker-compose.yml # Docker Compose
└── Makefile          # Команды сборки
```

## 🔧 Настройка магазинов

### Самокат
- **URL**: `https://samokat.ru`
- **Категории**: готовая-еда, кулинария, салаты, супы, горячие-блюда
- **Особенности**: динамическая загрузка, модальные окна выбора адреса

### Яндекс Лавка
- **URL**: `https://lavka.yandex.ru`  
- **Категории**: gotovaya-eda, kulinariya, salaty, supy-i-bulon
- **Особенности**: SPA архитектура, сложная навигация

### ВкусВилл
- **URL**: `https://vkusvill.ru`
- **Категории**: gotovaya-eda, kulinariya, salaty-i-zakuski
- **Особенности**: выбор магазина, табы с информацией

## 🚨 Антибот защита

### Встроенные меры
- 🕐 **Случайные задержки**: 1-3 сек между запросами
- 🎭 **Ротация User-Agent**: несколько реальных браузеров
- 🔄 **Повторные попытки**: до 3 попыток при ошибках
- 🚫 **Блокировка ресурсов**: CSS, изображения для ускорения
- 🌐 **Поддержка прокси**: ротация IP адресов

### Рекомендации
- Используйте задержки ≥1 сек для продакшена
- Настройте прокси для высоких нагрузок
- Мониторьте логи на 429/403 ошибки
- Запускайте в нерабочие часы

## 📈 Производительность

### Типичные показатели
- **Скорость**: ~50-100 товаров/минуту на магазин
- **Память**: ~200-500 МБ при parallel_workers=3
- **CPU**: умеренная нагрузка (браузер headless)
- **Сеть**: ~10-50 МБ трафика на 1000 товаров

### Оптимизация
```bash
# Высокая скорость (осторожно с антиботом!)
python -m app scrape --parallel 6 --delay-min 0.5 --delay-max 1.0

# Экономия ресурсов
python -m app scrape --parallel 2 --delay-min 2.0 --delay-max 4.0

# Минимум трафика (без изображений)
python -m app scrape --no-download-images
```

## ❓ FAQ

**Q: Скрейпер не находит товары**  
A: Проверьте правильность города/адреса, магазин может не доставлять в указанную зону.

**Q: Низкая полнота нутриентов**  
A: Некоторые товары могут не содержать БЖУ в карточке. Это нормально для ~1-5% товаров.

**Q: Ошибки 403/429**  
A: Увеличьте задержки, используйте прокси, запускайте реже.

**Q: Почему используется Firefox вместо Chrome?**  
A: Firefox показал лучшую совместимость с macOS и Apple Silicon чипами.

**Q: Как добавить новый магазин?**  
A: Создайте новый класс в `app/scrapers/`, наследуясь от `BaseScraper`.

**Q: Можно ли запускать на Windows?**  
A: Да, но рекомендуется Docker или WSL для лучшей совместимости.

**Q: Как запустить демонстрацию?**  
A: Выполните `python3 demo_scraper.py` для полной демонстрации с тестовыми данными.

## 📝 Лицензия

MIT License - см. файл [LICENSE](LICENSE)

## 🤝 Поддержка

- 🐛 **Баги**: создайте Issue в GitHub
- 💡 **Предложения**: Pull Request приветствуются  
- 📧 **Вопросы**: используйте Discussions

---

**⚠️ Важно**: Используйте скрейпер ответственно, соблюдайте robots.txt и условия использования сайтов. Автор не несет ответственности за неправомерное использование.
