# -*- coding: utf-8 -*-
"""
Build system for 'Green Patrol' (Оптимизированная версия с полной русификацией).
1. Собирает проект через goboscript build -> green_patrol_optimized.sb3
2. Русифицирует project.json:
   - Названия всех спрайтов (targets)
   - Названия всех глобальных и локальных переменных (variables)
   - Названия всех списков (lists)
   - Названия всех сообщений (broadcasts)
   - Названия всех костюмов и фонов (costumes/backdrops)
   - Названия всех пользовательских блоков/функций (custom procedures)
   - Все ссылки в блоках (сенсоры касания, переключение костюмов, выбор переменных)
3. Добавляет в project.json нативные блоки-заметки (Workspace Comments)
4. Регистрирует расширение 'pen' для мгновенной совместимости со Scratch Desktop
5. Оставляет строго ОДИН итоговый файл: green_patrol_optimized.sb3
"""

import os
import sys
import subprocess
import zipfile
import json
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FINAL_SB3 = os.path.join(SCRIPT_DIR, "green_patrol_optimized.sb3")

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
    for target in project_json.get("targets", []):
        for var_id, var_info in target.get("variables", {}).items():
            if var_info[0] in VAR_NAMES:
                var_info[0] = VAR_NAMES[var_info[0]]
        for list_id, list_info in target.get("lists", {}).items():
            if list_info[0] in VAR_NAMES:
                list_info[0] = VAR_NAMES[list_info[0]]

    # 3. Переименование сообщений (broadcasts) на Сцене
    stage = [t for t in project_json.get("targets", []) if t.get("isStage")][0]
    for bc_id, bc_name in list(stage.get("broadcasts", {}).items()):
        if bc_name in BROADCAST_NAMES:
            stage["broadcasts"][bc_id] = BROADCAST_NAMES[bc_name]

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
                    if f_key == "VARIABLE" and val_name in VAR_NAMES:
                        f_val[0] = VAR_NAMES[val_name]
                    elif f_key == "LIST" and val_name in VAR_NAMES:
                        f_val[0] = VAR_NAMES[val_name]
                    elif f_key == "BROADCAST_OPTION" and val_name in BROADCAST_NAMES:
                        f_val[0] = BROADCAST_NAMES[val_name]
                    elif f_key in ("COSTUME", "BACKDROP") and val_name in COSTUME_NAMES:
                        f_val[0] = COSTUME_NAMES[val_name]
                    elif f_key == "TOUCHINGOBJECTMENU" and val_name in SPRITE_NAMES:
                        f_val[0] = SPRITE_NAMES[val_name]

            # Входы блоков (inputs)
            inputs = block.get("inputs", {})
            for iname, ival in inputs.items():
                if isinstance(ival, list) and len(ival) >= 2 and isinstance(ival[1], list):
                    item = ival[1]
                    if len(item) >= 2 and item[0] in (12, 13) and item[1] in VAR_NAMES:
                        item[1] = VAR_NAMES[item[1]]
                    if len(item) >= 2 and item[0] == 11 and item[1] in BROADCAST_NAMES:
                        item[1] = BROADCAST_NAMES[item[1]]

    return project_json

def main():
    print("=" * 60)
    print(" 1. СБОРКА GOBOSCRIPT -> green_patrol_optimized.sb3")
    print("=" * 60)
    t0 = time.time()
    res = subprocess.run(["goboscript", "build", "-o", FINAL_SB3], cwd=SCRIPT_DIR, capture_output=True, text=True)
    if res.returncode != 0:
        print("[ОШИБКА КОМПИЛЯЦИИ]:")
        print(res.stdout)
        print(res.stderr)
        sys.exit(1)
    
    dt = time.time() - t0
    print(f"[+] Компиляция завершена за {dt:.2f} сек.")

    # Удаляем устаревшие файлы .sb3, чтобы остался строго ОДИН проект
    for old_name in ["green_patrol_opt.sb3", "task_final_opt.sb3", "zeleny_patrul_opt.sb3", "green-patrol.sb3", "test_ru.sb3"]:
        old_path = os.path.join(SCRIPT_DIR, old_name)
        if os.path.exists(old_path):
            try:
                os.remove(old_path)
            except Exception:
                pass

    print("\n" + "=" * 60)
    print(" 2. РУСИФИКАЦИЯ ЭЛЕМЕНТОВ И ДОБАВЛЕНИЕ БЛОКОВ-ЗАМЕТОК")
    print("=" * 60)

    temp_sb3 = os.path.join(SCRIPT_DIR, "temp_build.sb3")
    
    with zipfile.ZipFile(FINAL_SB3, "r") as zin:
        project_json = json.loads(zin.read("project.json").decode("utf-8"))
        
        # Гарантируем регистрацию расширения 'pen' для совместимости со Scratch Desktop
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

        # Перепаковываем архив с обновленным project.json
        with zipfile.ZipFile(temp_sb3, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == "project.json":
                    zout.writestr("project.json", json.dumps(project_json, ensure_ascii=False, indent=2))
                else:
                    zout.writestr(item, zin.read(item.filename))

    os.replace(temp_sb3, FINAL_SB3)
    size_kb = os.path.getsize(FINAL_SB3) / 1024

    print("\n" + "=" * 60)
    print(f" [УСПЕХ] Создан единый проект игры: green_patrol_optimized.sb3")
    print(f" Размер файла: {size_kb:.1f} КБ")
    print(f" Всего добавлено блоков-заметок: {added_count}")
    print("=" * 60)

if __name__ == "__main__":
    main()
