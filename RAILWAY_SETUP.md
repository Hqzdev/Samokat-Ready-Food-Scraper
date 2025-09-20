# 🚂 Развертывание на Railway

## Быстрая настройка (5 минут)

### 1. Подготовка репозитория
```bash
# Форкните этот репозиторий на GitHub
# Или клонируйте и загрузите в свой репозиторий
git clone https://github.com/your-username/Samokat-Ready-Food-Scraper.git
```

### 2. Развертывание на Railway
1. Зайдите на [railway.app](https://railway.app)
2. Нажмите **"Deploy from GitHub"**
3. Выберите ваш форк репозитория
4. Railway автоматически обнаружит `Dockerfile` и начнет сборку

### 3. Настройка переменных окружения
В панели Railway добавьте переменные:
```bash
PYTHONPATH=/app
PYTHONUNBUFFERED=1
```

### 4. Настройка команды запуска (опционально)
По умолчанию запускается:
```bash
python3 address.py "Москва, Тверская улица, 12" 1500
```

Для изменения команды:
1. Перейдите в **Settings** → **Deploy**
2. Измените **Start Command**:
```bash
# Быстрый парсер с другим адресом
python3 address.py "СПб, Невский проспект, 1" 1000

# Полный парсер
python3 moscow.py 1500
```

## 🔧 Настройка парсера

### Изменение User-Agent для обхода блокировок

**1. В файле `address.py` (строки 58-64):**
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0',  # ← Измените
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # ... остальные заголовки
}
```

**2. В файле `moscow.py` (строки ~40):**
```python  
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0',  # ← Измените
    # ... остальные заголовки
}
```

### Популярные User-Agent строки:
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

### Настройка таймаутов

**В `address.py` (строка ~460):**
```python
antibot_client = AntiBotClient(concurrency=3, timeout=60)  # ← Для Railway уменьшите concurrency
```

**В `moscow.py` (строки ~35):**
```python
self.semaphore = asyncio.Semaphore(2)  # ← Уменьшите для стабильности
self.timeout = 45  # ← Увеличьте timeout
```

## 📊 Получение результатов

### Через Railway CLI
```bash
# Установка CLI
npm install -g @railway/cli

# Логин
railway login

# Просмотр логов
railway logs

# Скачивание файлов (если есть volume)
railway shell
cat data/address_fast_*.csv > results.csv
```

### Через веб-интерфейс
1. Откройте проект на railway.app
2. Перейдите в **Deployments**
3. Откройте последний деплой
4. Смотрите логи в **Build Logs** и **Deploy Logs**

## 🐛 Устранение проблем

### Ошибка "Memory limit exceeded"
```bash
# Уменьшите количество товаров
python3 address.py "Москва" 500

# Или уменьшите concurrency в коде
```

### Ошибка "Request timeout"
```bash
# Увеличьте timeout в коде
# Уменьшите concurrency
# Смените User-Agent
```

### Парсер завершается сразу
```bash
# Проверьте логи Railway
# Убедитесь что нет синтаксических ошибок
# Проверьте переменные окружения
```

## 🚀 Автоматизация

### Запуск по расписанию
Railway не поддерживает cron из коробки, но можно использовать:
1. **GitHub Actions** с расписанием
2. **Внешний cron-сервис** (например, cron-job.org)
3. **Railway Cron Plugin** (если доступен)

### Пример GitHub Action:
```yaml
# .github/workflows/scrape.yml
name: Daily Scraping
on:
  schedule:
    - cron: '0 9 * * *'  # Каждый день в 9:00 UTC
  
jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        run: |
          curl -X POST ${{ secrets.RAILWAY_WEBHOOK_URL }}
```

## 💡 Советы

1. **Начните с быстрого парсера** - он работает мгновенно
2. **Используйте полный парсер** только для получения свежих данных
3. **Мониторьте логи** Railway для отладки
4. **Меняйте User-Agent** при блокировках
5. **Уменьшайте нагрузку** при ошибках timeout

## 📞 Поддержка

- 🐛 **Проблемы с Railway**: [railway.app/help](https://railway.app/help)
- 💬 **Вопросы по коду**: создайте Issue в репозитории
- 📧 **Срочные вопросы**: обратитесь через Railway Discord
