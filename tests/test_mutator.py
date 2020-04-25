import unittest
import copy
from santas_workshop_tour.antibody import Antibody
from santas_workshop_tour.mutator import BasicMutator, PreferenceMutator, \
    AdvancedPreferenceMutator
from tests.helpers import get_df_families


class TestMutator(unittest.TestCase):
    """Class for testing methods of `Mutator` classes."""

    def test_basic_mutate_solutions(self):
        """
        Test whether created `Antibody` was mutated by `BasicMutator`
        class.
        """
        fitness_value = 125
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
            df_families=df_families
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

    def test_preference_mutate_solutions(self):
        """
        Test whether created `Antibody` was mutated by
        `PreferenceMutator` and `AdvancedPreferenceMutator` classes.
        """
        fitness_value = 125
        n_mutations = 5
        n_performed_mutations, n_advanced_performed_mutations = 0, 0
        n_families, family_size = 1000, 20
        df_families = get_df_families(n_families, family_size)

        antibody = Antibody()
        antibody.generate_solution(df_families)
        antibody.fitness_value = fitness_value

        preference_mutator = PreferenceMutator()
        mutated_antibody = preference_mutator.mutate(
            [[copy.deepcopy(antibody)]],
            df_families=df_families
        )[0][0]

        advanced_preference_mutator = AdvancedPreferenceMutator()
        advanced_mutated_antibody = advanced_preference_mutator.mutate(
            [[copy.deepcopy(antibody)]],
            df_families=df_families
        )[0][0]

        families_choices = df_families[[f'choice_{i}' for i in range(10)]] \
            .values
        for i in range(n_families):
            if antibody.families[i] != mutated_antibody.families[i]:
                n_performed_mutations += 1
                self.assertTrue(
                    mutated_antibody.families[i] in families_choices[i],
                    msg=f'Day mutated family is going to workshop is '
                        f'{mutated_antibody.families[i]}, expected one of '
                        f'{families_choices[i]}.'
                )
            if antibody.families[i] != advanced_mutated_antibody.families[i]:
                n_advanced_performed_mutations += 1
                self.assertTrue(
                    advanced_mutated_antibody.families[i] in
                    families_choices[i],
                    msg=f'Day advanced mutated family is going to workshop is '
                        f'{advanced_mutated_antibody.families[i]}, expected '
                        f'one of {families_choices[i]}.'
                )

        self.assertEqual(
            n_mutations,
            n_performed_mutations,
            msg=f'Number of mutations was `{n_performed_mutations}`, expected '
                f'`{n_mutations}`.'
        )

        self.assertEqual(
            n_mutations,
            n_advanced_performed_mutations,
            msg=f'Number of advanced mutations was '
                f'`{n_advanced_performed_mutations}`, expected '
                f'`{n_mutations}`.'
        )
