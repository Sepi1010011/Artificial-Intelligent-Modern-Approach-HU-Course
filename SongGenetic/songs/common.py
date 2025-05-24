import random

def generate_songs(num=40):
    return [round(random.uniform(2.0, 3.0) * 60) for _ in range(num)]

def generate_intervals():
    return [round(random.uniform(10.0, 15.0) * 60) for _ in range(3)]
