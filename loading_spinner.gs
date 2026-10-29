costumes "assets/costumes/sprout_1.svg",
         "assets/costumes/sprout_2.svg",
         "assets/costumes/sprout_3.svg",
         "assets/costumes/sprout_4.svg";

onflag { hide; }

on "start_game" {
    goto 0, -10;
    show;
    repeat 4 {
        next_costume;
        wait 0.18;
    }
    hide;
}

on "open_menu" { hide; }
on "open_settings" { hide; }
on "begin_play" { hide; }
on "game_over" { hide; }
on "game_win" { hide; }
