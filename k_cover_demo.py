# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import random

points = []
point_to_class_map = {}
field_to_point_map = {}
point_to_field_map = {}


width = 100
S_size = 50
granurality = 5
K = 5
stepsize = width / granurality

def generate_points():
    global points, width, S_size
    
    points = [ (random.random() * width, random.random() * width) for _ in range(S_size)]

def show_all_points():
    global points, width, field_to_point_map, S_size
    draw_fields(lambda key : len(field_to_point_map[key]) > 0)
    
    plt.plot([point[0] for point in points], [point[1] for point in points], 'o', color='black')
    plt.axis([0, width, 0, width])
    plt.title('{} random points on a 5x5 field'.format(S_size))
    plt.grid(linestyle='-')
    plt.show()

def random_classify():
    global point_to_class_map
    for point in points:
        point_to_class_map[point] = random.randint(0, K - 1)
        

# aggregate the number of fields covered by each class
def evaluate_classification():
    global point_to_class_map
    class_to_field = {}
    
    for i in range(K):
        class_to_field[i] = []
        for point_and_class in point_to_class_map.items():
            if point_and_class[1] == i:
                class_to_field[i].append(point_to_field_map[point_and_class[0]])
        class_to_field[i] = set(class_to_field[i])
    
    return sum([len(setoffields) for setoffields in class_to_field.values()])
    
    
def greedy_classify():
    global point_to_class_map
    for point in points:
        point_to_class_map[point] = 0
        for i in range(1, K):
            original = point_to_class_map[point]
            original_value = evaluate_classification()
            
            point_to_class_map[point] = i
            new_value = evaluate_classification()
            if original_value > new_value:
                point_to_class_map[point] = original
            

def build_field_mapping():
    global granurality, field_to_point_map, width
    stepsize = width / granurality
    for x in range(granurality):
        for y in range(granurality):
            field_to_point_map[(x, y)] = []
            for point in points:
                if x * stepsize < point[0] < (x + 1) * stepsize and y * stepsize < point[1] < (y + 1) * stepsize:
                    field_to_point_map[(x, y)].append(point)
                    point_to_field_map[(point)] = (x, y)
                    
def draw_fields(fun):
    global field_to_point_map, granurality, width, stepsize
    filtered = filter(fun , field_to_point_map.keys())
    currentAxis = plt.gca()
    
    print field_to_point_map.keys()
    
    for field in filtered:
        currentAxis.add_patch(Rectangle((field[0] * stepsize, field[1] * stepsize), stepsize, stepsize, facecolor="grey", alpha=0.5))


def show_not_optimal_fields():
    global field_to_point_map, granurality, width, stepsize
    filtered = filter(lambda key : len(field_to_point_map[key]) > 0 , field_to_point_map.keys())
    currentAxis = plt.gca()
    
    print field_to_point_map.keys()
    
    for field in filtered:
        classes_in_field = set([point_to_class_map[point] for point in field_to_point_map[field]])
        if len(classes_in_field) != min(K, len(field_to_point_map[field])):
            currentAxis.add_patch(Rectangle((field[0] * stepsize, field[1] * stepsize), stepsize, stepsize, facecolor="red", alpha=0.5))


def show_classified_points(algo):
    global K
    for i in range(K):
        plt.plot([point[0] for point in points if point_to_class_map[point] == i], [point[1] for point in points if point_to_class_map[point] == i], 'o')
    
    plt.axis([0, width, 0, width])
    plt.title('Points classified into {} classes, with not optimal fields indicated. Algorithm = {}, Coverage = {}'.format(K, algo, evaluate_classification()))
    plt.grid(linestyle='-')
    plt.show()
    
def show_classification(algo):
    show_not_optimal_fields()
    show_classified_points(algo)

if __name__ == '__main__':
    generate_points()
    build_field_mapping()
    show_all_points()
    random_classify()
    show_classification('Random')
    greedy_classify()
    show_classification('Greedy')
    
