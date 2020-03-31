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
