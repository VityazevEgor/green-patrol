# 1. Используемые переменные:
# Данный спрайт не использует переменных.
#
# 2. Описание логики работы этого спрайта:
# Отображается в главном меню игры. При клике воспроизводит звук, анимирует нажатие
# и передает сообщение start_game для перехода к загрузке и игровому процессу.

costumes "assets/costumes/btn_start.svg";
sounds "assets/sounds/btn_start.wav";

onflag { hide; }

on "open_menu" {
    goto 0, 5;
    set_size 100;
    show;
}

onclick {
    start_sound "btn_start";
    set_size 92;
    wait 0.28;
    set_size 100;
    broadcast "start_game";
}

on "open_settings" { hide; }
on "start_game" { hide; }
on "game_over" { hide; }
on "game_win" { hide; }
