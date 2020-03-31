from abc import ABC, abstractmethod


class Selector(ABC):
    """Selector abstract class."""
    @abstractmethod
    def select(self, population):
        """
        Select new population from given `population`.

        :param population: list, list of `Antibody` objects.
        :return: list, list of `Antibody` objects.
        """
        pass
