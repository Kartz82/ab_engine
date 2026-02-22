import hashlib

class Randomizer:
    @staticmethod
    def get_variant(user_id: str, experiment_id: str, split: float = 0.5) -> str:
        """
        Assigns a user to 'A' or 'B' using SHA-256 hashing for consistency.
        """
        # Create a unique salt for this specific experiment
        input_str = f"{user_id}_{experiment_id}"
        
        # Hash the string and convert to a numeric bucket
        hash_hex = hashlib.sha256(input_str.encode()).hexdigest()
        
        # Take the first 8 characters of the hash and convert to int
        # Modulo 1000 gives us a bucket between 0 and 999
        bucket = int(hash_hex[:8], 16) % 1000
        
        # Assign variant based on the split threshold
        return "B" if bucket < (split * 1000) else "A"