from simulator.benchmarks import WorkloadBenchmarks
from simulator.algorithms import LRUAlgorithm
from simulator.simulator import VMSimulator
from simulator.ml_predictor import PredictiveAlgorithm


benchmarks = WorkloadBenchmarks.get_all_benchmarks()
num_frames = 4

results = []

for name, data in benchmarks.items():
    workload = data['workload']
    
    base_algo = LRUAlgorithm(num_frames)
    base_sim = VMSimulator(workload, num_frames, base_algo, use_tlb=False)
    base_result = base_sim.run()
    
    ml_algo = PredictiveAlgorithm(LRUAlgorithm(num_frames))
    ml_sim = VMSimulator(workload, num_frames, ml_algo, use_tlb=False)
    ml_result = ml_sim.run()
    ml_stats = ml_algo.get_prediction_stats()
    
    improvement = ((base_result['page_faults'] - ml_result['page_faults']) / 
                   base_result['page_faults'] * 100) if base_result['page_faults'] > 0 else 0
    
    results.append({
        'name': name,
        'base_faults': base_result['page_faults'],
        'ml_faults': ml_result['page_faults'],
        'improvement': improvement,
        'accuracy': ml_stats['accuracy'],
        'category': data['category']
    })



