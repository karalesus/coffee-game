"""
BLENDER: создание 3D-модели студентки для A-Frame
─────────────────────────────────────────────────
КАК ИСПОЛЬЗОВАТЬ:
  1) Открой Blender (3.x или 4.x / 5.x).
  2) Scripting → Open → выбери этот файл.
  3) Нажми Run Script (▶ или Alt+P).
  4) В папке assets/ появится student.glb.
  В A-Frame: <a-entity gltf-model="url(assets/student.glb)"></a-entity>
"""

import bpy
import os
import math

# ── Путь экспорта (папка assets рядом со скриптом) ──────────────────────────
try:
    script_path = bpy.context.space_data.text.filepath
    script_dir = os.path.dirname(os.path.abspath(script_path)) if script_path else os.path.expanduser("~")
except Exception:
    script_dir = os.path.expanduser("~")

EXPORT_PATH = os.path.join(script_dir, "assets", "student.glb")

# ── Очистка сцены ────────────────────────────────────────────────────────────
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in list(bpy.data.meshes):
        bpy.data.meshes.remove(block)
    for block in list(bpy.data.materials):
        bpy.data.materials.remove(block)

# ── Материал ─────────────────────────────────────────────────────────────────
def mat(name, color, roughness=0.7, metallic=0.0):
    m = bpy.data.materials.new(name=name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return m

# ── Вспомогательная функция: добавить объект и назначить материал ────────────
def add(obj, material):
    obj.data.materials.append(material)
    return obj

# ── Создание персонажа ───────────────────────────────────────────────────────
def create_student():
    parts = []

    # Ноги (левая и правая)
    for x_offset in (-0.06, 0.06):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.055, depth=0.35, location=(x_offset, 0, 0.175))
        leg = bpy.context.active_object
        leg.name = "Leg"
        add(leg, mat("Jeans", (0.1, 0.18, 0.45)))
        parts.append(leg)

    # Кроссовки
    for x_offset in (-0.06, 0.06):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x_offset, 0.03, -0.01))
        shoe = bpy.context.active_object
        shoe.scale = (0.065, 0.09, 0.04)
        bpy.ops.object.transform_apply(scale=True)
        shoe.name = "Shoe"
        add(shoe, mat("Shoes", (0.08, 0.08, 0.08)))
        parts.append(shoe)

    # Туловище
    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.32, location=(0, 0, 0.51))
    torso = bpy.context.active_object
    torso.name = "Torso"
    add(torso, mat("Hoodie", (0.55, 0.12, 0.12)))  # красная толстовка
    parts.append(torso)

    # Рюкзак (за спиной)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.16, 0.52))
    bag = bpy.context.active_object
    bag.scale = (0.14, 0.07, 0.18)
    bpy.ops.object.transform_apply(scale=True)
    bag.name = "Backpack"
    add(bag, mat("Backpack", (0.15, 0.35, 0.55)))  # синий рюкзак
    parts.append(bag)

    # Шея
    bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.07, location=(0, 0, 0.70))
    neck = bpy.context.active_object
    neck.name = "Neck"
    add(neck, mat("Skin", (0.88, 0.68, 0.50)))
    parts.append(neck)

    # Голова
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.11, location=(0, 0, 0.87))
    head = bpy.context.active_object
    head.name = "Head"
    add(head, mat("HeadSkin", (0.88, 0.68, 0.50)))
    parts.append(head)

    # Волосы (приплюснутая сфера сверху)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.115, location=(0, 0, 0.91))
    hair = bpy.context.active_object
    hair.scale = (1.0, 1.0, 0.55)
    bpy.ops.object.transform_apply(scale=True)
    hair.name = "Hair"
    add(hair, mat("Hair", (0.15, 0.08, 0.04)))  # тёмно-коричневые волосы
    parts.append(hair)

    # Глаза (два маленьких шара)
    for x_offset in (-0.04, 0.04):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.018, location=(x_offset, 0.10, 0.88))
        eye = bpy.context.active_object
        eye.name = "Eye"
        add(eye, mat("Eyes", (0.05, 0.05, 0.05)))
        parts.append(eye)

    # Руки (левая и правая)
    for x_offset, rot in ((-0.19, math.radians(15)), (0.19, math.radians(-15))):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.28, location=(x_offset, 0, 0.50))
        arm = bpy.context.active_object
        arm.rotation_euler = (0, rot, 0)
        bpy.ops.object.transform_apply(rotation=True)
        arm.name = "Arm"
        add(arm, mat("ArmSleeve", (0.50, 0.10, 0.10)))
        parts.append(arm)

    # Кисти рук
    for x_offset in (-0.21, 0.21):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.04, location=(x_offset, 0, 0.37))
        hand = bpy.context.active_object
        hand.name = "Hand"
        add(hand, mat("HandSkin", (0.88, 0.68, 0.50)))
        parts.append(hand)

    # Кофе в руке (маленький стаканчик)
    bpy.ops.mesh.primitive_cone_add(radius1=0.025, radius2=0.032, depth=0.07, location=(0.21, 0, 0.30))
    cup = bpy.context.active_object
    cup.name = "CupInHand"
    add(cup, mat("CupColor", (0.95, 0.90, 0.80)))
    parts.append(cup)

    # Надпись на толстовке (маленький плоский куб — "нашивка")
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.125, 0.53))
    badge = bpy.context.active_object
    badge.scale = (0.08, 0.005, 0.04)
    bpy.ops.object.transform_apply(scale=True)
    badge.name = "Badge"
    add(badge, mat("BadgeColor", (1.0, 0.85, 0.1)))  # жёлтый значок
    parts.append(badge)

    # Объединяем все части в один объект
    bpy.ops.object.select_all(action='DESELECT')
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()

    student = bpy.context.active_object
    student.name = "Student"

    # Центрируем по X/Y, основание у Z=0
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    student.location = (0, 0, 0)
    bpy.ops.object.transform_apply(location=True)

    return student

# ── Экспорт GLB ──────────────────────────────────────────────────────────────
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
    print("Экспортировано:", path)

# ── Запуск ───────────────────────────────────────────────────────────────────
def main():
    clear_scene()
    create_student()
    export_glb(EXPORT_PATH)
    print("Готово! Файл:", EXPORT_PATH)
    print("В A-Frame: <a-entity gltf-model=\"url(assets/student.glb)\" scale=\"1 1 1\"></a-entity>")

main()
