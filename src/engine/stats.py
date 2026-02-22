@staticmethod
    def get_decision(primary_result: Dict, guardrail_results: List[Dict]) -> str:
        """
        Logic to determine if a feature should be shipped.
        """
        # 1. Check if Primary Metric is Significant and Positive
        is_positive = primary_result['significant'] and primary_result['lift'] > 0
        
        # 2. Check Guardrails
        # If any guardrail shows a significant negative impact, we BLOCK.
        guardrail_violated = any(g['significant'] and g['lift'] < -0.02 for g in guardrail_results)
        
        if guardrail_violated:
            return "🛑 DO NOT SHIP: Guardrail Violated"
        if is_positive:
            return "✅ SHIP: Statistically Significant Gain"
        
        return "⚠️ INCONCLUSIVE: Keep A / Collect More Data"