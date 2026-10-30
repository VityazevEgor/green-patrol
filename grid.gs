costumes "assets/costumes/tile_light.svg",
         "assets/costumes/tile_dark.svg";

# Процедура отрисовки поля без единой переменной:
# 1. 'proc' компилируется с режимом warp: true («Запустить без обновления экрана») — рисуется моментально за 1 кадр!
# 2. Позиционирование через встроенные команды движения (set_x, set_y, change_x, change_y).
# 3. Чередование клеток через next_costume (плюс один дополнительный шаг в конце ряда для шахматного сдвига).
proc draw_field {
    erase_all;
    switch_costume "tile_light";
    set_y 170;
    repeat 18 {
        set_x -230;
        repeat 24 {
            stamp;
            next_costume;
            change_x 20;
        }
        next_costume;
        change_y -20;
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
