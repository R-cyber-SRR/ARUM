class AIProcessor:
    def _init_(self):
        self.active = False
        
    def start(self):
        """Start the AI processor"""
        self.active = True
        print("AI processor started")
        
    def stop(self):
        """Stop the AI processor"""
        self.active = False
        print("AI processor stopped")