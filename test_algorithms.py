"""
Test script for page replacement algorithms with TLB and working set tracking
"""
from simulator.algorithms import FIFOAlgorithm, LRUAlgorithm, LFUAlgorithm, OptimalAlgorithm, ClockAlgorithm
from simulator.simulator import VMSimulator

def test_algorithm(algorithm_class, name, num_frames, reference_string, use_tlb=True):
    """Test a single algorithm and print results"""
    algorithm = algorithm_class(num_frames)
    
    if name == "Optimal":
        algorithm.set_reference_string(reference_string)
    
    simulator = VMSimulator(reference_string, num_frames, algorithm, use_tlb=use_tlb)
    results = simulator.run()
    
    print(f"\n{name} Algorithm Results:")
    print(f"  Frames: {num_frames}")
    print(f"  Reference String: {reference_string}")
    print(f"  Page Faults: {results['page_faults']}")
    print(f"  Hits: {results['hits']}")
    print(f"  Hit Ratio: {results['hit_ratio']:.2%}")
    print(f"  Fault Ratio: {results['fault_ratio']:.2%}")
    
    if use_tlb and 'tlb_stats' in results:
        tlb = results['tlb_stats']
        print(f"\n  TLB Statistics:")
        print(f"    TLB Hits: {tlb['hits']}")
        print(f"    TLB Misses: {tlb['misses']}")
        print(f"    TLB Hit Ratio: {tlb['hit_ratio']:.2%}")
    
    if 'working_set_stats' in results:
        ws = results['working_set_stats']
        print(f"\n  Working Set Analysis:")
        print(f"    Final Working Set Size: {ws['current_working_set']}")
        print(f"    Fault Rate: {ws['fault_rate']:.2%}")
        print(f"    Thrashing: {'YES ⚠️' if ws['is_thrashing'] else 'NO ✓'}")

def main():
    """Run tests for all algorithms"""
    reference_string = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    num_frames = 3
    
    print("="*70)
    print("Virtual Memory Simulator - Extended Algorithm Tests")
    print("="*70)
    print(f"\nTest Configuration:")
    print(f"  Reference String Length: {len(reference_string)}")
    print(f"  Unique Pages: {len(set(reference_string))}")
    print(f"  Available Frames: {num_frames}")
    print(f"  TLB: Enabled (Size: 4)")
    
    algorithms = [
        (FIFOAlgorithm, "FIFO"),
        (LRUAlgorithm, "LRU"),
        (LFUAlgorithm, "LFU"),
        (OptimalAlgorithm, "Optimal"),
        (ClockAlgorithm, "Clock")
    ]
    
    for algo_class, name in algorithms:
        test_algorithm(algo_class, name, num_frames, reference_string, use_tlb=True)
    
    print("\n" + "="*70)
    print("\nKey Findings:")
    print("  Optimal algorithm provides theoretical minimum page faults")
    print("  LFU and LRU offer practical performance improvements over FIFO")
    print("  TLB caching significantly reduces memory access latency")
    print("  Working set exceeding frame count indicates potential thrashing")
    print("="*70)

if __name__ == "__main__":
    main()
