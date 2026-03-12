# Гайд: 3D-модель стаканчика в Blender для A-Frame

## Что нужно

- **Blender** 3.x или 4.x ([blender.org](https://www.blender.org/download/)).
- Скрипт `blender_coffee_cup.py` из этой папки.

## Шаги

### 1. Создать папку для экспорта

В папке `coffee-game` создай папку `assets` (если её ещё нет):

```
coffee-game/
  assets/
  index.html
  ar.html
  blender_coffee_cup.py
```

### 2. Открыть Blender и скрипт

1. Запусти Blender.
2. Вверху переключись на вкладку **Scripting**.
3. Нажми **Open** и выбери файл `blender_coffee_cup.py` из папки `coffee-game`.

### 3. Указать путь экспорта (если нужно)

В скрипте по умолчанию используется папка рядом со скриптом: `assets/`. Если хочешь сохранять в другое место, измени в начале скрипта:

```python
EXPORT_DIR = "C:/Users/ТвойПользователь/Desktop/vr ar/coffee-game/assets"  # Windows
# или
EXPORT_DIR = "/Users/ТвойПользователь/Desktop/vr ar/coffee-game/assets"     # macOS
EXPORT_PATH = os.path.join(EXPORT_DIR, "coffee_cup.glb")
```

### 4. Запустить скрипт

1. В редакторе скрипта нажми **Run Script** (▶) или **Alt+P**.
2. В консоли (внизу вкладки Scripting) должно появиться сообщение вида:  
   `Готово: стаканчик создан и экспортирован в .../assets/coffee_cup.glb`.
3. В папке `assets` появится файл **coffee_cup.glb**.

### 5. Использовать модель в A-Frame

Скопируй `coffee_cup.glb` в папку `assets` твоего проекта (если экспорт был в другое место). В HTML добавь в `<a-assets>`:

```html
<a-assets>
  <a-asset-item id="cup-model" src="assets/coffee_cup.glb"></a-asset-item>
</a-assets>
```

Вместо примитива стаканчика используй:

```html
<a-entity gltf-model="#cup-model" position="0 1 -3" scale="1 1 1"></a-entity>
```

Для игры можно заменить создание стаканчика в `createCup()` на подгрузку этой модели:

```javascript
el.setAttribute('gltf-model', 'url(assets/coffee_cup.glb)');
el.setAttribute('scale', '1 1 1');
```

## Ручной экспорт из Blender (без скрипта)

1. Создай цилиндр (Add → Mesh → Cylinder): Radius 0.04, Depth 0.12.
2. В Edit Mode немного сузь низ (Scale по X/Y).
3. Добавь тонкий тор для края (Add → Mesh → Torus).
4. Выдели все объекты, Object → Join.
5. File → Export → glTF 2.0 (.glb), выбери папку и имя `coffee_cup.glb`, нажми Export.

## Размеры в игре

В скрипте стаканчик имеет высоту ~0.12 и радиус ~0.04 (в единицах Blender). В A-Frame 1 единица ≈ 1 метр, поэтому модель будет небольшой. Масштаб можно менять атрибутом `scale`, например `scale="2 2 2"` для более крупного стаканчика.
