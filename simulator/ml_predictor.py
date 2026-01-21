import numpy as np
from collections import deque, defaultdict

class MLPagePredictor:
    """Machine Learning-based page access prediction for proactive prefetching"""
    
    def __init__(self, window_size=10, pattern_depth=3):
        self.window_size = window_size
        self.pattern_depth = pattern_depth
        self.access_history = deque(maxlen=window_size)
        self.pattern_frequency = defaultdict(lambda: defaultdict(int))
        self.total_predictions = 0
        self.correct_predictions = 0
        self.confidence_threshold = 0.5
        self.recent_accuracy = deque(maxlen=20)
        
    def record_access(self, page: int):
        """Record page access and learn patterns"""
        if len(self.access_history) >= self.pattern_depth:
            pattern = tuple(list(self.access_history)[-self.pattern_depth:])
            self.pattern_frequency[pattern][page] += 1
        
        self.access_history.append(page)
    
    def adapt_threshold(self):
        """Dynamically adjust confidence threshold based on recent accuracy"""
        if len(self.recent_accuracy) >= 10:
            recent_acc = sum(self.recent_accuracy) / len(self.recent_accuracy)
            
            if recent_acc > 0.8:
                self.confidence_threshold = max(0.3, self.confidence_threshold - 0.05)
            elif recent_acc < 0.5:
                self.confidence_threshold = min(0.7, self.confidence_threshold + 0.05)
    
    def predict_next_page(self) -> tuple:
        """Predict next page based on learned patterns"""
        if len(self.access_history) < self.pattern_depth:
            return None, 0.0
        
        current_pattern = tuple(list(self.access_history)[-self.pattern_depth:])
        
        if current_pattern not in self.pattern_frequency:
            return None, 0.0
        
        predictions = self.pattern_frequency[current_pattern]
        if not predictions:
            return None, 0.0
        
        predicted_page = max(predictions.items(), key=lambda x: x[1])[0]
        total_occurrences = sum(predictions.values())
        confidence = predictions[predicted_page] / total_occurrences
        
        return predicted_page, confidence
    
    def verify_prediction(self, predicted_page: int, actual_page: int):
        """Track prediction accuracy with adaptive learning"""
        self.total_predictions += 1
        is_correct = (predicted_page == actual_page)
        
        if is_correct:
            self.correct_predictions += 1
            self.recent_accuracy.append(1)
        else:
            self.recent_accuracy.append(0)
        
        self.adapt_threshold()
    
    def get_accuracy(self) -> float:
        """Get prediction accuracy percentage"""
        if self.total_predictions == 0:
            return 0.0
        return (self.correct_predictions / self.total_predictions) * 100
    
    def get_statistics(self) -> dict:
        """Get prediction statistics"""
        return {
            'total_predictions': self.total_predictions,
            'correct_predictions': self.correct_predictions,
            'accuracy': self.get_accuracy(),
            'patterns_learned': len(self.pattern_frequency),
            'confidence_threshold': self.confidence_threshold,
            'recent_accuracy': (sum(self.recent_accuracy) / len(self.recent_accuracy) * 100) 
                              if self.recent_accuracy else 0
        }


class PredictiveAlgorithm:
    """Enhanced algorithm with ML-based prefetching"""
    
    def __init__(self, base_algorithm, prefetch_size=2):
        self.base_algorithm = base_algorithm
        self.predictor = MLPagePredictor()
        self.prefetch_size = prefetch_size
        self.prefetch_buffer = set()
        self.prefetch_hits = 0
        self.prefetch_misses = 0
        self.prefetch_attempts = 0
        self.prefetch_skips = 0
        self._last_prediction = None
        
    def access_page(self, page: int) -> bool:
        """Access page with adaptive predictive prefetching"""
        if page in self.prefetch_buffer and page in self.base_algorithm.get_frames():
            self.prefetch_hits += 1
            self.prefetch_buffer.remove(page)
        elif page in self.prefetch_buffer:
            self.prefetch_buffer.remove(page)

        if self._last_prediction is not None:
            self.predictor.verify_prediction(self._last_prediction, page)
            self._last_prediction = None

        self.predictor.record_access(page)
        page_fault = self.base_algorithm.access_page(page)

        predicted, confidence = self.predictor.predict_next_page()
        threshold = self.predictor.confidence_threshold
        if predicted is not None and confidence > threshold:
            if predicted == page or predicted in self.base_algorithm.get_frames():
                self.prefetch_skips += 1
            else:
                self.prefetch_attempts += 1
                did_prefetch = self.base_algorithm.prefetch_page(predicted)
                if did_prefetch:
                    self.prefetch_buffer.add(predicted)
                else:
                    self.prefetch_misses += 1
            self._last_prediction = predicted

        return page_fault

    def observe_access(self, page: int):
        """Observe an access without affecting base algorithm counters."""
        if page in self.prefetch_buffer and page in self.base_algorithm.get_frames():
            self.prefetch_hits += 1
            self.prefetch_buffer.remove(page)
        elif page in self.prefetch_buffer:
            self.prefetch_buffer.remove(page)

        if self._last_prediction is not None:
            self.predictor.verify_prediction(self._last_prediction, page)
            self._last_prediction = None

        self.predictor.record_access(page)

        predicted, confidence = self.predictor.predict_next_page()
        threshold = self.predictor.confidence_threshold
        if predicted is not None and confidence > threshold:
            if predicted == page or predicted in self.base_algorithm.get_frames():
                self.prefetch_skips += 1
            else:
                self.prefetch_attempts += 1
                did_prefetch = self.base_algorithm.prefetch_page(predicted)
                if did_prefetch:
                    self.prefetch_buffer.add(predicted)
                else:
                    self.prefetch_misses += 1
            self._last_prediction = predicted
    
    def get_frames(self):
        return self.base_algorithm.get_frames()
    
    def get_name(self):
        return f"{self.base_algorithm.get_name()} + ML Prediction"
    
    def reset(self):
        self.base_algorithm.reset()
        self.predictor = MLPagePredictor()
        self.prefetch_buffer.clear()
        self.prefetch_hits = 0
        self.prefetch_misses = 0
        self.prefetch_attempts = 0
        self.prefetch_skips = 0
    
    def get_prediction_stats(self) -> dict:
        """Get ML prediction statistics"""
        stats = self.predictor.get_statistics()
        stats['prefetch_hits'] = self.prefetch_hits
        stats['prefetch_attempts'] = self.prefetch_attempts
        stats['prefetch_skips'] = self.prefetch_skips
        stats['prefetch_effectiveness'] = (
            (self.prefetch_hits / self.prefetch_attempts * 100)
            if self.prefetch_attempts > 0 else 0
        )
        return stats
    
    @property
    def page_faults(self):
        return self.base_algorithm.page_faults
    
    @page_faults.setter
    def page_faults(self, value):
        self.base_algorithm.page_faults = value
    
    @property
    def hits(self):
        return self.base_algorithm.hits
    
    @hits.setter
    def hits(self, value):
        self.base_algorithm.hits = value
