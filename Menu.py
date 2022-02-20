import connect4
import pygame
import pygame_menu
import OperateDB

pygame.init()
screen = pygame.display.set_mode((700, 800))
pygame.display.set_caption('CONNECT 4')

colour1 = 'Yellow'
colour2 = 'Red'
player1 = "player 1"
player2 = "player 2"
stat_val = ('none selected',"nil", "nil", "nil","nil", "nil")

colours = [('Yellow', 1), ('Blue', 2), ("Violet", 3), ('Red', 4), ('Orange', 5), ('Green', 6), ('Indigo', 7)]


def Home():
    HomeMenu = pygame_menu.Menu(height=800,
                                width=700,
                                theme=pygame_menu.themes.THEME_BLUE,
                                title="                          Connect4                          ")

    HomeMenu.add_button("Start Game", start_game)
    HomeMenu.add_button("Continue", continue_game)
    HomeMenu.add_button("How To Play", how_to_play)
    HomeMenu.add_button("Leader board", leaderboard)
    HomeMenu.add_button("Stats", stats)
    HomeMenu.mainloop(screen)


def start_game():
    start_gameMenu = pygame_menu.Menu(height=800,
                                      width=700,
                                      theme=pygame_menu.themes.THEME_BLUE,
                                      title="Start Game")
    start_gameMenu.add_text_input('Enter Name: ', default='Player 1', onchange=player_1_name)
    start_gameMenu.add_selector('Coin Colour 1:', colours, 0, onchange=set_colour1)
    start_gameMenu.add_label("")
    start_gameMenu.add_text_input('Enter Name: ', default='Player 2', onchange=player_2_name)
    start_gameMenu.add_selector('Coin Colour 2:', colours, 3, onchange=set_colour2)
    start_gameMenu.add_label("")
    start_gameMenu.add_button("Play Game", play_the_game)
    start_gameMenu.add_label("")
    start_gameMenu.add_button('Home', Home)

    start_gameMenu.mainloop(screen)


def player_1_name(value):
    global player1
    player1 = value


def player_2_name(value):
    global player2
    player2 = value

def set_colour1(value,colour):
    global colour1
    colour1 = value[0]


def set_colour2(value,colour):
    global colour2
    colour2 = value[0]


def play_the_game():
    OperateDB.AddToPlayerTable(player1)
    OperateDB.AddToPlayerTable(player2)
    connect4.playgame(pygame, screen, colour1, colour2, player1, player2,0)


def continue_game():
    l=OperateDB.GetLoadVariables()
    print(l)
    connect4.playgame(pygame, screen,l[0],l[1],l[2],l[3],l[4])

def how_to_play():
    how_to_playMenu = pygame_menu.Menu(height=800,
                             width=700,
                             theme=pygame_menu.themes.THEME_BLUE,
                             title="How to Play")
    how_to_playMenu.add_label("")
    how_to_playMenu.add_label("")
    how_to_playMenu.add_label("")
    how_to_playMenu.add_label("Be the first person to connect 4 of your coins. ")
    how_to_playMenu.add_label("Vertically or")
    how_to_playMenu.add_label("Horizontally or")
    how_to_playMenu.add_label("Diagonally.")
    how_to_playMenu.add_label("")
    how_to_playMenu.add_label("")
    how_to_playMenu.add_button("Next", vertical)
    how_to_playMenu.mainloop(screen)


def vertical():
    VerticalMenu = pygame_menu.Menu(height=800,
                                    width=700,
                                    theme=pygame_menu.themes.THEME_BLUE,
                                    title="How to Play")
    VerticalMenu.add_label("Yellow wins by connecting 4 vertically.")
    VerticalMenu.add_image(image_path="images/vertical.png", scale=(1 / 3, 1 / 3))
    VerticalMenu.add_label("")
    VerticalMenu.add_button("Next", horizontal)
    VerticalMenu.add_button("Back", how_to_play)
    VerticalMenu.mainloop(screen)


def horizontal():
    HorizontalMenu = pygame_menu.Menu(height=800,
                                      width=700,
                                      theme=pygame_menu.themes.THEME_BLUE,
                                      title="How to Play")
    HorizontalMenu.add_label("Yellow wins by connecting 4 horizontally.")
    HorizontalMenu.add_image(image_path="images/horizontal.png", scale=(1 / 3, 1 / 3))
    HorizontalMenu.add_label("")
    HorizontalMenu.add_button("Next", diagonal)
    HorizontalMenu.add_button("Back", vertical)
    HorizontalMenu.mainloop(screen)


def diagonal():
    DiagonalMenu = pygame_menu.Menu(height=800,
                                    width=700,
                                    theme=pygame_menu.themes.THEME_BLUE,
                                    title="How to Play")
    DiagonalMenu.add_label("Yellow wins by connecting 4 diagonally.")
    DiagonalMenu.add_image(image_path="images/diagonal.png", scale=(1 / 3, 1 / 3))
    DiagonalMenu.add_label("")
    DiagonalMenu.add_button("Home", Home)
    DiagonalMenu.add_button("Back", horizontal)
    DiagonalMenu.mainloop(screen)


def leaderboard():
    leaderboardMenu = pygame_menu.Menu(height=800,
                             width=700,
                             theme=pygame_menu.themes.THEME_BLUE,
                             title="Leaderboard")
    l=OperateDB.RetrieveLeaderBoard()
    leaderboardMenu.add_label("(NAME  |  ELO SCORE)")
    for element in l:
        leaderboardMenu.add_label(element)
    leaderboardMenu.add_button('Home', Home)
    leaderboardMenu.mainloop(screen)

def stats():
    StatsMenu = pygame_menu.Menu(height=800,
                             width=700,
                             theme=pygame_menu.themes.THEME_BLUE,
                             title="Stats")
    StatsMenu.add_text_input('Enter Name: ', default='Player', onchange=player_stats)
    StatsMenu.add_button('Search', search)
    StatsMenu.add_button('Home', Home)

    StatsMenu.mainloop(screen)

def player_stats(value):
    global stat_val
    stat_val = OperateDB.RetrievePlayerTable(value)
    print(stat_val)

def search():
    SearchMenu = pygame_menu.Menu(height=800,
                             width=700,
                             theme=pygame_menu.themes.THEME_BLUE,
                             title="Stats")
    try:
        SearchMenu.add_label("name : " + str(stat_val[0]))
        SearchMenu.add_label("elo score : " + str(stat_val[1]))
        SearchMenu.add_label("games played : " + str(stat_val[2]))
        SearchMenu.add_label("games won : " + str(stat_val[3]))
        SearchMenu.add_label("games lost : " + str(stat_val[4]))
        SearchMenu.add_label("games tied : " + str(stat_val[5]))
    except :
        SearchMenu.add_label("No such player")
    SearchMenu.add_button('Back', stats)
    SearchMenu.add_button('Home', Home)

    SearchMenu.mainloop(screen)

def game_over(outcome):
    GameOverMenu = pygame_menu.Menu(height=800,
                                width=700,
                                theme=pygame_menu.themes.THEME_BLUE,
                                title="Game Over")
    global l
    l = OperateDB.GetLoadVariables()
    if outcome == 1:
        GameOverMenu.add_label(l[2] + " WON!!!")
    elif outcome == 2:
        GameOverMenu.add_label(l[3] + " WON!!!")
    else:
        GameOverMenu.add_label( "It is a TIE!!!")
    GameOverMenu.add_label(" ")
    GameOverMenu.add_button("play again",play_again)
    GameOverMenu.add_label(" ")
    GameOverMenu.add_button("Home", Home)
    GameOverMenu.mainloop(screen)

def play_again():
    connect4.playgame(pygame, screen,l[0], l[1], l[2], l[3], 0)