import curses
import time
import random


def display_menu(stdscr, selected_option):
    """Отображает меню с кнопками."""
    stdscr.clear()
    
    # Отображаем название игры
    title = [
 "▄▀▀█▄▄   ▄▀▀▀▀▄   ▄▀▀▀▀▄      ▄▀▀▀▀▄          ▄▀▀▀▀▄    ▄▀▀█▄   ▄▀▀▄ ▄▀▄  ▄▀▀█▄▄▄▄", 
"▐ ▄▀   █ █      █ █    █      █    █          █         ▐ ▄▀ ▀▄ █  █ ▀  █ ▐  ▄▀   ▐", 
  "█▄▄▄▀  █      █ ▐    █      ▐    █          █    ▀▄▄    █▄▄▄█ ▐  █    █   █▄▄▄▄▄ ", 
  "█   █  ▀▄    ▄▀     █           █           █     █ █  ▄▀   █   █    █    █    ▌ ", 
 "▄▀▄▄▄▀    ▀▀▀▀     ▄▀▄▄▄▄▄▄▀   ▄▀▄▄▄▄▄▄▀     ▐▀▄▄▄▄▀ ▐ █   ▄▀  ▄▀   ▄▀    ▄▀▄▄▄▄  ", 
"█    ▐              █           █             ▐         ▐   ▐   █    █     █    ▐  ", 
"▐                   ▐           ▐                               ▐    ▐     ▐      "  
                                                                                                                         
                                                                                                                         

  ]
    
    # Проверяем ширину терминала
    max_width = curses.COLS
    for i, line in enumerate(title):
        if len(line) > max_width:
            line = line[:max_width]  # Обрезаем строку, если она слишком длинная
        stdscr.addstr(curses.LINES // 2 - 3 + i, (max_width - len(line)) // 2, line)

    options = ["Начать новую игру", "Выход"]
    
    for idx, option in enumerate(options):
        if idx == selected_option:
            stdscr.addstr(curses.LINES // 2 + 3 + idx, (max_width - len(option)) // 2, option, curses.A_REVERSE)  # Выделяем активную опцию
        else:
            stdscr.addstr(curses.LINES // 2 + 3 + idx, (max_width - len(option)) // 2, option)

    stdscr.refresh()

def main(stdscr):
    # Настройка окна
    curses.curs_set(0)  # Скрыть курсор
    stdscr.nodelay(1)   # Не блокировать ввод
    stdscr.timeout(100) # Устанавливаем таймаут для ввода

    selected_option = 0  # Индекс выбранной опции в меню

    # Список лиц
    faces = [
        "  (| |)    ",  # Нормальное лицо
        " ( | |) ",  # Руки
        "  (| | )    ",  # Улыбающееся лицо (слева)
        "  O__O    ",  # Удивленное лицо
        "  -__-    ",  # Уставшее лицо
        "  .__.    ",  # Лицо внизу
    ]
    face_index = 0  # Индекс текущего лица

    # Список случайных фраз
    phrases = [
        "Эй спойкойно",
        "Не стреляй",
        "Хватит!",
        "Узбогойся!ахахх не актуально да?",
        "Я дам тебе много денег! 3 копейки и плевок в лицо!",
        "Пошёл ты!",
        "Иди ты на@#%! Что за символы?",
        "Давай ты вскро@#%@$"

    ]

    last_phrase_time = time.time()  # Время последнего произнесения фразы
    phrase_interval = 5  # Интервал между фразами
    phrase_display_time = 3  # Время отображения фразы

    current_phrase = ""  # Текущая фраза
    phrase_start_time = 0  # Время начала отображения фразы

    while True:
        display_menu(stdscr, selected_option)

        key = stdscr.getch()
        if key == curses.KEY_UP and selected_option > 0:
            selected_option -= 1
        elif key == curses.KEY_DOWN and selected_option < 1:
            selected_option += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:  # Enter key
            if selected_option == 0:
                # Начинаем новую игру
                ball_x = random.randint(1, curses.COLS - 2)  # Случайная позиция по X
                ball_y = curses.LINES - 2  # Начальная позиция мяча по Y
                ball_dx = 1  # Направ ление мяча по X
                ball_dy = -1  # Направление мяча по Y (вверх)

                paddle_x = curses.COLS // 2 - 3  # Начальная позиция платформы
                paddle_y = curses.LINES - 1  # Позиция платформы по Y

                face_x = curses.COLS // 2 - 5  # Позиция лица по X
                face_y = 1  # Позиция лица по Y
                face_hp = 5  # Здоровье лица

                while True:
                    stdscr.clear()  # Очищаем экран

                    # Изменяем лицо в зависимости от положения мяча
                    if ball_x < face_x:
                        face_index = 2  # Улыбающееся лицо (слева)
                    elif ball_x > face_x + 5:
                        face_index = 1  # Руки (справа)
                    elif ball_y == paddle_y + 1:
                        face_index = 5  # Лицо внизу
                    else:
                        face_index = 0  # Нормальное лицо

                    # Отображаем лицо
                    stdscr.addstr(face_y, face_x, faces[face_index])  # Отображаем текущее лицо

                    # Отображаем здоровье лица
                    stdscr.addstr(face_y - 1, face_x, f"HP: {face_hp}", curses.A_BOLD)

                    # Отображаем мяч
                    if 0 <= ball_y < curses.LINES and 0 <= ball_x < curses.COLS:
                        stdscr.addstr(ball_y, ball_x, '@')

                    # Отображаем платформу
                    if 0 <= paddle_y < curses.LINES and 0 <= paddle_x < curses.COLS - 7:
                        stdscr.addstr(paddle_y, paddle_x, '=' * 7)

                    # Проверка времени для произнесения фразы
                    current_time = time.time()
                    if current_time - last_phrase_time >= phrase_interval:
                        current_phrase = random.choice(phrases)
                        phrase_start_time = current_time  # Запоминаем время начала отображения фразы
                        last_phrase_time = current_time  # Обновляем время последнего произнесения

                    # Проверка времени для отображения фразы
                    if current_time - phrase_start_time < phrase_display_time:
                        stdscr.addstr(face_y + 3, face_x, current_phrase)  # Отображаем фразу ниже лица

                    # Обновляем экран
                    stdscr.refresh()

                    # Обработка ввода
                    key = stdscr.getch()
                    if key == curses.KEY_LEFT and paddle_x > 0:
                        paddle_x -= 2  # Увеличиваем скорость платформы
                    elif key == curses.KEY_RIGHT and paddle_x < curses.COLS - 8:
                        paddle_x += 2  # Увеличиваем скорость платформы
                    elif key == ord('q'):
                        return

                    # Обновляем позицию мяча
                    ball_x += ball_dx
                    ball_y += ball_dy

                    # Проверка на столкновение с границами
                    if ball_x <= 0 or ball_x >= curses.COLS - 1:
                        ball_dx *= -1  # Отскок от стенки
                    if ball_y <= 0:
                        ball_dy *= -1  # Отскок от верхней границы
                    if ball_y == paddle_y - 1 and paddle_x <= ball_x <= paddle_x + 6:
                        ball_dy *= -1  # Отскок от платформы
                    elif ball_y >= curses.LINES:
                        break  # Мяч упал ниже платформы, игра окончена

                    # Проверка на столкновение с лицом
                    if face_y <= ball_y <= face_y + 2 and face_x <= ball_x <= face_x + 5:
                        ball_dy *= -1  # Отскок от лица
                        ball_y = face_y + 2  # Сбрасываем мяч на уровень лица
                        face_hp -= 1  # Уменьшаем здоровье лица
                        if face_hp <= 0:
                            stdscr.clear()
                            stdscr.addstr(curses.LINES // 2, curses.COLS // 2 - 5, "Вы победили!")
                            stdscr.refresh()
                            time.sleep(2)
                            break

                    time.sleep(0.01)  # Задержка для управления скоростью игры

                # Игра окончена, отображаем сообщение "Game Over"
                stdscr.clear()
                stdscr.addstr(curses.LINES // 2, curses.COLS // 2 - 5 , "Game Over")
                stdscr.addstr(curses.LINES // 2 + 1, curses.COLS // 2 - 15, "Нажмите 'r' для рестарта или 'q' для выхода.")
                stdscr.refresh()

                while True:
                    key = stdscr.getch()
                    if key == ord('r'):
                        break  # Перезапускаем игру
                    elif key == ord('q'):
                        return  # Выход из игры

            elif selected_option == 1:
                break  # Выход из программы

curses.wrapper(main)