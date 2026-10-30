costumes "assets/costumes/bin.svg";

onflag {
    hide;
}

on "spawn_bin" {
    if game_state == "игра" {
        goto (random(-11, 10) * 20 + 10), (random(-8, 7) * 20 + 10);
        show;
    }
}

on "open_menu" { hide; }
on "open_settings" { hide; }
on "game_over" { hide; }
on "game_win" { hide; }
