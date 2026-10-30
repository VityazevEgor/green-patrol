costumes "assets/costumes/tile_light.svg",
         "assets/costumes/tile_dark.svg";

var grid_x = 0;
var grid_y = 0;
var grid_row = 0;
var grid_col = 0;

# Процедура мгновенной процедурной генерации игрового поля (без обновления экрана)
nowarp proc draw_field {
    erase_all;
    grid_y = 170;
    grid_row = 0;
    repeat 18 {
        grid_x = -230;
        grid_col = 0;
        repeat 24 {
            goto grid_x, grid_y;
            if (grid_row + grid_col) % 2 == 0 {
                switch_costume "tile_light";
            }
            if (grid_row + grid_col) % 2 != 0 {
                switch_costume "tile_dark";
            }
            stamp;
            grid_x += 20;
            grid_col += 1;
        }
        grid_y -= 20;
        grid_row += 1;
    }
}

onflag {
    erase_all;
    hide;
}

on "begin_play" {
    draw_field;
    hide;
}

on "start_game" {
    erase_all;
    hide;
}

on "open_menu" {
    erase_all;
    hide;
}

on "open_settings" {
    erase_all;
    hide;
}

on "game_over" {
    erase_all;
    hide;
}

on "game_win" {
    erase_all;
    hide;
}
