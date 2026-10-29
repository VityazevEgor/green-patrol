costumes "assets/costumes/trash_1.svg",
         "assets/costumes/trash_2.svg",
         "assets/costumes/trash_3.svg";

var fx = 0;
var fy = 0;

onflag {
    hide;
}

on "spawn_food" {
    if game_state == "игра" {
        food_type = random(1, 3);
        if food_type == 1 { switch_costume "trash_1"; }
        if food_type == 2 { switch_costume "trash_2"; }
        if food_type == 3 { switch_costume "trash_3"; }
        
        fx = random(-10, 10) * 20;
        fy = random(-7, 7) * 20;
        goto fx, fy;
        show;
    }
}

on "open_menu" { hide; }
on "open_settings" { hide; }
on "game_over" { hide; }
on "game_win" { hide; }
