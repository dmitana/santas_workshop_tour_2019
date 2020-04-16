import numpy as np
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


class PercentileAffinitySelector(Selector):
    """
    Percentile Affinity Selector implementation.

    Selects members of population according to percentile of affinity of
    population. Affinity threshold is used as percentile.
    """

    def select(self, population):
        """
        Select new population from given `population`.

        Members in population are selected, if their affinity is not
        larger than percentile of affinity of population. Affinity
        threshold is used as percentile.

        :param population: list, list of `Antibody` objects.
        :return: list, list of `Antibody` objects.
        """
        if not (0 <= self.affinity_threshold <= 100):
            raise ValueError(
                'Value of `affinity_threshold` must be from interval <0, 100>.'
            )

        percentile = np.percentile(
            [x.affinity_value for x in population],
            self.affinity_threshold
        )

        return list(
            filter(lambda x: x.affinity_value <= percentile, population)
        )
