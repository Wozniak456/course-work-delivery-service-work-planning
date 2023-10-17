from func import *

class Car:
    def __init__(self, j):
        self.j = j
        self.S = []
        self.busyness = 0
        self.reward = 0
        self.is_delay = False

    def optimization(self):
        """Optimization: Rearranging elements pairwise within a single machine"""
        c = 0
        new_car = Car(100)
        new_car.is_delay = self.is_delay
        new_schedule = []
        new_schedule.extend(self.S)
        while c < 50 and new_car.is_delay:
            max_acceleration = max(new_schedule, key=lambda x: x.d-x.T)  # return an object
            x = new_schedule.index(max_acceleration)
            max_delay = get_the_largest_negative(new_schedule)
            y = new_schedule.index(max_delay)
            new_schedule[x], new_schedule[y] = new_schedule[y], new_schedule[x]
            update_T(new_car, new_schedule)
            new_reward = get_reward(new_schedule)
            if new_reward > self.reward:
                print(f'Objective function improved : Replaced {max_acceleration.i} with {max_delay.i}. New reward: {new_reward}.')
                self.S = new_schedule
                self.reward = new_reward
                c = 0
            else:
                update_T(self, self.S)
                c += 1

    def print_s(self):
        print(f"Car {self.j} has reward: {self.reward} UAH and such schedule:")
        for order in self.S:
            order.print_order()







