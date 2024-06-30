import copy
import random


class Hat():
    # Constructs and initializes a Hat instance. Takes a variable number of arguments that specify the count of each color of balls that are in the hat
    def __init__(self, **kwargs):
        # self.count will store a dictionary with the colors as the keys and counts as the values
        self.count = kwargs.copy()
        # The arguments passed into the hat object upon creation are converted to a contents instance variable which will be a list of strings containing one item for each ball in the hat
        self.contents = Counter.spread(**kwargs)

    # Returns a string representation of the hat object
    def __repr__(self):
        params = ', '.join(f"{color}={self.count[color]}" for color in self.count)
        return f"{type(self).__name__}({params})"
    
    # Accepts an argument indicating the number of balls to draw from the hat. Removes balls at random from contents and returns removed balls as a list of strings
    def draw(self, num_balls_drawn):
        removedBalls = []
        if num_balls_drawn >= len(self.contents):
            removedBalls = self.contents.copy()
            self.contents = []
            self.count = dict.fromkeys(self.count, 0)
        else:
             for _ in range(num_balls_drawn):
                 removedBalls.append(self.contents.pop(random.randint(0,len(self.contents)-1)))
                 self.count[removedBalls[-1]] -= 1
        return removedBalls

# A helper class: Used by the Hat class to handle count-to-list and list-to-count conversions
class Counter():
    # The spread class method converts any number of string = count key word arguments into a list of strings: for example: Counter.spread(r=1,s=2) will return: ['r', 's', 's']
    def spread(**kwargs):
        spread_contents = []
        for key, value in kwargs.items():
            for _ in range(value):
                spread_contents.append(key)
        return spread_contents
    # Converts a list of strings into a {string:count} dict. Example: Counter.count(['r','a','m','i','a','a','a','i']) will return: {'r': 1, 'a': 4, 'm': 1, 'i': 2}
    def count(spread):
        count = {}
        for item in spread:
            if item not in count:
                count[str(item)] = 1
            else:
                    count[item] += 1
        return count

# The experiment function takes in 4 parameters: (A hat, the expected balls {"color":count, ...}, the number of balls to draw out each time, and the total number of experiments) and returns the approximate probability resulting from the performed experiments
def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    # Define and initialize success_counter variable to count the number of successful experiments
    success_counter = 0
    # do num_experiments experiments
    for _ in range(num_experiments):
        # draw num_balls_drawn balls from (a clone of the given) hat (in each experiment)
        draw = Counter.count(copy.deepcopy(hat).draw(num_balls_drawn))
        # check if the expected_balls are within the collection of the drawn balls
        # If this draw of num_balls_drawn balls contains at least the expected_balls:
        if all(draw.get(ball, 0) >= count for ball, count in expected_balls.items()):
            # increment successful experiments (success_counter) counter
            success_counter += 1
        # calculate and return the estimated probability
    return success_counter/num_experiments



if __name__=="__main__":
    # Usage examples:
    print(f"The Counter helper class:\n--------------------\nCounter.spread(r=1,s=2) gives: {Counter.spread(r=1,s=2)}") # ['r', 's', 's']
    count = Counter.count(['r','a','m','i','a','a','a','i'])
    print(f"Counter.count(['r','a','m','i','a','a','a','i']) gives: {count}")
    # {'r': 1, 'a': 4, 'm': 1, 'i': 2}
    print(f"Counter.spread(**{count}) gives: {Counter.spread(**count)}")
    # ['r', 'a', 'a', 'a', 'a', 'm', 'i', 'i']
    print('-------------------\n')

    print(f"Hat objects string representations:\n--------------------")
    hat1 = Hat(yellow=3, blue=2, green=6)
    hat2 = Hat(red=5, orange=4)
    print(f"hat1:  {hat1}\nhat2:  {hat2}\n-------------------\n")

    # Output:
    # hat1:  Hat(yellow=3, blue=2, green=6)
    # hat2:  Hat(red=5, orange=4)

    print(f"The draw method:\n-------------------")
    hat3 = Hat(red=5, orange=4, black=1, blue=0, pink=2, striped=9)
    print(f"hat3:  {hat3}")
    # Output:
    # hat3:  Hat(red=5, orange=4, black=1, blue=0, pink=2, striped=9)
    print(f"Drawing 5 random balls from hat3:  {hat3.draw(5)}")
    # Potential output:
    # Drawing 5 random balls from hat3:  ['red', 'striped', 'red', 'striped', 'red']
    print(f"hat3 after the draw:  {hat3}")
    # Possible output based on the previous draw:
    # hat3:  Hat(red=2, orange=4, black=1, blue=0, pink=2, striped=7)
    print("--------------------\n")

    print(f"The experiment function: \n--------------------")
    hat4 = Hat(black=6, red=4, green=3)
    probability = experiment(hat=hat4,
                  expected_balls={"red":2, "green":1}, num_balls_drawn=5, num_experiments=2000)
    print(f"The approximate probability of having at least 2 red and 1 green balls after drawing 5 random balls from hat4[{hat4}] based on the average result of 2000 experiments is: {probability})")
    # Output is mostly a number in the range 0.34 - 0.39
    print("--------------------")
