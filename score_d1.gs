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
