# 1. Используемые переменные:
# Локальные переменные:
# - dir: текущее направление движения головы в градусах Scratch (90 - вправо, -90 - влево, 0 - вверх, 180 - вниз).
# - next_dir: буфер следующего направления, задаваемый стрелками клавиатуры.
# - chk_idx: счетчик цикла для проверки столкновения с собственным хвостом.
# Глобальные переменные:
# - game_state: текущее состояние игры (проверка режима игры).
# - score: текущий счет игры, увеличивается при сборе мусора и уменьшается в корзине.
# - snake_len: текущая длина змейки.
# - head_x, head_y: координаты головы змейки на сетке поля.
# - food_type: тип съеденного мусора для начисления очков.
# - last_eat_x, last_eat_y: точка сбора мусора для анимации проглатывания телом.
# - cell_size: размер клетки поля (20 px или 30 px) для шага и проверки границ.
# Глобальные списки:
# - hist_x, hist_y: история координат головы, куда добавляется каждый новый шаг.
#
# 2. Описание логики работы этого спрайта:
# Спрайт считывает нажатия стрелок клавиатуры, перемещает голову по сетке с шагом cell_size,
# переносит змейку через противоположные края экрана, проверяет сбор мусора, попадание в корзину
# и столкновение с собственным хвостом.

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
        add (hist_x[length hist_x] - cell_size) to hist_x;
        add head_y to hist_y;
    }
}

# 2. Шаг головы по направлению с точным смещением и заворот через край экрана
proc step_head {
    if dir == 90 { change_x cell_size; }
    if dir == -90 { change_x (0 - cell_size); }
    if dir == 0 { change_y cell_size; }
    if dir == 180 { change_y (0 - cell_size); }
    
    if x_position() > (240 - cell_size / 2) { set_x (-240 + cell_size / 2); }
    if x_position() < (-240 + cell_size / 2) { set_x (240 - cell_size / 2); }
    if y_position() > (180 - cell_size / 2) { set_y (-180 + cell_size / 2); }
    if y_position() < (-180 + cell_size / 2) { set_y (180 - cell_size / 2); }
    
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
    head_x = cell_size / 2;
    head_y = cell_size / 2;
    goto head_x, head_y;
    set_size (cell_size * 5);
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
