# NSGA-II-Women-Model-with-USDA-National-Nutrient-Database
Genetic Algorithm for solving Nutrition Diet for Women Model with USDA National Nutrient Database


The objective is to find the min calories and max protein for modeling. we use NSGA-II with some preparation of data.
For methodology <br>
<br>[1]. uniform crossover and swap mutation as method.
<br>[2]. tournament selection with 20% competition.
<br>[3]. Set constrain with fat, calories, protein, carbo and fiber.


- crossover rate : 80%
- mutation rate : 20%
- generation : 100
- chromosome = 6 genes (each gene represent raw data from dataset)
- population (pool size) = 50


*NOTE : This project do speed up hyper parameter for steep over local optimal in some case.


