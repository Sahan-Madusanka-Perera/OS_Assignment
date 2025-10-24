class PageTable:
    """Page table implementation for managing frame allocations"""
    
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.frames = []
        self.page_faults = 0
        self.hits = 0

    def is_page_in_memory(self, page):
        """Check if a page is currently in memory"""
        return page in self.frames
    
    def add_page(self, page):
        """Add a page to memory"""
        if len(self.frames) < self.num_frames:
            self.frames.append(page)
        else:
            self.replace_page(page)
        self.page_faults += 1
    
    def replace_page(self, new_page):
        """Replace a page in memory (to be overridden by subclasses)"""
        if self.frames:
            self.frames.pop(0)
            self.frames.append(new_page)
    
    def get_frames(self):
        """Get current frame contents"""
        return self.frames.copy()
    
    def reset(self):
        """Reset the page table"""
        self.frames.clear()
        self.page_faults = 0
        self.hits = 0
