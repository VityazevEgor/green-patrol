costumes "assets/costumes/head_1.svg",
         "assets/costumes/head_2.svg";

sounds "assets/sounds/trash.wav",
       "assets/sounds/bin.wav",
       "assets/sounds/crash.wav";

var dir_x = 0;
var dir_y = 0;
var next_dir_x = 0;
var next_dir_y = 0;
var new_head_x = 0;
var new_head_y = 0;
var chk_idx = 0;
var init_i = 0;
var r = 0;
var is_dead = 0;

# --- Управление стрелками клавиатуры ---
onkey "right arrow" {
    if game_state == "игра" and dir_x != -1 {
        next_dir_x = 1;
        next_dir_y = 0;
    }
}

onkey "left arrow" {
    if game_state == "игра" and dir_x != 1 {
        next_dir_x = -1;
        next_dir_y = 0;
    }
}

onkey "up arrow" {
    if game_state == "игра" and dir_y != -1 {
        next_dir_x = 0;
        next_dir_y = 1;
    }
}

onkey "down arrow" {
    if game_state == "игра" and dir_y != 1 {
        next_dir_x = 0;
        next_dir_y = -1;
    }
}

# --- Процедуры (функции) для прозрачности и простоты кода ---

# 1. Случайный выбор начального направления движения
nowarp proc pick_start_direction {
    r = random(1, 4);
    if r == 1 { dir_x = 1; dir_y = 0; }
    if r == 2 { dir_x = -1; dir_y = 0; }
    if r == 3 { dir_x = 0; dir_y = 1; }
    if r == 4 { dir_x = 0; dir_y = -1; }
    next_dir_x = dir_x;
    next_dir_y = dir_y;
}

# 2. Инициализация списков истории (тело строится позади головы)
nowarp proc init_history {
    delete hist_x;
    delete hist_y;
    add head_x to hist_x;
    add head_y to hist_y;
    init_i = 1;
    until init_i > 5 {
        add (0 - (init_i * dir_x * 20)) to hist_x;
        add (0 - (init_i * dir_y * 20)) to hist_y;
        init_i = init_i + 1;
    }
}

# 3. Поворот головы и анимация языка
nowarp proc update_head_look {
    if dir_x == 1 { point_in_direction 90; }
    if dir_x == -1 { point_in_direction -90; }
    if dir_y == 1 { point_in_direction 0; }
    if dir_y == -1 { point_in_direction 180; }
    next_costume;
}

# 4. Расчет следующей позиции головы и телепортация через край экрана
nowarp proc calculate_next_position {
    new_head_x = head_x + dir_x * 20;
    new_head_y = head_y + dir_y * 20;
    
    if new_head_x > 220 { new_head_x = -220; }
    if new_head_x < -220 { new_head_x = 220; }
    if new_head_y > 160 { new_head_y = -160; }
    if new_head_y < -160 { new_head_y = 160; }
}

# 5. Проверка столкновения со своим хвостом (начиная со 2-го звена)
nowarp proc check_self_collision {
    chk_idx = 2;
    repeat snake_len {
        if chk_idx <= length hist_x and hist_x[chk_idx] == new_head_x and hist_y[chk_idx] == new_head_y {
            is_dead = "да";
        }
        chk_idx = chk_idx + 1;
    }
}

# 6. Анимация гибели при столкновении
proc handle_death {
    start_sound "crash";
    repeat 3 {
        set_ghost_effect 70;
        wait 0.12;
        set_ghost_effect 0;
        wait 0.12;
    }
    hide;
    broadcast "game_over";
}

# 7. Шаг головы и запись позиции в историю
nowarp proc apply_move {
    head_x = new_head_x;
    head_y = new_head_y;
    goto head_x, head_y;
    
    insert head_x at hist_x[1];
    insert head_y at hist_y[1];
    
    until length hist_x <= snake_len + 5 {
        delete hist_x[length hist_x];
        delete hist_y[length hist_y];
    }
    
    broadcast "update_body";
}

# 8. Проверка сбора мусора
nowarp proc check_trash_pickup {
    if touching("trash") {
        start_sound "trash";
        score += food_type;
        snake_len += 1;
        last_eat_x = head_x;
        last_eat_y = head_y;
        
        if score >= 50 {
            broadcast "game_win";
        }
        if score < 50 {
            broadcast "spawn_food";
        }
    }
}

# 9. Проверка попадания в мусорную корзину (штраф)
nowarp proc check_bin_penalty {
    if touching("bin") {
        start_sound "bin";
        if score > 0 { score -= 1; }
        if snake_len > 1 { snake_len -= 1; }
        broadcast "spawn_bin";
    }
}

# --- Основной игровой цикл ---
on "begin_play" {
    score = 0;
    snake_len = 3;
    is_dead = "нет";
    last_eat_x = 9999;
    last_eat_y = 9999;
    head_x = 0;
    head_y = 0;
    goto head_x, head_y;
    set_ghost_effect 0;
    show;
    
    pick_start_direction;
    init_history;
    
    broadcast "spawn_food";
    broadcast "spawn_bin";
    broadcast "init_body";
    broadcast "update_body";
    
    until is_dead == "да" or game_state != "игра" {
        wait 0.16;
        dir_x = next_dir_x;
        dir_y = next_dir_y;
        
        update_head_look;
        calculate_next_position;
        check_self_collision;
        
        if is_dead == "да" {
            handle_death;
        }
        if is_dead != "да" {
            apply_move;
            check_trash_pickup;
            check_bin_penalty;
        }
    }
}

onflag { hide; }
on "open_menu" { hide; }
on "open_settings" { hide; }
on "game_over" { hide; }
on "game_win" { hide; }
