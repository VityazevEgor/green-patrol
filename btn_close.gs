# 1. Используемые переменные:
# Данный спрайт не использует переменных.
#
# 2. Описание логики работы этого спрайта:
# Отображается в виде крестика в правом верхнем углу экранов настроек и победы.
# При клике воспроизводит звук и возвращает игрока в главное меню игры.

costumes "assets/costumes/btn_close.svg";
sounds "assets/sounds/btn_close.wav";

onflag { hide; }

on "open_settings" {
    goto 205, 148;
    set_size 100;
    show;
}

on "game_win" {
    goto 205, 148;
    set_size 100;
    show;
}

onclick {
    start_sound "btn_close";
    set_size 90;
    wait 0.08;
    set_size 100;
    broadcast "open_menu";
}

on "open_menu" { hide; }
on "start_game" { hide; }
on "game_over" { hide; }
