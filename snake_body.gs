costumes "assets/costumes/segment_1.svg",
         "assets/costumes/segment_2.svg",
         "assets/costumes/segment_3.svg";

var seg_id = 0;
var cur_clones = 0;
var is_clone = 0;
var cost_idx = 0;
var p_idx = 0;

onflag {
    is_clone = "нет";
    cur_clones = 0;
    hide;
}

onclone {
    is_clone = "да";
}

# 1. Создание нужного количества звеньев хвоста
nowarp proc create_segments {
    until cur_clones >= snake_len {
        cur_clones = cur_clones + 1;
        seg_id = cur_clones;
        clone;
    }
}

# 2. Обновление внешнего вида и позиции одного клона-звена
nowarp proc update_clone_segment {
    # Активное звено в пределах длины змейки
    if seg_id <= snake_len {
        show;
        
        # Чередование костюмов трех цветов
        cost_idx = ((seg_id - 1) % 3) + 1;
        if cost_idx == 1 { switch_costume "segment_1"; }
        if cost_idx == 2 { switch_costume "segment_2"; }
        if cost_idx == 3 { switch_costume "segment_3"; }
        
        # Перемещение по истории координат
        p_idx = seg_id + 1;
        if p_idx <= length hist_x {
            goto hist_x[p_idx], hist_y[p_idx];
            
            # Анимация проглатывания мусора
            if x_position() == last_eat_x and y_position() == last_eat_y {
                set_size 125;
            }
            if x_position() != last_eat_x or y_position() != last_eat_y {
                set_size 100;
            }
        }
    }
    
    # Лишние звенья при уменьшении длины змейки скрываются
    if seg_id > snake_len {
        hide;
    }
}

# 3. Очистка клонов при перезапуске или выходе
nowarp proc cleanup_body {
    if is_clone == "да" {
        delete_this_clone;
    }
    if is_clone == "нет" {
        cur_clones = 0;
        hide;
    }
}

on "init_body" {
    if is_clone == "нет" {
        create_segments;
    }
}

on "update_body" {
    if is_clone == "нет" {
        create_segments;
    }
    if is_clone == "да" {
        update_clone_segment;
    }
}

on "start_game" { cleanup_body; }
on "open_menu" { cleanup_body; }
on "open_settings" { cleanup_body; }
on "game_over" { cleanup_body; }
on "game_win" { cleanup_body; }
