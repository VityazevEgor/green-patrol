# -*- coding: utf-8 -*-
"""
Build system for 'Green Patrol' (Оптимизированная версия).
1. Собирает проект через goboscript build -> green_patrol_optimized.sb3
2. Добавляет в project.json нативные блоки-заметки (Scratch Workspace Comments)
   с подробным описанием всех переменных на русском языке.
3. Оставляет строго ОДИН итоговый файл: green_patrol_optimized.sb3
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

# Описания переменных для добавления в виде блоков-заметок в Скретче
VARIABLE_NOTES = {
    "Stage": (
        "📌 ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ И СПИСКИ (ДЛЯ ВСЕХ СПРАЙТОВ):\n\n"
        "• score — текущий счет игрока (баллы). Цель: набрать 50 баллов.\n"
        "• game_state — режим игры: 'заставка', 'меню', 'настройки', 'загрузка', 'игра', 'победа', 'поражение'.\n"
        "• snake_len — длина змейки (количество звеньев хвоста). Стартует с 3.\n"
        "• head_x — координата X головы змейки на сетке поля.\n"
        "• head_y — координата Y головы змейки на сетке поля.\n"
        "• food_type — тип мусора: 1 (банка, +1), 2 (бутылка, +2), 3 (батарейка, +3).\n"
        "• last_eat_x — координата X точки, где съеден мусор (для анимации проглатывания).\n"
        "• last_eat_y — координата Y точки, где съеден мусор.\n"
        "• hist_x (список) — история координат X головы и звеньев змейки.\n"
        "• hist_y (список) — история координат Y головы и звеньев змейки."
    ),
    "snake_head": (
        "📌 ПЕРЕМЕННЫЕ СПРАЙТА «ГОЛОВА ЗМЕЙКИ»:\n\n"
        "• dir — текущее направление движения в градусах Scratch (90: вправо, -90: влево, 0: вверх, 180: вниз).\n"
        "• next_dir — буфер следующего направления, задаваемый стрелками клавиатуры.\n"
        "• chk_idx — счетчик цикла проверки столкновения головы со своим хвостом."
    ),
    "snake_body": (
        "📌 ПЕРЕМЕННЫЕ СПРАЙТА «ТЕЛО ЗМЕЙКИ»:\n\n"
        "• seg_id — номер звена хвоста (локальная переменная клона: 1, 2, 3...; у оригинала равна 0).\n"
        "• cur_clones — общее количество созданных клонов звеньев."
    ),
    "trash": (
        "📌 СПРАЙТ «МУСОР» (БЕЗ ПЕРЕМЕННЫХ):\n\n"
        "• Появляется в случайной точке сетки: goto (random(...) * 20 + 10).\n"
        "• Костюм выбирается напрямую по типу мусора: switch_costume food_type."
    ),
    "bin": (
        "📌 СПРАЙТ «МУСОРНАЯ КОРЗИНА» (БЕЗ ПЕРЕМЕННЫХ):\n\n"
        "• Координаты появления вычисляются напрямую в блоке goto."
    ),
    "score_d1": (
        "📌 СПРАЙТ «ЦИФРА ДЕСЯТКОВ» (БЕЗ ПЕРЕМЕННЫХ):\n\n"
        "• Костюм цифры вычисляется напрямую из счета: switch_costume ((score - (score % 10)) / 10 + 1)."
    ),
    "score_d2": (
        "📌 СПРАЙТ «ЦИФРА ЕДИНИЦ» (БЕЗ ПЕРЕМЕННЫХ):\n\n"
        "• Костюм цифры вычисляется напрямую из счета: switch_costume (score % 10 + 1)."
    ),
    "grid": (
        "📌 СПРАЙТ «ИГРОВОЕ ПОЛЕ» (БЕЗ ЕДИНОЙ ПЕРЕМЕННОЙ):\n\n"
        "• Процедура draw_field работает без обновления экрана (warp: true) — 432 клетки отрисовываются мгновенно за 0.01 сек.\n"
        "• Переменные не требуются: используются встроенные координаты спрайта (x, y) и переключение «следующий костюм»."
    ),
}

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
    for old_name in ["green_patrol_opt.sb3", "task_final_opt.sb3", "zeleny_patrul_opt.sb3", "green-patrol.sb3"]:
        old_path = os.path.join(SCRIPT_DIR, old_name)
        if os.path.exists(old_path):
            try:
                os.remove(old_path)
            except Exception:
                pass

    print("\n" + "=" * 60)
    print(" 2. ДОБАВЛЕНИЕ БЛОКОВ-ЗАМЕТОК С ОПИСАНИЕМ ПЕРЕМЕННЫХ")
    print("=" * 60)

    temp_sb3 = os.path.join(SCRIPT_DIR, "temp_build.sb3")
    
    with zipfile.ZipFile(FINAL_SB3, "r") as zin:
        project_json = json.loads(zin.read("project.json").decode("utf-8"))
        
        # Гарантируем регистрацию расширения 'pen' для совместимости со Scratch Desktop
        if "extensions" not in project_json or not isinstance(project_json["extensions"], list):
            project_json["extensions"] = []
        if "pen" not in project_json["extensions"]:
            project_json["extensions"].append("pen")

        # Добавляем заметки к каждому спрайту и сцене
        added_count = 0
        for target in project_json.get("targets", []):
            t_name = target.get("name")
            if t_name in VARIABLE_NOTES:
                if "comments" not in target or not isinstance(target["comments"], dict):
                    target["comments"] = {}
                
                comment_id = f"note_vars_{t_name}"
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
