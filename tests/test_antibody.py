import unittest
import numpy as np
from santas_workshop_tour.antibody import Antibody


class TestAntibody(unittest.TestCase):
    """Class for testing methods of `Antibody` class."""
    def test_affinity(self):
        """Test affinity computation."""
        combinations = (
            (np.array([10, 20, 13, 15]), np.array([10, 20, 13, 15]), 4),
            (np.array([10, 20, 13, 15]), np.array([11, 20, 14, 1]), 1),
            (np.array([10, 22, 13, 15]), np.array([11, 20, 14, 1]), 0)
        )

        for families1, families2, expected_affinity in combinations:
            a1 = Antibody(families=families1)
            a2 = Antibody(families=families2)
            affinity = a1.affinity(a2)
            self.assertEqual(
                affinity,
                expected_affinity,
                msg=f'Affinity value between families `{families1}` and '
                    f'`{families2}` is `{a1.affinity_value}`, expected '
                    f'`{expected_affinity}`.'
            )
