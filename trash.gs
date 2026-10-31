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
        set_size (cell_size * 5);
        goto (random(0 - 240 / cell_size, 240 / cell_size - 1) * cell_size + cell_size / 2), (random(0 - 180 / cell_size, 180 / cell_size - 1) * cell_size + cell_size / 2);
        show;
    }
}

on "open_menu" { hide; }
on "open_settings" { hide; }
on "game_over" { hide; }
on "game_win" { hide; }
