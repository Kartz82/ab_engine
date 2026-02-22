import yaml
import pandas as pd
import numpy as np
import yaml
from src.engine.stats import ExperimentStats
from src.engine.randomization import Randomizer

# Load settings from config/experiment_config.yaml
with open("config/experiment_config.yaml", "r") as f:
    config_data = yaml.safe_load(f)

EXP_ID = config_data['experiment_name']
BASELINE_CONVERSION = config_data['parameters']['baseline_value']
EXPECTED_LIFT = config_data['parameters']['mde']
N_USERS = 5000 # We can also move this to YAML

# 2. SIMULATION: Generate Data
print(f"🚀 Running Simulation for {EXP_ID}...")
data = []
for i in range(N_USERS):
    user_id = f"user_{i}"
    variant = Randomizer.get_variant(user_id, EXP_ID)
    
    # Simulate different conversion rates for A and B
    prob = BASELINE_CONVERSION * (1 + EXPECTED_LIFT) if variant == "B" else BASELINE_CONVERSION
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

# 5. SAFETY CHECK (The Google gTech Way)
# Let's pretend we also tracked "Page Load Latency"
# If latency increases significantly, we shouldn't ship even if conversions are up.
simulated_latency_impact = {"significant": False, "lift": 0.01} # 1% slower

final_decision = stats_engine.get_decision(results, [simulated_latency_impact])

print(f"Final Product Recommendation: {final_decision}")

# 6. VISUALIZATION
stats_engine.visualize_results(results, "data/simulated/results_chart.png")