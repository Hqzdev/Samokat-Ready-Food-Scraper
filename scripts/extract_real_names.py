#!/usr/bin/env python3
"""Извлечение настоящих названий товаров из URL и создание финального файла."""

import pandas as pd
import re
from pathlib import Path


def url_to_name(url: str) -> str:
    """Преобразование URL в читаемое название."""
    try:
        # Извлекаем часть с названием из URL
        if '/goods/' in url:
            # Для ВкусВилл: https://vkusvill.ru/goods/pasta-rizoni-s-syrnym-sousom-i-kuritsey-112440.html
            name_part = url.split('/goods/')[-1]
            name_part = name_part.split('.html')[0]  # Убираем .html
            name_part = re.sub(r'-\d+$', '', name_part)  # Убираем ID в конце
            
        elif '/product/' in url:
            # Для других магазинов
            name_part = url.split('/product/')[-1]
            
        else:
            return "Товар без названия"
        
        # Преобразуем в читаемое название
        # Заменяем дефисы на пробелы
        name = name_part.replace('-', ' ')
        
        # Словарь для замены сокращений
        replacements = {
            ' s ': ' с ',
            ' i ': ' и ',
            ' v ': ' в ',
            ' na ': ' на ',
            ' po ': ' по ',
            ' iz ': ' из ',
            ' so ': ' со ',
            'kurinoe': 'куриное',
            'kuriney': 'курицей',
            'kurinyy': 'куриный',
            'kurinaya': 'куриная',
            'file': 'филе',
            'zapechennoe': 'запеченное',
            'tsukini': 'цукини',
            'motsarelloy': 'моцареллой',
            'lazanya': 'лазанья',
            'kotleta': 'котлета',
            'kartofelnym': 'картофельным',
            'pyure': 'пюре',
            'pasta': 'паста',
            'rizoni': 'ризони',
            'syrnym': 'сырным',
            'sousom': 'соусом',
            'pirog': 'пирог',
            'tatarskiy': 'татарский',
            'kartofelem': 'картофелем',
            'myasom': 'мясом',
            'ptitsy': 'птицы',
            'sendvich': 'сендвич',
            'sando': 'сандо',
            'raduzhnoy': 'радужной',
            'forelyu': 'форелью',
            'tvorozhnym': 'творожным',
            'syrom': 'сыром',
            'pesto': 'песто',
            'pitstseta': 'пиццета',
            'tsyplenkom': 'цыпленком',
            'kombo': 'комбо',
            'nabor': 'набор',
            'grudka': 'грудка',
            'po derevenski': 'по-деревенски',
            'salat': 'салат',
            'letnikh': 'летних',
            'ovoshchey': 'овощей',
            'sup': 'суп',
            'syrnyy': 'сырный',
            'grenkami': 'гренками',
            'oladi': 'оладьи',
            'kurinye': 'куриные',
            'ezhiki': 'ежики',
            'myasnye': 'мясные',
            'otvarnoy': 'отварной',
            'grechkoy': 'гречкой',
            'roll': 'ролл',
            'tsezar': 'цезарь',
            'pekinskoy': 'пекинской',
            'kapustoy': 'капустой',
            'farfalle': 'фарфалле',
            'kuritsa': 'курица',
            'kartofelnym': 'картофельным',
            'khashbraunom': 'хашбрауном',
            'tortile': 'тортилье',
            'zapekanka': 'запеканка',
            'tvorozhnaya': 'творожная',
            'bez dob sakhara': 'без добавленного сахара',
            'myagkim': 'мягким',
            'rikotta': 'рикотта',
            'pibimpab': 'пибимпаб',
            'marinovannoy': 'маринованной',
            'govyadinoy': 'говядиной',
            'frikadelkami': 'фрикадельками',
            'zvezdochki': 'звездочки',
            'blinchiki': 'блинчики',
            'yaichnye': 'яичные',
            'aziatski': 'по-азиатски',
            'zhyulenom': 'жульеном',
            'vinegret': 'винегрет',
            'marinovannoy': 'маринованной',
            'zharenyy': 'жареный',
            'svininoy': 'свининой',
            'gribami': 'грибами',
            'smetannom': 'сметанном',
            'souse': 'соусе',
            'kabachkom': 'кабачком',
            'rostbifom': 'ростбифом',
            'bebi': 'беби',
            'kunzhutnym': 'кунжутным',
            'vitaminnyy': 'витаминный',
            'limonnoy': 'лимонной',
            'zapravkoy': 'заправкой',
            'mini': 'мини',
            'chiabatta': 'чиабатта',
            'vetchinoy': 'ветчиной',
            'omletom': 'омлетом',
            'rizotto': 'ризотто',
            'belymi': 'белыми',
            'gribami': 'грибами',
            'boul': 'боул',
            'zapechennoy': 'запеченной',
            'kuskusom': 'кускусом',
            'batatom': 'бататом',
            'maslyano': 'масляно',
            'limonnym': 'лимонным',
            'govyadina': 'говядина',
            'tushenaya': 'тушеная',
            'lisichkami': 'лисичками',
            'rizo': 'ризо',
            'slivochno': 'сливочно',
            'gribnom': 'грибном',
            'plov': 'плов',
            'borshch': 'борщ',
            'kotlety': 'котлеты',
            'bulgurom': 'булгуром',
            'kinoa': 'киноа',
            'ukrainskiy': 'украинский'
        }
        
        # Применяем замены
        for old, new in replacements.items():
            name = name.replace(old, new)
        
        # Приводим к нормальному виду
        name = name.strip().capitalize()
        
        # Убираем лишние пробелы
        name = re.sub(r'\s+', ' ', name)
        
        return name
        
    except Exception as e:
        return "Товар без названия"


def process_real_foods_file():
    """Обработка файла с настоящими товарами."""
    print("🔧 ОБРАБОТКА НАСТОЯЩИХ ТОВАРОВ")
    print("📂 Исходный файл: data/real_foods.csv")
    print("-" * 50)
    
    # Читаем данные
    df = pd.read_csv("data/real_foods.csv")
    print(f"📊 Загружено строк: {len(df)}")
    
    # Извлекаем настоящие названия из URL
    print("🔄 Извлекаем названия из URL...")
    
    real_names = []
    for i, row in df.iterrows():
        url = row.get('url', '')
        if url:
            real_name = url_to_name(url)
            real_names.append(real_name)
        else:
            real_names.append(row.get('name', 'Товар без названия'))
        
        if (i + 1) % 50 == 0:
            print(f"   ✅ Обработано {i + 1} товаров...")
    
    # Обновляем названия
    df['name'] = real_names
    
    # Фильтруем товары с нормальными названиями и ценами
    df_filtered = df[
        (df['name'] != 'Товар без названия') & 
        (df['name'].str.len() > 5) &
        (df['price'] > 0) &
        (df['portion_g'].notna()) &
        (df['portion_g'] > 0)
    ].copy()
    
    print(f"📊 После фильтрации: {len(df_filtered)} качественных товаров")
    
    # Сохраняем обработанный файл
    output_file = "data/FINAL_real_foods.csv"
    df_filtered.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"💾 Сохранено: {output_file}")
    
    # Показываем примеры
    print(f"\n📋 ПРИМЕРЫ НАСТОЯЩИХ ТОВАРОВ:")
    for i, row in df_filtered.head(10).iterrows():
        print(f"{i+1}. {row['name']}")
        print(f"   💰 Цена: {row['price']} руб")
        print(f"   ⚖️ Вес: {row['portion_g']}г")
        print(f"   💵 Цена за 100г: {row['price_per_100g']:.1f} руб")
        print(f"   🔗 URL: {row['url']}")
        print()
    
    # Статистика
    print(f"📊 СТАТИСТИКА:")
    print(f"   ✅ Всего товаров: {len(df_filtered)}")
    print(f"   💰 Средняя цена: {df_filtered['price'].mean():.1f} руб")
    print(f"   ⚖️ Средний вес: {df_filtered['portion_g'].mean():.1f}г")
    print(f"   💵 Средняя цена за 100г: {df_filtered['price_per_100g'].mean():.1f} руб")
    
    # Топ категории
    categories = df_filtered['category'].value_counts()
    print(f"\n🏷️ ТОП КАТЕГОРИИ:")
    for category, count in categories.head(5).items():
        print(f"   • {category}: {count} товаров")
    
    return len(df_filtered)


if __name__ == "__main__":
    print("🎯 ИЗВЛЕЧЕНИЕ НАСТОЯЩИХ НАЗВАНИЙ ТОВАРОВ")
    print("📋 Преобразование URL в читаемые названия")
    
    count = process_real_foods_file()
    
    if count > 0:
        print(f"\n🎉 ГОТОВО! {count} настоящих товаров с правильными названиями!")
        print("🔍 Файл: data/FINAL_real_foods.csv")
        print("\n✨ Теперь у вас есть качественная база настоящих товаров!")
    else:
        print("\n💥 Не удалось обработать товары")
        exit(1)
