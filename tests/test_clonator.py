import unittest
from santas_workshop_tour.antibody import Antibody
from santas_workshop_tour.clonator import BasicClonator


class TestClonator(unittest.TestCase):
    """Class for testing methods of `Clonator` classes."""

    def test_basic_clone_solutions(self):
        """
        Test number of clones created by clone method of `BasicClonator`
        class.
        """
        antibodies = []

        # Pairs of antibody fitness and expected number of clones
        fitness_clones_pair = [
            [128, 7],
            [64, 8],
            [256, 1],
            [127, 7],
            [254, 1]
        ]

        for fitness, _ in fitness_clones_pair:
            antibody = Antibody()
            antibody.fitness_value = fitness
            antibodies.append(antibody)

        basic_clonator = BasicClonator()
        clones_lists = basic_clonator.clone(antibodies)

        self.assertEqual(
            len(clones_lists),
            len(fitness_clones_pair),
            msg=f'Number of lists of clones is `{len(clones_lists)}`, '
                f'expected `{len(fitness_clones_pair)}`.'
        )

        for ((_, n_clones), clones) in zip(fitness_clones_pair, clones_lists):
            self.assertEqual(
                len(clones),
                n_clones,
                msg=f'Number of created clones is `{len(clones)}`, '
                    f'expected `{n_clones}`.'
            )
