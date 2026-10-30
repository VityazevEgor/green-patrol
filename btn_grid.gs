costumes "assets/costumes/grid_20.svg",
         "assets/costumes/grid_30.svg";
sounds "assets/sounds/btn_settings.wav";

onflag { hide; }

on "open_settings" {
    goto 120, -120;
    set_size 90;
    if cell_size == 20 { switch_costume "grid_20"; }
    if cell_size == 30 { switch_costume "grid_30"; }
    show;
}

onclick {
    start_sound "btn_settings";
    if cell_size == 20 {
        cell_size = 30;
        switch_costume "grid_30";
    } else {
        cell_size = 20;
        switch_costume "grid_20";
    }
}

on "open_menu" { hide; }
on "start_game" { hide; }
on "game_over" { hide; }
on "game_win" { hide; }
