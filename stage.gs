costumes "assets/backdrops/cover.svg",
         "assets/backdrops/menu.svg",
         "assets/backdrops/settings.svg",
         "assets/backdrops/loading.svg",
         "assets/backdrops/game_20.svg",
         "assets/backdrops/win.svg",
         "assets/backdrops/lose.svg";

sounds "assets/sounds/menu_music.wav",
       "assets/sounds/game_music.wav",
       "assets/sounds/win.wav";

# Глобальные переменные игры
var score = 0;
var game_state = 0; # "заставка", "меню", "настройки", "загрузка", "игра", "победа", "поражение"
var snake_len = 3;
var head_x = 0;
var head_y = 0;
var food_type = 1;
var last_eat_x = 9999;
var last_eat_y = 9999;

# Глобальные списки истории координат
list hist_x = [];
list hist_y = [];

onflag {
    game_state = "заставка";
    switch_backdrop "cover";
    wait 0.05;
    game_state = "меню";
    switch_backdrop "menu";
    broadcast "open_menu";
    
    forever {
        if game_state == "меню" or game_state == "настройки" {
            play_sound_until_done "menu_music";
        }
        if game_state == "игра" {
            play_sound_until_done "game_music";
        }
        wait 0.1;
    }
}

on "open_menu" {
    game_state = "меню";
    switch_backdrop "menu";
}

on "open_settings" {
    game_state = "настройки";
    switch_backdrop "settings";
}

on "start_game" {
    game_state = "загрузка";
    switch_backdrop "loading";
    stop_all_sounds;
    wait 0.8;
    switch_backdrop "game_20";
    game_state = "игра";
    broadcast "begin_play";
}

on "game_over" {
    game_state = "поражение";
    stop_all_sounds;
    switch_backdrop "lose";
}

on "game_win" {
    game_state = "победа";
    stop_all_sounds;
    switch_backdrop "win";
    start_sound "win";
}
