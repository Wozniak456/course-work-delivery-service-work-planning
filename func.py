def update_T(car, schedule):
    """Updates T values for every order in the schedule."""
    busy_ness = 0
    delay_num = 0
    for order in schedule:
        busy_ness += order.t
        order.T = busy_ness
        if busy_ness > order.d:
            delay_num += 1
        busy_ness += order.t
    if delay_num == 0:
        car.is_delay = False


def get_the_largest_negative(schedule):
    """Use to find the biggest negative value di-Ti through the orders in schedule"""
    max_delay_order = min(schedule, key=lambda x: x.d - x.T)
    for order in schedule:
        delay = order.d - order.T
        if 0 > delay > max_delay_order.d - max_delay_order.T:
            max_delay_order = order
    return max_delay_order


def get_reward(schedule):
    """Function computes and returns the reward for particular schedule."""
    reward = 0
    for order in schedule:
        if order.T <= order.d:
            reward += order.w
    return reward


