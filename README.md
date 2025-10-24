# Virtual Memory Simulator

A professional PyQt6-based desktop application for simulating and visualizing page replacement algorithms, TLB (Translation Lookaside Buffer), and working set behavior in virtual memory management.

## Features

### Core Page Replacement Algorithms
- **FIFO (First-In-First-Out)** - Simple queue-based replacement
- **LRU (Least Recently Used)** - Tracks page access history
- **Optimal (Belady's Algorithm)** - Theoretical best performance
- **Clock (Second Chance)** - Efficient circular buffer approach

### Advanced Memory Management Features
- **TLB Simulation** - Translation Lookaside Buffer for fast page table lookups
  - Configurable TLB size
  - TLB hit/miss statistics
  - Performance impact visualization
  
- **Working Set Tracking** - Monitor active page sets
  - Real-time working set size calculation
  - Historical tracking over time
  - Automatic thrashing detection with warnings

- **Multi-Algorithm Comparison** - Side-by-side performance analysis
  - Simultaneous execution of all algorithms
  - Comparative statistics tables
  - Visual performance charts

### Interactive Visualizations
- Step-by-step execution table with color coding
- Page fault vs hit bar charts
- TLB performance pie charts
- Working set size timeline graphs
- Algorithm comparison dashboards

### Performance Metrics
- Page fault count and hit count
- Hit ratio and fault ratio
- TLB hit ratio
- Working set size analysis
- Thrashing detection

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   .venv\Scripts\activate     # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Run the GUI Application
```bash
python main.py
```

### Using the Simulator

#### Single Algorithm Mode:
1. Configure simulation parameters:
   - Number of frames (1-10)
   - Algorithm selection
   - TLB size (2-16)
   - Enable/disable TLB
2. Enter reference string (comma-separated page numbers)
3. Click "Run Single Algorithm"
4. View results across multiple tabs:
   - Single Algorithm Results
   - TLB Analysis
   - Working Set & Thrashing

#### Comparison Mode:
1. Configure parameters
2. Enter reference string
3. Click "Compare All Algorithms"
4. View side-by-side comparison of all four algorithms

### Command Line Testing
```bash
python test_algorithms.py
```

## Example Usage

### Sample Input:
- **Frames**: 3
- **Reference String**: `7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2`
- **TLB**: Enabled (Size: 4)

### Expected Results:
- **Optimal**: Best hit ratio (~46%)
- **LRU/Clock**: Moderate performance (~31%)
- **FIFO**: Lower performance (~23%)
- **TLB**: Significant reduction in memory access time

## Project Structure

```
vm_simulator/
├── main.py                     # Application entry point
├── test_algorithms.py          # Command-line testing
├── gui/
│   ├── main_window.py          # Main application window with tabs
│   ├── visualization.py        # Single algorithm results display
│   ├── comparison_widget.py    # Multi-algorithm comparison
│   ├── tlb_widget.py           # TLB visualization
│   ├── working_set_widget.py   # Working set analysis
│   └── results_panel.py        # Statistics display
├── simulator/
│   ├── algorithms.py           # All page replacement algorithms
│   ├── simulator.py            # Core simulation engine with TLB
│   ├── tlb.py                  # TLB implementation
│   ├── working_set.py          # Working set tracker
│   └── page_table.py           # Page table management
└── utils/
    └── reference_generator.py  # Reference string generation utilities
```

## Algorithms

### FIFO (First-In-First-Out)
Replaces the oldest page in memory. Simple but can suffer from Belady's anomaly.

### LRU (Least Recently Used)
Replaces the page that hasn't been used for the longest time. Good practical performance.

### Optimal
Replaces the page that will not be used for the longest time in the future. Theoretical best performance (requires future knowledge).

### Clock (Second Chance)
Circular buffer with use bits, giving pages a second chance before replacement. Approximates LRU with better efficiency.

## Key Concepts Demonstrated

### TLB (Translation Lookaside Buffer)
- Hardware cache for page table entries
- Dramatically reduces memory access time
- Shows the full memory hierarchy: TLB → Page Table → Physical Memory → Disk

### Working Set
- Set of pages actively used by a process
- When working set > available frames → thrashing occurs
- System spends more time swapping pages than executing

### Thrashing Detection
- Monitors page fault rate over time
- Alerts when fault rate exceeds threshold (default: 70%)
- Suggests increasing frames or reducing working set

## Educational Value

This simulator demonstrates:
- Complete virtual memory management workflow
- Impact of different page replacement strategies
- Role of TLB in system performance
- Working set model and thrashing phenomenon
- Trade-offs between algorithm complexity and performance


## License

MIT License
