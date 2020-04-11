import unittest
from santas_workshop_tour.antibody import Antibody
from santas_workshop_tour.clonator import BasicClonator


class TestClonator(unittest.TestCase):
    """Class for testing methods of `Clonator` classes."""

    def test_basic_clone_solutions(self):
        """
        Test number of clones created by clone method of `BasicClonator`
        class.

        In `fitness_clones_pair` there are pairs of antibody fitness and
        expected cumulative number of clones. Cumulative number of
        clones is calculated with regards to all fitness values from
        `fitness_clones_pair` up to and including checked pair.
        """
        antibodies = []
        fitness_clones_pair = [
            [128, 1],
            [64, 7],
            [256, 16],
            [127, 23],
            [254, 24]
        ]

        basic_clonator = BasicClonator()

        for fitness, clones_cumulative in fitness_clones_pair:
            antibody = Antibody()
            antibody.fitness_value = fitness
            antibodies.append(antibody)

            returned_clones = basic_clonator.clone(antibodies)
            self.assertEqual(
                len(returned_clones),
                clones_cumulative,
                msg=f'Cumulative number of created clones was'
                    f'`{len(returned_clones)}`, expected '
                    f'`{clones_cumulative}`.'
            )
