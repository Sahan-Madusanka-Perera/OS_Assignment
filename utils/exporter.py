import csv
import json
from datetime import datetime
from typing import Dict, Any

class ResultsExporter:
    """Export simulation results to various formats"""
    
    @staticmethod
    def export_to_csv(results: Dict[str, Any], filename: str):
        """Export simulation history to CSV file"""
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Step', 'Page', 'Frames', 'Page Fault', 'TLB Hit', 'Working Set Size']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for step in results['history']:
                writer.writerow({
                    'Step': step['step'],
                    'Page': step['page'],
                    'Frames': str(step['frames']),
                    'Page Fault': 'Yes' if step['page_fault'] else 'No',
                    'TLB Hit': 'Yes' if step.get('tlb_hit') else 'No' if step.get('tlb_hit') is not None else 'N/A',
                    'Working Set Size': step.get('working_set_size', 'N/A')
                })
    
    @staticmethod
    def export_to_json(results: Dict[str, Any], filename: str):
        """Export complete results to JSON file"""
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'algorithm': results.get('algorithm'),
            'statistics': {
                'page_faults': results.get('page_faults'),
                'hits': results.get('hits'),
                'hit_ratio': results.get('hit_ratio'),
                'fault_ratio': results.get('fault_ratio')
            },
            'tlb_stats': results.get('tlb_stats'),
            'working_set_stats': results.get('working_set_stats'),
            'history': results.get('history')
        }
        
        with open(filename, 'w') as jsonfile:
            json.dump(export_data, jsonfile, indent=2)
    
    @staticmethod
    def export_comparison_to_csv(comparison_results: list, filename: str):
        """Export algorithm comparison to CSV"""
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Algorithm', 'Page Faults', 'Hits', 'Hit Ratio', 'Fault Ratio', 
                         'TLB Hits', 'TLB Misses', 'TLB Hit Ratio']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for name, result in comparison_results:
                row = {
                    'Algorithm': name,
                    'Page Faults': result['page_faults'],
                    'Hits': result['hits'],
                    'Hit Ratio': f"{result['hit_ratio']:.4f}",
                    'Fault Ratio': f"{result['fault_ratio']:.4f}"
                }
                
                if 'tlb_stats' in result:
                    tlb = result['tlb_stats']
                    row['TLB Hits'] = tlb['hits']
                    row['TLB Misses'] = tlb['misses']
                    row['TLB Hit Ratio'] = f"{tlb['hit_ratio']:.4f}"
                else:
                    row['TLB Hits'] = 'N/A'
                    row['TLB Misses'] = 'N/A'
                    row['TLB Hit Ratio'] = 'N/A'
                
                writer.writerow(row)
    
    @staticmethod
    def export_summary_report(results: Dict[str, Any], filename: str):
        """Export a text summary report"""
        with open(filename, 'w') as f:
            f.write("Virtual Memory Simulation Report\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Algorithm: {results.get('algorithm')}\n\n")
            
            f.write("Performance Metrics:\n")
            f.write("-" * 50 + "\n")
            f.write(f"Total Accesses: {len(results.get('history', []))}\n")
            f.write(f"Page Faults: {results.get('page_faults')}\n")
            f.write(f"Hits: {results.get('hits')}\n")
            f.write(f"Hit Ratio: {results.get('hit_ratio', 0):.2%}\n")
            f.write(f"Fault Ratio: {results.get('fault_ratio', 0):.2%}\n\n")
            
            if 'tlb_stats' in results:
                tlb = results['tlb_stats']
                f.write("TLB Statistics:\n")
                f.write("-" * 50 + "\n")
                f.write(f"TLB Hits: {tlb['hits']}\n")
                f.write(f"TLB Misses: {tlb['misses']}\n")
                f.write(f"TLB Hit Ratio: {tlb['hit_ratio']:.2%}\n")
                f.write(f"TLB Size: {tlb['size']}/{tlb['capacity']}\n\n")
            
            if 'working_set_stats' in results:
                ws = results['working_set_stats']
                f.write("Working Set Analysis:\n")
                f.write("-" * 50 + "\n")
                f.write(f"Final Working Set Size: {ws['current_working_set']}\n")
                f.write(f"Fault Rate: {ws['fault_rate']:.2%}\n")
                f.write(f"Thrashing Detected: {'Yes' if ws['is_thrashing'] else 'No'}\n")
