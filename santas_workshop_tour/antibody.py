import numpy as np


class Antibody:
    """
    This class represents one solution to the Santa's Workshop 2019
    problem.

    :param families: numpy.ndarray (default: None), array of target
        days for each family, where index represents the family.
    :param days: dict (default: None), dictionary of number of
        people scheduled for each day, where key represents the
        day.
    :param affinity_value: int (default: 0), affinity of antibody.
    :param fitness_value: float (default: 0.0), fitness of antibody.
    """

    def __init__(self, families=None, days=None):
        """
        Create a new object of class `Antibody`.

        :param families: numpy.ndarray (default: None), array of target
            days for each family, where index represents the family.
        :param days: numpy.ndarray (default: None), array of number of
            people scheduled for each day, where index represents the
            day.
        """
        self.families = families
        self.days = days
        self.affinity_value = 0
        self.fitness_value = 0.0

    def __eq__(self, other):
        """
        Rich comparison method for equivalence.

        :param other: Antibody, antibody to be compared with.
        :return: bool|NotImplemented, `True` if fitness values are equal
            otherwise `False`. `NotImplemented` is returned if `other`
            is not instance of `Antibody` class.
        """
        if not isinstance(other, Antibody):
            return NotImplemented
        return self.fitness_value == other.fitness_value

    def __lt__(self, other):
        """
        Rich comparison method for less than.

        :param other: Antibody, antibody to be compared with.
        :return: bool|NotImplemented, `True` if self's fitness values is
            lower than other's fitness value otherwise `False`.
            `NotImplemented` is returned if `other` is not instance of
            `Antibody` class.
        """
        if not isinstance(other, Antibody):
            return NotImplemented
        return self.fitness_value < other.fitness_value

    def generate_solution(self, df_families):
        """
        Generate random solution.

        Target day for each family will be stored to `self.families`,
        where index represent the family.

        Number of people scheduled for each day will be stored to
        `self.days`, where index represents the day.

        :param df_families: pandas.DataFrame, contains size and
            preferences of all families.
        :return: Antibody, self object.
        """
        n_families, n_days = len(df_families), 100
        families = np.empty(n_families, dtype=int)
        days = {}
        for i in range(1, n_days + 1):
            days[i] = 0
        days_under_limits = np.ones(n_days + 1, dtype=np.bool)
        len_days_under_limits = n_days  # Index 0 is not used

        # Generate random day for each family
        for i in range(n_families):
            family_size = df_families.iloc[i]['n_people']
            while True:
                # IF branch makes sure only days under limit are picked
                if len_days_under_limits > 0:
                    day = np.random.randint(1, len_days_under_limits + 1)
                    day = np.nonzero(days_under_limits)[0][day]
                else:
                    day = np.random.randint(1, n_days + 1)
                if (days[day] + family_size) <= 300:
                    days[day] += family_size
                    families[i] = day
                    if len_days_under_limits > 0 and days[day] > 125:
                        days_under_limits[day] = False
                        len_days_under_limits -= 1
                    break

        self.families = families
        self.days = days
        return self

    def affinity(self, other):
        """
        Compute affinity between `self` and `other` antibodies.

        Affinity is the number of families that have same day in both
        antibodies.

        :param other: Antibody, antibody towards which the affinity is
            computed.
        :return: int, affinity between `self` and `other` antibodies.
        """
        return (self.families == other.families).sum()

    def fitness(self, df_families):
        """
        Compute fitness function.

        Computed fitness is stored to `self.fitness`.

        Fitness is the sum of `preference cost` and `accounting penalty`.

        Santa provides consolation gifts (of varying value) to families
        according to their assigned day relative to their preferences.
        These sum up per family, and the total represents the `preference
        cost`.

        Santa's accountants have also developed an empirical equation
        for cost to Santa that arise from many different effects such as
        reduced shopping in the Gift Shop when it gets too crowded, extra
        cleaning costs, a very complicated North Pole tax code, etc.
        This cost in `accounting penalty`.

        Details can be found at
        https://www.kaggle.com/c/santa-workshop-tour-2019/overview/evaluation

        :param df_families: pandas.DataFrame, contains size and
            preferences of all families.
        :return: Antibody, self object.
        """
        preference_cost, accounting_penalty = 0, 0

        # Compute preference cost
        for i, day in enumerate(self.families):
            family = df_families.iloc[i]
            family_size = family['n_people']

            if day == family['choice_0']:
                consolation_gift = 0
            elif day == family['choice_1']:
                consolation_gift = 50
            elif day == family['choice_2']:
                consolation_gift = 50 + 9 * family_size
            elif day == family['choice_3']:
                consolation_gift = 100 + 9 * family_size
            elif day == family['choice_4']:
                consolation_gift = 200 + 9 * family_size
            elif day == family['choice_5']:
                consolation_gift = 200 + 18 * family_size
            elif day == family['choice_6']:
                consolation_gift = 300 + 18 * family_size
            elif day == family['choice_7']:
                consolation_gift = 300 + 36 * family_size
            elif day == family['choice_8']:
                consolation_gift = 400 + 36 * family_size
            elif day == family['choice_9']:
                consolation_gift = 500 + (36 + 199) * family_size
            else:
                consolation_gift = 500 + (36 + 398) * family_size

            preference_cost += consolation_gift

        # Compute accounting penalty
        days = list(self.days.values())
        previous_day = days[-1]
        for day in reversed(days):
            exponent = 1 / 2. + (day - previous_day) / 50.
            accounting_penalty += (day - 125) / 400. * day ** exponent
            previous_day = day

        self.fitness_value = preference_cost + accounting_penalty
        return self
