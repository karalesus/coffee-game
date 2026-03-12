"""
═══════════════════════════════════════════════════════════════════════════════
  BLENDER: создание 3D-модели стаканчика кофе для A-Frame
═══════════════════════════════════════════════════════════════════════════════

ЧТО ДЕЛАЕТ СКРИПТ:
  1) Очищает сцену от стандартного куба.
  2) Создаёт модель стаканчика: цилиндр (основа) + усечённый конус (чашка) + кольцо (край).
  3) Назначает простые материалы (коричневый корпус, тёмное «кофе», белый край).
  4) Экспортирует модель в формате glTF 2.0 (.glb) для использования в A-Frame.

КАК ИСПОЛЬЗОВАТЬ:
  1) Открой Blender (рекомендуется 3.x или 4.x).
  2) Перейди в режим Scripting (меню сверху: Scripting).
  3) Нажми "Open" и выбери этот файл blender_coffee_cup.py.
  4) Укажи путь EXPORT_PATH (папка, куда сохранить coffee_cup.glb).
  5) Нажми Run Script (▶ или Alt+P).
  6) В папке появится файл coffee_cup.glb — его можно подгрузить в A-Frame через
     <a-entity gltf-model="url(assets/coffee_cup.glb)">.

ЭКСПОРТ В GLTF:
  В Blender: File → Export → glTF 2.0 (.glb).
  Или скрипт сам экспортирует, если указан bpy.ops.export_scene.gltf (доступен в Blender 2.80+).

Запуск: Blender → Scripting → открыть скрипт → Run Script.
"""

import bpy
import os
import math

# ═══════════════════════════════════════════════════════════════════════════
#  НАСТРОЙКИ: измени путь под свою папку проекта
# ═══════════════════════════════════════════════════════════════════════════
# Папка, куда сохранить coffee_cup.glb. Если скрипт открыт из папки coffee-game — будет coffee-game/assets.
try:
    script_path = bpy.context.space_data.text.filepath
    script_dir = os.path.dirname(os.path.abspath(script_path)) if script_path else os.path.expanduser("~")
except Exception:
    script_dir = os.path.expanduser("~")
EXPORT_DIR = os.path.abspath(os.path.expanduser(os.path.join(script_dir, "assets")))
EXPORT_PATH = os.path.join(EXPORT_DIR, "coffee_cup.glb")

# Размеры стаканчика (в единицах Blender; в A-Frame 1 единица ≈ 1 метр, делаем ~0.15)
CUP_HEIGHT = 0.12
CUP_RADIUS_TOP = 0.04
CUP_RADIUS_BOTTOM = 0.03
RIM_HEIGHT = 0.008
RIM_RADIUS = 0.042

# ═══════════════════════════════════════════════════════════════════════════
#  Очистка сцены
# ═══════════════════════════════════════════════════════════════════════════
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for mesh in list(bpy.data.meshes):
        bpy.data.meshes.remove(mesh)
    for mat in list(bpy.data.materials):
        bpy.data.materials.remove(mat)

# ═══════════════════════════════════════════════════════════════════════════
#  Материалы
# ═══════════════════════════════════════════════════════════════════════════
def make_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.6
    bsdf.inputs["Metallic"].default_value = 0.0
    return mat

# ═══════════════════════════════════════════════════════════════════════════
#  Создание меша стаканчика
# ═══════════════════════════════════════════════════════════════════════════
def create_cup():
    # Корпус: усечённый конус (в Blender 4+/5 у cylinder один radius, конус — radius1/radius2)
    bpy.ops.mesh.primitive_cone_add(
        radius1=CUP_RADIUS_BOTTOM,
        radius2=CUP_RADIUS_TOP,
        depth=CUP_HEIGHT,
        location=(0, 0, CUP_HEIGHT / 2)
    )
    body = bpy.context.active_object
    body.name = "CupBody"
    mat_body = make_material("CupBody", (0.55, 0.27, 0.07))  # коричневый
    body.data.materials.append(mat_body)

    # Внутренность "кофе" (диск сверху)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=CUP_RADIUS_TOP - 0.005,
        depth=0.006,
        location=(0, 0, CUP_HEIGHT - 0.003)
    )
    coffee = bpy.context.active_object
    coffee.name = "Coffee"
    mat_coffee = make_material("Coffee", (0.15, 0.08, 0.04))
    coffee.data.materials.append(mat_coffee)

    # Край стаканчика (торус или тонкий цилиндр)
    bpy.ops.mesh.primitive_torus_add(
        major_radius=CUP_RADIUS_TOP + 0.002,
        minor_radius=RIM_HEIGHT / 2,
        location=(0, 0, CUP_HEIGHT)
    )
    rim = bpy.context.active_object
    rim.name = "Rim"
    mat_rim = make_material("Rim", (0.95, 0.95, 0.9))
    rim.data.materials.append(mat_rim)

    # Собираем в один объект (опционально: можно оставить разнесёнными)
    bpy.ops.object.select_all(action='DESELECT')
    body.select_set(True)
    coffee.select_set(True)
    rim.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.join()
    cup = bpy.context.active_object
    cup.name = "CoffeeCup"
    return cup

# ═══════════════════════════════════════════════════════════════════════════
#  Экспорт в GLB
# ═══════════════════════════════════════════════════════════════════════════
def export_glb(path):
    path = os.path.abspath(os.path.expanduser(path))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(
        filepath=path,
        export_format='GLB',
        use_selection=True,
        export_apply=True,
        export_lights=False,
        export_cameras=False,
    )
    print("Exported:", path)

# ═══════════════════════════════════════════════════════════════════════════
#  Главная последовательность
# ═══════════════════════════════════════════════════════════════════════════
def main():
    clear_scene()
    cup = create_cup()
    export_glb(EXPORT_PATH)
    print("Готово: стаканчик создан и экспортирован в", EXPORT_PATH)
    print("В A-Frame используй: <a-entity gltf-model=\"url(assets/coffee_cup.glb)\" scale=\"1 1 1\"></a-entity>")

if __name__ == "__main__":
    main()
