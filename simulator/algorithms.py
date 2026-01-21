from abc import ABC, abstractmethod
from collections import deque
from typing import List, Tuple, Any

class Algorithm(ABC):
    def __init__(self, frame_count: int):
        self.num_frames = frame_count
        self.page_faults = 0
        self.hits = 0

    @abstractmethod
    def access_page(self, page: int) -> bool:
        pass

    @abstractmethod
    def get_frames(self) -> List[int]:
        pass

    @abstractmethod
    def reset(self):
        pass

    def get_name(self) -> str:
        pass

    def prefetch_page(self, page: int) -> bool:
        """Prefetch a page without affecting hit/fault counters."""
        raise NotImplementedError

class FIFOAlgorithm(Algorithm):
    def __init__(self, num_frames: int):
        super().__init__(num_frames)
        self.frames = deque()

    def access_page(self, page: int) -> bool:
        if page in self.frames:
            self.hits += 1
            return False
        
        self.page_faults += 1

        if len(self.frames) < self.num_frames:
            self.frames.append(page)
        else:
            self.frames.popleft()
            self.frames.append(page)

        return True
    
    def get_frames(self) -> List[int]:
        return list(self.frames)
    
    def reset(self):
        self.frames.clear()
        self.page_faults = 0
        self.hits = 0

    def get_name(self) -> str:
        return "FIFO"

    def prefetch_page(self, page: int) -> bool:
        if page in self.frames:
            return False
        if len(self.frames) < self.num_frames:
            self.frames.append(page)
        else:
            self.frames.popleft()
            self.frames.append(page)
        return True
    
class LRUAlgorithm(Algorithm):
    def __init__(self, num_frames: int):
        super().__init__(num_frames)
        self.frames = {}
        self.time = 0
    
    def access_page(self, page: int) -> bool:
        self.time += 1

        if page in self.frames:
            self.frames[page] = self.time
            self.hits += 1
            return False
        
        self.page_faults += 1

        if len(self.frames) < self.num_frames:
            self.frames[page] = self.time
        else:
            lru_page = min(self.frames, key=self.frames.get)
            del self.frames[lru_page]
            self.frames[page] = self.time

        return True
    
    def get_frames(self) -> List[int]:
        return list(self.frames.keys())
    
    def reset(self):
        self.frames.clear()
        self.page_faults = 0
        self.hits = 0
        self.time = 0

    def get_name(self) -> str:
        return "LRU"

    def prefetch_page(self, page: int) -> bool:
        if page in self.frames:
            return False
        self.time += 1
        if len(self.frames) < self.num_frames:
            self.frames[page] = self.time
        else:
            lru_page = min(self.frames, key=self.frames.get)
            del self.frames[lru_page]
            self.frames[page] = self.time
        return True


class OptimalAlgorithm(Algorithm):
    def __init__(self, num_frames: int):
        super().__init__(num_frames)
        self.frames = []
        self.reference_string = []
        self.current_index = 0

    def set_reference_string(self, reference_string: List[int]):
        self.reference_string = reference_string

    def access_page(self, page: int) -> bool:
        if page in self.frames:
            self.hits += 1
            self.current_index += 1
            return False
        
        self.page_faults += 1

        if len(self.frames) < self.num_frames:
            self.frames.append(page)
        else:
            farthest_use = -1
            victim_index = 0
            
            for i, frame_page in enumerate(self.frames):
                try:
                    next_use = self.reference_string[self.current_index + 1:].index(frame_page)
                except ValueError:
                    victim_index = i
                    break
                
                if next_use > farthest_use:
                    farthest_use = next_use
                    victim_index = i
            
            self.frames[victim_index] = page

        self.current_index += 1
        return True
    
    def get_frames(self) -> List[int]:
        return self.frames.copy()
    
    def reset(self):
        self.frames.clear()
        self.page_faults = 0
        self.hits = 0
        self.current_index = 0

    def get_name(self) -> str:
        return "Optimal"

    def prefetch_page(self, page: int) -> bool:
        if page in self.frames:
            return False
        if len(self.frames) < self.num_frames:
            self.frames.append(page)
            return True
        farthest_use = -1
        victim_index = 0
        for i, frame_page in enumerate(self.frames):
            try:
                next_use = self.reference_string[self.current_index + 1:].index(frame_page)
            except ValueError:
                victim_index = i
                break
            if next_use > farthest_use:
                farthest_use = next_use
                victim_index = i
        self.frames[victim_index] = page
        return True


class ClockAlgorithm(Algorithm):
    def __init__(self, num_frames: int):
        super().__init__(num_frames)
        self.frames = []
        self.use_bits = []
        self.hand = 0

    def access_page(self, page: int) -> bool:
        if page in self.frames:
            index = self.frames.index(page)
            self.use_bits[index] = 1
            self.hits += 1
            return False
        
        self.page_faults += 1

        if len(self.frames) < self.num_frames:
            self.frames.append(page)
            self.use_bits.append(1)
        else:
            while self.use_bits[self.hand] == 1:
                self.use_bits[self.hand] = 0
                self.hand = (self.hand + 1) % self.num_frames
            
            self.frames[self.hand] = page
            self.use_bits[self.hand] = 1
            self.hand = (self.hand + 1) % self.num_frames

        return True
    
    def get_frames(self) -> List[int]:
        return self.frames.copy()
    
    def reset(self):
        self.frames.clear()
        self.use_bits.clear()
        self.page_faults = 0
        self.hits = 0
        self.hand = 0

    def get_name(self) -> str:
        return "Clock"

    def prefetch_page(self, page: int) -> bool:
        if page in self.frames:
            return False
        if len(self.frames) < self.num_frames:
            self.frames.append(page)
            self.use_bits.append(1)
            return True
        while self.use_bits[self.hand] == 1:
            self.use_bits[self.hand] = 0
            self.hand = (self.hand + 1) % self.num_frames
        self.frames[self.hand] = page
        self.use_bits[self.hand] = 1
        self.hand = (self.hand + 1) % self.num_frames
        return True


class LFUAlgorithm(Algorithm):
    """Least Frequently Used: replaces page with lowest access frequency"""
    
    def __init__(self, num_frames: int):
        super().__init__(num_frames)
        self.frames = {}
        self.frequency = {}
        self.time = 0
    
    def access_page(self, page: int) -> bool:
        self.time += 1
        
        if page in self.frames:
            self.frequency[page] += 1
            self.hits += 1
            return False
        
        self.page_faults += 1
        
        if len(self.frames) < self.num_frames:
            self.frames[page] = self.time
            self.frequency[page] = 1
        else:
            min_freq = min(self.frequency.values())
            lfu_candidates = [p for p, f in self.frequency.items() if f == min_freq]
            
            if len(lfu_candidates) == 1:
                victim = lfu_candidates[0]
            else:
                victim = min(lfu_candidates, key=lambda p: self.frames[p])
            
            del self.frames[victim]
            del self.frequency[victim]
            self.frames[page] = self.time
            self.frequency[page] = 1
        
        return True
    
    def get_frames(self) -> List[int]:
        return list(self.frames.keys())
    
    def reset(self):
        self.frames.clear()
        self.frequency.clear()
        self.page_faults = 0
        self.hits = 0
        self.time = 0
    
    def get_name(self) -> str:
        return "LFU"

    def prefetch_page(self, page: int) -> bool:
        if page in self.frames:
            return False
        self.time += 1
        if len(self.frames) < self.num_frames:
            self.frames[page] = self.time
            self.frequency[page] = 1
            return True
        min_freq = min(self.frequency.values())
        lfu_candidates = [p for p, f in self.frequency.items() if f == min_freq]
        if len(lfu_candidates) == 1:
            victim = lfu_candidates[0]
        else:
            victim = min(lfu_candidates, key=lambda p: self.frames[p])
        del self.frames[victim]
        del self.frequency[victim]
        self.frames[page] = self.time
        self.frequency[page] = 1
        return True

