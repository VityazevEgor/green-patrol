# 1. Используемые переменные:
# Глобальные переменные:
# - cell_size: размер клетки сетки поля (20 px или 30 px).
# Локальные переменные: отсутствуют.
#
# 2. Описание логики работы этого спрайта:
# Отображается на экране настроек. Показывает текущий режим сетки (20 px или 30 px)
# и при нажатии переключает значение переменной cell_size и соответствующий костюм кнопки.

costumes "assets/costumes/grid_20.svg",
         "assets/costumes/grid_30.svg";
sounds "assets/sounds/btn_settings.wav";

onflag { hide; }

on "open_settings" {
    goto 120, -116;
    set_size 90;
    if cell_size == 20 { switch_costume "grid_20"; }
    if cell_size == 30 { switch_costume "grid_30"; }
    show;
}

onclick {
    start_sound "btn_settings";
    if cell_size == 20 {
        cell_size = 30;
        switch_costume "grid_30";
    } else {
        cell_size = 20;
        switch_costume "grid_20";
    }
}

on "open_menu" { hide; }
on "start_game" { hide; }
on "game_over" { hide; }
on "game_win" { hide; }
