from simulator.algorithms import LRUAlgorithm
from simulator.simulator import VMSimulator
from simulator.ml_predictor import PredictiveAlgorithm

print('=' * 70)
print('ML PREDICTION FUNCTIONALITY TEST')
print('=' * 70)

# Test 1: Check if ML learns patterns
reference_string = [1,2,3,1,2,3,1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4,5,1,2,3,4,5,1,2,3,4,5]
num_frames = 3

print(f'\nTest Pattern: 1,2,3 repeating, then adds 4, then 5')
print(f'Frames: {num_frames} | Length: {len(reference_string)}\n')

# BASE LRU
base_algo = LRUAlgorithm(num_frames)
base_sim = VMSimulator(reference_string, num_frames, base_algo, use_tlb=False)
base_results = base_sim.run()

print(f'BASE LRU:')
print(f'  Page Faults: {base_results["page_faults"]}')
print(f'  Hits: {base_results["hits"]}')
print(f'  Hit Ratio: {base_results["hit_ratio"]:.1%}')

# ML-ENHANCED LRU
ml_algo = PredictiveAlgorithm(LRUAlgorithm(num_frames))
ml_sim = VMSimulator(reference_string, num_frames, ml_algo, use_tlb=False)
ml_results = ml_sim.run()
ml_stats = ml_algo.get_prediction_stats()

print(f'\nML-ENHANCED LRU:')
print(f'  Page Faults: {ml_results["page_faults"]}')
print(f'  Hits: {ml_results["hits"]}')
print(f'  Hit Ratio: {ml_results["hit_ratio"]:.1%}')

print(f'\nML STATISTICS:')
print(f'  Prediction Accuracy: {ml_stats["accuracy"]:.1f}%')
print(f'  Correct Predictions: {ml_stats["correct_predictions"]}/{ml_stats["total_predictions"]}')
print(f'  Patterns Learned: {ml_stats["patterns_learned"]}')
print(f'  Prefetch Hits: {ml_stats["prefetch_hits"]}')
print(f'  Prefetch Effectiveness: {ml_stats["prefetch_effectiveness"]:.1f}%')

fault_reduction = base_results['page_faults'] - ml_results['page_faults']
hit_improvement = ml_results['hits'] - base_results['hits']

print(f'\nIMPACT ANALYSIS:')
print(f'  Fault Reduction: {fault_reduction}')
print(f'  Additional Hits: +{hit_improvement}')
if base_results['page_faults'] > 0:
    improvement_pct = (fault_reduction / base_results['page_faults'] * 100)
    print(f'  Improvement: {improvement_pct:.1f}%')

print('\n' + '=' * 70)
if ml_stats['accuracy'] > 0:
    print('✅ ML IS WORKING - Pattern recognition active')
    print(f'   Learning rate: {ml_stats["accuracy"]:.0f}% prediction accuracy')
    if ml_stats['patterns_learned'] > 5:
        print(f'   {ml_stats["patterns_learned"]} patterns identified')
    if ml_stats['prefetch_hits'] > 0:
        print(f'   {ml_stats["prefetch_hits"]} successful prefetches')
else:
    print('❌ ML not learning - needs investigation')

print('=' * 70)
