import pandas as pd
import numpy as np
from src.engine.randomization import Randomizer

class ExperimentSimulator:
    @staticmethod
    def generate_data(n_users: int, exp_id: str, true_p_a: float, true_p_b: float) -> pd.DataFrame:
        """
        Creates a synthetic dataset of users and their conversion outcomes.
        """
        data = []
        randomizer = Randomizer()

        for i in range(n_users):
            user_id = f"user_{i:05d}"
            # 1. Assign variant using our deterministic hashing
            variant = randomizer.get_variant(user_id, exp_id)
            
            # 2. Simulate conversion based on the 'True' probability of that group
            # Group B usually has the 'lift'
            prob = true_p_b if variant == "B" else true_p_a
            converted = np.random.binomial(1, prob)
            
            data.append({
                "user_id": user_id,
                "variant": variant,
                "converted": converted
            })
            
        return pd.DataFrame(data)