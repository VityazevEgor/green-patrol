costumes "assets/costumes/bin.svg";

onflag {
    hide;
}

on "spawn_bin" {
    if game_state == "игра" {
        set_size (cell_size * 5);
        goto (random(1 - 240 / cell_size, 240 / cell_size - 2) * cell_size + cell_size / 2), (random(1 - 180 / cell_size, 180 / cell_size - 2) * cell_size + cell_size / 2);
        show;
    }
}

on "open_menu" { hide; }
on "open_settings" { hide; }
on "game_over" { hide; }
on "game_win" { hide; }
