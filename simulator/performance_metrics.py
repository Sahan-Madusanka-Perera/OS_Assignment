class PerformanceMetrics:
    """Calculate realistic memory access times and performance metrics"""
    
    TLB_ACCESS_TIME = 2
    PAGE_TABLE_ACCESS_TIME = 100
    MEMORY_ACCESS_TIME = 100
    DISK_ACCESS_TIME = 10_000_000
    
    def __init__(self):
        self.total_time = 0
        self.tlb_access_count = 0
        self.page_table_access_count = 0
        self.memory_access_count = 0
        self.disk_access_count = 0
    
    def record_tlb_hit(self):
        """Record TLB hit (fastest path)"""
        self.tlb_access_count += 1
        self.memory_access_count += 1
        self.total_time += self.TLB_ACCESS_TIME + self.MEMORY_ACCESS_TIME
    
    def record_tlb_miss_memory_hit(self):
        """Record TLB miss but page in memory"""
        self.tlb_access_count += 1
        self.page_table_access_count += 1
        self.memory_access_count += 1
        self.total_time += (self.TLB_ACCESS_TIME + 
                           self.PAGE_TABLE_ACCESS_TIME + 
                           self.MEMORY_ACCESS_TIME)
    
    def record_page_fault(self):
        """Record page fault (slowest path)"""
        self.tlb_access_count += 1
        self.page_table_access_count += 1
        self.disk_access_count += 1
        self.memory_access_count += 1
        self.total_time += (self.TLB_ACCESS_TIME + 
                           self.PAGE_TABLE_ACCESS_TIME + 
                           self.DISK_ACCESS_TIME + 
                           self.MEMORY_ACCESS_TIME)
    
    def get_average_access_time(self, total_accesses: int) -> float:
        """Calculate average memory access time"""
        if total_accesses == 0:
            return 0
        return self.total_time / total_accesses
    
    def get_effective_access_time(self) -> dict:
        """Get detailed timing breakdown"""
        return {
            'total_time_ns': self.total_time,
            'total_time_ms': self.total_time / 1_000_000,
            'tlb_accesses': self.tlb_access_count,
            'page_table_accesses': self.page_table_access_count,
            'disk_accesses': self.disk_access_count,
            'memory_accesses': self.memory_access_count
        }
    
    def reset(self):
        """Reset all counters"""
        self.total_time = 0
        self.tlb_access_count = 0
        self.page_table_access_count = 0
        self.memory_access_count = 0
        self.disk_access_count = 0
