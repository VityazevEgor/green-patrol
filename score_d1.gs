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

var tens = 0;

onflag { hide; }

on "begin_play" {
    goto 192, 155;
    set_size 100;
    show;
    until game_state != "игра" {
        tens = (score / 10) % 10;
        switch_costume tens + 1;
        wait 0.1;
    }
}

on "game_over" {
    goto -12, -38;
    set_size 125;
    tens = (score / 10) % 10;
    switch_costume tens + 1;
    show;
}

on "open_menu" { hide; }
on "open_settings" { hide; }
on "start_game" { hide; }
on "game_win" { hide; }
