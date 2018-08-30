
from console_graphics import *
from time import sleep

class Color:
    BLACK = 0
    WHITE = 1





class Stone:
    STR = "⬤"

    def __init__(self, color = Color.BLACK):
        self.color = color

    def __eq__(self, other):
        if(type(other) != Stone):
            return False

        return self.color == other.color
        
    def __str__(self):
        return STR

    def reverse(self):
        self.color ^= 0x01

    def copy(source):
        return Stone(source.color)




"""   
 -→ x
↓
y


"""
class Board:


    # [上, 右上, 右, 右下, 下, 左下, 左, 左上]
    DIRECTION_MAP = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]


    STONE_INTERVAL = ""
    
    def __init__(self, rows = 8, cols = 8):
        self.rows = rows
        self.cols = cols

        # stones[row][col]
        # stones[y][x]
        self.stones = [[None for col in range(self.cols)] for row in range(self.rows)]
    
        self.just_put_stone(Stone(Color.WHITE), 3, 3)
        self.just_put_stone(Stone(Color.WHITE), 4, 4)
        self.just_put_stone(Stone(Color.BLACK), 3, 4)
        self.just_put_stone(Stone(Color.BLACK), 4, 3)
        

    
    def copy(source):
        board = Board(source.rows, source.cols)

        for i in range(source.rows):
            for j in range(source.cols):
                if(source.stones[i][j] is None):
                    board.stones[i][j] = None
                else:
                    board.stones[i][j] = Stone.copy(source.stones[i][j])

        return board


    
    def print(self):

        line = Graphics.Figure.BLACK + "|" + Graphics.Figure.DEFAULT
        black_stone = Graphics.Figure.BLACK + Stone.STR + Graphics.Figure.DEFAULT
        white_stone = Graphics.Figure.WHITE + Stone.STR + Graphics.Figure.DEFAULT

        print(Graphics.Background.GREEN)
        for row in range(self.rows):
            for col in range(self.cols):
                
                if(self.stones[row][col] is None):
                    print(line + "  ", end = "") 
                elif(self.stones[row][col].color == Color.WHITE):
                    print(line + white_stone + "", end = "")
                else:
                    print(line + black_stone + "", end = "")

            print(line)
    
        print(Graphics.END)


    


    # (上, 右上, 右, 右下, 下, 左下, 左, 左上)
    def count_sandwiched_stones(self, stone, position_x, position_y):
        return [self.count_sandwiched_stones_one_direction(stone, position_x, position_y, self.DIRECTION_MAP[i]) for i in range(len(self.DIRECTION_MAP))]


    def count_sandwiched_stones_one_direction(self, stone, position_x, position_y, direction):

        i = position_x
        j = position_y

        count = 0

        while(True):
            i += direction[0]
            j += direction[1]

            if(i < 0 or j < 0 or i >= self.cols or j >= self.rows or type(self.stones[j][i]) != Stone):
                return 0

            if(self.stones[j][i].color == stone.color):
                break

            count += 1

        
        return count
        


    def put_stone(self, stone, position_x, position_y, anim = False):
        if(position_x < 0 or position_x >= self.cols or position_y < 0 or position_y >= self.rows):
            return

        sandwiched_stones_count_list = self.count_sandwiched_stones(stone, position_x, position_y)

        
        self.just_put_stone(stone, position_x, position_y)

        if(anim):
            print("reversing...")
            self.print()
            sleep(0.5)

        for i in range(len(sandwiched_stones_count_list)):

            x = position_x
            y = position_y

            while(True):
                if(sandwiched_stones_count_list[i] <= 0):
                    break

                sandwiched_stones_count_list[i] -= 1

                x += self.DIRECTION_MAP[i][0]
                y += self.DIRECTION_MAP[i][1]

                self.stones[y][x].reverse()

                if(anim):
                    print("reversing...")
                    self.print()
                    sleep(0.5)






    def just_put_stone(self, stone, position_x, position_y):
        if(position_x < 0 or position_x >= self.cols or position_y < 0 or position_y >= self.rows):
            return

        self.stones[position_y][position_x] = stone
        

    def search_placeable_position(self, stone):
        position_map = {}

        for y in range(self.rows):
            for x in range(self.cols):


                if(type(self.stones[y][x]) == Stone and self.stones[y][x].color != stone.color):
                    
                    for direction in self.DIRECTION_MAP:
                        if(x + direction[0] >= 0 and x + direction[0] < self.cols \
                           and y + direction[1] >= 0 and y + direction[1] < self.rows):

                            if(self.stones[y + direction[1]][x + direction[0]] is None):
                                position_map[(x + direction[0], y + direction[1])] = True

        position_list = []

        for position in position_map:
            counts = self.count_sandwiched_stones(stone, position[0], position[1])

            for count in counts:
                if(count != 0):
                    position_list.append(position)
                    break

                                
        return position_list

    def count_stones(self, stone):
        count = 0
        for row in self.stones:
            for s in row:
                if(s == stone):
                    count += 1
        
        return count