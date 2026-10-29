costumes "assets/costumes/btn_start.svg";
sounds "assets/sounds/btn_start.wav";

onflag { hide; }

on "open_menu" {
    goto 0, 30;
    set_size 100;
    show;
}

onclick {
    start_sound "btn_start";
    set_size 92;
    wait 0.08;
    set_size 100;
    broadcast "start_game";
}

on "open_settings" { hide; }
on "start_game" { hide; }
on "game_over" { hide; }
on "game_win" { hide; }
