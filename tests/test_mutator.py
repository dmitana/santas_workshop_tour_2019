import unittest
import copy
from santas_workshop_tour.antibody import Antibody
from santas_workshop_tour.mutator import BasicMutator
from tests.helpers import get_df_families


class TestMutator(unittest.TestCase):
    """Class for testing methods of `Mutator` classes."""

    def test_basic_mutate_solutions(self):
        """
        Test whether created `Antibody` was mutated by `BasicMutator`
        class.
        """
        fitness_value = 25
        n_mutations = 5
        n_performed_mutations = 0
        n_families, family_size = 1000, 20
        df_families = get_df_families(n_families, family_size)

        antibody = Antibody()
        antibody.generate_solution(df_families)
        antibody.fitness_value = fitness_value

        basic_mutator = BasicMutator()
        mutated_antibody = basic_mutator.mutate(
            [[copy.deepcopy(antibody)]],
            [family_size] * n_families
        )[0][0]

        for i in range(n_families):
            if antibody.families[i] != mutated_antibody.families[i]:
                n_performed_mutations += 1

        self.assertEqual(
            n_mutations,
            n_performed_mutations,
            msg=f'Number of mutations was `{n_performed_mutations}`, expected '
                f'`{n_mutations}`.'
        )
