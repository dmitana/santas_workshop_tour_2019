import math
import numpy as np
from abc import ABC, abstractmethod


class Mutator(ABC):
    """Mutator abstract class."""

    @abstractmethod
    def mutate(self, population, families_sizes):
        """
        Mutate given `population`.

        :param population: list, list of `Antibody` objects.
        :param families_sizes: list, list of sizes of all families.
        :return: list, list of `Antibody` objects.
        """
        pass


class BasicMutator(Mutator):
    """
    Basic Mutator implementation.
    """

    def mutate(self, clones, families_sizes):
        """
        Mutate `population` of `Antibody` objects.

        :param clones: list, list of list of `Antibody` objects.
        :param families_sizes: list, list of sizes of all families.
        :return: list, list of list of mutated `Antibody` objects.
        """
        for clones_list in clones:
            for clone in clones_list:
                self._mutate(clone, families_sizes)
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
        n_mutations = round(math.pow(antibody.fitness_value, 1/3))
        n_families = len(families_sizes)
        families_original_days = {}
        for _ in range(n_mutations):
            while True:
                day_to_move_from = np.random.randint(0, 100)
                day_to_move_to = np.random.randint(0, 100)
                if day_to_move_from == day_to_move_to:
                    continue

                family = np.random.randint(0, n_families)
                family_size = families_sizes[family]

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
