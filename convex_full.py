#!/usr/bin/env python3
import csv
import sys
import math
import itertools

from common import print_solution, read_input

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)



def cal_path_length(dist, tour): #経路の合計距離
    path_length = sum(dist[tour[i]][tour[(i + 1) % N]] for i in range(N))
    return path_length



def init_dist():
    dist = [[0] * N for city1_index in range(N)]
    for city1_index in range(N):
        for j in range(city1_index, N):
            dist[city1_index][j] = dist[j][city1_index] = distance(cities[city1_index], cities[j])

    return dist



def cal_dist(cities): #距離の隣接行列を作成
    global N
    N = len(cities)

    dist = init_dist()

    return dist



def check_min_way_three(tour, city1_index, city2_index, city3_index, city4_index, city5_index): 
    dis1_2 = dist[tour[city1_index]][tour[city2_index]]
    dis2_3 = dist[tour[city2_index]][tour[city3_index]]
    dis4_5 = dist[tour[city4_index]][tour[city5_index]]
    dis1_3 = dist[tour[city1_index]][tour[city3_index]]
    dis2_4 = dist[tour[city2_index]][tour[city4_index]]
    dis2_5 = dist[tour[city2_index]][tour[city5_index]]

    if dis1_2 + dis2_3 + dis4_5 > dis1_3 + dis2_4 + dis2_5:
        return True #変えた方が短くなる
    else:
        return False



def chenge_tour_three(tour, i, j):
    poped = tour.pop(i) #抜き出す要素
    
    if i < j:
        tour.insert(j, poped) #iがポップされたことにより、jの位置が前より一個後ろの要素(city5) を指していることに注意
    else:
        tour.insert(j + 1, poped)

    return tour



def get_min_tour_3points(tour, count, city1_index, city2_index, city3_index, city4_index, city5_index):

    if check_min_way_three(tour, city1_index, city2_index, city3_index, city4_index, city5_index):
        tour = chenge_tour_three(tour, city2_index, city4_index) #つなぎ変える
        count += 1

    return tour, count



def get_tmp_min_tour_3points(tour):
    count = 0

    for i in range(N):
        city1_index = i - 1
        city2_index = i
        city3_index = (i + 1) % N

        for j in range((i + 2) % N, (i + 2) % N + N - 4): #city1 -> city2 -> city3 に隣接していない辺についてそれぞれcity2とのつなぎ変えを考える
            city4_index = j % N
            city5_index = (j + 1) % N

            tour, count = get_min_tour_3points(tour, count, city1_index, city2_index, city3_index, city4_index, city5_index) #「つなぎ変えorそのまま」のどちらか距離が最小のものが返ってくる 

    return tour, count



def optimize_3(tour):
    while(True):
        tour, count = get_tmp_min_tour_3points(tour) #交差を入れ替えた経路（交差が完全には覗かれていない場合あり）  
        if count == 0: #つなぎ変えが発生しなかったら終了
            break

    return tour



def check_min_way_two(tour, city1_index, city2_index, city3_index, city4_index):
    dist1_2 = dist[tour[city1_index]][tour[city2_index]]
    dist3_4 = dist[tour[city3_index]][tour[city4_index]]
    dist1_3 = dist[tour[city1_index]][tour[city3_index]]
    dist2_4 = dist[tour[city2_index]][tour[city4_index]]

    if (dist1_2 + dist3_4 > dist1_3 + dist2_4):
        return True #変えた方が短くなる
    else:
        return False



def chenge_tour_two(tour, city2_index, city4_index):

    new_path = tour[city2_index:city4_index] #vity4_indexがtourのインデックスを超えていた場合、tourの最後の要素までが切り取られる
    tour[city2_index:city4_index] = new_path[::-1]

    return tour



def get_min_tour_2points(tour, count, city1_index, city2_index, city3_index, city4_index):
    if check_min_way_two(tour, city1_index, city2_index, city3_index, city4_index):
        tour = chenge_tour_two(tour, city2_index, city3_index + 1)
        count += 1
    return tour, count



def get_tmp_min_tour_2points(tour):
    count = 0
    for i in range(N - 2):
        city1_index = i
        city2_index = i + 1

        for j in range(i + 2, N):
            city3_index = j
            city4_index = (j + 1) % N

            tour, count = get_min_tour_2points(tour, count, city1_index, city2_index, city3_index, city4_index)   

    return tour, count



def optimize_2(tour):
    while (True):
        tour, count = get_tmp_min_tour_2points(tour) #交差を入れ替えた経路（交差が完全には覗かれていない場合あり）

        if count == 0: 
            break

    return tour



def save_file(path, tour): #結果保存
    with open(path, "w") as f:
     
        writer = csv.writer(f)
        writer.writerow(["index"])
        for city1_index in tour:
            writer.writerow([str(city1_index)])



def find_min_y_city(cities):
    min_y = 10**9
    min_y_city = -1
    for i in range(N):
        if cities[i][1] < min_y:
            min_y = cities[i][1]
            min_y_city = i

    return min_y_city



def cal_radian(dist, from_position_index, to_position_index):
    from_position = cities[from_position_index]
    to_position = cities[to_position_index]
    from_x = from_position[0]
    from_y = from_position[1]
    to_x = to_position[0]
    to_y = to_position[1]

    bec_x = to_x - from_x
    bec_y = to_y - from_y

    tan = math.atan2(bec_y, bec_x) #-pi から piまでで返ってくる

    return math.degrees(tan) #角度で返す



def make_outer_convex(dist, cities):
    unvisited_cities = [i for i in range(0, N)] 
    start_point = find_min_y_city(cities) #y座標が一番小さい都市から始める
    
    outer_tour = [start_point] #outer_tourで回る都市を追加していく
    unvisited_cities.remove(start_point)

    from_position = start_point
    prev_radian = 200

    for _ in range(N):
        best_radian = -200
        best_index = None

        for to_position in range(N):
           
            if not to_position in outer_tour:
                radian = cal_radian(dist, from_position, to_position)
                if best_radian < radian and radian <= prev_radian: #最も角度が大きくなる都市を選ぶ

                    best_radian = radian
                    best_index = to_position
                    
        if best_index == None: #一周した
            break

        else:
            outer_tour.append(best_index)
            unvisited_cities.remove(best_index) 
            prev_radian = best_radian
            from_position = best_index

    outer_tour.append(start_point) #一周した
    return outer_tour, unvisited_cities



def cal_cost(dist, from_city_index, to_city_index, unvisited_city_index):
    cost = dist[from_city_index][unvisited_city_index] + dist[unvisited_city_index][to_city_index] - dist[from_city_index][to_city_index]
    return cost



def gift_packing(tour, dist, cities, unvisited_cities):
    while len(unvisited_cities) != 0:
        best_min_cost = 10**9 #全体の中で、最もコストが低い（次に訪問する）都市へのコスト
        next_city_candidate = None
        next_city_candidate_insert_position = None

        for unvisited_city_index in unvisited_cities: #全てのunvisited citiesについて最小の挿入コストを計算
            min_cost = 10**9
            min_cost_city_insert_position = None
   
            for i in range(len(tour) - 1):
                from_city_index = tour[i]
                to_city_index = tour[i + 1]

                cost = cal_cost(dist, from_city_index, to_city_index, unvisited_city_index)

                if min_cost > cost:
                    min_cost = cost #unvisited_city_indexを挿入するのにかかる最小コスト
                    min_cost_city_insert_position = i + 1 #unvisited_cityを挿入するとしたら、to_city_indexのところ

            if best_min_cost > min_cost:
                best_min_cost = min_cost
                next_city_candidate = unvisited_city_index
                next_city_candidate_insert_position = min_cost_city_insert_position 

        if next_city_candidate != None:
            tour.insert(next_city_candidate_insert_position, next_city_candidate)
            unvisited_cities.remove(next_city_candidate)

    return tour



def get_min_tour(dist, cities):
  
    tour, unvisited_cities = make_outer_convex(dist, cities) #凸包を探す

    tour = gift_packing(tour, dist, cities, unvisited_cities)

    tour = optimize_3(tour) #3点のつなぎ変え
    print("three done")

    tour = optimize_2(tour) #2点のつなぎ変え
    print("two done")

    return tour



if __name__ == '__main__':

    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    dist = cal_dist(cities) #データ読み込み
    
    print("load done")

    tour = get_min_tour(dist, cities)

    print(sys.argv[1][6])
    path = "solution_yours_" + sys.argv[1][6] + ".csv"
    save_file(path, tour)

   