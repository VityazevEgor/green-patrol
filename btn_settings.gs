costumes "assets/costumes/btn_settings.svg";
sounds "assets/sounds/btn_settings.wav";

onflag { hide; }

on "open_menu" {
    goto 0, -45;
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
