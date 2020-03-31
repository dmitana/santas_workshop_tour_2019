import pandas as pd


def get_df_families(n_families, family_size):
    """
    Get families dataframe.

    :param n_families: int, number of families.
    :param family_size: int, size of each family.
    :return: pandas.DataFrame, families dataframe.
    """
    return pd.DataFrame(
        [
            [i, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, family_size]
            for i in range(n_families)
        ],
        columns=[
            'family_id', 'choice_0', 'choice_1', 'choice_2', 'choice_3',
            'choice_4', 'choice_5', 'choice_6', 'choice_7', 'choice_8',
            'choice_9', 'n_people'
        ]
    )
