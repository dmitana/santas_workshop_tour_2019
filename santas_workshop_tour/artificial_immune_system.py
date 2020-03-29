import pandas as pd


class ArtificialImmuneSystem:
    """
    Class representing Artificial Immune System algorithm.
    """

    def __init__(self, path_to_data):
        """
        Create a new object of class `ArtificialImmuneSystem`.

        :param path_to_data: str, path to the data to be optimized.
        """
        self.families = pd.read_csv(path_to_data)
