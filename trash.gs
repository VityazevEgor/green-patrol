# 1. Используемые переменные:
# Глобальные переменные:
# - game_state: проверка активного состояния игры.
# - food_type: случайный тип мусора (1 - банка, 2 - бутылка, 3 - батарейка).
# - cell_size: размер клетки для масштаба спрайта и расчета координат появления.
# Локальные переменные: отсутствуют.
#
# 2. Описание логики работы этого спрайта:
# При получении сигнала появления спрайт выбирает случайный тип мусора, рассчитывает случайные
# координаты на сетке поля без наложения на границы и отображается на экране.

costumes "assets/costumes/trash_1.svg",
         "assets/costumes/trash_2.svg",
         "assets/costumes/trash_3.svg";

onflag {
    hide;
}

on "spawn_food" {
    if game_state == "игра" {
        food_type = random(1, 3);
        switch_costume food_type;
        set_size (cell_size * 5);
        goto (random(0 - 240 / cell_size, 240 / cell_size - 1) * cell_size + cell_size / 2), (random(0 - 180 / cell_size, 180 / cell_size - 1) * cell_size + cell_size / 2);
        show;
    }
}

on "open_menu" { hide; }
on "open_settings" { hide; }
on "game_over" { hide; }
on "game_win" { hide; }
