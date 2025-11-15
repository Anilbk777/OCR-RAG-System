import json
import os

class filekeygenerator:
    def __init__(self, counter_file="counters.json"):
        self.counter_file = counter_file
        # Load counters from file if exists
        if os.path.exists(self.counter_file):
            with open(self.counter_file, "r") as f:
                self.counters = json.load(f)
        else:
            self.counters = {
                "receipt": 0,
                "payment": 0,
                "statement": 0,
                "general": 0
            }

    def save_counters(self):
        with open(self.counter_file, "w") as f:
            json.dump(self.counters, f)

    def generate_key(self, document_type: str) -> str:
        """
        Generate a unique key based on document type:
        Receipt -> RCT
        Payment -> PAY
        Statement -> STM
        Unknown -> GEN
        """
        doc = document_type.lower()

        if "receipt" in doc:
            prefix = "RCT"
            self.counters["receipt"] += 1
            count = self.counters["receipt"]
        elif "payment" in doc:
            prefix = "PAY"
            self.counters["payment"] += 1
            count = self.counters["payment"]
        elif "statement" in doc:
            prefix = "STM"
            self.counters["statement"] += 1
            count = self.counters["statement"]
        else:
            prefix = "GEN"
            self.counters["general"] += 1
            count = self.counters["general"]

        # Save updated counters
        self.save_counters()

        return f"{prefix}{count:03d}"  # e.g., RCT001
