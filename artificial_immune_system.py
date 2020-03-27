import pandas as pd


class ArtificialImmuneSystem:
    """
    Class representing Artificial Immune System algorithm.
    """

    def __init__(self, path_to_data):
        self.families = pd.read_csv(path_to_data)
