# 1. Используемые переменные:
# Данный спрайт не использует переменных.
#
# 2. Описание логики работы этого спрайта:
# Отображается в главном меню игры. При клике воспроизводит звук нажатия и передает
# сообщение open_settings для открытия экрана правил и настроек.

costumes "assets/costumes/btn_settings.svg";
sounds "assets/sounds/btn_settings.wav";

onflag { hide; }

on "open_menu" {
    goto 0, -60;
    set_size 100;
    show;
}

onclick {
    start_sound "btn_settings";
    set_size 92;
    wait 0.08;
    set_size 100;
    broadcast "open_settings";
}

on "open_settings" { hide; }
on "start_game" { hide; }
on "game_over" { hide; }
on "game_win" { hide; }
