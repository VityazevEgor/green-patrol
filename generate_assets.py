# -*- coding: utf-8 -*-
import os
import math
import struct
import wave
import random
from vector_text import text_path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
BD_DIR = os.path.join(ASSETS_DIR, "backdrops")
CS_DIR = os.path.join(ASSETS_DIR, "costumes")
SD_DIR = os.path.join(ASSETS_DIR, "sounds")

os.makedirs(BD_DIR, exist_ok=True)
os.makedirs(CS_DIR, exist_ok=True)
os.makedirs(SD_DIR, exist_ok=True)

print("1. Generating Backdrops...")

# 1. COVER (Заставка)
cover_svg = f"""<svg width="480" height="360" viewBox="0 0 480 360" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="cov_sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1b4332"/>
      <stop offset="60%" stop-color="#2d6a4f"/>
      <stop offset="100%" stop-color="#40916c"/>
    </linearGradient>
    <linearGradient id="cov_panel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#081c15"/>
      <stop offset="100%" stop-color="#1b4332"/>
    </linearGradient>
  </defs>
  <rect width="480" height="360" fill="url(#cov_sky)"/>
  <circle cx="240" cy="180" r="160" fill="#52b788" opacity="0.15"/>
  <circle cx="240" cy="180" r="120" fill="#74c69d" opacity="0.2"/>
  
  <rect x="30" y="25" width="420" height="310" rx="20" fill="url(#cov_panel)" fill-opacity="0.95" stroke="#52b788" stroke-width="3"/>
  
  <g transform="translate(240, 165)">
    <circle cx="0" cy="0" r="45" fill="#1b4332" stroke="#74c69d" stroke-width="3"/>
    <path d="M-25,10 Q-15,-20 0,-15 Q15,-10 20,-25 Q25,-15 15,10 Q5,25 -10,15 Z" fill="#52b788"/>
    <circle cx="16" cy="-20" r="3" fill="#ffffff"/>
    <circle cx="17" cy="-20" r="1.5" fill="#081c15"/>
    <path d="M22,-22 Q28,-26 31,-24 M28,-26 Q32,-28 34,-30" stroke="#e63946" stroke-width="2" stroke-linecap="round"/>
  </g>
  
  {text_path("ЗЕЛЕНЫЙ ПАТРУЛЬ", 240, 75, 26, fill="#74c69d", align="middle", bold=True)}
  {text_path("Миссия юных экологов по спасению леса", 240, 102, 13, fill="#d8f3dc", align="middle", bold=False)}
  
  {text_path("Команда: Скрэтчерионы", 240, 228, 14, fill="#ffffff", align="middle", bold=True)}
  {text_path("Иванушкин Дмитрий Яковлевич · Витезева Ева Денисовна", 240, 252, 11, fill="#ffffff", align="middle", bold=False)}
  {text_path("Школа №1558", 240, 274, 13, fill="#95d5b2", align="middle", bold=True)}
  {text_path("Нажмите Зеленый флаг для старта проекта", 240, 306, 12, fill="#ffd166", align="middle", bold=True)}
</svg>"""
with open(os.path.join(BD_DIR, "cover.svg"), "w", encoding="utf-8") as f:
    f.write(cover_svg)

# 2. MENU
menu_svg = f"""<svg width="480" height="360" viewBox="0 0 480 360" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="m_sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#40916c"/>
      <stop offset="60%" stop-color="#52b788"/>
      <stop offset="100%" stop-color="#95d5b2"/>
    </linearGradient>
  </defs>
  <rect width="480" height="360" fill="url(#m_sky)"/>
  
  <polygon points="20,280 60,180 100,280" fill="#1b4332" opacity="0.6"/>
  <polygon points="70,290 120,160 170,290" fill="#2d6a4f" opacity="0.6"/>
  <polygon points="310,290 360,160 410,290" fill="#2d6a4f" opacity="0.6"/>
  <polygon points="380,280 420,180 460,280" fill="#1b4332" opacity="0.6"/>
  
  <ellipse cx="240" cy="320" rx="280" ry="100" fill="#1b4332"/>
  <ellipse cx="240" cy="330" rx="250" ry="85" fill="#2d6a4f"/>
  
  <!-- Title Badge centered -->
  <rect x="50" y="35" width="380" height="90" rx="18" fill="#081c15" fill-opacity="0.9" stroke="#74c69d" stroke-width="3"/>
  {text_path("ЗЕЛЕНЫЙ ПАТРУЛЬ", 240, 75, 28, fill="#52b788", align="middle", bold=True)}
  {text_path("Аркадная игра-миссия", 240, 105, 14, fill="#d8f3dc", align="middle", bold=False)}
</svg>"""
with open(os.path.join(BD_DIR, "menu.svg"), "w", encoding="utf-8") as f:
    f.write(menu_svg)

# 3. SETTINGS & RULES
settings_svg = f"""<svg width="480" height="360" viewBox="0 0 480 360" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="s_bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#081c15"/>
      <stop offset="100%" stop-color="#1b4332"/>
    </linearGradient>
  </defs>
  <rect width="480" height="360" fill="url(#s_bg)"/>
  <rect x="20" y="15" width="440" height="330" rx="16" fill="#102d23" stroke="#52b788" stroke-width="2"/>
  
  {text_path("ПРАВИЛА И НАСТРОЙКИ", 240, 48, 20, fill="#74c69d", align="middle", bold=True)}
  
  {text_path("1. Главная цель: набрать 50 баллов и спасти лес", 40, 78, 12.5, fill="#ffffff", align="start", bold=False)}
  {text_path("2. Управление змейкой: клавиши Стрелки (Вверх, Вниз, Влево, Вправо)", 40, 102, 12.5, fill="#ffffff", align="start", bold=False)}
  {text_path("3. Мусор 1 (банка): +1 балл, рост хвоста на 1 сегмент", 40, 126, 12.5, fill="#a7c957", align="start", bold=False)}
  {text_path("4. Мусор 2 (бутылка): +2 балла, рост хвоста на 1 сегмент", 40, 150, 12.5, fill="#38b000", align="start", bold=False)}
  {text_path("5. Мусор 3 (батарейка): +3 балла, рост хвоста на 1 сегмент", 40, 174, 12.5, fill="#ffd166", align="start", bold=False)}
  {text_path("6. Корзина: штраф -1 балл и уменьшение хвоста на 1 сегмент", 40, 198, 12.5, fill="#ff9f1c", align="start", bold=False)}
  {text_path("7. Поражение: столкновение змейки с собственным телом", 40, 222, 12.5, fill="#ff6b6b", align="start", bold=False)}
  {text_path("8. Для возврата в меню нажмите крестик в правом верхнем углу", 40, 246, 11.5, fill="#95d5b2", align="start", bold=True)}

  <!-- Блок настройки сетки -->
  <rect x="35" y="264" width="410" height="64" rx="12" fill="#081c15" fill-opacity="0.8" stroke="#2d6a4f" stroke-width="1.5"/>
  {text_path("Размерность сетки поля:", 55, 292, 13, fill="#d8f3dc", align="start", bold=True)}
  {text_path("20 px (24×18)  |  30 px (16×12)", 55, 312, 11, fill="#74c69d", align="start", bold=False)}
</svg>"""
with open(os.path.join(BD_DIR, "settings.svg"), "w", encoding="utf-8") as f:
    f.write(settings_svg)

# 4. LOADING
loading_svg = f"""<svg width="480" height="360" viewBox="0 0 480 360" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="l_bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1b4332"/>
      <stop offset="100%" stop-color="#2d6a4f"/>
    </linearGradient>
  </defs>
  <rect width="480" height="360" fill="url(#l_bg)"/>
  
  <rect x="50" y="55" width="380" height="250" rx="20" fill="#081c15" fill-opacity="0.95" stroke="#52b788" stroke-width="2.5"/>
  {text_path("ЗАГРУЗКА...", 240, 115, 28, fill="#74c69d", align="middle", bold=True)}
  {text_path("Подготовка лесной поляны к патрулю", 240, 265, 14, fill="#d8f3dc", align="middle", bold=False)}
</svg>"""
with open(os.path.join(BD_DIR, "loading.svg"), "w", encoding="utf-8") as f:
    f.write(loading_svg)

# 5. GAME BACKDROP (Универсальный фон игры, сетка рисуется процедурно спрайтом grid)
game_svg = """<svg width="480" height="360" viewBox="0 0 480 360" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="g_bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#143628"/>
      <stop offset="100%" stop-color="#0b2319"/>
    </linearGradient>
  </defs>
  <rect width="480" height="360" fill="url(#g_bg)"/>
</svg>"""
with open(os.path.join(BD_DIR, "game.svg"), "w", encoding="utf-8") as f:
    f.write(game_svg)

# 7. WIN
win_svg = f"""<svg width="480" height="360" viewBox="0 0 480 360" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="w_bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1b4332"/>
      <stop offset="100%" stop-color="#2d6a4f"/>
    </linearGradient>
  </defs>
  <rect width="480" height="360" fill="url(#w_bg)"/>
  <circle cx="240" cy="180" r="140" fill="#ffd166" opacity="0.15"/>
  
  <rect x="40" y="45" width="400" height="270" rx="20" fill="#081c15" fill-opacity="0.9" stroke="#ffd166" stroke-width="3"/>
  <polygon points="240,85 246,103 265,103 250,114 256,132 240,121 224,132 230,114 215,103 234,103" fill="#ffd166"/>
  
  {text_path("ПОБЕДА!", 240, 170, 36, fill="#ffd166", align="middle", bold=True)}
  {text_path("Лесная поляна полностью очищена!", 240, 205, 16, fill="#52b788", align="middle", bold=True)}
  {text_path("Собрано 50 единиц опасного мусора.", 240, 235, 13, fill="#d8f3dc", align="middle", bold=False)}
  {text_path("Природа спасена благодаря вам!", 240, 255, 13, fill="#d8f3dc", align="middle", bold=False)}
  {text_path("Нажмите крестик для возврата в меню", 240, 290, 12, fill="#ffd166", align="middle", bold=False)}
</svg>"""
with open(os.path.join(BD_DIR, "win.svg"), "w", encoding="utf-8") as f:
    f.write(win_svg)

# 8. LOSE
lose_svg = f"""<svg width="480" height="360" viewBox="0 0 480 360" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="los_bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#3d0c02"/>
      <stop offset="100%" stop-color="#1a0400"/>
    </linearGradient>
  </defs>
  <rect width="480" height="360" fill="url(#los_bg)"/>
  <rect x="40" y="45" width="400" height="270" rx="20" fill="#140402" fill-opacity="0.9" stroke="#e63946" stroke-width="3"/>
  
  {text_path("ПОРАЖЕНИЕ!", 240, 105, 34, fill="#e63946", align="middle", bold=True)}
  {text_path("Змейка запуталась в собранной ноше...", 240, 140, 15, fill="#f1faee", align="middle", bold=False)}
  {text_path("Не удалось вовремя утилизировать отходы", 240, 165, 13, fill="#e63946", align="middle", bold=False)}
  {text_path("ИТОГОВЫЙ СЧЕТ:", 240, 195, 14, fill="#ffd166", align="middle", bold=True)}
</svg>"""
with open(os.path.join(BD_DIR, "lose.svg"), "w", encoding="utf-8") as f:
    f.write(lose_svg)

print("Backdrops generated successfully!")

# -------------------------------------------------------------
# 2. COSTUMES
# -------------------------------------------------------------
print("2. Generating Costumes...")

# HEAD 1 (20x20 exact, centered)
head_1_svg = """<svg width="20" height="20" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="20" height="20" fill="none" opacity="0"/>
  <path d="M 2,3 C 2,3 10,1 18,6 C 20,10 20,10 18,14 C 10,19 2,17 2,17 C 1,14 1,6 2,3 Z" fill="#2d6a4f" stroke="#1b4332" stroke-width="1.2"/>
  <circle cx="12" cy="5.5" r="2.8" fill="#ffffff"/>
  <circle cx="13" cy="5.5" r="1.5" fill="#081c15"/>
  <circle cx="12" cy="14.5" r="2.8" fill="#ffffff"/>
  <circle cx="13" cy="14.5" r="1.5" fill="#081c15"/>
  <circle cx="17.5" cy="8.5" r="0.8" fill="#1b4332"/>
  <circle cx="17.5" cy="11.5" r="0.8" fill="#1b4332"/>
</svg>"""

# HEAD 2 (20x20 exact, centered)
head_2_svg = """<svg width="20" height="20" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="20" height="20" fill="none" opacity="0"/>
  <path d="M 2,3 C 2,3 10,1 18,6 C 20,10 20,10 18,14 C 10,19 2,17 2,17 C 1,14 1,6 2,3 Z" fill="#2d6a4f" stroke="#1b4332" stroke-width="1.2"/>
  <circle cx="12" cy="5.5" r="2.8" fill="#ffffff"/>
  <circle cx="13" cy="5.5" r="1.5" fill="#081c15"/>
  <circle cx="12" cy="14.5" r="2.8" fill="#ffffff"/>
  <circle cx="13" cy="14.5" r="1.5" fill="#081c15"/>
  <circle cx="17.5" cy="8.5" r="0.8" fill="#1b4332"/>
  <circle cx="17.5" cy="11.5" r="0.8" fill="#1b4332"/>
  <path d="M 17,10 L 18.5,10 L 20,8.5 M 18.5,10 L 20,11.5" stroke="#e63946" stroke-width="1.2" stroke-linecap="round" fill="none"/>
</svg>"""

with open(os.path.join(CS_DIR, "head_1.svg"), "w", encoding="utf-8") as f:
    f.write(head_1_svg)
with open(os.path.join(CS_DIR, "head_2.svg"), "w", encoding="utf-8") as f:
    f.write(head_2_svg)

# SEGMENTS 1..3 (20x20 exact, centered)
seg_1_svg = """<svg width="20" height="20" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="20" height="20" fill="none" opacity="0"/>
  <rect x="1.5" y="1.5" width="17" height="17" rx="5" fill="#40916c" stroke="#1b4332" stroke-width="1.2"/>
  <path d="M 7,13 Q 10,6 14,7 Q 10,14 7,13 Z" fill="#95d5b2"/>
</svg>"""

seg_2_svg = """<svg width="20" height="20" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="20" height="20" fill="none" opacity="0"/>
  <rect x="1.5" y="1.5" width="17" height="17" rx="5" fill="#52b788" stroke="#1b4332" stroke-width="1.2"/>
  <line x1="5" y1="5" x2="15" y2="15" stroke="#74c69d" stroke-width="1.8"/>
  <line x1="5" y1="10" x2="10" y2="15" stroke="#74c69d" stroke-width="1.8"/>
  <line x1="10" y1="5" x2="15" y2="10" stroke="#74c69d" stroke-width="1.8"/>
</svg>"""

seg_3_svg = """<svg width="20" height="20" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="20" height="20" fill="none" opacity="0"/>
  <rect x="1.5" y="1.5" width="17" height="17" rx="5" fill="#74c69d" stroke="#2d6a4f" stroke-width="1.2"/>
  <circle cx="10" cy="10" r="4.5" fill="#b7e4c7"/>
  <circle cx="10" cy="10" r="2.2" fill="#2d6a4f"/>
</svg>"""

with open(os.path.join(CS_DIR, "segment_1.svg"), "w", encoding="utf-8") as f:
    f.write(seg_1_svg)
with open(os.path.join(CS_DIR, "segment_2.svg"), "w", encoding="utf-8") as f:
    f.write(seg_2_svg)
with open(os.path.join(CS_DIR, "segment_3.svg"), "w", encoding="utf-8") as f:
    f.write(seg_3_svg)

# TRASH ITEMS (20x20 exact, centered)
trash_1_svg = """<svg width="20" height="20" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="20" height="20" fill="none" opacity="0"/>
  <rect x="4" y="3" width="12" height="14" rx="2" fill="#adb5bd" stroke="#495057" stroke-width="1"/>
  <ellipse cx="10" cy="3" rx="6" ry="2" fill="#ced4da" stroke="#495057" stroke-width="0.8"/>
  <ellipse cx="10" cy="17" rx="6" ry="2" fill="#6c757d" stroke="#495057" stroke-width="0.8"/>
  <rect x="4" y="7" width="12" height="6" fill="#e63946"/>
  <line x1="7" y1="10" x2="13" y2="10" stroke="#ffffff" stroke-width="1"/>
</svg>"""

trash_2_svg = """<svg width="20" height="20" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="20" height="20" fill="none" opacity="0"/>
  <rect x="8" y="1" width="4" height="3" fill="#1d3557" rx="0.5"/>
  <path d="M 7,4 L 13,4 L 15,8 L 15,17 C 15,18 14,19 13,19 L 7,19 C 6,19 5,18 5,17 L 5,8 Z" fill="#48cae4" fill-opacity="0.85" stroke="#0077b6" stroke-width="1"/>
  <rect x="5" y="10" width="10" height="5" fill="#0096c7"/>
</svg>"""

trash_3_svg = """<svg width="20" height="20" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="20" height="20" fill="none" opacity="0"/>
  <rect x="8" y="1" width="4" height="2" fill="#ffd166" rx="0.5"/>
  <rect x="4" y="3" width="12" height="15" rx="2" fill="#212529" stroke="#ffd166" stroke-width="1"/>
  <rect x="4" y="3" width="12" height="5" fill="#e63946" rx="1"/>
  <line x1="10" y1="5" x2="10" y2="7" stroke="#ffffff" stroke-width="1"/>
  <line x1="9" y1="6" x2="11" y2="6" stroke="#ffffff" stroke-width="1"/>
  <line x1="8" y1="14" x2="12" y2="14" stroke="#ffffff" stroke-width="1"/>
</svg>"""

with open(os.path.join(CS_DIR, "trash_1.svg"), "w", encoding="utf-8") as f:
    f.write(trash_1_svg)
with open(os.path.join(CS_DIR, "trash_2.svg"), "w", encoding="utf-8") as f:
    f.write(trash_2_svg)
with open(os.path.join(CS_DIR, "trash_3.svg"), "w", encoding="utf-8") as f:
    f.write(trash_3_svg)

# BIN (20x20 exact, centered)
bin_svg = """<svg width="20" height="20" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="20" height="20" fill="none" opacity="0"/>
  <rect x="3" y="2" width="14" height="2.5" rx="1" fill="#2d6a4f" stroke="#1b4332" stroke-width="0.8"/>
  <rect x="8" y="0.5" width="4" height="1.5" rx="0.5" fill="#1b4332"/>
  <path d="M 4,4.5 L 5.5,18 C 5.5,18.5 6,19 7,19 L 13,19 C 14,19 14.5,18.5 14.5,18 L 16,4.5 Z" fill="#52b788" stroke="#1b4332" stroke-width="1"/>
  <line x1="7.5" y1="7" x2="8" y2="15" stroke="#1b4332" stroke-width="1"/>
  <line x1="10" y1="7" x2="10" y2="15" stroke="#1b4332" stroke-width="1"/>
  <line x1="12.5" y1="7" x2="12" y2="15" stroke="#1b4332" stroke-width="1"/>
</svg>"""
with open(os.path.join(CS_DIR, "bin.svg"), "w", encoding="utf-8") as f:
    f.write(bin_svg)

# BUTTONS (All 0 0 W H, centered)
btn_start_svg = f"""<svg width="160" height="50" viewBox="0 0 160 50" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="160" height="50" fill="none" opacity="0"/>
  <rect x="3" y="3" width="154" height="44" rx="12" fill="#2d6a4f" stroke="#74c69d" stroke-width="2.5"/>
  {text_path("СТАРТ", 80, 32, 20, fill="#ffffff", align="middle", bold=True)}
</svg>"""
with open(os.path.join(CS_DIR, "btn_start.svg"), "w", encoding="utf-8") as f:
    f.write(btn_start_svg)

btn_settings_svg = f"""<svg width="160" height="50" viewBox="0 0 160 50" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="160" height="50" fill="none" opacity="0"/>
  <rect x="3" y="3" width="154" height="44" rx="12" fill="#1b4332" stroke="#52b788" stroke-width="2"/>
  {text_path("НАСТРОЙКИ", 80, 31, 16, fill="#d8f3dc", align="middle", bold=True)}
</svg>"""
with open(os.path.join(CS_DIR, "btn_settings.svg"), "w", encoding="utf-8") as f:
    f.write(btn_settings_svg)

btn_restart_svg = f"""<svg width="160" height="50" viewBox="0 0 160 50" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="160" height="50" fill="none" opacity="0"/>
  <rect x="3" y="3" width="154" height="44" rx="12" fill="#e76f51" stroke="#f4a261" stroke-width="2.5"/>
  {text_path("ЕЩЕ РАЗ", 80, 31, 18, fill="#ffffff", align="middle", bold=True)}
</svg>"""
with open(os.path.join(CS_DIR, "btn_restart.svg"), "w", encoding="utf-8") as f:
    f.write(btn_restart_svg)

btn_close_svg = """<svg width="34" height="34" viewBox="0 0 34 34" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="34" height="34" fill="none" opacity="0"/>
  <circle cx="17" cy="17" r="15" fill="#e63946" stroke="#ffffff" stroke-width="2"/>
  <line x1="11" y1="11" x2="23" y2="23" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="23" y1="11" x2="11" y2="23" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round"/>
</svg>"""
with open(os.path.join(CS_DIR, "btn_close.svg"), "w", encoding="utf-8") as f:
    f.write(btn_close_svg)

grid_20_svg = f"""<svg width="150" height="32" viewBox="0 0 150 32" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="150" height="32" fill="none" opacity="0"/>
  <rect x="2" y="2" width="146" height="28" rx="8" fill="#40916c" stroke="#74c69d" stroke-width="2"/>
  {text_path("СЕТКА: 20 PX", 75, 21, 13, fill="#ffffff", align="middle", bold=True)}
</svg>"""

grid_30_svg = f"""<svg width="150" height="32" viewBox="0 0 150 32" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="150" height="32" fill="none" opacity="0"/>
  <rect x="2" y="2" width="146" height="28" rx="8" fill="#1b4332" stroke="#52b788" stroke-width="2"/>
  {text_path("СЕТКА: 30 PX", 75, 21, 13, fill="#d8f3dc", align="middle", bold=True)}
</svg>"""

with open(os.path.join(CS_DIR, "grid_20.svg"), "w", encoding="utf-8") as f:
    f.write(grid_20_svg)
with open(os.path.join(CS_DIR, "grid_30.svg"), "w", encoding="utf-8") as f:
    f.write(grid_30_svg)

# SPINNER (48x48 exact)
for i, ang in enumerate([0, 90, 180, 270], start=1):
    sprout_svg = f"""<svg width="48" height="48" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
      <rect x="0" y="0" width="48" height="48" fill="none" opacity="0"/>
      <g transform="translate(24, 24) rotate({ang})">
        <circle cx="0" cy="0" r="7" fill="#52b788"/>
        <path d="M0,-7 C6,-16 16,-14 11,-4 C8,-2 4,-3 0,-7 Z" fill="#74c69d"/>
        <path d="M0,7 C-6,16 -16,14 -11,4 C-8,2 -4,3 0,7 Z" fill="#74c69d"/>
        <path d="M7,0 C16,6 14,16 4,11 C2,8 3,4 7,0 Z" fill="#95d5b2"/>
        <path d="M-7,0 C-16,-6 -14,-16 -4,-11 C-2,-8 -3,-4 -7,0 Z" fill="#95d5b2"/>
      </g>
    </svg>"""
    with open(os.path.join(CS_DIR, f"sprout_{i}.svg"), "w", encoding="utf-8") as f:
        f.write(sprout_svg)

# SCORE LABEL (60x24 exact, center 30, 12)
score_label_svg = f"""<svg width="60" height="24" viewBox="0 0 60 24" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="60" height="24" fill="none" opacity="0"/>
  <rect x="1" y="1" width="58" height="22" rx="4" fill="#081c15" fill-opacity="0.85" stroke="#52b788" stroke-width="1.2"/>
  {text_path("СЧЕТ:", 30, 16, 11, fill="#74c69d", align="middle", bold=True)}
</svg>"""
with open(os.path.join(CS_DIR, "score_label.svg"), "w", encoding="utf-8") as f:
    f.write(score_label_svg)

# DIGITS 0..9 (18x24 exact, center 9, 12)
for d in range(10):
    digit_svg = f"""<svg width="18" height="24" viewBox="0 0 18 24" xmlns="http://www.w3.org/2000/svg">
      <rect x="0" y="0" width="18" height="24" fill="none" opacity="0"/>
      <rect x="1" y="1" width="16" height="22" rx="4" fill="#081c15" fill-opacity="0.85" stroke="#74c69d" stroke-width="1.2"/>
      {text_path(str(d), 9, 17, 16, fill="#ffd166", align="middle", bold=True)}
    </svg>"""
    with open(os.path.join(CS_DIR, f"digit_{d}.svg"), "w", encoding="utf-8") as f:
        f.write(digit_svg)

print("Costumes generated successfully!")

# -------------------------------------------------------------
# 3. SOUNDS
# -------------------------------------------------------------
print("3. Generating Sounds...")

def write_wav(filename, samples, sample_rate=22050):
    filepath = os.path.join(SD_DIR, filename)
    with wave.open(filepath, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        raw = bytearray()
        for s in samples:
            val = max(-32767, min(32767, int(s * 32767)))
            raw.extend(struct.pack("<h", val))
        wf.writeframes(raw)

SR = 22050

def gen_btn_start():
    dur = 0.25
    n = int(SR * dur)
    samples = []
    for i in range(n):
        t = i / SR
        env = (1.0 - i / n) ** 1.2
        f = 523.25 if t < 0.1 else 659.25
        s = math.sin(2 * math.pi * f * t) * env * 0.7
        samples.append(s)
    return samples

def gen_btn_settings():
    dur = 0.08
    n = int(SR * dur)
    samples = []
    for i in range(n):
        t = i / SR
        env = (1.0 - i / n) ** 2
        f = 600 - 300 * (i / n)
        s = math.sin(2 * math.pi * f * t) * env * 0.6
        samples.append(s)
    return samples

def gen_btn_restart():
    dur = 0.2
    n = int(SR * dur)
    samples = []
    for i in range(n):
        t = i / SR
        env = (1.0 - i / n) ** 1.5
        f = 440 + 440 * (i / n)
        s = math.sin(2 * math.pi * f * t) * env * 0.7
        samples.append(s)
    return samples

def gen_btn_close():
    dur = 0.06
    n = int(SR * dur)
    samples = []
    for i in range(n):
        t = i / SR
        env = (1.0 - i / n) ** 3
        f = 900 - 400 * (i / n)
        s = math.sin(2 * math.pi * f * t) * env * 0.5
        samples.append(s)
    return samples

def gen_trash():
    dur = 0.18
    n = int(SR * dur)
    samples = []
    for i in range(n):
        t = i / SR
        env = (1.0 - i / n) ** 1.3
        s = (math.sin(2 * math.pi * 880 * t) + 0.5 * math.sin(2 * math.pi * 1760 * t)) * env * 0.65
        samples.append(s)
    return samples

def gen_bin():
    dur = 0.25
    n = int(SR * dur)
    samples = []
    for i in range(n):
        t = i / SR
        env = (1.0 - i / n) ** 1.8
        f = 220 - 80 * (i / n)
        s = (1.0 if math.sin(2 * math.pi * f * t) > 0 else -1.0) * env * 0.5
        samples.append(s)
    return samples

def gen_crash():
    dur = 0.35
    n = int(SR * dur)
    samples = []
    for i in range(n):
        t = i / SR
        env = (1.0 - i / n)
        f = 180 - 100 * (i / n)
        noise = (random.random() * 2 - 1) * 0.3
        s = ((1.0 if math.sin(2 * math.pi * f * t) > 0 else -1.0) * 0.5 + noise) * env * 0.7
        samples.append(s)
    return samples

def gen_win():
    notes = [523.25, 659.25, 783.99, 1046.50]
    dur_note = 0.16
    samples = []
    for f in notes:
        n = int(SR * dur_note)
        for i in range(n):
            t = i / SR
            env = math.sin(math.pi * i / n)
            s = (math.sin(2 * math.pi * f * t) + 0.3 * math.sin(4 * math.pi * f * t)) * env * 0.7
            samples.append(s)
    return samples

def gen_menu_music():
    melody = [329.63, 392.00, 440.00, 523.25, 440.00, 392.00]
    note_dur = 0.5
    samples = []
    for f in melody:
        n = int(SR * note_dur)
        for i in range(n):
            t = i / SR
            env = math.sin(math.pi * (i / n) ** 0.5)
            s = (math.sin(2 * math.pi * f * t) + 0.2 * math.sin(4 * math.pi * f * t)) * env * 0.35
            samples.append(s)
    return samples

def gen_game_music():
    bass_notes = [130.81, 146.83, 164.81, 196.00, 220.00, 196.00, 164.81, 146.83]
    step_dur = 0.2
    samples = []
    for b in bass_notes:
        n = int(SR * step_dur)
        for i in range(n):
            t = i / SR
            env = (1.0 - i / n) ** 0.8
            s = math.sin(2 * math.pi * b * t) * 0.35
            if i < int(SR * 0.02):
                s += (random.random() * 2 - 1) * 0.2
            samples.append(s * env)
    return samples

write_wav("btn_start.wav", gen_btn_start())
write_wav("btn_settings.wav", gen_btn_settings())
write_wav("btn_restart.wav", gen_btn_restart())
write_wav("btn_close.wav", gen_btn_close())
write_wav("trash.wav", gen_trash())
write_wav("bin.wav", gen_bin())
write_wav("crash.wav", gen_crash())
write_wav("win.wav", gen_win())
write_wav("menu_music.wav", gen_menu_music())
write_wav("game_music.wav", gen_game_music())

print("Audio WAVs generated successfully!")
print("ALL ASSETS READY!")
