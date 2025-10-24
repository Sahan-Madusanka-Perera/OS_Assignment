# Quick Start Guide

## Installation
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

## Running the Application
```bash
python main.py
```

## Quick Test
```bash
python test_algorithms.py
```

## Basic Usage

### 1. Run Single Algorithm
1. Set **Frames**: 3
2. Select **Algorithm**: FIFO, LRU, Optimal, or Clock
3. Set **TLB Size**: 4 (recommended)
4. Check **Enable TLB**: ✓
5. Enter **Reference String**: `7,0,1,2,0,3,0,4,2,3,0,3,2`
6. Click **Run Single Algorithm**
7. View results in tabs:
   - Tab 1: Step-by-step execution
   - Tab 3: TLB statistics
   - Tab 4: Working set analysis

### 2. Compare All Algorithms
1. Configure same settings as above
2. Click **Compare All Algorithms**
3. View Tab 2: Side-by-side comparison

## Sample Reference Strings

### Small Test (Good for learning):
```
7,0,1,2,0,3,0,4,2,3,0,3,2
```

### Medium Test (Shows differences):
```
7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1
```

### Thrashing Demo (Working set > frames):
```
1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6
Frames: 3
Result: High fault rate, thrashing detected
```

### Good Locality (Low faults):
```
1,2,3,1,2,3,1,2,3,1,2,3,1,2,3
Frames: 3
Result: After initial faults, mostly hits
```

## Understanding Results

### Green Cells = Good
- Hits (page already in memory)
- TLB hits (fast lookup)

### Red Cells = Expensive
- Page faults (disk access required)

### Key Metrics
- **Hit Ratio**: Higher is better (aim for >30%)
- **TLB Hit Ratio**: Higher is better (aim for >40%)
- **Working Set**: Should be ≤ frames to avoid thrashing

## Common Scenarios

### Scenario 1: Normal Operation
```
Frames: 3
Working Set: 2-3
Fault Rate: <50%
Status: ✓ Normal
```

### Scenario 2: Thrashing
```
Frames: 3
Working Set: 5+
Fault Rate: >70%
Status: ⚠️ THRASHING
Solution: Increase frames OR reduce working set
```

### Scenario 3: Optimal TLB Usage
```
TLB Size: 4
Unique Pages: 4-5
TLB Hit Ratio: 40-50%
Status: Good performance
```

## Tips

1. **Start small**: Use 3 frames and short reference strings
2. **Compare algorithms**: Use comparison mode to see differences
3. **Experiment with TLB**: Try sizes 2, 4, 8 to see impact
4. **Watch for thrashing**: If working set > frames, increase frames
5. **Understand Optimal**: It's theoretical best (requires future knowledge)

## Troubleshooting

### No results showing?
- Check reference string format (comma-separated integers)
- Ensure at least one page in reference string

### GUI not opening?
- Check PyQt6 is installed: `pip install PyQt6`
- Check matplotlib: `pip install matplotlib`

### Strange results?
- Verify reference string is valid integers
- Try a simpler test case first
- Compare with test_algorithms.py output

## Project Structure
```
vm_simulator/
├── main.py              # GUI launcher
├── test_algorithms.py   # CLI testing
├── README.md            # Full documentation
├── FEATURES.md          # Detailed feature explanation
└── QUICKSTART.md        
```

## Next Steps

1. Read **README.md** for complete documentation
2. Read **FEATURES.md** for technical details
3. Experiment with different configurations
4. Try creating custom reference strings
5. You can check the results via charts

## For Suimulation

### What to Demonstrate:
1. Run all 4 algorithms on same input
2. Show comparison charts
3. Explain TLB performance impact
4. Demonstrate thrashing detection
5. Discuss algorithm trade-offs




