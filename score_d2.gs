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

var units = 0;

onflag { hide; }

on "begin_play" {
    goto 212, 155;
    set_size 100;
    show;
    until game_state != "игра" {
        units = score % 10;
        switch_costume units + 1;
        wait 0.1;
    }
}

on "game_over" {
    goto 12, -38;
    set_size 125;
    units = score % 10;
    switch_costume units + 1;
    show;
}

on "open_menu" { hide; }
on "open_settings" { hide; }
on "start_game" { hide; }
on "game_win" { hide; }
