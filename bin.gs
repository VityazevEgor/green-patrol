# 1. Используемые переменные:
# Глобальные переменные:
# - game_state: проверка активного состояния игры.
# - cell_size: размер клетки для масштаба спрайта и расчета координат появления.
# Локальные переменные: отсутствуют.
#
# 2. Описание логики работы этого спрайта:
# При получении сигнала появления спрайт размещается в случайной клетке поля с отступом от краев,
# показывается игроку и служит объектом штрафа (уменьшает счет и длину хвоста при контакте).

costumes "assets/costumes/bin.svg";

onflag {
    hide;
}

on "spawn_bin" {
    if game_state == "игра" {
        set_size (cell_size * 5);
        goto (random(1 - 240 / cell_size, 240 / cell_size - 2) * cell_size + cell_size / 2), (random(1 - 180 / cell_size, 180 / cell_size - 2) * cell_size + cell_size / 2);
        show;
    }
}

on "open_menu" { hide; }
on "open_settings" { hide; }
on "game_over" { hide; }
on "game_win" { hide; }
