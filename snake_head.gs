costumes "assets/costumes/head_1.svg",
         "assets/costumes/head_2.svg";

sounds "assets/sounds/trash.wav",
       "assets/sounds/bin.wav",
       "assets/sounds/crash.wav";

var dir = 90;
var next_dir = 90;
var chk_idx = 0;

# --- Управление стрелками клавиатуры (направление в градусах Scratch) ---
onkey "right arrow" {
    if game_state == "игра" and dir != -90 {
        next_dir = 90;
    }
}

onkey "left arrow" {
    if game_state == "игра" and dir != 90 {
        next_dir = -90;
    }
}

onkey "up arrow" {
    if game_state == "игра" and dir != 180 {
        next_dir = 0;
    }
}

onkey "down arrow" {
    if game_state == "игра" and dir != 0 {
        next_dir = 180;
    }
}

# --- Процедуры логики змейки ---

# 1. Заполнение начальной истории позади головы
proc init_history {
    delete hist_x;
    delete hist_y;
    add head_x to hist_x;
    add head_y to hist_y;
    repeat 5 {
        add (hist_x[length hist_x] - 20) to hist_x;
        add head_y to hist_y;
    }
}

# 2. Шаг головы по направлению с точным смещением и заворот через край экрана
proc step_head {
    if dir == 90 { change_x 20; }
    if dir == -90 { change_x -20; }
    if dir == 0 { change_y 20; }
    if dir == 180 { change_y -20; }
    
    if x_position() > 230 { set_x -230; }
    if x_position() < -230 { set_x 230; }
    if y_position() > 170 { set_y -170; }
    if y_position() < -170 { set_y 170; }
    
    head_x = x_position();
    head_y = y_position();
}

# 3. Проверка столкновения со своим хвостом (начиная со 2-го звена)
proc check_self_collision {
    chk_idx = 2;
    repeat snake_len {
        if chk_idx <= length hist_x and hist_x[chk_idx] == head_x and hist_y[chk_idx] == head_y {
            goto hist_x[1], hist_y[1];
            head_x = hist_x[1];
            head_y = hist_y[1];
            handle_death;
        }
        chk_idx += 1;
    }
}

# 4. Анимация гибели при столкновении
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

# 5. Запись новой позиции головы в историю для звеньев тела
proc record_history {
    insert head_x at hist_x[1];
    insert head_y at hist_y[1];
    
    until length hist_x <= snake_len + 5 {
        delete hist_x[length hist_x];
        delete hist_y[length hist_y];
    }
    
    broadcast "update_body";
}

# 6. Проверка сбора мусора
proc check_trash_pickup {
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

# 7. Проверка попадания в мусорную корзину (штраф)
proc check_bin_penalty {
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
    last_eat_x = 9999;
    last_eat_y = 9999;
    head_x = 10;
    head_y = 10;
    goto head_x, head_y;
    set_ghost_effect 0;
    show;
    
    dir = 90;
    next_dir = 90;
    point_in_direction dir;
    init_history;
    
    broadcast "spawn_food";
    broadcast "spawn_bin";
    broadcast "init_body";
    broadcast "update_body";
    
    until game_state != "игра" {
        wait 0.16;
        dir = next_dir;
        point_in_direction dir;
        next_costume;
        
        step_head;
        check_self_collision;
        
        if game_state == "игра" {
            record_history;
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
