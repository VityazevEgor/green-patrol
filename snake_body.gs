costumes "assets/costumes/segment_1.svg",
         "assets/costumes/segment_2.svg",
         "assets/costumes/segment_3.svg";

var seg_id = 0;
var cur_clones = 0;

onflag {
    seg_id = 0;
    cur_clones = 0;
    hide;
}

# 1. Создание звеньев хвоста (выполняет только спрайт-оригинал с seg_id == 0)
proc create_segments {
    until cur_clones >= snake_len {
        cur_clones += 1;
        seg_id = cur_clones;
        clone;
        seg_id = 0;
    }
}

# 2. Обновление внешнего вида и позиции одного клона-звена (выполняет клон с seg_id > 0)
proc update_clone_segment {
    # Активное звено в пределах длины змейки
    if seg_id <= snake_len {
        show;
        
        # Чередование трех цветов костюмов напрямую по номеру без лишних переменных
        switch_costume (((seg_id - 1) % 3) + 1);
        
        # Перемещение по истории координат
        if (seg_id + 1) <= length hist_x {
            goto hist_x[seg_id + 1], hist_y[seg_id + 1];
            
            # Анимация проглатывания мусора
            if x_position() == last_eat_x and y_position() == last_eat_y {
                set_size 125;
            }
            if x_position() != last_eat_x or y_position() != last_eat_y {
                set_size 100;
            }
        }
    }
    
    # Лишние звенья при штрафе мусорной корзины скрываются
    if seg_id > snake_len {
        hide;
    }
}

# 3. Очистка клонов при смене состояния игры
proc cleanup_body {
    if seg_id > 0 {
        delete_this_clone;
    }
    if seg_id == 0 {
        cur_clones = 0;
        hide;
    }
}

on "init_body" {
    if seg_id == 0 {
        create_segments;
    }
}

on "update_body" {
    if seg_id == 0 {
        create_segments;
    }
    if seg_id > 0 {
        update_clone_segment;
    }
}

on "start_game" { cleanup_body; }
on "open_menu" { cleanup_body; }
on "open_settings" { cleanup_body; }
on "game_over" { cleanup_body; }
on "game_win" { cleanup_body; }
