from collections import OrderedDict
from typing import Optional, Tuple

class TLB:
    """Translation Lookaside Buffer - cache for page table entries"""
    
    def __init__(self, capacity: int = 4):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.hits = 0
        self.misses = 0
    
    def lookup(self, page: int) -> Tuple[bool, Optional[int]]:
        """
        Look up a page in the TLB
        Returns: (hit, frame_number)
        """
        if page in self.cache:
            self.hits += 1
            self.cache.move_to_end(page)
            return True, self.cache[page]
        else:
            self.misses += 1
            return False, None
    
    def update(self, page: int, frame: int):
        """Add or update a page-to-frame mapping in TLB"""
        if page in self.cache:
            self.cache.move_to_end(page)
        else:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
            self.cache[page] = frame
    
    def invalidate(self, page: int):
        """Remove a page from TLB when it's evicted from memory"""
        if page in self.cache:
            del self.cache[page]
    
    def get_hit_ratio(self) -> float:
        """Calculate TLB hit ratio"""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0
    
    def reset(self):
        """Clear TLB"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
    
    def get_stats(self) -> dict:
        """Get TLB statistics"""
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_ratio': self.get_hit_ratio(),
            'size': len(self.cache),
            'capacity': self.capacity
        }
