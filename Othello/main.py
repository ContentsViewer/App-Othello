from game import *

from ai import *

def main():
    ai = AI()
    game = Game(put_white_stone_func = ai.put_stone)
    #game = Game(put_white_stone_func = ai.put_stone, put_black_stone_func = ai.random_put_stone)
    #game = Game(put_white_stone_func = ai.put_stone, put_black_stone_func = ai.put_stone)


    game.loop()

if __name__ == "__main__":
    main()