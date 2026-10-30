costumes "assets/costumes/bin.svg";

var bx = 0;
var by = 0;

onflag {
    hide;
}

on "spawn_bin" {
    if game_state == "игра" {
        bx = (random(-11, 10) * 20) + 10;
        by = (random(-8, 7) * 20) + 10;
        goto bx, by;
        show;
    }
}

on "open_menu" { hide; }
on "open_settings" { hide; }
on "game_over" { hide; }
on "game_win" { hide; }
