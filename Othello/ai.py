
from othello import *
from game import *
from game_tree import *

from time import sleep

import math

import random

class AI:

    CORNER_SCORE = 5.0
    EDGE_SCORE = 2.0
    NEAR_CORNER_SCORE = -2.0
    GRAD_SCORE_WEIGHT = 0.5
    ENEMY_MINIMUM_STEPS_WEIGHT = 1.0
    CENTER_SCORE = 0.8

    # 4隅の位置
    CORNER_MAP = {(0, 0): True, (7, 0): True, (7, 7): True, (0, 7): True}


    CENTER_MAP = {(2, 2): True, (3, 2): True, (4, 2): True, (5, 2): True,
                  (2, 3): True, (3, 3): True, (4, 3): True, (5, 3): True,
                  (2, 4): True, (3, 4): True, (4, 4): True, (5, 4): True,
                  (2, 5): True, (3, 5): True, (4, 5): True, (5, 5): True
                 }

    # 一辺に含まれる各点をキーとした連想マップ
    #
    # 
    # 
    # 
    EDGE_MAP = {(0, 0): [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)], \
                (1, 0): [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)], \
                (2, 0): [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)], \
                (3, 0): [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)], \
                (4, 0): [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)], \
                (5, 0): [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)], \
                (6, 0): [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)], \
                (7, 0): [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)], \


                (0, 0): [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)], \
                (0, 1): [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)], \
                (0, 2): [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)], \
                (0, 3): [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)], \
                (0, 4): [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)], \
                (0, 5): [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)], \
                (0, 6): [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)], \
                (0, 7): [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)], \


                (0, 7): [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)], \
                (1, 7): [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)], \
                (2, 7): [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)], \
                (3, 7): [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)], \
                (4, 7): [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)], \
                (5, 7): [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)], \
                (6, 7): [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)], \
                (7, 7): [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)], \


                (7, 0): [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)], \
                (7, 1): [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)], \
                (7, 2): [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)], \
                (7, 3): [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)], \
                (7, 4): [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)], \
                (7, 5): [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)], \
                (7, 6): [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)], \
                (7, 7): [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)]  \
                }

    
    # コーナ付近の連想マップ
    # 各コーナをキーとしてその周りを値とする
    NEAR_CORNER_MAP = {(0, 0) : {(1, 0): True, (1, 1): True, (0, 1): True}, \
                       (0, 7) : {(0, 6): True, (1, 6): True, (1, 7): True}, \
                       (7, 7) : {(6, 7): True, (6, 6): True, (7, 6): True}, \
                       (7, 0) : {(6, 0): True, (6, 1): True, (7, 1): True}  \
                      }

    

    def __init__(self):
        pass

    def random_put_stone(self, turn, board, placeable_position_list):
        print("thinking...")
        sleep(1)
        return random.randrange(len(placeable_position_list))

    def put_stone(self, turn, board, placeable_position_list):
        print("thinking...")

        my_stone = Stone(Color.BLACK) if turn == Game.Turn.BLACK else Stone(Color.WHITE)
        enemy_stone = Stone(Color.WHITE) if turn == Game.Turn.BLACK else Stone(Color.BLACK)

        tree = GameTree()
        tree.root = Node(name = "root", other_infos = {"board": board})

        AI.compute_next_step(tree.root, my_stone, board, placeable_position_list)

        for node in tree.root.next_nodes:
            # 相手が打ったときの展開を計算
            next_placeable_position_list = node.other_infos["board"].search_placeable_position(enemy_stone)
            AI.compute_next_step(node, enemy_stone, node.other_infos["board"], next_placeable_position_list)
            

        tree.print()
        # print(AI.compute_center(board, Stone(Color.WHITE)))

        # print(AI.compute_center(board, Stone(Color.BLACK)))

        total_enemy_steps_count = 0.0
        for node in tree.root.next_nodes:
            total_enemy_steps_count += len(node.next_nodes)
            max_score_node = node.get_max_score_next_node()
            if(max_score_node is not None):
                node.score -= max_score_node.score

        #print(enemy_steps_count)

        for node in tree.root.next_nodes:
            #print(len(node.next_nodes) / total_enemy_steps_count)
            node.score -= len(node.next_nodes) / total_enemy_steps_count * AI.ENEMY_MINIMUM_STEPS_WEIGHT

        tree.print()


        sleep(1)

        # 最大スコアを持つ次ノードを選択
        max_node = tree.root.get_max_score_next_node()

        print(Graphics.Background.PURPLE + "selected: " + str(max_node.other_infos["position_to_put"]))

        print(Graphics.END)
        return max_node.other_infos["position_to_put"]


    def compute_next_step(base_node, stone, board, placeable_position_list):
        
        for i in range(len(placeable_position_list)):
            next_board = Board.copy(board)
            next_board.put_stone(stone, placeable_position_list[i][0], placeable_position_list[i][1])

            score =  AI.compute_score(board, stone, placeable_position_list[i])
            next_node = Node(name = str(placeable_position_list[i]) + ": " + str(score), \
                             other_infos = {"board": next_board, "position_to_put":  placeable_position_list[i]})
            next_node.score = score

            base_node.append(next_node)

    def compute_score(board, stone, position_to_put):
        enemy_stone = Stone(Color.WHITE) if stone.color == Color.BLACK else Stone(Color.BLACK)

        score = 0.0

        if(position_to_put in AI.CORNER_MAP.keys()):

            score += AI.CORNER_SCORE

        
        if(position_to_put in AI.CENTER_MAP.keys()):

            score += AI.CENTER_SCORE

        if(position_to_put in AI.EDGE_MAP.keys()):
            
            all_none = True
            for edge in AI.EDGE_MAP[position_to_put]:
                if(board.stones[edge[1]][edge[0]] is not None):
                    all_none = False
                    break
            
            if(all_none):
                if(position_to_put == AI.EDGE_MAP[position_to_put][2] or position_to_put == AI.EDGE_MAP[position_to_put][5]):
                    score += AI.EDGE_SCORE
                else:
                    score -= AI.EDGE_SCORE
            
            else:
                for i in range(len(AI.EDGE_MAP[position_to_put])):
                    if(AI.EDGE_MAP[position_to_put][i] == position_to_put):
                        break
                
                #print(i)

                # 前後が同じ色のとき
                if(i - 1 >= 0 and i + 1 < len(AI.EDGE_MAP[position_to_put]) and \
                   board.stones[AI.EDGE_MAP[position_to_put][i - 1][1]][AI.EDGE_MAP[position_to_put][i - 1][0]] == stone and \
                   board.stones[AI.EDGE_MAP[position_to_put][i + 1][1]][AI.EDGE_MAP[position_to_put][i + 1][0]] == stone):

                    # 必ず埋めるようにする
                    score += AI.EDGE_SCORE * 2.0
                
                # 二つ先(前)が同じ色, 間には何もないとき
                elif((i + 2 < len(AI.EDGE_MAP[position_to_put]) and 
                     board.stones[AI.EDGE_MAP[position_to_put][i + 1][1]][AI.EDGE_MAP[position_to_put][i + 1][0]] is None and\
                     board.stones[AI.EDGE_MAP[position_to_put][i + 2][1]][AI.EDGE_MAP[position_to_put][i + 2][0]] == stone) or \
                     (i - 2 >= 0 and \
                     board.stones[AI.EDGE_MAP[position_to_put][i - 1][1]][AI.EDGE_MAP[position_to_put][i - 1][0]] is None and\
                     board.stones[AI.EDGE_MAP[position_to_put][i - 2][1]][AI.EDGE_MAP[position_to_put][i - 2][0]] == stone)):

                    # そこは避ける
                    score -= AI.EDGE_SCORE

                # # 前後が異なる色のとき
                # elif(i - 1 >= 0 and i + 1 < len(AI.EDGE_MAP[position_to_put]) and \
                #      board.stones[AI.EDGE_MAP[position_to_put][i - 1][1]][AI.EDGE_MAP[position_to_put][i - 1][0]] == enemy_stone and \
                #      board.stones[AI.EDGE_MAP[position_to_put][i + 1][1]][AI.EDGE_MAP[position_to_put][i + 1][0]] == enemy_stone):

                #     # そこは避ける
                #     score -= AI.EDGE_SCORE

                else:
                    score += AI.EDGE_SCORE


        # コーナ部分に石がないとき, その周りの場所には石を置かない.
        for corner in AI.NEAR_CORNER_MAP.keys():
            if(board.stones[corner[1]][corner[0]] == None):
                if position_to_put in AI.NEAR_CORNER_MAP[corner].keys():
                    score += AI.NEAR_CORNER_SCORE
                    

        # --- 勾配スコアの算出 ----------------------------------------------
        # 黒白それぞれの重心を求め, その近くに石を置く.
        # 石が散らばらないようにする
        white_center = AI.compute_center(board, Stone(Color.WHITE))
        black_center = AI.compute_center(board, Stone(Color.BLACK))
        
        center_x = (white_center[0] + black_center[0]) / 2.0
        center_y = (white_center[1] + black_center[1]) / 2.0
        
        vec_x = position_to_put[0] - center_x
        vec_y = position_to_put[1] - center_y

        grad_x = 0.0
        grad_y = 0.0

        if(stone.color == Color.BLACK):
            grad_x = black_center[0] - white_center[0]
            grad_y = black_center[1] - white_center[1]
        else:
            grad_x = white_center[0] - black_center[0]
            grad_y = white_center[1] - black_center[1]

        grad_mag = grad_x * grad_x + grad_y * grad_y
        if grad_mag != 0.0:
                
            l = vec_x * grad_x + vec_y * grad_y
            sim = l / math.sqrt(vec_x * vec_x + vec_y * vec_y) / math.sqrt(grad_x * grad_x + grad_y * grad_y)

            #print(sim)
            l /= grad_mag

            vec_x *= l
            vec_y *= l

            #print(vec_x, vec_y)

            grad_score = (math.sqrt(vec_x * vec_x + vec_y * vec_y)) / 8.0 
            grad_score *= 1.0 if sim > 0.0 else -1.0
            #print(grad_score)

            score += grad_score * AI.GRAD_SCORE_WEIGHT

        # end 勾配スコアの算出 ---------------------------
            
        return score

    def compute_center(board, stone):
        stones_count = 0
        center_x = 0.0
        center_y = 0.0

        for i in range(board.rows):
            for j in range(board.cols):
                if(board.stones[i][j] == stone):
                    stones_count += 1
                    center_x += j
                    center_y += i
        

        if(stones_count == 0):
            return (-1, -1)
        
        return (center_x / stones_count, center_y / stones_count)

    