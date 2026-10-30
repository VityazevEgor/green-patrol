# -*- coding: utf-8 -*-
"""
Build system for 'Green Patrol'.
Создаёт две версии проекта:
1. green_patrol_optimized.sb3 — оригинальная версия, скомпилированная через goboscript без перевода.
2. ru_green_patrol_optimized.sb3 — русифицированная версия с полным переводом всех переменных,
   списков, сообщений, спрайтов, костюмов, функций и добавлением блоков-заметок (Workspace Comments).
"""

import os
import sys
import subprocess
import zipfile
import json
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ORIGINAL_SB3 = os.path.join(SCRIPT_DIR, "green_patrol_optimized.sb3")
RU_SB3 = os.path.join(SCRIPT_DIR, "ru_green_patrol_optimized.sb3")

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# --- СЛОВАРИ РУСИФИКАЦИИ ---

SPRITE_NAMES = {
    # Примечание: Согласно спецификации sb3_schema имя сцены (isStage: True) строго обязано быть "Stage".
    # В интерфейсе самого Скретча оно автоматически отображается на языке интерфейса ("Сцена").
    "snake_head": "Голова змейки",
    "snake_body": "Тело змейки",
    "trash": "Мусор",
    "bin": "Мусорная корзина",
    "grid": "Игровое поле",
    "score_d1": "Десятки счёта",
    "score_d2": "Единицы счёта",
    "score_label": "Надпись Счёт",
    "btn_start": "Кнопка Старт",
    "btn_settings": "Кнопка Настройки",
    "btn_close": "Кнопка Закрыть",
    "btn_restart": "Кнопка Заново",
    "btn_grid": "Кнопка Сетка",
    "loading_spinner": "Индикатор загрузки",
}

VAR_NAMES = {
    # Глобальные переменные
    "score": "счет",
    "game_state": "режим игры",
    "snake_len": "длина змейки",
    "head_x": "голова X",
    "head_y": "голова Y",
    "food_type": "тип мусора",
    "last_eat_x": "съедено X",
    "last_eat_y": "съедено Y",
    "cell_size": "размер клетки",
    # Локальные переменные
    "dir": "направление",
    "next_dir": "следующее направление",
    "chk_idx": "проверка столкновения",
    "seg_id": "номер звена",
    "cur_clones": "число звеньев",
    # Списки
    "hist_x": "история X",
    "hist_y": "история Y",
}

BROADCAST_NAMES = {
    "open_menu": "открыть меню",
    "open_settings": "открыть настройки",
    "start_game": "запустить игру",
    "begin_play": "начать раунд",
    "spawn_food": "создать мусор",
    "spawn_bin": "создать корзину",
    "init_body": "создать тело",
    "update_body": "обновить тело",
    "game_over": "поражение",
    "game_win": "победа",
}

PROCEDURE_NAMES = {
    "draw_field": "нарисовать поле",
    "create_segments": "создать звенья",
    "update_clone_segment": "обновить звено",
    "cleanup_body": "очистить тело",
    "init_history": "начальная история",
    "step_head": "шаг головы",
    "check_self_collision": "проверить столкновение",
    "handle_death": "анимация гибели",
    "record_history": "записать историю",
    "check_trash_pickup": "проверить мусор",
    "check_bin_penalty": "проверить корзину",
}

COSTUME_NAMES = {
    # Фоны сцены
    "cover": "Заставка",
    "menu": "Меню",
    "settings": "Настройки",
    "loading": "Загрузка",
    "game_20": "Игра 20 px",
    "game_30": "Игра 30 px",
    "win": "Победа",
    "lose": "Поражение",
    # Игровое поле
    "tile_light": "Светлая клетка",
    "tile_dark": "Тёмная клетка",
    # Мусор
    "trash_1": "Жестяная банка",
    "trash_2": "Пластиковая бутылка",
    "trash_3": "Батарейка",
    # Корзина
    "bin": "Корзина",
    # Голова змейки
    "head_1": "Голова обычная",
    "head_2": "Голова с языком",
    # Тело змейки
    "segment_1": "Звено зелёное",
    "segment_2": "Звено бирюзовое",
    "segment_3": "Звено изумрудное",
    # Загрузка
    "sprout_1": "Росток 1",
    "sprout_2": "Росток 2",
    "sprout_3": "Росток 3",
    "sprout_4": "Росток 4",
    # Кнопки
    "btn_start": "Кнопка Старт",
    "btn_settings": "Кнопка Настройки",
    "btn_close": "Кнопка Закрыть",
    "btn_restart": "Кнопка Заново",
    "score_label": "Табличка Счёт",
    "grid_20": "Кнопка 20 px",
    "grid_30": "Кнопка 30 px",
    # Цифры
    "digit_0": "Цифра 0",
    "digit_1": "Цифра 1",
    "digit_2": "Цифра 2",
    "digit_3": "Цифра 3",
    "digit_4": "Цифра 4",
    "digit_5": "Цифра 5",
    "digit_6": "Цифра 6",
    "digit_7": "Цифра 7",
    "digit_8": "Цифра 8",
    "digit_9": "Цифра 9",
}

# Описания переменных для добавления в виде блоков-заметок в Скретче
VARIABLE_NOTES = {
    "Stage": (
        "📌 ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ И СПИСКИ (ДЛЯ ВСЕХ СПРАЙТОВ):\n\n"
        "• счет — текущий счет игрока (баллы). Цель: набрать 50 баллов.\n"
        "• режим игры — состояние игры: 'заставка', 'меню', 'настройки', 'загрузка', 'игра', 'победа', 'поражение'.\n"
        "• длина змейки — количество звеньев хвоста (стартует с 3).\n"
        "• голова X, голова Y — текущие координаты головы змейки на сетке поля.\n"
        "• тип мусора — тип появившегося предмета: 1 (банка, +1), 2 (бутылка, +2), 3 (батарейка, +3).\n"
        "• съедено X, съедено Y — координаты точки проглатывания мусора (для эффекта прохождения кома по телу).\n"
        "• размер клетки — размерность сетки поля: 20 px или 30 px (выбирается в настройках).\n"
        "• история X, история Y (списки) — история шагов головы и позиций для звеньев хвоста."
    ),
    "Голова змейки": (
        "📌 ПЕРЕМЕННЫЕ СПРАЙТА «ГОЛОВА ЗМЕЙКИ»:\n\n"
        "• направление — текущее направление движения в градусах Scratch (90: вправо, -90: влево, 0: вверх, 180: вниз).\n"
        "• следующее направление — буфер следующего направления, задаваемый стрелками клавиатуры.\n"
        "• проверка столкновения — счетчик цикла проверки удара головы о звенья своего хвоста."
    ),
    "Тело змейки": (
        "📌 ПЕРЕМЕННЫЕ СПРАЙТА «ТЕЛО ЗМЕЙКИ»:\n\n"
        "• номер звена — порядковый номер звена хвоста (локальная переменная клона: 1, 2, 3...; у оригинала равна 0).\n"
        "• число звеньев — общее количество созданных клонов звеньев хвоста."
    ),
    "Мусор": (
        "📌 СПРАЙТ «МУСОР» (БЕЗ ПЕРЕМЕННЫХ):\n\n"
        "• Появляется в случайной точке сетки: goto (random(...) * 20 + 10).\n"
        "• Костюм выбирается напрямую по типу мусора: switch_costume (тип мусора)."
    ),
    "Мусорная корзина": (
        "📌 СПРАЙТ «МУСОРНАЯ КОРЗИНА» (БЕЗ ПЕРЕМЕННЫХ):\n\n"
        "• Координаты появления вычисляются напрямую в блоке goto."
    ),
    "Десятки счёта": (
        "📌 СПРАЙТ «ЦИФРА ДЕСЯТКОВ» (БЕЗ ПЕРЕМЕННЫХ):\n\n"
        "• Костюм цифры вычисляется напрямую из счета: switch_costume ((счет - (счет % 10)) / 10 + 1)."
    ),
    "Единицы счёта": (
        "📌 СПРАЙТ «ЦИФРА ЕДИНИЦ» (БЕЗ ПЕРЕМЕННЫХ):\n\n"
        "• Костюм цифры вычисляется напрямую из счета: switch_costume (счет % 10 + 1)."
    ),
    "Кнопка Сетка": (
        "📌 СПРАЙТ «КНОПКА СЕТКА»:\n\n"
        "• Переключает размерность сетки поля (20 px / 30 px) в окне настроек.\n"
        "• При клике переключает значение переменной «размер клетки» и свой костюм.\n"
        "• Сетка и все объекты (змейка, еда, корзина) автоматически масштабируются."
    ),
    "Игровое поле": (
        "📌 СПРАЙТ «ИГРОВОЕ ПОЛЕ» (БЕЗ ПЕРЕМЕННЫХ):\n\n"
        "• Процедура «нарисовать поле» работает без обновления экрана (warp: true) — 432 клетки отрисовываются за 0.01 сек.\n"
        "• Переменные не требуются: используются встроенные координаты спрайта (x, y) и переключение «следующий костюм»."
    ),
}

def localize_project(project_json):
    """Выполняет полную русификацию всех сущностей в project.json"""
    # 1. Переименование спрайтов и сцены
    for target in project_json.get("targets", []):
        old_name = target.get("name")
        if old_name in SPRITE_NAMES:
            target["name"] = SPRITE_NAMES[old_name]

    # 2. Переименование переменных и списков в заголовках
    # В Scratch 3 для корректной работы имя и ID переменной/списка должны совпадать
    for target in project_json.get("targets", []):
        if "variables" in target and isinstance(target["variables"], dict):
            new_variables = {}
            for var_id, var_info in target["variables"].items():
                old_name = var_info[0]
                new_name = VAR_NAMES.get(old_name, VAR_NAMES.get(var_id, old_name))
                new_id = VAR_NAMES.get(var_id, new_name)
                new_info = [new_name] + var_info[1:]
                new_variables[new_id] = new_info
            target["variables"] = new_variables

        if "lists" in target and isinstance(target["lists"], dict):
            new_lists = {}
            for list_id, list_info in target["lists"].items():
                old_name = list_info[0]
                new_name = VAR_NAMES.get(old_name, VAR_NAMES.get(list_id, old_name))
                new_id = VAR_NAMES.get(list_id, new_name)
                new_info = [new_name] + list_info[1:]
                new_lists[new_id] = new_info
            target["lists"] = new_lists

    # 3. Переименование сообщений (broadcasts) во всех целях (включая Сцену)
    # В Scratch 3 для корректной работы имя и ID сообщения должны совпадать
    for target in project_json.get("targets", []):
        if "broadcasts" in target and isinstance(target["broadcasts"], dict):
            new_broadcasts = {}
            for bc_id, bc_name in target["broadcasts"].items():
                target_name = BROADCAST_NAMES.get(bc_name, BROADCAST_NAMES.get(bc_id, bc_name))
                new_broadcasts[target_name] = target_name
            target["broadcasts"] = new_broadcasts

    # 4. Переименование костюмов и фонов в target.costumes
    for target in project_json.get("targets", []):
        for costume in target.get("costumes", []):
            c_name = costume.get("name")
            if c_name in COSTUME_NAMES:
                costume["name"] = COSTUME_NAMES[c_name]

    # 5. Обновление всех блоков во всех спрайтах
    for target in project_json.get("targets", []):
        for block_id, block in target.get("blocks", {}).items():
            if not isinstance(block, dict):
                continue
            
            opcode = block.get("opcode", "")

            # Пользовательские процедуры: прототипы и вызовы
            if opcode in ("procedures_prototype", "procedures_call"):
                mutation = block.get("mutation", {})
                proccode = mutation.get("proccode")
                if proccode in PROCEDURE_NAMES:
                    mutation["proccode"] = PROCEDURE_NAMES[proccode]

            # Поля блоков (fields)
            fields = block.get("fields", {})
            for f_key, f_val in fields.items():
                if isinstance(f_val, list) and len(f_val) >= 1:
                    val_name = f_val[0]
                    if f_key == "VARIABLE":
                        if val_name in VAR_NAMES:
                            f_val[0] = VAR_NAMES[val_name]
                        if len(f_val) > 1 and f_val[1] in VAR_NAMES:
                            f_val[1] = VAR_NAMES[f_val[1]]
                    elif f_key == "LIST":
                        if val_name in VAR_NAMES:
                            f_val[0] = VAR_NAMES[val_name]
                        if len(f_val) > 1 and f_val[1] in VAR_NAMES:
                            f_val[1] = VAR_NAMES[f_val[1]]
                    elif f_key == "BROADCAST_OPTION":
                        if val_name in BROADCAST_NAMES:
                            f_val[0] = BROADCAST_NAMES[val_name]
                        if len(f_val) > 1 and f_val[1] in BROADCAST_NAMES:
                            f_val[1] = BROADCAST_NAMES[f_val[1]]
                    elif f_key in ("COSTUME", "BACKDROP") and val_name in COSTUME_NAMES:
                        f_val[0] = COSTUME_NAMES[val_name]
                    elif f_key == "TOUCHINGOBJECTMENU" and val_name in SPRITE_NAMES:
                        f_val[0] = SPRITE_NAMES[val_name]

            # Входы блоков (inputs)
            inputs = block.get("inputs", {})
            for iname, ival in inputs.items():
                if isinstance(ival, list):
                    for sub_idx in (1, 2):
                        if len(ival) > sub_idx and isinstance(ival[sub_idx], list):
                            sub_item = ival[sub_idx]
                            if len(sub_item) >= 2 and sub_item[0] in (12, 13):
                                if sub_item[1] in VAR_NAMES:
                                    sub_item[1] = VAR_NAMES[sub_item[1]]
                                if len(sub_item) >= 3 and sub_item[2] in VAR_NAMES:
                                    sub_item[2] = VAR_NAMES[sub_item[2]]
                            if len(sub_item) >= 2 and sub_item[0] == 11:
                                if sub_item[1] in BROADCAST_NAMES:
                                    sub_item[1] = BROADCAST_NAMES[sub_item[1]]
                                if len(sub_item) >= 3 and sub_item[2] in BROADCAST_NAMES:
                                    sub_item[2] = BROADCAST_NAMES[sub_item[2]]

    return project_json

def ensure_pen_extension(sb3_path):
    """Гарантирует регистрацию расширения 'pen' для совместимости со Scratch Desktop."""
    temp_sb3 = sb3_path + ".tmp_pen"
    needs_update = False
    with zipfile.ZipFile(sb3_path, "r") as zin:
        project_json = json.loads(zin.read("project.json").decode("utf-8"))
        if "extensions" not in project_json or not isinstance(project_json["extensions"], list):
            project_json["extensions"] = []
        if "pen" not in project_json["extensions"]:
            project_json["extensions"].append("pen")
            needs_update = True
            with zipfile.ZipFile(temp_sb3, "w", zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    if item.filename == "project.json":
                        zout.writestr("project.json", json.dumps(project_json, ensure_ascii=False, indent=2))
                    else:
                        zout.writestr(item, zin.read(item.filename))
    if needs_update:
        os.replace(temp_sb3, sb3_path)

def main():
    print("=" * 60)
    print(" 1. СБОРКА GOBOSCRIPT -> green_patrol_optimized.sb3")
    print("=" * 60)
    t0 = time.time()
    res = subprocess.run(["goboscript", "build", "-o", ORIGINAL_SB3], cwd=SCRIPT_DIR, capture_output=True, text=True)
    if res.returncode != 0:
        print("[ОШИБКА КОМПИЛЯЦИИ]:")
        print(res.stdout)
        print(res.stderr)
        sys.exit(1)
    
    # Регистрация pen для Scratch Desktop в оригинальном проекте
    ensure_pen_extension(ORIGINAL_SB3)
    dt = time.time() - t0
    orig_kb = os.path.getsize(ORIGINAL_SB3) / 1024
    print(f"[+] Оригинальный проект собран: green_patrol_optimized.sb3 ({orig_kb:.1f} КБ) за {dt:.2f} сек.")

    # Удаляем устаревшие файлы .sb3
    for old_name in ["green_patrol_opt.sb3", "task_final_opt.sb3", "zeleny_patrul_opt.sb3", "green-patrol.sb3", "test_ru.sb3"]:
        old_path = os.path.join(SCRIPT_DIR, old_name)
        if os.path.exists(old_path):
            try:
                os.remove(old_path)
            except Exception:
                pass

    print("\n" + "=" * 60)
    print(" 2. РУСИФИКАЦИЯ ЭЛЕМЕНТОВ -> ru_green_patrol_optimized.sb3")
    print("=" * 60)

    temp_sb3 = os.path.join(SCRIPT_DIR, "temp_build.sb3")
    
    with zipfile.ZipFile(ORIGINAL_SB3, "r") as zin:
        project_json = json.loads(zin.read("project.json").decode("utf-8"))

        # Гарантируем регистрацию pen
        if "extensions" not in project_json or not isinstance(project_json["extensions"], list):
            project_json["extensions"] = []
        if "pen" not in project_json["extensions"]:
            project_json["extensions"].append("pen")

        # Полная русификация всех элементов игры
        project_json = localize_project(project_json)
        print("[+] Русификация успешно применена ко всем спрайтам, переменным, спискам, костюмам и функциям.")

        # Добавляем заметки к каждому спрайту и сцене
        added_count = 0
        for target in project_json.get("targets", []):
            t_name = target.get("name")
            if t_name in VARIABLE_NOTES:
                if "comments" not in target or not isinstance(target["comments"], dict):
                    target["comments"] = {}
                
                comment_id = f"note_vars_{target.get('id', t_name)}"
                target["comments"][comment_id] = {
                    "blockId": None,
                    "x": 380,
                    "y": 60,
                    "width": 380,
                    "height": 260,
                    "minimized": False,
                    "text": VARIABLE_NOTES[t_name]
                }
                added_count += 1
                print(f"[+] Заметка добавлена в спрайт: {t_name}")

        # Сохраняем русскоязычную версию
        with zipfile.ZipFile(temp_sb3, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == "project.json":
                    zout.writestr("project.json", json.dumps(project_json, ensure_ascii=False, indent=2))
                else:
                    zout.writestr(item, zin.read(item.filename))

    os.replace(temp_sb3, RU_SB3)
    ru_kb = os.path.getsize(RU_SB3) / 1024

    print("\n" + "=" * 60)
    print(" [УСПЕХ] Собраны две версии игры:")
    print(f" 1. Оригинал (goboscript):       green_patrol_optimized.sb3    ({orig_kb:.1f} КБ)")
    print(f" 2. Русифицированная (с заметками): ru_green_patrol_optimized.sb3 ({ru_kb:.1f} КБ)")
    print("=" * 60)

if __name__ == "__main__":
    main()
