costumes "assets/costumes/trash_1.svg",
         "assets/costumes/trash_2.svg",
         "assets/costumes/trash_3.svg";

onflag {
    hide;
}

on "spawn_food" {
    if game_state == "игра" {
        food_type = random(1, 3);
        switch_costume food_type;
        goto (random(-12, 11) * 20 + 10), (random(-9, 8) * 20 + 10);
        show;
    }
}

on "open_menu" { hide; }
on "open_settings" { hide; }
on "game_over" { hide; }
on "game_win" { hide; }
