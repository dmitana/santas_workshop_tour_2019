from abc import ABC, abstractmethod


class Selector(ABC):
    """
    Selector abstract class.

    :param affinity_threshold: int, threshold according to which the
        selection is done.
    """

    def __init__(self, affinity_threshold):
        """
        Constructor of `Selector` class.

        Since, `Selector` is an abstract class, this constructor is used
        to set attributes that will be inherited.

        :param affinity_threshold: int, threshold according to which the
            selection is done.
        """
        self.affinity_threshold = affinity_threshold

    @abstractmethod
    def select(self, population):
        """
        Select new population from given `population`.

        :param population: list, list of `Antibody` objects.
        :return: list, list of `Antibody` objects.
        """
        pass


class BasicSelector(Selector):
    """
    Basic Selector implementation.
    """

    def select(self, population):
        """
        Select new population from given `population`.

        Members in population are selected if their affinity is not
        larger than specified threshold.

        :param population: list, list of `Antibody` objects.
        :return: list, list of `Antibody` objects.
        """
        return list(
            filter(
                lambda x: x.affinity_value <= self.affinity_threshold,
                population
            )
        )
