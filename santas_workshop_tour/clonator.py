import math
import copy
from abc import ABC, abstractmethod


class Clonator(ABC):
    """Clonator abstract class."""

    @abstractmethod
    def clone(self, population):
        """
        Clone given `population`.

        :param population: list, list of `Antibody` objects.
        :return: list, list of `Antibody` objects.
        """
        pass


class BasicClonator(Clonator):
    """
    Basic Clonator implementation using `population` inverse fitness
    values.
    """

    def clone(self, population):
        """
        Creates clones for each member of `population`.

        Number of created clones depends on inverse fitness of member of
        `population`.

        :param population: list, list of `Antibody` objects which will
            be cloned.
        :return: list, list of `Antibody` objects, which are clones of
            `population`.
        """
        clones = []
        max_fitness = 0
        for member in population:
            if member.fitness_value > max_fitness:
                max_fitness = member.fitness_value

        for member in population:
            fitness_diff = max_fitness - member.fitness_value
            if fitness_diff > 2:
                num_of_clones = round(math.log2(fitness_diff))
            else:
                num_of_clones = 1
            for _ in range(num_of_clones):
                clones.append(copy.deepcopy(member))

        return clones
