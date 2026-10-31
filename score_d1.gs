# 1. Используемые переменные:
# Глобальные переменные:
# - score: текущий счет игры для вычисления десятков.
# - game_state: состояние игры для контроля цикла обновления во время раунда.
# Локальные переменные: отсутствуют.
#
# 2. Описание логики работы этого спрайта:
# Отображает цифру десятков текущего счета в правом верхнем углу во время игры
# и по центру экрана на карточке поражения. Номер костюма вычисляется математически.

costumes "assets/costumes/digit_0.svg",
         "assets/costumes/digit_1.svg",
         "assets/costumes/digit_2.svg",
         "assets/costumes/digit_3.svg",
         "assets/costumes/digit_4.svg",
         "assets/costumes/digit_5.svg",
         "assets/costumes/digit_6.svg",
         "assets/costumes/digit_7.svg",
         "assets/costumes/digit_8.svg",
         "assets/costumes/digit_9.svg";

onflag { hide; }

on "begin_play" {
    goto 203, 161;
    set_size 100;
    show;
    until game_state != "игра" {
        switch_costume ((score - (score % 10)) / 10 + 1);
        wait 0.1;
    }
}

on "game_over" {
    goto -12, -38;
    set_size 125;
    switch_costume ((score - (score % 10)) / 10 + 1);
    show;
}

on "open_menu" { hide; }
on "open_settings" { hide; }
on "start_game" { hide; }
on "game_win" { hide; }
