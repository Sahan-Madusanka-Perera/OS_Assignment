class Statistics:
    """Statistical analysis utilities for algorithm performance"""
    
    @staticmethod
    def calculate_efficiency_score(results: dict) -> float:
        """Calculate overall efficiency score (0-100)"""
        hit_ratio = results.get('hit_ratio', 0)
        tlb_stats = results.get('tlb_stats', {})
        tlb_hit_ratio = tlb_stats.get('hit_ratio', 0) if tlb_stats else 0
        
        ws_stats = results.get('working_set_stats', {})
        thrashing = ws_stats.get('thrashing_detected', False) if ws_stats else False
        
        score = (hit_ratio * 0.5 + tlb_hit_ratio * 0.3) * 100
        
        if thrashing:
            score *= 0.5
        
        return min(100, max(0, score))
    
    @staticmethod
    def rank_algorithms(results_list: list) -> list:
        """Rank algorithms by multiple criteria"""
        rankings = []
        
        for name, result in results_list:
            score = Statistics.calculate_efficiency_score(result)
            avg_time = result.get('average_access_time', float('inf'))
            
            rankings.append({
                'algorithm': name,
                'efficiency_score': score,
                'page_faults': result['page_faults'],
                'avg_access_time_us': avg_time / 1000,
                'hit_ratio': result['hit_ratio']
            })
        
        rankings.sort(key=lambda x: (-x['efficiency_score'], x['page_faults'], x['avg_access_time_us']))
        
        for i, rank in enumerate(rankings, 1):
            rank['rank'] = i
        
        return rankings
    
    @staticmethod
    def get_recommendation(rankings: list) -> str:
        """Get algorithm recommendation based on rankings"""
        if not rankings:
            return "No data available"
        
        best = rankings[0]
        best_name = best['algorithm']
        score = best['efficiency_score']
        
        if score >= 80:
            return f"{best_name} - Excellent performance with high efficiency ({score:.1f}/100)"
        elif score >= 60:
            return f"{best_name} - Good performance, suitable for most cases ({score:.1f}/100)"
        elif score >= 40:
            return f"{best_name} - Moderate performance, consider optimization ({score:.1f}/100)"
        else:
            return f"{best_name} - Low efficiency, increase frames or review reference pattern ({score:.1f}/100)"
