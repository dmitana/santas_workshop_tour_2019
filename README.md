# FIIT Nature Inspired Computing Project

This project is elaborated as an assignment for the Nature Inspired Computing course (SS 2019/2020) at FIIT STU by [Denis Mitana](https://github.com/dmitana/) and [Miroslav Sumega](https://github.com/xsumegam/).

Detailed description of our solution is in the attached [paper](paper.pdf).

## Task
[Santa's Workshop Tour 2019](https://www.kaggle.com/c/santa-workshop-tour-2019/overview) is a Kaggle competition that defines scheduling optimization problem. The goal of this task is to schedule the families to Santa's Workshop in a way that minimizes the penalty cost to Santa. Every family must be scheduled for one and only one day. The proposed nature-inspired optimization method of Artificial Immune System algorithm (AIS) is used for finding optimal day to visit the workshop for each family while minimizing Santa's costs.

## Data
Provided data consists of 5,000 families that have listed their top 10 preferences for the dates they'd like to attend Santa's workshop tour. Dates are integer values representing the days before Christmas. Each family also has a number of people attending.

## Results
The AIS algorithm is tested with three and two different methods of mutation and selection, respectively, showing that more informed mutations and less selected Antibodies for the next generation can significantly improve results. Experiments also showed that negative selection is more appropriate than positive selection, which got stuck in the local minimum. Our best achieved score is 2,789,989. The results show that AIS algorithm is suitable for the given scheduling optimization task.

## Running Code
1. Clone the repository.
```bash
$ git clone git@github.com:dmitana/santas_workshop_tour_2019.git
```

2. Install [requirements](requirements.txt).
```bash
$ pip install -r requirements.txt
```

3. Download [data](https://www.kaggle.com/c/santa-workshop-tour-2019/data?select=family_data.csv#) and move it to the `data/` directory.

4. Show help about program usage and command line arguments.
```bash
$ python -m santas_workshop_tour -h
usage: santas_workshop_tour [-h] --data-file-path DATA_FILE_PATH --clonator
                            {basic} --mutator {basic,preference} --selector
                            {basic,percentile} --affinity-threshold
                            AFFINITY_THRESHOLD --population-size
                            POPULATION_SIZE --n-generations N_GENERATIONS
                            [--logging-level {critical,error,warning,info,debug}]
                            [--n-cpu N_CPU] [--interactive-plot]
                            [--output-directory OUTPUT_DIRECTORY]

Program to solve the Santa's Workshop Tour 2019 problem.

optional arguments:
  -h, --help            show this help message and exit
  --logging-level {critical,error,warning,info,debug}
                        Logging level (default: 20).
  --n-cpu N_CPU         Number of CPU to be used (default: 1).
  --interactive-plot    Whether plot is rendering during optimization
                        (default: False).
  --output-directory OUTPUT_DIRECTORY
                        Directory where output files (plot, best solution and
                        logs) will be saved (default: output).

required named arguments:
  --data-file-path DATA_FILE_PATH
                        Path to the data to be optimized.

cloning algorithm required named arguments:
  --clonator {basic}    Cloning algorithm to be used.

mutation algorithm required named arguments:
  --mutator {basic,preference}
                        Mutation algorithm to be used.

selection algorithm required named arguments:
  --selector {basic,percentile}
                        Selection algorithm to be used.
  --affinity-threshold AFFINITY_THRESHOLD
                        Threshold according to which the selection is done.

artificial immune system algorithm required named arguments:
  --population-size POPULATION_SIZE
                        Size of population.
  --n-generations N_GENERATIONS
                        Number of generations.
```

5. Run the optimization using the Artificial Immune System algorithm.
```bash
$ python -m santas_workshop_tour <arguments>
```
