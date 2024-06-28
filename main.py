import copy
import random


class Hat():
    def __init__(self, **kwargs):
        self.count = kwargs
        self.contents = Counter.spread(**kwargs)

    def __str__(self):
        params = ', '.join(f"{color}={self.count[color]}" for color in self.count)
        return f"{type(self).__name__}({params})"

    def draw(self, num_balls_drawn):
        removedBalls = []
        if num_balls_drawn >= len(self.contents):
            removedBalls = self.contents.copy()
            self.count = dict.fromkeys(self.count, 0)
            self.contents=[]
        else:
             for _ in range(num_balls_drawn):
                 removedBalls.append(self.contents.pop(random.randint(0,len(self.contents)-1)))
                 self.count[removedBalls[-1]] -= 1
        return removedBalls

class Counter():
    def spread(**kwargs):
        spread_contents = []
        for key, value in kwargs.items():
            for _ in range(value):
                spread_contents.append(key)
        return spread_contents
    def count(spread):
        count = {}
        for item in spread:
            if item not in count:
                count[str(item)] = 1
            else:
                    count[item] += 1
        return count


def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    counter = 0
    for _ in range(num_experiments):
        draw = Counter.count(copy.deepcopy(hat).draw(num_balls_drawn))
        if expected_balls.items() <= draw.items():
            counter += 1
        print(f'{_+1}-{counter}: {draw}')
    return counter/num_experiments


if __name__=='__main__':
    hat1 = Hat(yellow=3, blue=2, green=6)
    hat2 = Hat(red=5, orange=4)
    print('hat1:  '+str(hat1)+'\nhat2:  '+str(hat2)+'\n-------------------\n')

    hat3 = Hat(red=5, orange=4, black=1, blue=0, pink=2, striped=9)
    print('hat3: ', hat3)
    print('Draw 5 random balls from hat3: ', hat3.draw(5))
    print('hat3: ', hat3)
    print('--------------------\n')
    hat4 = Hat(black=2, red=1, green=3)
    probability = experiment(hat=hat4, expected_balls={"red":1,"green":1},
    num_balls_drawn=3, num_experiments=2000)
    print(f'The probability of getting 1 red and 1 green balls from drawing 3 balls from {hat4} is estimated to be {probability} based on the results of 2000 experiments)')
