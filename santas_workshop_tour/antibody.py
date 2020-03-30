import numpy as np


class Antibody:
    """
    This class represents one solution to the Santa's Workshop 2019
    problem.
    """
    def __init__(self, families=None):
        """
        Create a new object of class `Antibody`.

        :param families: numpy.ndarray (default: None),
        """
        self.families = families
        self.days = None
        self.affinity_value = 0

    def generate_solution(self, df_families):
        """
        Generate random solution.

        Target day for each family will be stored to `self.families`,
        where index represent the family.

        Number of people and IDs of all families scheduled for given day
        will be stored to `self.days`. Index represent the day.

        :param df_families: DataFrame, contains size and preferences of
            all families.
        """
        n_families, n_days = 5000, 100
        families = np.empty(n_families, dtype=object)
        days = np.empty(n_days, dtype=object)
        days_under_limits = np.ones(n_days, dtype=np.bool)

        # Initialize days
        for i in range(n_days):
            # Num of people, IDs of families
            days[i] = {'size': 0, 'families': []}
            days_under_limits[i] = i

        # Generate random day for each family
        for i in range(n_families):
            family_size = df_families.iloc[i]['n_people']
            while True:
                # IF branch makes sure only days under limit are picked
                if days_under_limits.sum() > 0:
                    day = np.random.randint(0, days_under_limits.sum())
                    day = np.nonzero(days_under_limits)[0][day]
                else:
                    day = np.random.randint(0, n_days)
                if (days[day]['size'] + family_size) <= 300:
                    days[day]['size'] += family_size
                    days[day]['families'].append(i)
                    families[i] = day
                    if days_under_limits.sum() > 0 and days[day]['size'] > 125:
                        days_under_limits[day] = False
                    break

        self.families = families
        self.days = days

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
