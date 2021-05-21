import pandas as pd
from random import random
import collections
import random as r
import copy


# ===============================
class Chromosome:
    # Static variable which means that this values always has the value we can pull this value out , no need class to be object.
    path = 'Clean_dummy_3.csv'
    status = ''
    gene_num = 6
    pop_num = 50
    lenght_x = 70
    mutation_rate = 0.2
    crossover_rate = 0.8
    data = pd.read_csv(path)
    df = data[['FoodGroup', 'Energy_kcal', 'Protein_g', 'Fat_g', 'Carb_g', 'Sugar_g', 'Fiber_g']]

    # Initial class is the constructor class
    def __init__(self):
        self.chromosome = []
        self.pareto_font = 0
        self.fit_Mincalories = 0
        self.fit_Maxprotein = 0
        self.crowding_dist = 0
        self.niche_count = 0
        self.calories = 0
        self.fat = 0
        self.protein = 0
        self.carbo = 0
        self.fiber = 0

    # use this as comparison with if-else
    def __eq__(self, other):
        if isinstance(other, Chromosome):
            return self.chromosome == other.chromosome
        return False

    def __repr__(self):
        '''return '\nChromosome : {!r}'.format(self.chromosome) \
               + '\ncal : {} '.format(self.calories) \
               + '\nprotien : {} '.format(self.protein) \
               + '\nP-rank : {}'.format(self.pareto_font) \
               + '\nCD : {}'.format(self.crowding_dist) \
               + '\nNiche_count : {}'.format(self.niche_count)'''
        return '\nChromosome : {!r}'.format(self.chromosome) \
                + '\ncal : {} '.format(self.calories) + ' | protien : {} '.format(self.protein)

    # Annotation of the characteristic of function/method
    @staticmethod
    def pop_chromosome():
        pop_chromosome = []
        mp = []

        while len(pop_chromosome) < Chromosome.pop_num:
            g = Chromosome()
            for j in range(Chromosome.gene_num):
                g.chromosome.append(r.randint(0, Chromosome.lenght_x))

            mp.append(g.chromosome.copy())
            cal11, pro11, fat11, carbo11, fiber11 = Chromosome.fitness_function(mp)
            if cal11 >= 1500 and carbo11 <= 325.0 and 45.0 <= pro11 <= 60.0 and 44.0 <= fat11 <= 77.0 and 20.0 <= fiber11 <= 30.0:
                if g.chromosome not in pop_chromosome and len(pop_chromosome) < Chromosome.pop_num:
                    g.calories = cal11
                    g.protein = pro11
                    g.fat = fat11
                    g.carbo = carbo11
                    g.fiber = fiber11
                    pop_chromosome.append(g)
            mp.clear()

        return pop_chromosome

    @staticmethod
    def fitness_function(pop_chromosome):
        flag = ['Energy_kcal', 'Protein_g', 'Fat_g', 'Carb_g', 'Fiber_g']
        temp = []
        result = []
        for x in flag:
            for i in pop_chromosome:
                for j in i:
                    temp.append(Chromosome.df[x][j].copy())

            result.append(sum(temp))
            temp.clear()

        return result[0], result[1], result[2], result[3], result[4]

    @staticmethod
    def fast_non_dominate_sorting(chromosome_list):
        # calculate niche score ( non-dominate count )
        for x in chromosome_list:
            x.niche_count = sum(
                [1 if y.calories < x.calories and y.protein > x.protein else 0 for y in chromosome_list])
        # x.cal 1628 , x.pro 46 , y.cal 1557, y.pro 52.26

        # sorted list by niche count (DESC)
        Chromosome.status = 'niche-sort'
        chromosome_list = sorted(chromosome_list)

        # assign pareto rank regraded Front pareto ranking.
        for x in range(len(chromosome_list)):
            if chromosome_list[x].niche_count == 0:
                chromosome_list[x].pareto_font = 1
            else:
                if chromosome_list[x].niche_count > chromosome_list[x - 1].niche_count:
                    chromosome_list[x].pareto_font = chromosome_list[x - 1].pareto_font + 1
                else:
                    chromosome_list[x].pareto_font = chromosome_list[x - 1].pareto_font

        # sorted list by pareto rank (ASC)
        Chromosome.status = 'pareto-sort'
        chromosome_list = sorted(chromosome_list)

        return chromosome_list

    def __lt__(self, other):
        if Chromosome.status == 'niche-sort':
            if self.niche_count != other.niche_count:
                return self.niche_count < other.niche_count
            else:
                if self.calories != other.calories:
                    return self.calories < other.calories
                elif self.calories == other.calories:
                    return self.protein > other.protein
        if Chromosome.status == 'pareto-sort':
            return self.pareto_font < other.pareto_font

    @staticmethod
    def crowding_dist(chromosome_list):

        last_p_rank = chromosome_list[len(chromosome_list) - 1].pareto_font
        front_set_index = []

        # create range of index in each pareto front.
        # ( For simplify an implementation of calculated crowding distance )
        for p_rank in range(1, last_p_rank + 1):
            sum_of_pareto_front = sum([1 for obj in chromosome_list if p_rank == obj.pareto_font])

            if p_rank == 1:
                front_set_index.append((0, sum_of_pareto_front - 1))
                last_index = sum_of_pareto_front
            else:
                front_set_index.append((last_index, (last_index + sum_of_pareto_front) - 1))
                last_index = last_index + sum_of_pareto_front

        # get min and max from both objective
        min_calories = Chromosome.M_min(chromosome_list, 'calories')
        max_calories = Chromosome.M_max(chromosome_list, 'calories')
        min_protein = Chromosome.M_min(chromosome_list, 'protein')
        max_protein = Chromosome.M_max(chromosome_list, 'protein')

        # calculate crowding distance
        for start, end in front_set_index:
            for index in range(start, end + 1):
                if index == start:
                    chromosome_list[index].crowding_dist = 0
                elif index == end:
                    chromosome_list[index].crowding_dist = 1
                else:
                    chromosome_list[index].crowding_dist = abs(
                        (chromosome_list[index - 1].calories - chromosome_list[index + 1].calories) / (
                                max_calories - min_calories)) + abs(
                        (chromosome_list[index - 1].protein - chromosome_list[index + 1].protein) / (
                                max_protein - min_protein))

        return chromosome_list

    @staticmethod
    def M_min(chromosome_list, status):
        if status == 'calories':
            best = chromosome_list[0].calories
            for i in chromosome_list:
                best = best if best < i.calories else i.calories
            return best
        if status == 'protein':
            best = chromosome_list[0].protein
            for i in chromosome_list:
                best = best if best < i.protein else i.protein
            return best

    @staticmethod
    def M_max(chromosome_list, status):
        if status == 'calories':
            best = chromosome_list[0].calories
            for i in chromosome_list:
                best = best if best > i.calories else i.calories
            return best
        if status == 'protein':
            best = chromosome_list[0].protein
            for i in chromosome_list:
                best = best if best > i.protein else i.protein
            return best

    @staticmethod
    def tournament_sel(result):
        tournament_size = 0.2

        while True:

            k = [r.randint(0, Chromosome.pop_num - 1) for _ in range(int(tournament_size * Chromosome.pop_num))]
            parent_1 = []
            for _ in k:
                if not parent_1 or parent_1.pareto_font < result[_].pareto_font:
                    parent_1 = copy.deepcopy(result[_])
                elif parent_1.pareto_font == result[_].pareto_font:
                    if parent_1.crowding_dist > result[_].crowding_dist:
                        parent_1 = copy.deepcopy(result[_])

            k = [r.randint(0, Chromosome.pop_num - 1) for _ in range(int(tournament_size * Chromosome.pop_num))]
            parent_2 = []
            for _ in k:
                if not parent_2 or parent_2.pareto_font < result[_].pareto_font:
                    parent_2 = copy.deepcopy(result[_])
                elif parent_2.pareto_font == result[_].pareto_font:
                    if parent_2.crowding_dist > result[_].crowding_dist:
                        parent_2 = copy.deepcopy(result[_])

            if parent_1 != parent_2:
                break


        # create new chromosome for some issue.
        pr1 = Chromosome()
        pr2 = Chromosome()
        pr1.chromosome = parent_1.chromosome.copy()
        pr2.chromosome = parent_2.chromosome.copy()

        return pr1, pr2

    # อันนี้ให้เป็น crossover นะ
    @staticmethod
    def crossover(*parent1: list) -> list:
        p1, p2 = parent1[0][0], parent1[0][1]
        l_pos_p1 = []
        l_pos_p2 = []
        swap_num = 3
        
        if random() < Chromosome.crossover_rate:
            for i in range(swap_num):
                l_pos_p1.append(r.randint(0, 5))
                l_pos_p2.append(r.randint(0, 5))

            for i in range(swap_num):
                p1.chromosome[l_pos_p1[i]], p2.chromosome[l_pos_p2[i]] = p2.chromosome[l_pos_p2[i]], p1.chromosome[l_pos_p1[i]]

        return p1, p2

    # ตัวนี้ให้เป็น mutation นะ
    @staticmethod
    def mutation(*parent1: list) -> list:
        p1, p2 = parent1[0][0], parent1[0][1]

        if random() > Chromosome.mutation_rate:
            p1.chromosome[r.randint(0, 5)] = r.randint(0, Chromosome.lenght_x)
            p2.chromosome[r.randint(0, 5)] = r.randint(0, Chromosome.lenght_x)

        return p1, p2

    @staticmethod
    def new_habitat() -> list:
        list_random = []
        for j in range(Chromosome.gene_num):
            list_random.append(r.randint(0, Chromosome.lenght_x))
        return list_random