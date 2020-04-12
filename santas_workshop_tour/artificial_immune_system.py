import logging
from santas_workshop_tour.antibody import Antibody


class ArtificialImmuneSystem:
    """
    Class representing Artificial Immune System algorithm.

    :param df_families: pandas.DataFrame, contains size and
        preferences of all families. Data to be optimized.
    :param clonator: Clonator, object to perform cloning.
    :param mutator: Mutator, object to perform mutations.
    :param selector: Selector, object to perform selection.
    :param population_size: int, size of population.
    :param n_generations: int, number of generations.
    """

    def __init__(
        self,
        df_families,
        clonator,
        mutator,
        selector,
        population_size,
        n_generations
    ):
        """
        Create a new object of class `ArtificialImmuneSystem`.

        :param df_families: pandas.DataFrame, contains size and
            preferences of all families. Data to be optimized.
        :param clonator: Clonator, object to perform cloning.
        :param mutator: Mutator, object to perform mutations.
        :param selector: Selector, object to perform selection.
        :param population_size: int, size of population.
        :param n_generations: int, number of generations.
        """
        self.df_families = df_families
        self.clonator = clonator
        self.mutator = mutator
        self.selector = selector
        self.population_size = population_size
        self.n_generations = n_generations
        self._logger = logging.getLogger(__name__) \
            .getChild(self.__class__.__name__)

    def generate_population(self):
        """
        Generate random population of antibodies of size
        `self.population_size`.

        :return: list, list of `Antibody` object.
        """
        return [
            Antibody().generate_solution(self.df_families)
            for _ in range(self.population_size)
        ]

    @staticmethod
    def affinity(population):
        """
        Compute affinity between each antibody in `population`.

        :param population: list, list of `Antibody` objects.
        """
        for i, a1 in enumerate(population):
            for a2 in population[i + 1:]:
                affinity = a1.affinity(a2)
                a1.affinity_value += affinity
                a2.affinity_value += affinity

    def fitness(self, population):
        """
        Compute fitness of each antibody in `population`.

        :param population: list, list of `Antibody` objects.
        :return:
            float, minimum fitness value.
            float, average fitness value.
        """
        min_fitness, sum_fitness = 999999999999, 0
        for antibody in population:
            antibody.fitness(self.df_families)
            sum_fitness += antibody.fitness_value
            if antibody.fitness_value < min_fitness:
                min_fitness = antibody.fitness_value

        return min_fitness, sum_fitness / len(population)

    def optimize(self):
        """
        Artificial Immune System optimization.

        Optimize solution for data in `self.df_families`.
        """
        # Initialization
        self._logger.info('Generating initial population')
        population = self.generate_population()
        self._logger.debug('Computing affinity')
        self.affinity(population)

        # Optimization loop
        for i in range(self.n_generations):
            self._logger.info(f'Generation {i+1}')
            self._logger.debug('Computing fitness')
            min_fitness, avg_fitness = self.fitness(population)
            self._logger.debug('Cloning')
            clones = self.clonator.clone(population)
            self._logger.debug('Mutating')
            clones = self.mutator.mutate(
                clones,
                self.df_families['n_people'].values
            )
            self._logger.debug('Computing affinity')
            self.affinity(clones)
            self._logger.debug('Selection')
            population = self.selector.select(clones)
            self._logger.info(
                f'Min fitness: {min_fitness}, Avg fitness: {avg_fitness}'
            )
