
from othello import *
from console_graphics import *

class Game:
    class Turn:
        BLACK = Color.BLACK
        WHITE = Color.WHITE


    def craete_placeable_position_map(placeable_position_list):

        placeable_position_map = {}
        for i in range(len(placeable_position_list)):
            placeable_position_map[placeable_position_list[i]] = i

        return placeable_position_map


    def __init__(self, put_white_stone_func = None, put_black_stone_func = None):
        self.board = Board()


        self.placeable_position_list = [[]]
        self.placeable_position_map = {}
        
        if(put_white_stone_func is None):
            put_white_stone_func = self.put_stone_default

        
        if(put_black_stone_func is None):
            put_black_stone_func = self.put_stone_default

            

        self.put_white_stone_func = put_white_stone_func
        self.put_black_stone_func = put_black_stone_func

        print(Graphics.Background.GREEN)
        print(Graphics.Figure.BLACK + Stone.STR + "|" + Graphics.Figure.WHITE + Stone.STR + "|")
        print(Graphics.END)
        print("Looks correctly?[y / n] << ", end ="")
        response = input()
        if(response == 'n'):
            Stone.STR = "⬤ "
        

        self.board.print()


        print("game initialized")


        #print(self.board.search_placeable_position(Stone(Color.BLACK)))
    

    def loop(self):

        
        turn = Game.Turn.BLACK
        turn_count = 0
        
        pass_count = 0
        placed_stones_count = 4


        # --- game main loop --------------------------------
        while(True):

            if(pass_count >= 2 or placed_stones_count >= self.board.rows * self.board.cols):
                # skipが二回以上(双方が打てなくなった)とき, 石が埋まっているときループを抜ける.
                break


            # --- turn の表示 ----
            print("===================================================")
            print("Turn: " + Graphics.Background.WHITE + Graphics.Figure.BLACK +\
                ( "Black" if (turn == Game.Turn.BLACK) else "White"), end ="")

            print(Graphics.END + " " + Graphics.Background.GREEN, end = "")
            print(Graphics.Figure.BLACK if(turn == Game.Turn.BLACK) else Graphics.Figure.WHITE, end ="")
            print(Stone.STR)

            print(Graphics.END)
            # end turn の表示 ---


            # これから置く石の用意
            stone = Stone(Color.BLACK if(turn == Game.Turn.BLACK) else Color.WHITE)

            # 置ける場所の計算
            self.placeable_position_list = self.board.search_placeable_position(stone)


            # 打てる場所がないとき
            if(len(self.placeable_position_list) <= 0):
                
                print(Graphics.Figure.BLUE + "PASS")
                print(Graphics.END)

                pass_count += 1

                    
                # turnの切り替え
                turn ^= 0x01
                
                turn_count += 1
                continue


            pass_count = 0
                
                
            # 置ける場所をハイライトしたボードの表示
            self.placeable_position_map = Game.craete_placeable_position_map(self.placeable_position_list)

            self.print_board_with_placeable_highlight()




            
            position_x_to_put = 0
            position_y_to_put = 0
            
            response = None

            if(turn == Game.Turn.BLACK):
                response = self.put_black_stone_func(turn, self.board, self.placeable_position_list)
            else:
                response = self.put_white_stone_func(turn, self.board, self.placeable_position_list)

            if(type(response) == int):
                if(response < 0 or response >= len(self.placeable_position_list)):
                    raise Exception(ValueError)

                position_x_to_put = self.placeable_position_list[response][0]
                position_y_to_put = self.placeable_position_list[response][1]

            elif(type(response) == tuple):
                if(not response in self.placeable_position_map.keys()):
                    raise Exception(ValueError)

                
                position_x_to_put = response[0]
                position_y_to_put = response[1]
                
                
            else:
                raise Exception(ValueError)

            
            self.board.put_stone(stone, position_x_to_put, position_y_to_put, True)
            placed_stones_count += 1

            # turnの切り替え
            turn ^= 0x01

            turn_count += 1

        # end game main loop ----------------------
        

        # --- 結果の表示 ----------------------------
        print("===================================================")
        
        print("Result: ")
        self.board.print()

        black_stones_count = self.board.count_stones(Stone(Color.BLACK))
        white_stones_count = self.board.count_stones(Stone(Color.WHITE))

        print(Graphics.Background.WHITE, end="")
        print(Graphics.Figure.BLACK, end="")
        print("BLACK:", end="")
        print(Graphics.END, end="")
        print(" ", end="")

        print(Graphics.Background.GREEN, end="")
        print(Graphics.Figure.BLACK, end="")
        for i in range(0, black_stones_count, 2):
            print(Stone.STR, end="")

        print(Graphics.END + " " + str(black_stones_count))
        
        print(Graphics.Background.WHITE, end="")
        print(Graphics.Figure.BLACK, end="")
        print("WHITE:", end="")
        print(Graphics.END, end="")
        print(" ", end="")

        print(Graphics.Background.GREEN, end="")
        print(Graphics.Figure.WHITE, end="")
        for i in range(0, white_stones_count, 2):
            print(Stone.STR, end="")

        
        print(Graphics.END + " " + str(white_stones_count))


        print(Graphics.END)
        # end 結果の表示 -----------------------



    # 置ける場所をハイライトしたボードを表示
    # 
    # --- WARNING ---
    #  placeable_position_map を作成後にこの関数を実行して下さい
    #  craete_placeable_position_map()で作成可能です.
    #
    def print_board_with_placeable_highlight(self):
        
        line = Graphics.Figure.BLACK + "|" + Graphics.Figure.DEFAULT
        black_stone = Graphics.Figure.BLACK + Stone.STR + Graphics.Figure.DEFAULT
        white_stone = Graphics.Figure.WHITE + Stone.STR + Graphics.Figure.DEFAULT

        print(Graphics.Background.GREEN)
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                
                if(self.board.stones[row][col] is None):
                    if((col, row) in self.placeable_position_map.keys() ):
                        print(line, end = "")
                        print(Graphics.Background.PURPLE, end = "")

                        if(len(str(self.placeable_position_map[(col, row)])) == 1):
                            print(" ", end = "")
                        print(str(self.placeable_position_map[(col, row)]), end = "")
                        
                        print(Graphics.Background.GREEN, end = "")
                    
                    else:
                        print(line + "  ", end = "") 


                elif(self.board.stones[row][col].color == Color.WHITE):
                    print(line + white_stone + "", end = "")
                else:
                    print(line + black_stone + "", end = "")

            print(line)
    
        print(Graphics.END)



    # 石を置くためのコールバック関数
    # デフォルト関数
    #
    # ユーザからの入力を待つ
    def put_stone_default(self, turn, board, placeable_position_list):

        position = -1

        while(True):
            print("Please enter position number to put a stone. << ", end = "")
            try:
                position = int(input())

                if(position >= 0 and position < len(placeable_position_list)):
                    break

            except ValueError:
                pass

            print(Graphics.Figure.RED + "[ERROR] wrong position number." + Graphics.END)

        return position







