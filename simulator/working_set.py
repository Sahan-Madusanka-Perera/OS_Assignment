from collections import deque
from typing import List, Set

class WorkingSetTracker:
    """Track working set and detect thrashing"""
    
    def __init__(self, window_size: int = 10, thrashing_threshold: float = 0.7):
        self.window_size = window_size
        self.thrashing_threshold = thrashing_threshold
        self.recent_accesses = deque(maxlen=window_size)
        self.recent_faults = deque(maxlen=window_size)
        self.working_set_history = []
    
    def record_access(self, page: int, is_fault: bool):
        """Record a page access"""
        self.recent_accesses.append(page)
        self.recent_faults.append(1 if is_fault else 0)
        
        current_working_set = len(set(self.recent_accesses))
        self.working_set_history.append(current_working_set)
    
    def get_working_set_size(self) -> int:
        """Get current working set size"""
        return len(set(self.recent_accesses))
    
    def get_fault_rate(self) -> float:
        """Get recent page fault rate"""
        if not self.recent_faults:
            return 0.0
        return sum(self.recent_faults) / len(self.recent_faults)
    
    def is_thrashing(self) -> bool:
        """Detect if system is thrashing"""
        if len(self.recent_faults) < self.window_size:
            return False
        return self.get_fault_rate() >= self.thrashing_threshold
    
    def get_statistics(self) -> dict:
        """Get working set statistics"""
        return {
            'current_working_set': self.get_working_set_size(),
            'fault_rate': self.get_fault_rate(),
            'is_thrashing': self.is_thrashing(),
            'working_set_history': self.working_set_history.copy()
        }
    
    def reset(self):
        """Reset tracking"""
        self.recent_accesses.clear()
        self.recent_faults.clear()
        self.working_set_history.clear()
