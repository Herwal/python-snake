from uib_inf100_graphics.event_app import run_app
from snake_view import draw_board
import random as rd


def app_started(app):
    # Modellen.
    # Denne funksjonen kalles én gang ved programmets oppstart.
    # Her skal vi __opprette__ variabler i som behøves i app.
    app.direction = "east"
    app.debug_mode = True
    app.apples = 0  # Tellar for antall epler spist
    app.board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 2, 3, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    add_apple_at_random_location(app.board, app)  # Startar med random eple
    app.snake_size = 3
    app.head_pos = (3, 4)
    app.state = "active"
    app.timer_delay = 200


def is_legal(pos: tuple, board: list):  # Sjekker om neste pos er gyldig
    a, b = pos
    if (
        a >= len(board)  # Sjekker venstre og høgre
        or a < 0
        or b >= len(board[0])  # Sjekker topp og botn
        or b < 0
        or board[a][b] >= 1  # sjekker at nestre rute er gyldig
    ):
        return False

    return True


def add_apple_at_random_location(board: list, app):  # Legger til nytt eple dersom ledig
    counter = 0
    max_attempts = len(board) * len(board[0])

    a = rd.choice(range(len(board)))
    b = rd.choice(range(len(board[0])))
    while counter < max_attempts:
        a = rd.choice(range(len(board)))
        b = rd.choice(range(len(board[0])))
        try:
            if board[a][b] == 0:
                board[a][b] = -1
                app.apples += 1
                return
        except IndexError:
            pass
        counter += 1
    raise RuntimeError("No available space for apple after max attempts")


def timer_fired(app):
    # En kontroller.
    # Denne funksjonen kalles ca 10 ganger per sekund som standard.
    # Funksjonen kan __endre på__ eksisterende variabler i app.
    if app.debug_mode == False and app.state == "active":  # kjører "automatisk"
        move_snake(app)


def key_pressed(app, event):  # Styrer taste trykk
    # En kontroller.
    # Denne funksjonen kalles hver gang brukeren trykker på tastaturet.
    # Funksjonen kan __endre på__ eksisterende variabler i app.
    if app.state == "active":
        if app.debug_mode:
            if event.key == "Space":
                move_snake(app)
                app.direction = "east"
        if event.key == "d":
            app.debug_mode = not app.debug_mode

        elif event.key == "Up":
            app.direction = "north"
        elif event.key == "Down":
            app.direction = "south"
        elif event.key == "Left":
            app.direction = "west"
        elif event.key == "Right":
            app.direction = "east"

    elif app.state == "gameover":
        if event.key == "d":
            if app.debug_mode:
                app.debug_mode = not app.debug_mode
        if event.key == "r":
            run_app(width=800, height=600, title="Snake")


def substract_one_from_all_positives(board):  # oppdaterer brettet tilbake til 0
    for rows in range(len(board)):
        for cols in range(len(board[0])):
            if board[rows][cols] > 0:
                board[rows][cols] = board[rows][cols] - 1


# Henter neste head_pos
def get_next_head_pos(head_pos: tuple, direction: str, board: list):
    r, c = head_pos
    new_head_pos = head_pos

    if direction == "east":
        if c + 1 < len(board[0]):
            new_head_pos = (r, c + 1)

    elif direction == "west":
        if c - 1 >= 0:
            new_head_pos = (r, c - 1)

    elif direction == "north":
        if r - 1 >= 0:
            new_head_pos = (r - 1, c)

    elif direction == "south":
        if r + 1 < len(board):
            new_head_pos = (r + 1, c)

    return new_head_pos


def move_snake(app):  # Flyttar slangen
    app.head_pos = get_next_head_pos(app.head_pos, app.direction, app.board)
    a, b = app.head_pos

    if not is_legal(app.head_pos, app.board):
        app.state = "gameover"
        return

    if app.board[a][b] == -1:
        app.board[a][b] = 0
        app.snake_size += 1
        if app.timer_delay > 80:
            app.timer_delay -= 10
        add_apple_at_random_location(app.board, app)

    substract_one_from_all_positives(app.board)

    app.board[a][b] = app.snake_size


def redraw_all(app, canvas):  # Tegnar canvas
    # Visningen.
    # Denne funksjonen tegner vinduet. Funksjonen kalles hver gang
    # modellen har endret seg, eller vinduet har forandret størrelse.
    # Funksjonen kan __lese__ variabler fra app, men har ikke lov til
    # å endre på dem.

    if app.debug_mode:  # Kun i debug_mode
        canvas.create_text(
            250,
            10,
            text=f"app.head_pos={app.head_pos}, app.snake_size={app.snake_size}, app.direction={app.direction}, app.state={app.state}",
        )
    else:  # Ikkje debug mode
        canvas.create_text(app.width / 2, 10, text=f"Apples eaten: {app.apples}")

    if app.state == "active":
        draw_board(
            canvas,
            25,
            25,
            app.width - 25,
            app.height - 25,
            app.board,
            app.debug_mode,
        )

    elif app.state == "gameover":
        canvas.create_text(
            app.width / 2,
            app.height / 2,
            text=f"Game Over",
            font=("Comic sans MS", 40),
        )
        canvas.create_text(
            app.width / 2,
            app.height / 1.5,
            text=f"Press R to restart",
            font=("Comic sans MS", 20),
        )


run_app(width=800, height=600, title="Snake")
