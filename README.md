# Virtual Memory Simulator

A professional desktop application for simulating and analyzing page replacement algorithms, Translation Lookaside Buffer (TLB), and working set behavior in virtual memory management systems.

## Overview

This simulator implements core operating system concepts related to virtual memory management. It provides comprehensive analysis tools for understanding how different page replacement algorithms perform under various workload conditions, demonstrating the practical impact of theoretical OS concepts.

## Core Features

### Page Replacement Algorithms
- **FIFO (First-In-First-Out)** - Queue-based replacement strategy
- **LRU (Least Recently Used)** - Recency-based replacement  
- **LFU (Least Frequently Used)** - Frequency-based replacement
- **Optimal (Belady's Algorithm)** - Theoretical optimal performance baseline
- **Clock (Second Chance)** - Efficient approximation of LRU

### Memory Management Components
- **TLB Simulation** - Hardware-level page table caching
  - Configurable cache size
  - Hit/miss ratio analysis
  - Performance impact quantification
  
- **Working Set Analysis** - Active page set monitoring
  - Real-time size calculation
  - Historical trend tracking
  - Thrashing detection system

- **Algorithm Comparison** - Parallel execution framework
  - Simultaneous multi-algorithm execution
  - Statistical comparison tables
  - Performance visualization

### Analysis Capabilities
- Step-by-step execution tracing
- Page fault and hit tracking
- TLB performance metrics
- Working set size monitoring
- Thrashing detection and warnings
- Export functionality (CSV, JSON, TXT)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup
```bash
git clone https://github.com/Sahan-Madusanka-Perera/OS_Assignment.git
cd OS_Assignment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## Usage

### GUI Application
```bash
python main.py
```

### Configuration
1. Set number of memory frames (1-10)
2. Select page replacement algorithm
3. Configure TLB size (2-16 entries)
4. Enable/disable TLB functionality
5. Input reference string (comma-separated page numbers)

### Execution Modes

#### Single Algorithm Analysis
Run one algorithm with detailed metrics:
- Click "Run Single Algorithm"
- View detailed execution in "Single Algorithm Results" tab
- Examine TLB performance in "TLB Analysis" tab
- Monitor working set in "Working Set & Thrashing" tab

#### Multi-Algorithm Comparison
Compare all algorithms simultaneously:
- Click "Compare All Algorithms"  
- View comparative analysis in "Algorithm Comparison" tab
- Export results for documentation

### Export Options
Export simulation data in multiple formats:
- **CSV** - Tabular data for spreadsheet analysis
- **JSON** - Structured data for programmatic processing
- **TXT** - Human-readable summary reports

## Command-Line Testing
```bash
python test_algorithms.py
```

## Example

### Input Configuration
```
Frames: 3
Algorithm: LRU
TLB Size: 4
Reference String: 7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1
```

### Expected Output
```
Algorithm Performance:
- FIFO: 15 page faults (25% hit ratio)
- LRU:  15 page faults (25% hit ratio)  
- LFU:  14 page faults (30% hit ratio)
- Optimal: 13 page faults (35% hit ratio)
- Clock: 15 page faults (25% hit ratio)

TLB Impact: 25-35% of accesses served from cache
Working Set: 5 unique pages (exceeds frame capacity)
```

## Project Structure

```
vm_simulator/
├── main.py                     # Application entry point
├── test_algorithms.py          # Command-line testing
├── gui/
│   ├── main_window.py          # Main window with tabbed interface
│   ├── visualization.py        # Single algorithm results
│   ├── comparison_widget.py    # Multi-algorithm comparison
│   ├── tlb_widget.py           # TLB performance visualization
│   ├── working_set_widget.py   # Working set analysis
│   └── results_panel.py        # Statistics display
├── simulator/
│   ├── algorithms.py           # Algorithms (FIFO, LRU, LFU, Optimal, Clock)
│   ├── simulator.py            # Simulation engine with TLB integration
│   ├── tlb.py                  # Translation Lookaside Buffer
│   ├── working_set.py          # Working set tracker with thrashing detection
│   └── page_table.py           # Page table management
└── utils/
    ├── reference_generator.py  # Test data generation
    └── exporter.py             # Results export (CSV, JSON, TXT)
```

## Algorithms

### FIFO (First-In-First-Out)
Replaces the oldest page in memory. Simple but can suffer from Belady's anomaly.

### LRU (Least Recently Used)
Replaces the page that hasn't been used for the longest time. Good practical performance.

### LFU (Least Frequently Used)
Replaces the page with the lowest access frequency. Effective for workloads with strong access patterns.

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
