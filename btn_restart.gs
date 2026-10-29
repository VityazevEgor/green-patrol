costumes "assets/costumes/btn_restart.svg";
sounds "assets/sounds/btn_restart.wav";

onflag { hide; }

on "game_over" {
    goto 0, -98;
    set_size 100;
    show;
}

onclick {
    start_sound "btn_restart";
    set_size 92;
    wait 0.08;
    set_size 100;
    broadcast "start_game";
}

on "open_menu" { hide; }
on "open_settings" { hide; }
on "start_game" { hide; }
on "game_win" { hide; }
