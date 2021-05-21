from NSGA_KIM_PROJECT.chromosome import Chromosome
import copy
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

iteration = 100
best_chromosome = Chromosome()
best_chromosome.calories = 2000
best_chromosome.protein = 0
local_state = 0
start = time.time()
calories_p = []
protein_p = []
loop = 0


if __name__ == '__main__':

    for gen in range(iteration):
        print(f'============================ Gen : {gen} ============================')
        next_list = []
        loop = loop + 1
        if gen == 0:
            # Initial population
            initial_pop = Chromosome.pop_chromosome()
            initial_pop = Chromosome.fast_non_dominate_sorting(initial_pop)
            initial_pop = Chromosome.crowding_dist(initial_pop)

        else:
            while len(next_list) < Chromosome.pop_num:
                mp1 = []
                mp2 = []

                # Perform tournament selection -> crossover -> mutation
                ch1, ch2 = Chromosome.mutation(Chromosome.crossover(Chromosome.tournament_sel(initial_pop)))
                mp1.append(ch1.chromosome.copy())
                mp2.append(ch2.chromosome.copy())

                # set fitness value to child object
                cal1, pro1, fat1, carbo1, fiber1 = Chromosome.fitness_function(mp1)
                ch1.calories = cal1
                ch1.protein = pro1
                ch1.fat = fat1
                ch1.carbo = carbo1
                ch1.fiber = fiber1
                cal2, pro2, fat2, carbo2, fiber2 = Chromosome.fitness_function(mp2)
                ch2.calories = cal2
                ch2.protein = pro2
                ch2.fat = fat2
                ch2.carbo = carbo2
                ch2.fiber = fiber2

                # checking condition based on constraint and duplicate
                if cal1 >= 1500 and carbo1 <= 325.0 and 45.0 <= pro1 <= 60.0 and 44.0 <= fat1 <= 77.0 and 20.0 <= fiber1 <= 30.0:
                    ch1.chromosome = sorted(ch1.chromosome)
                    if ch1 not in next_list and ch1 not in initial_pop and len(next_list) < Chromosome.pop_num:
                        next_list.append(ch1)

                if cal2 >= 1500 and carbo2 <= 325.0 and 45.0 <= pro2 <= 60.0 and 44.0 <= fat2 <= 77.0 and 20.0 <= fiber2 <= 30.0:
                    ch2.chromosome = sorted(ch2.chromosome)
                    if ch2 not in next_list and ch2 not in initial_pop and len(next_list) < Chromosome.pop_num :
                        next_list.append(ch2)

            # combine old and new population
            totalChunk = []
            for _ in initial_pop:
                totalChunk.append(_)
            for _ in next_list:
                totalChunk.append(_)

            # perform non dominate and crowding dist
            totalChunk = Chromosome.fast_non_dominate_sorting(totalChunk)
            totalChunk = Chromosome.crowding_dist(totalChunk)

            # clear parent and child population
            initial_pop.clear()
            next_list.clear()

            for i in range(Chromosome.pop_num):
                initial_pop.append(totalChunk[i])

            totalChunk.clear()

        # check stuck at local optimal
        if initial_pop[0].calories < best_chromosome.calories or (initial_pop[0].calories <= best_chromosome.calories and initial_pop[0].protein > best_chromosome.protein):
            local_state = 0
            best_chromosome.calories = initial_pop[0].calories
            best_chromosome.protein = initial_pop[0].protein
            Chromosome.mutation_rate = 0.2
            Chromosome.crossover_rate = 0.8
        else:
            local_state = local_state + 1

        # increase hyper parameter when encouter local optimal
        if local_state >= 20:
            Chromosome.mutation_rate = 0.3
            Chromosome.crossover_rate = 0.9

        # show best chromosome
        print(initial_pop[0])

        # prepare data for plot
        calories_p.append(initial_pop[0].calories)
        protein_p.append(initial_pop[0].protein)

        # terminator condition
        # Global optimal solution is calories 1500 and protein 59.67
        # but protein that greater than 58.0 is satisfy enough to use in real life
        if initial_pop[0].calories == 1500 and initial_pop[0].protein > 59.0:
            break

    end = time.time()
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)

    # ชั่วโมง:นาที:วินาที.milliวินาที
    print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))

    #print(initial_pop)

    # Data
    df = pd.DataFrame({'Generation': range(1, loop+1), 'Calories': calories_p, 'Protein': protein_p})

    figure, axis = plt.subplots(2)

    # multiple line plots
    axis[0].plot('Generation', 'Calories', data=df, marker='', color='skyblue', linewidth=2)
    axis[0].set_title("Min : Calories")
    axis[1].plot('Generation', 'Protein', data=df, marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")
    axis[1].set_title("Max : Protein")


    # show graph
    plt.show()
