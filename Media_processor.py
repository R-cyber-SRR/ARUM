class MediaServer:
    def _init_(self):
        self.active = False
        
    def start(self):
        """Start the media server"""
        self.active = True
        print("Media server started")
        
    def stop(self):
        """Stop the media server"""
        self.active = False
        print("Media server stopped")