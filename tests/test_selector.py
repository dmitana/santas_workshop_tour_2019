import unittest
import numpy as np
from santas_workshop_tour.antibody import Antibody
from santas_workshop_tour.selector import BasicSelector, \
    PercentileAffinitySelector


class TestSelector(unittest.TestCase):
    """Class for testing methods of `Selector` classes."""

    def test_basic_select_solutions(self):
        """
        Test whether selected `Antibody` objects were selected according
        to `BasicSelector` rules.
        """
        antibodies = []
        affinity_threshold = 30
        affinities = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
        filtered_affinities = [15, 20, 25, 30]

        for affinity in affinities:
            antibody = Antibody()
            antibody.affinity_value = affinity
            antibodies.append(antibody)

        basic_selector = BasicSelector(affinity_threshold=affinity_threshold)
        selected_antibodies = basic_selector.select(antibodies)

        for antibody in selected_antibodies:
            self.assertTrue(
                antibody.affinity_value in filtered_affinities,
                msg=f'Antibody had affinity value '
                    f'`{antibody.affinity_value}`, expected value smaller or '
                    f'equal to `{affinity_threshold}`.'
            )

    def test_percentile_affinity_select_solutions(self):
        """
        Test whether selected `Antibody` objects were selected according
        to `PercentileAffinitySelector` rules.
        """
        antibodies = []
        affinities = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
        filtered_affinities = [
            [15, 20, 25, 30, 35],
            [15, 20, 25],
            [15, 20],
            [15]
        ]

        for affinity in affinities:
            antibody = Antibody()
            antibody.affinity_value = affinity
            antibodies.append(antibody)

        percentile_selector = PercentileAffinitySelector(affinity_threshold=50)
        for affinities_list in filtered_affinities:
            antibodies = percentile_selector.select(antibodies)

            for i, antibody in enumerate(antibodies):
                self.assertEqual(
                    antibody.affinity_value,
                    affinities_list[i],
                    msg=f'Antibody had affinity value '
                        f'`{antibody.affinity_value}`, expected '
                        f'`{affinities_list[i]}`.'
                )
