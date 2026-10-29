costumes "assets/costumes/bin.svg";

var bx = 0;
var by = 0;

onflag {
    hide;
}

on "spawn_bin" {
    if game_state == "игра" {
        bx = random(-10, 10) * 20;
        by = random(-7, 7) * 20;
        goto bx, by;
        show;
    }
}

on "open_menu" { hide; }
on "open_settings" { hide; }
on "game_over" { hide; }
on "game_win" { hide; }
