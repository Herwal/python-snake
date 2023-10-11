# Hjelpe funksjon
def get_color(num: int, row: int, col: int):  # Styrer farge
    if num == 0:
        if (row + col) % 2 == 0:
            color = "lightgreen"  # Bakgrunn
        else:
            color = "green"
    elif num > 0:
        if num % 2 == 0:
            color = "yellow"  # Slange
        elif num % 2 != 0:
            color = "orange"
    elif num < 0:
        color = "red"  # Eple
    return color


def draw_board(  # Tegner brette
    canvas, x1: int, y1: int, x2: int, y2: int, board: list, debug_mode: bool
):
    width = (x2 - x1) / len(board[0])
    height = (y2 - y1) / len(board)

    for rows in range(len(board)):
        for cols in range(len(board[0])):
            color = get_color(board[rows][cols], rows, cols)
            cell_x1 = x1 + width * cols
            cell_x2 = cell_x1 + width
            cx = (cell_x1 + cell_x2) / 2

            cell_y1 = y1 + height * rows
            cell_y2 = cell_y1 + height
            cy = (cell_y1 + cell_y2) / 2

            canvas.create_rectangle(
                cell_x1,
                cell_y1,
                cell_x2,
                cell_y2,
                fill=color,
            )

            if debug_mode:
                canvas.create_text(
                    cx,
                    cy,
                    text=f"{rows},{cols} \n{board[rows][cols]}",
                    fill="black",
                )
