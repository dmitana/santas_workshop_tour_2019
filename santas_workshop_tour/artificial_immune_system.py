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

    def generate_population(self, n=None):
        """
        Generate random population of antibodies of size
        `self.population_size`.

        :param n: int (default: None), size of population to be
            generated. If `None` then population of size
            `self.population_size` will be generated.
        :return: list, list of `Antibody` object.
        """
        n = self.population_size if n is None else n
        return [
            Antibody().generate_solution(self.df_families) for _ in range(n)
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
            Antibody, antibody with minimum fitness value.
            float, average fitness value.
        """
        sum_fitness = 0
        best_antibody = Antibody()
        best_antibody.fitness_value = 999999999999

        for antibody in population:
            antibody.fitness(self.df_families)
            sum_fitness += antibody.fitness_value
            if antibody.fitness_value < best_antibody.fitness_value:
                best_antibody = antibody

        return best_antibody, sum_fitness / len(population)

    def select_best(self, population, clones):
        """
        Select best antibodies from population and clones.

        i-th best antibody is one whose fitness is the lowest among i-th
        antibody in `population` and its corresponding i-th `clones`.

        :param population: list, list of `Antibody` objects.
        :param clones: list, list of list of `Antibody` objects.
        """
        new_population = []
        for antibody, list_of_clones in zip(population, clones):
            best_clone = min(list_of_clones)
            new_population.append(
                best_clone if best_clone < antibody else antibody
            )
        return new_population

    def optimize(self):
        """
        Artificial Immune System optimization.

        Optimize solution for data in `self.df_families`.
        """
        # Initialization
        self._logger.info('Initial population generation')
        population = self.generate_population()
        self._logger.debug('Affinity computation')
        self.affinity(population)

        # Optimization loop
        for i in range(self.n_generations):
            self._logger.info(f'Generation {i+1}')
            self._logger.debug('Fitness computation')
            best_antibody, avg_fitness = self.fitness(population)

            self._logger.debug('Cloning')
            clones = self.clonator.clone(population)

            self._logger.debug('Mutating')
            clones = self.mutator.mutate(
                clones,
                self.df_families['n_people'].values
            )

            self._logger.debug('Clones fitness computation')
            for list_of_clones in clones:
                self.fitness(list_of_clones)

            self._logger.debug(
                f'Best antibody from population and clones selection'
            )
            population = self.select_best(population, clones)

            self._logger.debug('Affinity computation')
            self.affinity(population)

            self._logger.debug('Selecting')
            population = self.selector.select(population)
            self._logger.debug(
                f'Population size after selection {len(population)}'
            )

            n = self.population_size - len(population)
            if n > 0:
                self._logger.debug('New antibodies generation')
                population.extend(self.generate_population(n=n))

            self._logger.info(
                f'Min fitness: {best_antibody.fitness_value}, '
                f'Avg fitness: {avg_fitness}'
            )
