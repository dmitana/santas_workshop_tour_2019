import unittest
import numpy as np
import pandas as pd
from santas_workshop_tour.antibody import Antibody


class TestAntibody(unittest.TestCase):
    """Class for testing methods of `Antibody` class."""
    def test_affinity(self):
        """Test affinity computation."""
        combinations = (
            (np.array([10, 20, 13, 15]), np.array([10, 20, 13, 15]), 4),
            (np.array([10, 20, 13, 15]), np.array([11, 20, 14, 1]), 1),
            (np.array([10, 22, 13, 15]), np.array([11, 20, 14, 1]), 0)
        )

        for families1, families2, expected_affinity in combinations:
            a1 = Antibody(families=families1)
            a2 = Antibody(families=families2)
            affinity = a1.affinity(a2)
            self.assertEqual(
                affinity,
                expected_affinity,
                msg=f'Affinity value between families `{families1}` and '
                    f'`{families2}` is `{a1.affinity_value}`, expected '
                    f'`{expected_affinity}`.'
            )

    def test_fitness(self):
        """Test fitness computation."""
        family_size = 126
        n_days = 11
        df_families = pd.DataFrame(
            [
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, family_size + 1],
                [1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, family_size],
                [2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, family_size],
                [3, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, family_size],
                [4, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, family_size],
                [5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, family_size],
                [6, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, family_size],
                [7, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, family_size],
                [8, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, family_size],
                [9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, family_size],
                [10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, family_size]
            ],
            columns=[
                'family_id', 'choice_0', 'choice_1', 'choice_2', 'choice_3',
                'choice_4', 'choice_5', 'choice_6', 'choice_7', 'choice_8',
                'choice_9', 'n_people'
            ]
        )
        families = np.array([i for i in range(1, n_days + 1)])
        days = np.array([family_size] * n_days)
        days[0] += 1

        expected_fitness = 50 * 2 + 100 + 200 * 2 + 300 * 2 + 400 + 500 * 2
        expected_fitness += (9 * 3 + 18 * 2 + 36 * 4 + 199 + 398) * family_size
        expected_fitness += 1 / 400. * family_size**(1 / 2.) * (n_days - 1)
        expected_fitness += 2 / 400. * (family_size + 1)**(1 / 2. + 1 / 50.)

        antibody = Antibody(families=families, days=days)
        antibody.fitness(df_families)

        self.assertAlmostEqual(
            antibody.fitness_value,
            expected_fitness,
            places=7,
            msg=f'Fitness of antibody is `{antibody.fitness_value}`, expected '
                f'`{expected_fitness}`.'
        )
