from abc import ABC, abstractmethod


class Mutator(ABC):
    """Mutator abstract class."""
    @abstractmethod
    def mutate(self, population):
        """
        Mutate given `population`.

        :param population: list, list of `Antibody` objects.
        :return: list, list of `Antibody` objects.
        """
        pass
