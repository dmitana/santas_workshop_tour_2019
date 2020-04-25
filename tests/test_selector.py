import unittest
import copy
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
        negative_filtered_affinities = [15, 20, 25, 30]
        positive_filtered_affinities = [30, 35, 40, 45, 50, 55, 60]

        for affinity in affinities:
            antibody = Antibody()
            antibody.affinity_value = affinity
            antibodies.append(antibody)

        negative_basic_selector = BasicSelector(
            affinity_threshold=affinity_threshold,
            select_type='negative'
        )
        selected_antibodies = negative_basic_selector.select(antibodies)

        for antibody in selected_antibodies:
            self.assertTrue(
                antibody.affinity_value in negative_filtered_affinities,
                msg=f'Antibody had affinity value '
                    f'`{antibody.affinity_value}`, expected value smaller or '
                    f'equal to `{affinity_threshold}`.'
            )

        positive_basic_selector = BasicSelector(
            affinity_threshold=affinity_threshold,
            select_type='positive'
        )
        selected_antibodies = positive_basic_selector.select(antibodies)

        for antibody in selected_antibodies:
            self.assertTrue(
                antibody.affinity_value in positive_filtered_affinities,
                msg=f'Antibody had affinity value '
                    f'`{antibody.affinity_value}`, expected value greater or '
                    f'equal to `{affinity_threshold}`.'
            )

    def test_percentile_affinity_select_solutions(self):
        """
        Test whether selected `Antibody` objects were selected according
        to `PercentileAffinitySelector` rules.
        """
        antibodies = []
        affinities = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
        negative_filtered_affinities = [
            [15, 20, 25, 30, 35],
            [15, 20, 25],
            [15, 20],
            [15]
        ]

        positive_filtered_affinities = [
            [40, 45, 50, 55, 60],
            [50, 55, 60],
            [55, 60],
            [60]
        ]

        for affinity in affinities:
            antibody = Antibody()
            antibody.affinity_value = affinity
            antibodies.append(antibody)

        negative_percentile_selector = PercentileAffinitySelector(
            affinity_threshold=50,
            select_type='negative'
        )
        filtered_antibodies = copy.deepcopy(antibodies)
        for affinities_list in negative_filtered_affinities:
            filtered_antibodies = negative_percentile_selector.select(
                filtered_antibodies
            )

            for i, antibody in enumerate(filtered_antibodies):
                self.assertEqual(
                    antibody.affinity_value,
                    affinities_list[i],
                    msg=f'Antibody had affinity value '
                        f'`{antibody.affinity_value}`, expected '
                        f'`{affinities_list[i]}`.'
                )

        positive_percentile_selector = PercentileAffinitySelector(
            affinity_threshold=50,
            select_type='positive'
        )
        filtered_antibodies = copy.deepcopy(antibodies)
        for affinities_list in positive_filtered_affinities:
            filtered_antibodies = positive_percentile_selector.select(
                filtered_antibodies
            )

            for i, antibody in enumerate(filtered_antibodies):
                self.assertEqual(
                    antibody.affinity_value,
                    affinities_list[i],
                    msg=f'Antibody had affinity value '
                        f'`{antibody.affinity_value}`, expected '
                        f'`{affinities_list[i]}`.'
                )

    def test_selector_select_type(self):
        """
        Test whether incorrect select_type value raises ValueError.
        """
        self.assertRaises(ValueError, BasicSelector, 0, 'sfd')
