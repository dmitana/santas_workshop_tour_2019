import unittest
import numpy as np
import pandas as pd
import os
from tests.helpers import get_df_families
from santas_workshop_tour.antibody import Antibody


class TestAntibody(unittest.TestCase):
    """Class for testing methods of `Antibody` class."""

    def test_equal(self):
        """Test equal comparison between two antibodies."""
        fitnesses = (0, 5, 10)
        for fitness in fitnesses:
            a1 = Antibody()
            a1.fitness_value = fitness
            a2 = Antibody()
            a2.fitness_value = fitness
            self.assertEqual(
                a1,
                a2,
                msg=f'Antibody `{a1}` should equal to `{a2}`.'
            )

    def test_lower_than(self):
        """Test less than comparison between two antibodies."""
        fitnesses = ((0, 1), (5, 10))
        for f1, f2 in fitnesses:
            a1 = Antibody()
            a1.fitness_value = f1
            a2 = Antibody()
            a2.fitness_value = f2
            self.assertLess(
                a1,
                a2,
                msg=f'Antibody `{a1}` should be less than `{a2}`.'
            )

    def test_generate_solution(self):
        """Test random solution generating."""
        expected_min_day_size = 125
        expected_max_day_size = 300
        real_data_path = 'data/family_data.csv'

        dfs = [get_df_families(1000, 20)]
        if os.path.isfile(real_data_path):
            dfs.append(pd.read_csv(real_data_path))

        for df_families in dfs:
            antibody = Antibody()
            antibody.generate_solution(df_families)

            day_sizes = {}
            for i, day in enumerate(antibody.families):
                value = day_sizes.get(day, 0)
                day_sizes[day] = value + df_families.iloc[i]['n_people']

            for key, size in antibody.days.items():
                expected_day_size = day_sizes[key]
                self.assertTrue(
                    expected_min_day_size <= size <= expected_max_day_size,
                    msg=f'Number of people scheduled for `{key + 1}th` day is '
                        f'`{size}`, expected to be '
                        f'in `<{expected_min_day_size}, '
                        f'{expected_max_day_size}>`.'
                )
                self.assertEqual(
                    size,
                    expected_day_size,
                    msg=f'Number of people scheduled for `{key + 1}th` day is '
                        f'{size}, expected `{expected_day_size}`.'
                )

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
        df_families = get_df_families(n_days, family_size)
        df_families.iloc[0]['n_people'] += 1
        families = np.array([i for i in range(1, n_days + 1)])
        days = {i: family_size for i in range(n_days)}
        days[0] += 1

        expected_fitness = 50 * 2 + 100 + 200 * 2 + 300 * 2 + 400 + 500 * 2
        expected_fitness += (9 * 3 + 18 * 2 + 36 * 4 + 199 + 398) * family_size
        expected_fitness += 1 / 400. * family_size ** (1 / 2.) * (n_days - 1)
        expected_fitness += 2 / 400. * (family_size + 1) ** (1 / 2. + 1 / 50.)

        antibody = Antibody(families=families, days=days)
        antibody.fitness(df_families)

        self.assertAlmostEqual(
            antibody.fitness_value,
            expected_fitness,
            places=7,
            msg=f'Fitness of antibody is `{antibody.fitness_value}`, expected '
                f'`{expected_fitness}`.'
        )
