import copy
import pygame
import socket

numWin = 4

lines = 6
rows = 7

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500

SERVER_IP = '0.0.0.0'
CLIENT_IP = '127.0.0.1'
PORT = 5001

isRed = False

my_socket = socket.socket()
server_socket = socket.socket()

try:
    my_socket.connect((CLIENT_IP, PORT))
    print("you blue")
    isRed = False
except:
    server_socket.bind((SERVER_IP, PORT))
    server_socket.listen(1)
    print("\nWaiting for the opponent...")
    (client_socket, client_address) = server_socket.accept()
    isRed = True
    print("you red")


def main():
    global rows
    global lines
    global numWin

    global WINDOW_WIDTH
    global WINDOW_HEIGHT

    board = []
    createBoard(board)

    win = False
    drow = False
    sum = 0

    pygame.init()
    size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Game")

    finish = False
    isEnd = False
    RED = (255, 0, 0)
    paint(screen, WINDOW_WIDTH, WINDOW_HEIGHT, RED)
    sum_t = 1

    while not finish and not isEnd:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True

            if sum_t % 2 == 0 and not isRed:
                # print('a')
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos_x = pygame.mouse.get_pos()[0] // (WINDOW_WIDTH // rows)
                    user = 2

                    putBoard(board, screen, user, pos_x, my_socket, True)
                    sum_t += 1
            elif sum_t % 2 == 1 and isRed:
                # print('b')
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos_x = pygame.mouse.get_pos()[0] // (WINDOW_WIDTH // rows)
                    user = 1

                    putBoard(board, screen, user, pos_x, client_socket, True)
                    sum_t += 1
            elif isRed and sum_t % 2 == 0:
                pos_client = client_socket.recv(1).decode()
                pos_client = int(pos_client)
                user = 2

                # putBoard(board, screen, user, pos_client, client_socket, False)

                y = manage(board, pos_client, user)


                if y != -1:
                    pos = (((WINDOW_WIDTH//rows) * pos_client) + ((WINDOW_WIDTH//rows)//2), ((WINDOW_HEIGHT//lines) * y) + ((WINDOW_HEIGHT//lines)//2))


                    drawCircle(screen, pos, (0, 0, 255))

                    sum_t += 1
                    win = isWin(board, user)
                    if win:
                        isEnd = True
                        print('winner', user)
                pygame.event.clear()

            elif not isRed and sum_t % 2 == 1:
                pos_client = my_socket.recv(1).decode()
                pos_client = int(pos_client)
                user = 1

                # putBoard(board, screen, user, pos_client, my_socket, False)

                y = manage(board, pos_client, user)

                if y != -1:
                    pos = (((WINDOW_WIDTH//rows) * pos_client) + ((WINDOW_WIDTH//rows)//2), ((WINDOW_HEIGHT//lines) * y) + ((WINDOW_HEIGHT//lines)//2))
                    drawCircle(screen, pos, (255, 0, 0))

                    sum_t += 1
                    win = isWin(board, user)
                    if win:
                        isEnd = True
                        print('winner', user)
                pygame.event.clear()


    isClose = False
    while not isClose:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == 13:
                    isClose = True
                    pygame.quit()


def manage(board, x, user):
    insert_x = -1
    copyBoard = copy.deepcopy(board)
    # while copyBoard == board:
    try:
        if x < 0:
            a = 1/0
        insert_y = insert(board, x, user)
        if insert_y == -1:
            return -1
        isOK = False
    except:
        board = copy.deepcopy(copyBoard)
    return insert_y


def isDrow(board):
    if not (0 in board) and not isWin(board, 1) and not isWin(board, 2):
        return True
    return False

def isWin(board, user):
    global lines
    global rows

    for i in range(lines):
        for j in range(rows):
            if isWinner(board, user, i, j):
                return True
    return False

def insert(board, row, user):
    global rows
    global lines
    for i in range(lines):
        if i == lines - 1:
            board[i][row] = user
            return i
        else:
            try:
                if board[i + 1][row] != 0:
                    if board[i][row] != 0:
                        return -1
                    board[i][row] = user
                    return i
            except:
                return -1
def createBoard(board):
    global rows
    global lines

    for line in range(lines):
        board.append([])
        for row in range(rows):
            board[-1].append(0)

def createInstructions():
    arr = []
    chars = '0+-'
    for i in chars:
        for j in chars:
            arr.append(f'{i}{j}')
    return arr[1:]

def isWinner(board, user, line, row):
    global rows
    global lines
    global numWin

    instructions = createInstructions()
    save = line, row

    for k in range(len(instructions)):
        line, row = save
        sum = 0
        for i in range(numWin):
            if 0 <= row < rows and 0 <= line < lines:
                if board[line][row] == user:
                    sum += 1
                actions = act(instructions[k], line, row)
                line, row = actions
        if sum >= numWin:
            return True
    return False

def act(act, line, row):
    all = [line, row]
    for i in range(len(all)):
        if act[i] == '0':
            all[i] += 0
        elif act[i] == '+':
            all[i] += 1
        elif act[i] == '-':
            all[i] -= 1

    return all[0], all[1]

def drawCircle(screen, pos, color):
    pygame.draw.circle(screen, color, pos, (int(WINDOW_WIDTH * 0.04)))
    pygame.display.flip()

def paint(screen, WINDOW_WIDTH, WINDOW_HEIGHT, color):
    global lines
    global rows

    space_x = WINDOW_WIDTH // (lines + 1)
    space_y = WINDOW_HEIGHT // (rows - 1)

    start_y = space_y
    end_y = space_y

    for i in range(lines - 1):
        pygame.draw.line(screen,color,[0,start_y],[WINDOW_WIDTH,end_y],4)

        start_y += space_y
        end_y += space_y

    start_x = space_x
    end_x = space_x

    for i in range(rows - 1):
        pygame.draw.line(screen,color,[start_x,0],[end_x,WINDOW_HEIGHT],4)

        start_x += space_x
        end_x += space_x


    pygame.display.flip()

def putBoard(board, screen, user, pos_x, my_socket, isSend):
    # print("a-1")
    color = (0, 0, 0)
    if user == 1:
        color = (255, 0, 0)
    else:
        color = (0, 0, 255)
    y = manage(board, pos_x, user)
    # print("a-2")

    if y != -1:
        pos = (((WINDOW_WIDTH//rows) * pos_x) + ((WINDOW_WIDTH//rows)//2), ((WINDOW_HEIGHT//lines) * y) + ((WINDOW_HEIGHT//lines)//2))
        drawCircle(screen, pos, color)
        # print("a-3")
        win = isWin(board, user)
        # print("a-4")
        if isSend:
            my_socket.send(str(pos_x).encode())
            # print("a-5")
        # print("a-6")
        if win:
            isEnd = True
            print('winner', user)
    pygame.event.clear()

if __name__ == '__main__':
    try:
        main()
    except:
        pass
