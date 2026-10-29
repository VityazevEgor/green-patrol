costumes "assets/costumes/btn_close.svg";
sounds "assets/sounds/btn_close.wav";

onflag { hide; }

on "open_settings" {
    goto 205, 148;
    set_size 100;
    show;
}

on "game_win" {
    goto 205, 148;
    set_size 100;
    show;
}

onclick {
    start_sound "btn_close";
    set_size 90;
    wait 0.08;
    set_size 100;
    broadcast "open_menu";
}

on "open_menu" { hide; }
on "start_game" { hide; }
on "game_over" { hide; }
