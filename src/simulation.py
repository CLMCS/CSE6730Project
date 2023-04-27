from functools import partial
from multiprocessing import Process
import random

import model


def gen_person_conf_default(desired_v: float = 1.5):
    return {'radius': 0.3, 'mass': 80, 'desired_v': desired_v,
            'goal_select': model.GPerson.goal_select_1}


def gen_person_conf_1(desired_v: float = 1.5):
    r = random.uniform(0.25, 0.35)
    m = 20 + 1850 * r ** 3
    return {'radius': r, 'mass': m, 'desired_v': desired_v,
            'goal_select': model.GPerson.goal_select_1}


def load_room(s: model.GServer, fname: str, gen_person_conf: callable = gen_person_conf_default):
    from model import GVec, GLine, GPerson, GGoal, GBarrierLine
    x0y0 = GVec()
    with open(fname, 'r') as f:
        for line in f.readlines():
            if line.startswith('randomseed'):
                random.seed(int(line.split()[1]))
            elif line.startswith('offset'):
                x0y0 = GVec(*map(float, line.split()[1:5]))
            elif line.startswith('BarrierLine'):
                GBarrierLine(s, GLine(*map(float, line.split()[1:5])).add(x0y0))
            elif line.startswith('Goal'):
                GGoal(s, GLine(*map(float, line.split()[1:])).add(x0y0))
            elif line.startswith('PeopleRand'):
                args = line.split()
                n = int(args[1])
                xs, ys = list(map(float, args[2::2])), list(map(float, args[3::2]))
                if len(xs) == 2:
                    for _ in range(n):
                        pt = GVec(random.uniform(*xs), random.uniform(*ys))
                        GPerson(s, pt.add(x0y0), **gen_person_conf())
                else:
                    pts = [GVec(x, y) for x, y in zip(xs, ys)]
                    x0, y0, x1, y1 = GVec.bounds(pts)
                    while n:
                        pt = GVec(random.uniform(x0, x1), random.uniform(y0, y1))
                        if pt.inside(pts):
                            GPerson(s, pt.add(x0y0), **gen_person_conf())
                            n -= 1
            elif line.startswith('PeopleGrid'):
                args = line.split()
                dx, dy = map(float, args[1:3])
                xs, ys = list(map(float, args[3::2])), list(map(float, args[4::2]))
                if len(xs) == 2:
                    for i in range(int((xs[1] - xs[0]) / dx) + 1):
                        for j in range(int((ys[1] - ys[0]) / dy) + 1):
                            pt = GVec(xs[0] + dx * i, ys[0] + dy * j)
                            GPerson(s, pt.add(x0y0), **gen_person_conf())
                else:
                    pts = [GVec(x, y) for x, y in zip(xs, ys)]
                    x0, y0, x1, y1 = GVec.bounds(pts)
                    for i in range(int((x1 - x0) / dx) + 1):
                        for j in range(int((y1 - y0) / dy) + 1):
                            pt = GVec(x0 + dx * i, y0 + dy * j)
                            if pt.inside(pts): GPerson(s, pt.add(x0y0), **gen_person_conf())


import numpy as np


def generate_uniform_distribution_points(count: int, xmin=0, xmax=1, ymin=0, ymax=1):
    points = np.random.uniform(low=[xmin, ymin], high=[xmax, ymax], size=(count, 2))
    return points


def generate_normal_distribution_points(count: int, mean=None, stddev=None):
    if mean is None:
        mean = [0.5, 0.5]
    if stddev is None:
        stddev = 0.1
    points = np.random.normal(loc=mean, scale=stddev, size=(count, 2))
    return points


def generate_Beta_distribution_points(count: int, a=None, b=None):
    if a is None:
        a = 0.5
    if b is None:
        b = 0.5
    points = np.random.beta(a=a, b=b, size=(count, 2))
    return points


def start_server_test():
    from model import GServer, GVec, GLine, GPerson, GGoal, GBarrierLine, GStat
    s = GServer(display=True)
    room_w, room_h = 15, 12
    x0, y0 = 2, 1
    x1, y1 = x0 + room_w, y0 + room_h
    door1_w = 2
    door1_y = y0 + room_h // 2
    door2_w = 1.5
    door2_x = x0 + room_w // 2
    walls = [
        # (x0, y0, x1, y0), # top
        (x0, y0, door2_x - door2_w / 2, y0),  # top left
        (x1, y0, door2_x + door2_w / 2, y0),  # top right
        (x0, y0, x0, y1),  # left
        (x0, y1, x1, y0 + room_h),  # bottom
        (x1, y0, x1, door1_y - door1_w / 2),  # right top
        (x1, y1, x1, door1_y + door1_w / 2)  # right bottom
    ]
    for wall in walls:
        GBarrierLine(s, GLine(*wall))

    GGoal(s, GLine(x1, door1_y - door1_w / 2, x1, door1_y + door1_w / 2))
    GGoal(s, GLine(door2_x - door2_w / 2, y0, door2_x + door2_w / 2, y0))
    random.seed(0)
    num_people = 70
    mean, std_dev = 0.5, 0.1  # params for gaussian distribution (speed)
    desired_speeds = np.clip(np.random.normal(loc=mean, scale=std_dev, size=num_people), 0, 1)
    base_speed = 1.5
    for speed in desired_speeds:
        GPerson(server=s, pos=GVec(x0 + room_w / 10 + random.random() * (room_w * 0.8),
                                   y0 + room_h / 10 + random.random() * (room_h * 0.8)), desired_v=speed * base_speed)
    GStat(s, '30_Beta.csv')
    if s.view: s.running = False
    s.run()


def exp2():
    from model import GServer, GVec, GLine, GPerson, GGoal, GBarrierLine, GStat
    s = GServer(display=True)
    room_w, room_h = 15, 12
    x0, y0 = 0, 0
    # GBarrierLine(s, GLine(0, 0, 0, 12))
    # GBarrierLine(s, GLine(0, 12, 15, 12))
    # GBarrierLine(s, GLine(15, 0, 15, 12))
    ## door 1 settings
    GBarrierLine(s, GLine(0, 0, 6, 0))
    GGoal(s, GLine(6, 0, 9, 0))
    GBarrierLine(s, GLine(9, 0, 15, 0))

    ## door 2 settings
    GBarrierLine(s, GLine(15, 0, 15, 4.5))
    GGoal(s, GLine(15, 4.5, 15, 7.5))
    GBarrierLine(s, GLine(15, 7.5, 15, 12))

    ## door 3 settings
    GBarrierLine(s, GLine(0, 0, 0, 4.5))
    GGoal(s, GLine(0, 4.5, 0, 7.5))
    GBarrierLine(s, GLine(0, 7.5, 0, 12))

    ## door 4 settings
    GBarrierLine(s, GLine(0, 12, 6, 12))
    GGoal(s, GLine(6, 12, 9, 12))
    GBarrierLine(s, GLine(9, 12, 15, 12))

    random.seed(0)
    num_people = 150
    mean, std_dev = 0.5, 0.1  # params for gaussian distribution (speed)
    desired_speeds = np.clip(np.random.normal(loc=mean, scale=std_dev, size=num_people), 0, 1)
    base_speed = 1.5
    for speed in desired_speeds:
        GPerson(server=s, pos=GVec(x0 + room_w / 10 + random.random() * (room_w * 0.8),
                                   y0 + room_h / 10 + random.random() * (room_h * 0.8)), desired_v=speed * base_speed)
    GStat(s, '4door_300.csv')
    if s.view: s.running = False
    s.run()

def exp3():
    from model import GServer, GVec, GLine, GPerson, GGoal, GBarrierLine, GStat
    ## gate size = 1.5
    s = GServer(display=True)
    room_w, room_h = 15, 12
    x0, y0 = 0, 0
    # GBarrierLine(s, GLine(0, 0, 0, 12))
    # GBarrierLine(s, GLine(0, 12, 15, 12))
    # GBarrierLine(s, GLine(15, 0, 15, 12))
    ## door 1 settings
    GBarrierLine(s, GLine(0, 0, 6, 0))
    GGoal(s, GLine(6, 0, 7.5, 0))
    GBarrierLine(s, GLine(7.5, 0, 15, 0))

    ## door 2 settings
    GBarrierLine(s, GLine(15, 0, 15, 4.5))
    GGoal(s, GLine(15, 4.5, 15, 6))
    GBarrierLine(s, GLine(15, 6, 15, 12))

    ## door 3 settings
    GBarrierLine(s, GLine(0, 0, 0, 4.5))
    GGoal(s, GLine(0, 4.5, 0, 6))
    GBarrierLine(s, GLine(0, 6, 0, 12))

    ## door 4 settings
    GBarrierLine(s, GLine(0, 12, 6, 12))
    GGoal(s, GLine(6, 12, 7.5, 12))
    GBarrierLine(s, GLine(7.5, 12, 15, 12))

    random.seed(0)
    num_people = 70
    mean, std_dev = 0.5, 0.1  # params for gaussian distribution (speed)
    desired_speeds = np.clip(np.random.normal(loc=mean, scale=std_dev, size=num_people), 0, 1)
    base_speed = 1.5
    for speed in desired_speeds:
        GPerson(server=s, pos=GVec(x0 + room_w / 10 + random.random() * (room_w * 0.8),
                                   y0 + room_h / 10 + random.random() * (room_h * 0.8)), desired_v=speed * base_speed)
    GStat(s, '3door_150.csv')
    if s.view: s.running = False
    s.run()


def exp4():
    from model import GServer, GVec, GLine, GPerson, GGoal, GBarrierLine, GStat
    for seed in range(1):
        s = GServer(display=True)
        room_w, room_h = 15, 12
        x0, y0 = 0, 0
        # GBarrierLine(s, GLine(0, 0, 0, 12))
        # GBarrierLine(s, GLine(0, 12, 15, 12))
        # GBarrierLine(s, GLine(15, 0, 15, 12))
        ## door 1 settings
        GBarrierLine(s, GLine(0, 0, 6, 0))
        GGoal(s, GLine(6, 0, 7.5, 0))
        GBarrierLine(s, GLine(7.5, 0, 15, 0))

        ## door 2 settings
        GBarrierLine(s, GLine(15, 0, 15, 4.5))
        GGoal(s, GLine(15, 4.5, 15, 6))
        GBarrierLine(s, GLine(15, 6, 15, 12))

        ## door 3 settings
        GBarrierLine(s, GLine(0, 0, 0, 4.5))
        GGoal(s, GLine(0, 4.5, 0, 6))
        GBarrierLine(s, GLine(0, 6, 0, 12))

        ## door 4 settings
        GBarrierLine(s, GLine(0, 12, 6, 12))
        GGoal(s, GLine(6, 12, 7.5, 12))
        GBarrierLine(s, GLine(7.5, 12, 15, 12))

        num_people = 100
        desired_speeds = np.random.normal(1.34, 0.26, num_people)
        for speed in desired_speeds:
            GPerson(server=s, pos=GVec(x0 + room_w / 15 + random.random() * (room_w * 0.9),
                                       y0 + room_h / 15 + random.random() * (room_h * 0.9)), desired_v=speed)
        GStat(s, '/Users/liqilin/CSE6730-Project/1door/seed_{}.csv'.format(seed))
        if s.view: s.running = False
        s.run()

def start_server_from_file(input_fname, output_fname: str = None,
                           display: bool = True):  # output file name & display = false
    s = model.GServer(display=display)
    load_room(s, input_fname, gen_person_conf=partial(gen_person_conf_1, 1.5))
    model.GStat(s, output_fname)
    if s.view: s.running = False
    s.run()


if __name__ == '__main__':
    # a = generate_uniform_distribution_points(20)
    # print(a)
    # print("-----")
    # b = generate_uniform_distribution_points(20)
    # print(b)
    # print("-----")
    #
    # c = generate_normal_distribution_points(20)
    # print(c)
    # print("-----")
    #
    # d = generate_Beta_distribution_points(20)
    # print(d)
    # print("-----")
    exp4()
    # start_server_test()
    # start_server_from_file('room1.txt', 'stat.csv')
    # multiprocess
    # p1 = Process(target=start_server_from_file, args=('room1.txt',))
    # p1.start()
    # p2 = Process(target=start_server_test)
    # p2.start()
    # p1.join()
    # p2.join()
