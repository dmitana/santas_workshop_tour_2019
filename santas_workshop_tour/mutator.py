import math
import numpy as np
from abc import ABC, abstractmethod


class Mutator(ABC):
    """Mutator abstract class."""

    @abstractmethod
    def mutate(self, population, df_families):
        """
        Mutate given `population`.

        :param population: list, list of `Antibody` objects.
        :param df_families: pandas.Dataframe, contains size and
            preferences of all families.
        :return: list, list of `Antibody` objects.
        """
        pass


class BasicMutator(Mutator):
    """
    Basic Mutator implementation.
    """

    def mutate(self, clones, df_families):
        """
        Mutate `population` of `Antibody` objects.

        :param clones: list, list of list of `Antibody` objects.
        :param df_families: pandas.Dataframe, contains size and
            preferences of all families.
        :return: list, list of list of mutated `Antibody` objects.
        """
        for clones_list in clones:
            for clone in clones_list:
                self._mutate(clone, df_families['n_people'].values)
        return clones

    def _mutate(self, antibody, families_sizes):
        """
        Mutates `antibody` in place by changing days families visit
        workshops.

        Number of mutations depends on fitness value of `antibody`.
        Higher fitness means worse solution and therefore more mutations
        and vice versa.

        :param antibody: Antibody, Antibody which will be mutated.
        :param families_sizes: list, list of sizes of all families.
        """
        n_mutations = round(math.pow(antibody.fitness_value, 1 / 3))
        n_families = len(families_sizes)
        families_original_days = {}
        for _ in range(n_mutations):
            while True:
                family = np.random.randint(0, n_families)
                family_size = families_sizes[family]

                day_to_move_from = antibody.families[family]
                day_to_move_to = np.random.randint(1, 101)
                if day_to_move_from == day_to_move_to:
                    continue

                if antibody.days[day_to_move_from] - family_size <= 125 or \
                        antibody.days[day_to_move_to] + family_size > 300:
                    continue

                if family in families_original_days:
                    if families_original_days[family] == day_to_move_to:
                        continue
                else:
                    families_original_days[family] = day_to_move_from

                antibody.families[family] = day_to_move_to
                antibody.days[day_to_move_from] -= family_size
                antibody.days[day_to_move_to] += family_size
                break


class PreferenceMutator(Mutator):
    """
    Preference Mutator implementation.

    When mutating, families preferences are taken into consideration.
    """

    def mutate(self, clones, df_families):
        """
        Mutate `population` of `Antibody` objects.

        :param clones: list, list of list of `Antibody` objects.
        :param df_families: pandas.Dataframe, contains size and
            preferences of all families.
        :return: list, list of list of mutated `Antibody` objects.
        """
        for clones_list in clones:
            for clone in clones_list:
                self._mutate(clone, df_families)
        return clones

    def _mutate(self, antibody, df_families):
        """
        Mutates `antibody` in place by changing days families visit
        workshops.

        Number of mutations depends on fitness value of `antibody`.
        Higher fitness means worse solution and therefore more mutations
        and vice versa.

        Mutations are performed by moving families to their prioritized
        days.

        :param antibody: Antibody, Antibody which will be mutated.
        :param df_families: pandas.Dataframe, contains size and
            preferences of all families.
        """
        n_mutations = round(math.pow(antibody.fitness_value, 1 / 3))
        n_families = len(df_families)
        families_hash_table = {}
        for _ in range(n_mutations):
            while True:
                family = np.random.randint(0, n_families)
                family_choice = np.random.randint(0, 10)

                family_row = df_families[df_families.family_id == family]
                family_size = family_row['n_people'].values[0]

                day_to_move_from = antibody.families[family]
                day_to_move_to = family_row[f'choice_{family_choice}'] \
                    .values[0]
                if day_to_move_from == day_to_move_to:
                    continue

                if antibody.days[day_to_move_from] - family_size <= 125 or \
                        antibody.days[day_to_move_to] + family_size > 300:
                    continue

                if family in families_hash_table:
                    continue
                else:
                    families_hash_table[family] = True

                antibody.families[family] = day_to_move_to
                antibody.days[day_to_move_from] -= family_size
                antibody.days[day_to_move_to] += family_size
                break
