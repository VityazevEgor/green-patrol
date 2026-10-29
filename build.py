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
        "• dir_x — текущее направление по X (1: вправо, -1: влево, 0: нет движения).\n"
        "• dir_y — текущее направление по Y (1: вверх, -1: вниз, 0: нет движения).\n"
        "• next_dir_x — следующее направление по X (буфер стрелок клавиатуры).\n"
        "• next_dir_y — следующее направление по Y (буфер стрелок клавиатуры).\n"
        "• new_head_x — расчетная координата X для следующего шага головы.\n"
        "• new_head_y — расчетная координата Y для следующего шага головы.\n"
        "• chk_idx — счетчик цикла проверки столкновения головы с телом.\n"
        "• init_i — счетчик при начальном построении хвоста змейки.\n"
        "• r — случайное число (1..4) для выбора направления на старте.\n"
        "• is_dead — флаг гибели ('да' / 'нет') при ударе о свой хвост."
    ),
    "snake_body": (
        "📌 ПЕРЕМЕННЫЕ СПРАЙТА «ТЕЛО ЗМЕЙКИ»:\n\n"
        "• seg_id — порядковый номер звена змейки (1, 2, 3...).\n"
        "• cur_clones — общее количество созданных клонов звеньев.\n"
        "• is_clone — флаг ('да' / 'нет'), отличающий клон от оригинального спрайта.\n"
        "• cost_idx — номер костюма (1..3) для чередования цветов звеньев.\n"
        "• p_idx — индекс в списках hist_x/hist_y для получения координат звена."
    ),
    "trash": (
        "📌 ПЕРЕМЕННЫЕ СПРАЙТА «МУСОР»:\n\n"
        "• fx — случайная координата X появления мусора (сетка 20 px).\n"
        "• fy — случайная координата Y появления мусора (сетка 20 px)."
    ),
    "bin": (
        "📌 ПЕРЕМЕННЫЕ СПРАЙТА «МУСОРНАЯ КОРЗИНА»:\n\n"
        "• bx — случайная координата X появления корзины (сетка 20 px).\n"
        "• by — случайная координата Y появления корзины (сетка 20 px)."
    ),
    "score_d1": (
        "📌 ПЕРЕМЕННЫЕ СПРАЙТА «ЦИФРА ДЕСЯТКОВ»:\n\n"
        "• tens — цифра разряда десятков текущего счета: (score / 10) % 10."
    ),
    "score_d2": (
        "📌 ПЕРЕМЕННЫЕ СПРАЙТА «ЦИФРА ЕДИНИЦ»:\n\n"
        "• units — цифра разряда единиц текущего счета: score % 10."
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
