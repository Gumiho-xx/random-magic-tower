import random
import copy
from PIL import Image
import matplotlib.pyplot as plt
import itertools

WALL_CHAR = '#'
PATH_CHAR = ' '
ORIGIN_CHAR = "T"
START_CHAR = '#'
END_CHAR = '#'

# 有效范围
maze_size = 11

# 控制房间大小的概率
pa=0.45
pb=0.45
pc=0.25

room_size = {
    "[1,1]":pa*0.1,
    "[1,2]":pa*0.15,
    "[1,3]":pa*0.2,
    "[1,4]":pa*0.3,
    "[1,5]":pa*0.2,
    "[1,6]":pa*0.1,
    "[2,2]":pb*0.44,
    "[2,3]":pb*0.65,
    "[2,4]":pb*0.08,
    "[2,5]":pb*0.04,
    "[3,3]":pc*0.9,
    "[3,4]":pc*0.03,
    "[3,5]":pc*0.02,
}



def has_common_elements(list1, list2):
    for item in list1:
        if item in list2:
            return True
    return False

def if_overlap(x,y,width,height,rooms):
    this_room_list=[]
    # 扩大1表示相邻，不扩大是检测重叠
    for w in range(-1,width+1):
        for h in range(-1,height+1):
            this_room_list.append((x+w,y+h))
    #print(f'this_room_list:{this_room_list}')

    for room in rooms:
        pre_room_list=[]
        pre_x = room['x']
        pre_y = room['y']
        pre_width = room['width']
        pre_height = room['height']
        for w in range(0,pre_width):
            for h in range(0,pre_height):
                pre_room_list.append((pre_x+w,pre_y+h))
        #print(f'pre_room_list:{pre_room_list}')
        if has_common_elements(this_room_list,pre_room_list):
            return True
    return False


def weighted_sample(weights):
    """
    从给定的字典中进行带权重的抽样
    参数：
    weights：dict，权重字典，键为抽样的值，值为对应的权重
    返回：
    任一键，根据权重进行抽样得到的结果
    """
    if not isinstance(weights, dict):
        raise TypeError("权重参数必须为字典类型")
    if not weights:
        raise ValueError("权重字典不能为空")
    items = list(weights.keys())
    weights_list = list(weights.values())
    cumulative_weights = [sum(weights_list[:i+1]) for i in range(len(weights_list))]
    rand = random.uniform(0, cumulative_weights[-1])
    for i, cum_weight in enumerate(cumulative_weights):
        if rand <= cum_weight:
            return items[i]

def count_passage_in4(x,y,type):
    c = 0
    for i in range(-1,2):
        for j in range(-1,2):
            if (i+j) == 1 or (i+j) == -1:
                try:
                    if maze[y+i][x+j] == type:
                        c += 1 
                except:
                    pass
    return c

def count_passage_in9(x,y,type):
    c = 0
    for i in range(-1,2):
        for j in range(-1,2):
            try:
                if maze[y+i][x+j] == type:
                    c += 1 
            except:
                pass
    return c

def dfs(maze, x, y):
    if x < 0 or x >= len(maze) or y < 0 or y >= len(maze[0]) or maze[x][y] != ' ':
        return 0
    maze[x][y] = '#'  # 标记当前格子已访问
    count = 1  # 计数当前格子
    count += dfs(maze, x - 1, y)  # 上方格子
    count += dfs(maze, x + 1, y)  # 下方格子
    count += dfs(maze, x, y - 1)  # 左方格子
    count += dfs(maze, x, y + 1)  # 右方格子
    return count

def get_max_grid_count(maze, x, y):
    maze_copy = copy.deepcopy(maze)
    return dfs(maze_copy, x, y)


# 加载墙壁和通道的图片
wall_image = Image.open('1.png')
passage_image = Image.open('2.png')
life_red_image = Image.open('item_l1.png')
life_blue_image = Image.open('item_l2.png')
gem_red_image = Image.open('item_b1.png')
gem_blue_image = Image.open('item_b2.png')
gem_green_image = Image.open('item_b3.png')
key_yellow_image = Image.open('item_key1.png')
key_blue_image = Image.open('item_key2.png')
door1_image = Image.open('door1.png')





maze = [[ORIGIN_CHAR for _ in range(maze_size)] for _ in range(maze_size)]
# 如果点已经在生成区域中则为$
maze_gen = [[" " for _ in range(maze_size)] for _ in range(maze_size)]

room_list=[]

def get_row_col(maze):
    for _,m in enumerate(maze):
        if m == ["$"] * maze_size:
            pass
        else:
            return [_,m.index(" ")]
    return None

def change_maze(m,value,x,y,width,height):
    for i in range(0,width):
        for j in range(0,height):
            if 0 <= y+j <= maze_size-1 and 0 <= x+i <= maze_size-1:
                m[y+j][x+i] = value
                
flag = 0
while flag<=125:
    flag+=1
    xy = get_row_col(maze_gen)
    if xy == None:break
    x = xy[1]
    y = xy[0]
    wh = eval(weighted_sample(room_size))
    width = wh[0]
    height = wh[1]
    if random.randint(0,1)==0:
        width = wh[1]
        height = wh[0]
    gap = maze_size-x
    if "$" in maze_gen[y][x:-1]:gap = maze_gen[y][x:-1].index("$")
    width = min(width,gap)
    if gap - width == 1:width += 1
    gap = maze_size-y
    height = min(height,gap)
    if gap - height == 1:height += 1
            
    change_maze(maze_gen,"$",x-1,y-1,width+2,height+2)
    change_maze(maze,WALL_CHAR,x-1,y-1,width+2,height+2)
    change_maze(maze,PATH_CHAR,x,y,width,height)
    
    blocks=[[x+i,y+j] for i,j in list(itertools.product(list(range(0,width)), list(range(0,height))))]
    
    room_list.append({"x":x,"y":y,"w":width,"h":height,"a":width*height,"blocks":blocks})
    
# 挖出一些房间的通道
for room in room_list:
    # 确定一个方向 y,x
    ds = [(-1,0),(1,0),(0,-1),(0,1)]
    if room["x"] == 0:
        ds.remove((0,-1))
    if room["y"] == 0:
        ds.remove((-1,0))
    if room["x"]+room["w"] == maze_size:
        ds.remove((0,1))
    if room["y"]+room["h"] == maze_size:
        ds.remove((1,0))
    d = random.choice(ds)
    if d == (-1,0): #向上开路径，xy
        block_list = [[room["x"]+_,room["y"]] for _ in range(0,room["w"])]
    if d == (1,0): #向下开路径，xy
        block_list = [[room["x"]+_,room["y"]+room["h"]-1] for _ in range(0,room["w"])]
    if d == (0,-1): #向左开路径，xy
        block_list = [[room["x"],room["y"]+_] for _ in range(0,room["h"])]
    if d == (0,1): #向右开路径，xy
        block_list = [[room["x"]+room["w"]-1,room["y"]+_] for _ in range(0,room["h"])]
    block = random.choice(block_list)
    # 判断对面是否是通道，如果挖空不能链接通道，则考虑挖2格
    maze[block[1]+d[0]][block[0]+d[1]] = PATH_CHAR
    if maze[block[1]+d[0]*2][block[0]+d[1]*2] != PATH_CHAR:maze[block[1]+d[0]*2][block[0]+d[1]*2] = PATH_CHAR
    if random.randint(0,5)==0:
        ds = [(-1,0),(1,0),(0,-1),(0,1)]
        if room["x"] == 0:
            ds.remove((0,-1))
        if room["y"] == 0:
            ds.remove((-1,0))
        if room["x"]+room["w"] == maze_size:
            ds.remove((0,1))
        if room["y"]+room["h"] == maze_size:
            ds.remove((1,0))
        d = random.choice(ds)
        if d == (-1,0): #向上开路径，xy
            block_list = [[room["x"]+_,room["y"]] for _ in range(0,room["w"])]
        if d == (1,0): #向下开路径，xy
            block_list = [[room["x"]+_,room["y"]+room["h"]-1] for _ in range(0,room["w"])]
        if d == (0,-1): #向左开路径，xy
            block_list = [[room["x"],room["y"]+_] for _ in range(0,room["h"])]
        if d == (0,1): #向右开路径，xy
            block_list = [[room["x"]+room["w"]-1,room["y"]+_] for _ in range(0,room["h"])]
        block = random.choice(block_list)
        # 判断对面是否是通道，如果挖空不能链接通道，则考虑挖2格
        maze[block[1]+d[0]][block[0]+d[1]] = PATH_CHAR
        if maze[block[1]+d[0]*2][block[0]+d[1]*2] != PATH_CHAR:maze[block[1]+d[0]*2][block[0]+d[1]*2] = PATH_CHAR
        
"""
先放门之类的
"""

def count_wall(blocks):
    c = 0
    for block in blocks:
        if block[0] not in list(range(0,maze_size)) or block[1] not in list(range(0,maze_size)):
            c+=1
        elif maze[block[1]][block[0]] == WALL_CHAR:
            c+=1
    return c

def check_axis(maze,x,y,axis,value):
    if axis != "lr" and axis != "ud":raise TypeError("axis是ud或lr")
    maze_copy=copy.deepcopy(maze)
    for _ in maze_copy:
        _.append("#")
        _.insert(0,"#")
    maze_copy.append(["#"]*(maze_size+2))
    maze_copy.insert(0,["#"]*(maze_size+2))
    # 生产一个临时maze_copy
    x+=1
    y+=1
    if axis == "lr":
        if maze_copy[y][x+1] == value and maze_copy[y][x-1] == value:
            return True
    if axis == "ud":
        if maze_copy[y+1][x] == value and maze_copy[y-1][x] == value:
            return True
    return False

def find_door_points(maze):
    door_points=[]
    for y in range(maze_size):
        for x in range(maze_size):
            if maze[y][x] == PATH_CHAR:
                door_flag = 0
                # 左右是墙，上下不是墙：或者反之
                if check_axis(maze,x,y,"lr",WALL_CHAR) and check_axis(maze,x,y,"ud",PATH_CHAR):
                    if x not in [0,maze_size-1] and y not in [0,maze_size-1]:
                        # 判断周围空地包括自身应该有4个至少
                        if count_passage_in9(x,y,PATH_CHAR) >=5 or (count_passage_in9(x,y,PATH_CHAR) >=5 and random.randint(0,5)>=3):
                            door_points.append([x,y,"ud"])
                            continue
                    elif count_wall([[x+i,y] for i in range(-2,3)])==4:
                        door_points.append([x,y,"ud"])
                        continue
                if check_axis(maze,x,y,"lr",PATH_CHAR) and check_axis(maze,x,y,"ud",WALL_CHAR):
                    if x not in [0,maze_size-1] and y not in [0,maze_size-1]:
                        # 判断周围空地包括自身应该有4个至少
                        if count_passage_in9(x,y,PATH_CHAR) >=5 or (count_passage_in9(x,y,PATH_CHAR) >=5 and random.randint(0,5)>=3):
                            door_points.append([x,y,"lr"])
                            continue
                    elif count_wall([[x,y+i] for i in range(-2,3)])==4:
                        door_points.append([x,y,"lr"])
                        continue
    return door_points

door_points = find_door_points(maze)
for item in door_points:
    maze[item[1]][item[0]] = "D"

    

def add_border(maze):
    a=copy.deepcopy(maze)
    for _ in a:
        _.append("#")
        _.insert(0,"#")
    a.append(["#"]*(maze_size+2))
    a.insert(0,["#"]*(maze_size+2))
    return a

m = add_border(maze)
             
image = Image.new('RGB', (maze_size * 32 + 64, maze_size * 32 + 64), color=(255, 255, 255)) 
             
for y in range(maze_size+2):
    for x in range(maze_size+2):
        if m[y][x] == WALL_CHAR:
            image.paste(wall_image, (x * 32, y * 32))
        elif m[y][x] == PATH_CHAR:
            image.paste(passage_image, (x * 32, y * 32))
        elif m[y][x] == "D":
            image.paste(door1_image, (x * 32, y * 32))
# 保存生成的地牢图片
image.save('dungeon.png')
print("生成完毕，请看目录下的dungeon.png")
plt.imshow(image)