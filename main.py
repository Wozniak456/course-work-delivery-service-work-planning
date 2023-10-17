import random
import sys
from datetime import datetime, timedelta
from Order import Order
from Car import *
from matplotlib import pyplot as plt
import time
import json


def sort_orders_t(orders):
    """Sorts orders due to w/t value. Starts with the order with the biggest value."""
    sorted_list = sorted(orders, key=lambda x: x.w / x.t, reverse=True)
    return sorted_list


def create_schedule(orders, cars):  # orders are sorted
    """Creates schedule for cars. Computes a busyness for every car and add next order to the car
    with the smallest busyness"""
    i = 0
    # for every car add first order
    if len(orders) < len(cars):
        sys.exit("no sense in scheduling")
    for car in cars:
        car.S.append(orders[i])
        car.busyness += orders[i].t
        orders[i].T = car.busyness
        if car.busyness > orders[i].d:
            car.is_delay = True
        car.busyness += orders[i].t  # back to post station
        i += 1

    # find the car with the smallest busyness, and it's index
    min_busyness = min(cars, key=lambda x: x.busyness, default=None)
    min_index = cars.index(min_busyness)

    # to sort orders between cars (add an order to a car with the smallest busyness)
    for i in range(len(cars), len(orders)):
        cars[min_index].S.append(orders[i])
        cars[min_index].busyness += orders[i].t  # момент доставки замовлення
        orders[i].T = cars[min_index].busyness
        if cars[min_index].busyness > orders[i].d:
            cars[min_index].is_delay = True
        cars[min_index].busyness += orders[i].t  # момент повернення до станції
        min_busyness = min(cars, key=lambda x: x.busyness, default=None)  # перерахунок найменш навантаженої машини
        min_index = cars.index(min_busyness)

    for car in cars:
        car.reward = get_reward(car.S)


def own_data():
    own_order_list = []
    own_order_list.extend(
        [Order(1, 4, 10, 102),
         Order(2, 5, 7, 154),
         Order(3, 1, 13, 176),
         Order(4, 8, 9, 123),
         Order(5, 13, 31, 176),
         Order(6, 5, 15, 199),
         Order(7, 2, 11, 147),
         Order(8, 4, 16, 120)
         ])
    own_order_list = sort_orders_t(own_order_list)
    own_car_list = [Car(1), Car(2)]
    return own_order_list, own_car_list


def create_data(start, end, n, k, dispersion):
    """This function generates random income data due to amount of cars,
    amount of orders, start and end of the period"""
    order_list = []
    for i in range(1, n + 1):
        t = random.randint(1, 10)
        d = start + timedelta(days=random.randint(t, (end - start).days))
        delta = d - start
        d_time = delta.days
        if dispersion == 0:
            w = random.randint(100, 200)
        elif dispersion == 1:
            w = random.randint(100, 2000)
        order_list.append(Order(i, t, d_time, w))
    order_list = sort_orders_t(order_list)  # sort due to t

    car_list = []
    for i in range(1, k + 1):
        car_list.append(Car(i))
    return order_list, car_list


def run_experiment(start_date, end_date, num_of_orders, num_of_cars, case):
    num = list(range(1, 21))
    fact_reward = 0
    w_relative = []
    time_value = []

    for u in range(1, 21):
        print(f'Number of exp: {u}')
        start_time = time.time()
        #orders, cars = own_data()
        orders, cars = create_data(start_date, end_date, num_of_orders, num_of_cars, case)
        general_reward = 0
        for i in range(0, len(orders)):
            general_reward += orders[i].w
        create_schedule(orders, cars)
        fact_reward = 0

        print('--------------- First Schedule \n')
        for car in cars:
            car.print_s()
            print()

        for car in cars:
            print(f'\n--------------- Best schedule for {car.j} car\n')
            if car.is_delay:
                car.optimization()
                fact_reward += car.reward
                car.print_s()
            else:
                print(f'\n\tno delay in {car.j} car from the beginning\n')
                fact_reward += car.reward
                car.print_s()
        end_time = time.time()
        time_value.append(end_time - start_time)
        w_relative.append(fact_reward / general_reward)
    return num, w_relative, time_value


def run_experiment2(start_date, end_date, num_of_cars, case):
    n_amount = [20 + 5 * i for i in range(20)]
    fact_reward = 0
    w_relative = []
    time_value = []

    for u in range(20):
        print(f'Num of exp: {u+1}')
        start_time = time.time()
        #orders, cars = own_data()
        orders, cars = create_data(start_date, end_date, n_amount[u], num_of_cars, case)
        general_reward = 0
        for i in range(0, len(orders)):
            general_reward += orders[i].w
        create_schedule(orders, cars)
        fact_reward = 0

        for car in cars:
            if car.is_delay:
                car.optimization()
                fact_reward += car.reward
            else:
                fact_reward += car.reward
        end_time = time.time()
        time_value.append(end_time - start_time)
        w_relative.append(fact_reward / general_reward)
        print(f'n: {n_amount[u]}, t: {end_time - start_time}')
    return n_amount, w_relative, time_value


def get_graphic(plot):
    if plot == 0:
        plt.plot(n1, w1)
        plt.plot(n1, w2)
        plt.ylabel("Relative reward")
        plt.ylim(0, 1)
        plt.xlabel("Iteration")
    elif plot == 2:
        plt.plot(n1, w1)
        plt.plot(n1, w2)
        plt.ylabel("Relative reward")
        plt.xlabel("The capacity of order amount")
        plt.ylim(0, 1.1)
    elif plot == 1:
        plt.plot(n1, t1, 'o')
        plt.plot(n1, t2, 'o')
        for i in range(len(n1)):
            plt.plot([n1[i], n1[i]], [t1[i], t2[i]], linestyle='--', color='gray')
        plt.ylabel("Time, sec")
        plt.xlabel("Iteration")
    elif plot == 3:
        plt.plot(n1, t1, 'o')
        plt.plot(n1, t2, 'o')
        for i in range(len(n1)):
            plt.plot([n1[i], n1[i]], [t1[i], t2[i]], linestyle='--', color='gray')
        plt.ylabel("Time, sec")
        plt.xlabel("The capacity of order amount")
    plt.title("Visualization of experiment")
    plt.legend(["Small dispersion", "Big dispersion"])
    plt.show()


def input_values():
    start = datetime.strptime(input("Введіть початкову дату у форматі (рік-місяць-день): "), "%Y-%m-%d")
    end = datetime.strptime(input("Введіть кінцеву дату у форматі (рік-місяць-день): "), "%Y-%m-%d")
    num_cars = int(input("Введіть кількість машин: "))
    num_orders = int(input("Введіть кількість робіт: "))
    return start, end, num_cars, num_orders


if __name__ == '__main__':
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 5, 30)
    num_of_cars = 20
    num_of_orders = 100

    answer = input("Чи бажаєте ви задати розмірність задачі самостійно? Введіть 'так', якщо бажаєте: ")
    if answer.lower() == "так":
        start_date, end_date, num_of_cars, num_of_orders = input_values()

    n1, w1, t1 = run_experiment(start_date, end_date, num_of_orders, num_of_cars, 0)
    n1, w2, t2 = run_experiment(start_date, end_date, num_of_orders, num_of_cars, 1)

    plot = 0
    get_graphic(plot)

    plot = 1
    get_graphic(plot)

    n1, w1, t1 = run_experiment2(start_date, end_date, num_of_cars, 0)
    n1, w2, t2 = run_experiment2(start_date, end_date, num_of_cars, 1)

    plot = 2
    get_graphic(plot)

    plot = 3
    get_graphic(plot)










