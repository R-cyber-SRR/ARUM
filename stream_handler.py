class StreamHandler:
    def _init_(self):
        self.active = False
        
    def start(self):
        """Start the stream handler"""
        self.active = True
        print("Stream handler started")
        
    def stop(self):
        """Stop the stream handler"""
        self.active = False
        print("Stream handler stopped")