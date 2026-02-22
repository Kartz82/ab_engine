import pandas as pd
import numpy as np
from src.engine.stats import ExperimentStats
from src.engine.randomization import Randomizer

# 1. SETUP: Configure the Experiment
EXP_ID = "google_ads_conversion_test_2026"
BASELINE_CONVERSION = 0.12  # 12% baseline
EXPECTED_LIFT = 0.10        # We expect a 10% relative lift (to 13.2%)
N_USERS = 5000              # Total users to simulate

# 2. SIMULATION: Generate Data
print(f"🚀 Running Simulation for {EXP_ID}...")
data = []
for i in range(N_USERS):
    user_id = f"user_{i}"
    variant = Randomizer.get_variant(user_id, EXP_ID)
    
    # Simulate different conversion rates for A and B
    prob = BASELINE_CONVERSION * 1.12 if variant == "B" else BASELINE_CONVERSION
    converted = np.random.binomial(1, prob)
    
    data.append({"user_id": user_id, "variant": variant, "converted": converted})

df = pd.DataFrame(data)

# 3. ANALYSIS: Run the Stats
stats_engine = ExperimentStats()
counts = df.groupby("variant")["converted"].agg(['sum', 'count'])

# Handle cases where a variant might be missing
results = stats_engine.analyze_proportions(
    count_a=counts.loc['A', 'sum'], nob_a=counts.loc['A', 'count'],
    count_b=counts.loc['B', 'sum'], nob_b=counts.loc['B', 'count']
)

# 4. REPORTING
print("\n" + "="*30)
print("EXPERIMENT RESULTS")
print("="*30)
print(f"Group A (Control):   {results['p_a']*100:.2f}% conversion")
print(f"Group B (Treatment): {results['p_b']*100:.2f}% conversion")
print(f"Relative Lift:       {results['lift']*100:.2f}%")
print(f"Statistical Sig:     {results['significant']}")
print(f"P-Value:             {results['p_value']}")
print("="*30)