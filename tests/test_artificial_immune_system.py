import unittest
import numpy as np
from tests.helpers import get_df_families
from santas_workshop_tour.antibody import Antibody
from santas_workshop_tour.artificial_immune_system import \
    ArtificialImmuneSystem


class TestArtificialImmuneSystem(unittest.TestCase):
    """Class for testing methods of `ArtificialImmuneSystem` class."""

    def test_generate_population(self):
        """Test generating of initial population."""
        df_families = get_df_families(100, 20)
        population_sizes = (0, 1, 2, 100)
        for population_size in population_sizes:
            ais = ArtificialImmuneSystem(
                df_families=df_families, clonator=None, mutator=None,
                selector=None, population_size=population_size, n_generations=0
            )

            population = ais.generate_population()
            self.assertEqual(
                len(population),
                population_size,
                msg=f'Population size is `{len(population)}, expected '
                    f'`{population_size}`.'
            )

            population_size += 1
            population = ais.generate_population(n=population_size)
            self.assertEqual(
                len(population),
                population_size,
                msg=f'Population size from parameter `n` is '
                    f'`{len(population)}, expected `{population_size}`.'
            )

    def test_affinity(self):
        """Test affinity computation."""
        population = (
            Antibody(families=np.array([10, 20, 13, 15])),
            Antibody(families=np.array([10, 22, 13, 15])),
            Antibody(families=np.array([11, 20, 14, 1])),
        )
        expected_affinities = [4, 3, 1]
        ArtificialImmuneSystem.affinity(population)
        affinities = [a.affinity_value for a in population]

        self.assertEqual(
            affinities,
            expected_affinities,
            msg=f'Affinities values are `{affinities}`, expected '
                f'`{expected_affinities}`.'
        )

    def test_fitness(self):
        """Test fitness computation."""
        n_families, family_size = 3, 125
        df_families = get_df_families(n_families, family_size)
        days = np.array([family_size] * n_families)
        population = (
            Antibody(families=np.array([1, 2, 3]), days=days),
            Antibody(families=np.array([3, 3, 3]), days=days),
            Antibody(families=np.array([1, 1, 2]), days=days),
        )
        fitnesses = (
            50 * 2 + 9 * family_size, (50 + 9 * family_size) * n_families, 50
        )
        expected_fitness_min = np.min(fitnesses)
        expected_fitness_avg = np.mean(fitnesses)

        ais = ArtificialImmuneSystem(
            df_families=df_families, clonator=None, mutator=None,
            selector=None, population_size=0, n_generations=0
        )
        best_antibody, fitness_avg = ais.fitness(population)
        fitness_min = best_antibody.fitness_value

        self.assertAlmostEqual(
            fitness_min,
            expected_fitness_min,
            places=7,
            msg=f'Minimum fitness is `{fitness_min}`, expected '
                f'`{expected_fitness_min}`.'
        )
        self.assertAlmostEqual(
            fitness_avg,
            expected_fitness_avg,
            places=7,
            msg=f'Average fitness is `{fitness_avg}`, expected '
                f'`{expected_fitness_avg}`.'
        )

    def test_select_best(self):
        """
        Test selecting of best antibodies from population and clones.
        """
        ais = ArtificialImmuneSystem(
            df_families=None, clonator=None, mutator=None,
            selector=None, population_size=0, n_generations=0
        )
        population_fitness = [25, 15, 5, 38]
        clones_fitness = [[20, 20], [16, 16], [20, 15], [10, 40]]
        min_fitnesses = [20, 15, 5, 10]
        population, clones = [], []

        for fitness in population_fitness:
            antibody = Antibody()
            antibody.fitness_value = fitness
            population.append(antibody)

        for list_of_fitnesses in clones_fitness:
            clones_list = []
            for fitness in list_of_fitnesses:
                antibody = Antibody()
                antibody.fitness_value = fitness
                clones_list.append(antibody)
            clones.append(clones_list)

        new_population = ais.select_best(population, clones)
        for antibody, expected_fitness in zip(new_population, min_fitnesses):
            self.assertEqual(
                antibody.fitness_value,
                expected_fitness,
                msg=f'Fitness of antibody is `{antibody.fitness_value}`, '
                    f'expected `{expected_fitness}`.'
            )
