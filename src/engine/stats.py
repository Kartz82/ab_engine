import numpy as np
from scipy import stats
from typing import Dict, List, Union

class ExperimentStats:
    @staticmethod
    def calculate_sample_size(baseline: float, mde: float, alpha: float = 0.05, power: float = 0.8) -> int:
        """Calculates required sample size per variant for a 2-sample proportion test."""
        p1 = baseline
        p2 = baseline * (1 + mde)
        p_avg = (p1 + p2) / 2
        
        z_alpha = stats.norm.ppf(1 - alpha / 2)
        z_beta = stats.norm.ppf(power)
        
        n = (z_alpha * np.sqrt(2 * p_avg * (1 - p_avg)) + z_beta * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2)))**2 / (p1 - p2)**2
        return int(np.ceil(n))

    @staticmethod
    def analyze_proportions(count_a: int, nob_a: int, count_b: int, nob_b: int, alpha: float = 0.05) -> Dict[str, Union[float, bool, list]]:
        """Performs a two-sample Z-test for proportions."""
        p_a = count_a / nob_a
        p_b = count_b / nob_b
        p_pooled = (count_a + count_b) / (nob_a + nob_b)
        
        se = np.sqrt(p_pooled * (1 - p_pooled) * (1/nob_a + 1/nob_b))
        z_stat = (p_b - p_a) / se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
        
        ci_lower = (p_b - p_a) - stats.norm.ppf(1 - alpha / 2) * se
        ci_upper = (p_b - p_a) + stats.norm.ppf(1 - alpha / 2) * se
        
        return {
            "p_a": round(p_a, 4),
            "p_b": round(p_b, 4),
            "lift": round((p_b - p_a) / p_a, 4),
            "p_value": round(p_value, 5),
            "ci": [round(ci_lower, 4), round(ci_upper, 4)],
            "significant": bool(p_value < alpha)
        }

    @staticmethod
    def get_decision(primary_result: Dict, guardrail_results: List[Dict]) -> str:
        """Determines if a feature should be shipped based on primary results and guardrails."""
        # 1. Check Primary Metric
        is_positive = primary_result.get('significant', False) and primary_result.get('lift', 0) > 0
        
        # 2. Check Guardrails (Block if any significant drop > 2%)
        guardrail_violated = any(
            g.get('significant', False) and g.get('lift', 0) < -0.02 
            for g in guardrail_results
        )
        
        if guardrail_violated:
            return "🛑 DO NOT SHIP: Guardrail Violated"
        if is_positive:
            return "✅ SHIP: Statistically Significant Gain"
        
        return "⚠️ INCONCLUSIVE: Keep A / Collect More Data"