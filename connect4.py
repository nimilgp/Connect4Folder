def playgame(pygame, screen, colour1, colour2, player1, player2,starter):
    import numpy as np
    import random as r
    import math
    import sys
    import Menu
    import OperateDB


    # Variables
    COLUMNS = 7
    ROWS = 6
    CONNECT = 4

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    COIN_COLOURS = {"RED": (255, 0, 0), "BLUE": (0, 0, 255), "ORANGE": (255, 69, 0), "GREEN": (0, 240, 25),
                    "VIOLET": (238, 130, 238), "INDIGO": (75, 0, 130), "YELLOW": (255, 255, 0)}

    PLAYER_1_NAME = player1
    PLAYER_2_NAME = player2

    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2

    if colour1 != colour2:
        COLOUR1 = COIN_COLOURS[colour1.upper()]
        COLOUR2 = COIN_COLOURS[colour2.upper()]
    else:
        COLOUR1 = (r.choice(list(COIN_COLOURS.values())))
        COLOUR2 = (r.choice(list(COIN_COLOURS.values())))
    BOARD_COLOUR = BLACK
    BACK_GRD_COLOUR = WHITE




    def make_board():
        # makes a 2D array ROWS X COLUMNS
        # filled with zeroes and returns
        board = np.zeros((ROWS, COLUMNS))
        return board

    def display_board(board):
        # numpy numbers from the top
        # flips the 2D array along x-axis
        return np.flip(board, axis=0)

    def fix_piece(board, row, col, PLAYER):
        # replaces that spot with the piece
        board[row][col] = PLAYER

    def where_piece_falls(board, col):
        # returns which row in the column
        # the piece will fall into
        for i in range(ROWS):
            if board[i][col] == 0:
                return i

    def validate_move(board, col):
        # checks if the column is full
        # checks if the last row is empty in column
        return board[ROWS - 1][col] == 0

    def check_for_winner(board, PLAYER):
        # counts number of adjacent pieces
        # Horizontal check
        count = 0
        for i in range(ROWS):
            for j in range(COLUMNS):
                if PLAYER == board[i][j]:
                    count += 1
                else:
                    count = 0
                if count == CONNECT:
                    return True
            count = 0

        # Vertical check
        count = 0
        for j in range(COLUMNS):
            for i in range(ROWS):
                if PLAYER == board[i][j]:
                    count += 1
                else:
                    count = 0
                if count == CONNECT:
                    return True
            count = 0

        # Diagonal check
        def get_diagonals(array_2D):
            temp_array2 = []
            # there are rows + columns -1 number of diagonals
            for line in range(1, (ROWS + COLUMNS)):
                # start column is 0 for rows number of diagonals then it becomes line - rows
                start_col = max(0, line - ROWS)
                count = min(line, (COLUMNS - start_col), ROWS)
                temp_array1 = []
                for j in range(0, count):
                    temp_array1.append(array_2D[min(ROWS, line) - j - 1][start_col + j])
                temp_array2.append(temp_array1)
            return temp_array2

        # +ve slope
        pos_diagonal = get_diagonals(board)

        # flips the 2D array along y-axis
        flip_board = np.flip(board, axis=1)

        # -ve slope
        neg_diagonal = get_diagonals(flip_board)

        # all the diagonals
        diagonals = pos_diagonal + neg_diagonal
        count = 0
        for i in diagonals:
            for j in i:
                if j == PLAYER:
                    count += 1
                else:
                    count = 0
                if count == CONNECT:
                    return True
            count = 0

    def check_for_tie(board):
        for i in range(ROWS):
            for j in range(COLUMNS):
                if board[i][j] == 0:
                    return False
        return True

    def draw_GUI_board():
        # flipped the board
        flipped_board = display_board(board)
        # draws a large rectangle(board)
        pygame.draw.rect(screen, BOARD_COLOUR, (0, extra_rows * SQUARESIDE, COLUMNS * SQUARESIDE, ROWS * SQUARESIDE))
        for i in range(ROWS):
            for j in range(COLUMNS):
                # checks the 2D board array pieces
                # and accordingly colours in coins
                if flipped_board[i][j] == EMPTY:
                    pygame.draw.circle(screen, BACK_GRD_COLOUR, (
                        int(j * SQUARESIDE + SQUARESIDE / 2), int((i + extra_rows) * SQUARESIDE + SQUARESIDE / 2)),
                                       RADIUS)
                elif flipped_board[i][j] == PLAYER1:
                    pygame.draw.circle(screen, COLOUR1, (
                        int(j * SQUARESIDE + SQUARESIDE / 2), int((i + extra_rows) * SQUARESIDE + SQUARESIDE / 2)),
                                       RADIUS)
                elif flipped_board[i][j] == PLAYER2:
                    pygame.draw.circle(screen, COLOUR2, (
                        int(j * SQUARESIDE + SQUARESIDE / 2), int((i + extra_rows) * SQUARESIDE + SQUARESIDE / 2)),
                                       RADIUS)
        pygame.display.update()

    def coin_shadow():
        posx = event.pos[0]
        if posx % SQUARESIDE > 10 and posx % SQUARESIDE < 90:
            col = int(math.floor(posx / SQUARESIDE))
            row = where_piece_falls(board, col)
            colour = player_colour()
            pygame.draw.circle(screen, colour, (
                col * SQUARESIDE + SQUARESIDE / 2, int((extra_rows + (ROWS - row - 1)) * SQUARESIDE + SQUARESIDE / 2)),
                               RADIUS)
            pygame.draw.circle(screen, BACK_GRD_COLOUR, (
                col * SQUARESIDE + SQUARESIDE / 2, int((extra_rows + (ROWS - row - 1)) * SQUARESIDE + SQUARESIDE / 2)),
                               RADIUS / 2)
            pygame.display.update()

    def player_colour():
        # takes in player
        # gives out that players colour
        if PLAYER == PLAYER1:
            return COLOUR1
        elif PLAYER == PLAYER2:
            return COLOUR2

    def mouse_motion():
        # shows which column piece will be dropped in
        # piece is drawn on top of rectangle
        # to prevent screen from getting filled with pieces
        pygame.draw.rect(screen, BACK_GRD_COLOUR, (0, SQUARESIDE, width, SQUARESIDE * (extra_rows-1)))
        posx = event.pos[0]
        colour = player_colour()
        pygame.draw.circle(screen, colour, (posx, int(SQUARESIDE + SQUARESIDE / 2)), RADIUS)
        pygame.display.update()

    def mouse_input_playable():
        # x-coordinate of mouse
        posx = event.pos[0]
        # gives location of mouse
        # with respect to columns
        if posx % SQUARESIDE > 10 and posx % SQUARESIDE < 90:
            col = int(math.floor(posx / SQUARESIDE))
            if validate_move(board, col):
                row = where_piece_falls(board, col)
                fix_piece(board, row, col, PLAYER)
                return True

    def switch_player(PLAYER):
        # takes in player who just played
        # changes to other player
        if PLAYER == PLAYER1:
            return PLAYER2
        elif PLAYER == PLAYER2:
            return PLAYER1
        
    def current_player(PLAYER):
        if PLAYER == PLAYER1:
            current = player1
        if PLAYER == PLAYER2:
            current = player2
        pygame.draw.rect(screen, BACK_GRD_COLOUR, (0, 0, width- 2* SQUARESIDE, SQUARESIDE * (extra_rows - 1)))
        label = myfont.render(current+"'s turn", 1, BLACK)
        screen.blit(label, (40, 10))

    def put_board_into_db():
        for i in range(ROWS):
            for j in range(COLUMNS):
                OperateDB.AddSaveStateTable(j,i,board[i][j])

    def save_n_goto_menu():
        OperateDB.AddLoadVariables(colour1,colour2,PLAYER_1_NAME, PLAYER_2_NAME,PLAYER)
        put_board_into_db()
        Menu.Home()

    from pygame_widgets import Button
    button_home = Button(
        screen, 540,10, 150, 50, text='HOME',
        fontSize=50, margin=20,
        inactiveColour=(50, 50, 250),
        pressedColour=(0, 255, 0), radius=20,
        onClick = save_n_goto_menu
    )

    pygame.display.set_caption('CONNECT 4')



    # Variables for GUI
    SQUARESIDE = 100
    extra_rows = 2
    width = COLUMNS * SQUARESIDE
    height = (ROWS + extra_rows) * SQUARESIDE
    myfont = pygame.font.SysFont('freesansbold.ttf', 70)

    screen.fill(BACK_GRD_COLOUR)

    # so that the circles don't touch
    adjustment = 5
    # piece radius
    RADIUS = int(SQUARESIDE / 2 - adjustment)

    game_over = False

    # chooses who gets to start first
    if starter == 0:
        PLAYER = r.randint(1, 2)
        board = make_board()
    else:
        board = make_board()
        PLAYER = starter
        l = OperateDB.RetrieveSaveStateTable()
        for element in l:
            fix_piece(board,element[1],element[0],element[2])

    TIE = False




    # main loop
    while not game_over and not TIE:
        # get all the events
        # (eg: mouse clicks, mouse motion, key strokes etc)
        current_player(PLAYER)
        for event in pygame.event.get():
            # draws the board
            draw_GUI_board()
            button_home.listen(event)
            button_home.draw()
            pygame.display.update()
            try:
                coin_shadow()
            except:
                pass
            # quits program if (X)QUIT used
            if event.type == pygame.QUIT:
                OperateDB.AddLoadVariables(colour1, colour2, PLAYER_1_NAME, PLAYER_2_NAME, PLAYER)
                put_board_into_db()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                mouse_motion()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_input_playable():
                    draw_GUI_board()
                    if check_for_winner(board, PLAYER):
                        OperateDB.ModifyPlayerTable(PLAYER_1_NAME, PLAYER_2_NAME, PLAYER)
                        OperateDB.AddLoadVariables(colour1, colour2, PLAYER_1_NAME, PLAYER_2_NAME, PLAYER)
                        Menu.game_over(PLAYER)
                        game_over = True
                        break
                    elif check_for_tie(board):
                        PLAYER = 0
                        OperateDB.ModifyPlayerTable(PLAYER_1_NAME, PLAYER_2_NAME, PLAYER)
                        OperateDB.AddLoadVariables(colour1, colour2, PLAYER_1_NAME, PLAYER_2_NAME, PLAYER)
                        Menu.game_over(PLAYER)
                        TIE = True
                    mouse_motion()
                    PLAYER = switch_player(PLAYER)


