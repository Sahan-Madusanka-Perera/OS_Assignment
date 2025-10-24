from simulator.tlb import TLB
from simulator.working_set import WorkingSetTracker
from simulator.performance_metrics import PerformanceMetrics

class VMSimulator:
    def __init__(self, reference_string, num_frames, algorithm, use_tlb=True, tlb_size=4):
        self.reference_string = reference_string
        self.num_frames = num_frames
        self.algorithm = algorithm
        self.history = []
        self.use_tlb = use_tlb
        self.tlb = TLB(tlb_size) if use_tlb else None
        self.working_set_tracker = WorkingSetTracker()
        self.performance_metrics = PerformanceMetrics()

    def run(self):
        for i, page in enumerate(self.reference_string):
            tlb_hit = False
            
            if self.use_tlb and self.tlb:
                tlb_hit, frame = self.tlb.lookup(page)
                if tlb_hit:
                    page_fault = False
                    self.algorithm.hits += 1
                    self.performance_metrics.record_tlb_hit()
                else:
                    old_frames = set(self.algorithm.get_frames())
                    page_fault = self.algorithm.access_page(page)
                    new_frames = set(self.algorithm.get_frames())
                    
                    evicted_pages = old_frames - new_frames
                    for evicted_page in evicted_pages:
                        self.tlb.invalidate(evicted_page)
                    
                    if page in self.algorithm.get_frames():
                        frame_index = self.algorithm.get_frames().index(page)
                        self.tlb.update(page, frame_index)
                    
                    if page_fault:
                        self.performance_metrics.record_page_fault()
                    else:
                        self.performance_metrics.record_tlb_miss_memory_hit()
            else:
                page_fault = self.algorithm.access_page(page)
                if page_fault:
                    self.performance_metrics.record_page_fault()
                else:
                    self.performance_metrics.record_tlb_miss_memory_hit()
            
            self.working_set_tracker.record_access(page, page_fault)
            
            self.history.append({
                'step': i + 1,
                'page': page,
                'frames': self.algorithm.get_frames(),
                'page_fault': page_fault,
                'tlb_hit': tlb_hit if self.use_tlb else None,
                'working_set_size': self.working_set_tracker.get_working_set_size()
            })

        return self.get_results()

    def get_results(self):
        total_accesses = len(self.reference_string)
        results = {
            'page_faults': self.algorithm.page_faults,
            'hits': self.algorithm.hits,
            'hit_ratio': self.algorithm.hits / total_accesses if total_accesses > 0 else 0,
            'fault_ratio': self.algorithm.page_faults / total_accesses if total_accesses > 0 else 0,
            'history': self.history,
            'algorithm': self.algorithm.get_name()
        }
        
        if self.use_tlb and self.tlb:
            results['tlb_stats'] = self.tlb.get_stats()
        
        results['working_set_stats'] = self.working_set_tracker.get_statistics()
        results['performance_metrics'] = self.performance_metrics.get_effective_access_time()
        results['average_access_time'] = self.performance_metrics.get_average_access_time(total_accesses)
        
        return results