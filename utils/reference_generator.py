import random
from typing import List

class ReferenceGenerator:
    """Utility class to generate page reference strings for testing"""
    
    @staticmethod
    def generate_random(length: int, page_range: int) -> List[int]:
        """Generate random reference string"""
        return [random.randint(0, page_range - 1) for _ in range(length)]
    
    @staticmethod
    def generate_sequential(length: int, page_range: int) -> List[int]:
        """Generate sequential reference string"""
        return [i % page_range for i in range(length)]
    
    @staticmethod
    def generate_with_locality(length: int, page_range: int, locality_size: int = 5) -> List[int]:
        """Generate reference string with locality of reference"""
        reference_string = []
        current_set = random.sample(range(page_range), min(locality_size, page_range))
        
        for i in range(length):
            if i % 20 == 0 and i > 0:
                current_set = random.sample(range(page_range), min(locality_size, page_range))
            
            reference_string.append(random.choice(current_set))
        
        return reference_string
    
    @staticmethod
    def parse_from_string(ref_string: str) -> List[int]:
        """Parse reference string from comma-separated text"""
        return [int(x.strip()) for x in ref_string.split(',') if x.strip()]
