import unittest
import numpy as np
import pandas as pd
from santas_workshop_tour.antibody import Antibody
from santas_workshop_tour.artificial_immune_system import \
    ArtificialImmuneSystem


def get_df_families(n_families, family_size):
    """
    Get families dataframe.

    :param n_families: int, number of families.
    :param family_size: int, size of each family.
    :return: pandas.DataFrame, families dataframe.
    """
    return pd.DataFrame(
        [
            [i, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, family_size]
            for i in range(n_families)
        ],
        columns=[
            'family_id', 'choice_0', 'choice_1', 'choice_2', 'choice_3',
            'choice_4', 'choice_5', 'choice_6', 'choice_7', 'choice_8',
            'choice_9', 'n_people'
        ]
    )


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
        days = np.array([{'size': family_size} for _ in range(n_families)])
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
        fitness_min, fitness_avg = ais.fitness(population)

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
