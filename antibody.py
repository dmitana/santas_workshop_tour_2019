import numpy as np


class Antibody:
    """
    This class represents one solution to the Santa's Workshop 2019
    problem.
    """

    def __init__(self, families):
        """
        Generate random solution. ID of day, number of people and IDs of
        all families scheduled for given day will be stored.

        :param families: DataFrame, contains size and preferences of all
            families.
        """
        days = {}
        days_under_limits = {}
        len_days_under_limits = 100

        # Initialize days dictionary
        for i in range(1, 101):
            # Day ID, num of people, IDs of families
            days[i] = {'id': i, 'size': 0, 'families': []}
            days_under_limits[i] = i

        # Generate random day for each family
        for i in range(1, 5001):
            family_size = families[families.family_id == i]['n_people']
            while True:
                # IF branch makes sure only days under limit are picked
                if len_days_under_limits > 0:
                    day = np.random.randint(0, len_days_under_limits + 1)
                    day = list(days_under_limits.values())[day]
                else:
                    day = np.random.randint(0, 101)
                if days[day]['size'] + family_size <= 300:
                    days[day]['size'] += family_size
                    days[day]['families'].append(i)
                    if len_days_under_limits > 0 & days[day]['size'] > 125:
                        len_days_under_limits -= 1
                        del days_under_limits[day]
        self.days = days
