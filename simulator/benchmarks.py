import random
from typing import List

class WorkloadBenchmarks:
    """Industry-standard memory access patterns for algorithm evaluation"""
    
    @staticmethod
    def sequential_access(start: int = 0, length: int = 30) -> List[int]:
        """Simulates sequential file reading or array traversal"""
        return list(range(start, start + length))
    
    @staticmethod
    def loop_pattern(pages: List[int], iterations: int = 5) -> List[int]:
        """Simulates repeated loop execution in programs"""
        return pages * iterations
    
    @staticmethod
    def random_access(num_pages: int = 10, accesses: int = 40, seed: int = 42) -> List[int]:
        """Simulates database random queries or hash table lookups"""
        random.seed(seed)
        return [random.randint(0, num_pages - 1) for _ in range(accesses)]
    
    @staticmethod
    def locality_burst(hot_set: List[int], cold_set: List[int], bursts: int = 8) -> List[int]:
        """Simulates temporal locality (80/20 rule)"""
        pattern = []
        for _ in range(bursts):
            pattern.extend(hot_set * 4)
            pattern.extend(cold_set)
        return pattern
    
    @staticmethod
    def web_browsing() -> List[int]:
        """Simulates browser tab switching with working set"""
        tabs = [1, 2, 3, 4, 5]
        pattern = []
        
        pattern.extend([1, 2, 3])
        pattern.extend([1, 2])
        pattern.extend([4, 5])
        pattern.extend([1, 2, 3])
        pattern.extend([6, 7])
        pattern.extend([1, 2])
        pattern.extend([3, 4])
        pattern.extend([8, 9])
        pattern.extend([1, 2, 3])
        
        return pattern
    
    @staticmethod
    def video_streaming() -> List[int]:
        """Simulates video playback with seeks"""
        stream = list(range(1, 45))
        
        stream[15:15] = [5, 6, 7, 8]
        stream[30:30] = [20, 21, 22]
        stream[40:40] = [35, 36, 37, 38]
        
        return stream
    
    @staticmethod
    def database_query() -> List[int]:
        """Simulates database index and data page access"""
        pattern = []
        
        for query in range(5):
            pattern.append(0)
            pattern.extend([query * 2 + 1, query * 2 + 2])
        
        pattern.append(0)
        pattern.extend([3, 5, 7])
        pattern.append(0)
        pattern.extend([2, 4, 6])
        
        return pattern
    
    @staticmethod
    def matrix_multiplication() -> List[int]:
        """Simulates matrix operations with row/column access"""
        n = 4
        pattern = []
        
        for i in range(n):
            for j in range(n):
                pattern.append(i)
                pattern.append(n + j)
                pattern.append(2 * n + i * n + j)
        
        return pattern
    
    @staticmethod
    def get_all_benchmarks() -> dict:
        """Returns all benchmark workloads with metadata"""
        return {
            'Sequential': {
                'workload': WorkloadBenchmarks.sequential_access(),
                'description': 'Sequential file reading',
                'category': 'High Locality'
            },
            'Loop': {
                'workload': WorkloadBenchmarks.loop_pattern([1, 2, 3, 4]),
                'description': 'Repeated loop execution',
                'category': 'High Locality'
            },
            'Random': {
                'workload': WorkloadBenchmarks.random_access(),
                'description': 'Random database queries',
                'category': 'Low Locality'
            },
            'Locality Burst': {
                'workload': WorkloadBenchmarks.locality_burst([1, 2, 3], [4, 5, 6, 7]),
                'description': 'Temporal locality (80/20)',
                'category': 'Medium Locality'
            },
            'Web Browsing': {
                'workload': WorkloadBenchmarks.web_browsing(),
                'description': 'Browser tab switching',
                'category': 'Medium Locality'
            },
            'Video Streaming': {
                'workload': WorkloadBenchmarks.video_streaming(),
                'description': 'Video with seeks',
                'category': 'High Locality'
            },
            'Database': {
                'workload': WorkloadBenchmarks.database_query(),
                'description': 'Database index lookups',
                'category': 'Medium Locality'
            },
            'Matrix Ops': {
                'workload': WorkloadBenchmarks.matrix_multiplication(),
                'description': 'Matrix multiplication',
                'category': 'Medium Locality'
            }
        }
    
    @staticmethod
    def get_workload_stats(workload: List[int]) -> dict:
        """Calculate statistics for a workload"""
        return {
            'length': len(workload),
            'unique_pages': len(set(workload)),
            'working_set_ratio': len(set(workload)) / len(workload)
        }
