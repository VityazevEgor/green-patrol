costumes "assets/costumes/score_label.svg";

onflag { hide; }

on "begin_play" {
    goto 150, 155;
    show;
}

on "open_menu" { hide; }
on "open_settings" { hide; }
on "start_game" { hide; }
on "game_over" { hide; }
on "game_win" { hide; }
