from flask import Flask, render_template
from backend.Media_processor import MediaServer
from backend.ai_processor import AIProcessor
from backend.stream_handler import StreamHandler
from config.settings import Config

app = Flask(__name__)
app.config.from_object(Config)

class ARUM:
    def __init__(self):
        self.media_server = MediaServer()
        self.ai_processor = AIProcessor()
        self.stream_handler = StreamHandler()
        
    def initialize(self):
        """Initialize all components"""
        self.media_server.start()
        self.ai_processor.start()
        self.stream_handler.start()
        
    def shutdown(self):
        """Gracefully shutdown all components"""
        self.media_server.stop()
        self.ai_processor.stop()
        self.stream_handler.stop()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream/<stream_id>')
def stream(stream_id):
    return render_template('stream.html', stream_id=stream_id)

if __name__ == '__main__':
    arum = ARUM()
    arum.initialize()
    app.run(debug=True)