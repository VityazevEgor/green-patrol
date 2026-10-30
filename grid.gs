costumes "assets/costumes/tile_light.svg",
         "assets/costumes/tile_dark.svg";

# Процедура параметрической отрисовки поля для любой сетки (20 px или 30 px):
# 1. 'proc' компилируется с режимом warp: true («Запустить без обновления экрана») — рисуется моментально за 1 кадр!
# 2. Масштаб плитки вычисляется параметрически: cell_size * 5 (20 px -> 100%, 30 px -> 150%).
# 3. Число рядов и столбцов: 360 / cell_size и 480 / cell_size.
# 4. Начальные координаты: (-240 + cell_size / 2, 180 - cell_size / 2).
proc draw_field {
    erase_all;
    set_size (cell_size * 5);
    switch_costume "tile_light";
    set_y (180 - cell_size / 2);
    repeat (360 / cell_size) {
        set_x (-240 + cell_size / 2);
        repeat (480 / cell_size) {
            stamp;
            next_costume;
            change_x cell_size;
        }
        next_costume;
        change_y (0 - cell_size);
    }
}

onflag {
    erase_all;
    hide;
}

on "begin_play" {
    draw_field;
    hide;
}

on "start_game" {
    erase_all;
    hide;
}

on "open_menu" {
    erase_all;
    hide;
}

on "open_settings" {
    erase_all;
    hide;
}

on "game_over" {
    erase_all;
    hide;
}

on "game_win" {
    erase_all;
    hide;
}
