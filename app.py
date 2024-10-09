from flask import Flask, request, jsonify
from PIL import Image, ImageDraw
from datetime import datetime
import os
from utils.transformers import BannerTransformer, StylePresets

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/banners'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def generate_unique_filename(base_filename):
    """Generate a unique filename using timestamp"""
    name, ext = os.path.splitext(base_filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{name}_{timestamp}{ext}"

def save_banner(image, filename, upload_folder):
    """Save the banner image to the specified folder"""
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    filepath = os.path.join(upload_folder, filename)
    image.save(filepath)
    return filepath

def create_banner_response(filepath, width, height):
    """Create standardized response for successful banner generation"""
    return jsonify({
        'success': True,
        'banner_url': filepath,
        'dimensions': {
            'width': width,
            'height': height
        }
    })

def validate_banner_request(request_data):
    """Validate the incoming banner generation request"""
    required_fields = ['width', 'height', 'style']
    for field in required_fields:
        if field not in request_data:
            raise ValueError(f"Missing required field: {field}")
    
    width = int(request_data['width'])
    height = int(request_data['height'])
    
    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive numbers")
    
    if width > 4000 or height > 4000:
        raise ValueError("Maximum dimensions exceeded (4000x4000)")
    
    return width, height, request_data.get('style', 'modern')

@app.route('/generate-banner', methods=['POST'])
def generate_banner():
    try:
        # Validate request data
        request_data = request.get_json()
        width, height, style = validate_banner_request(request_data)
        
        # Create base image
        image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        
        # Initialize transformer
        transformer = BannerTransformer(image)
        
        # Get style preset
        style_preset = getattr(StylePresets, style, StylePresets.modern)()
        
        # Apply transformations
        if 'gradient' in style_preset:
            transformer.apply_gradient(**style_preset['gradient'])
        if 'texture' in style_preset:
            transformer.apply_texture(**style_preset['texture'])
        if 'overlay' in style_preset:
            transformer.apply_overlay(**style_preset['overlay'])
        if 'effects' in style_preset:
            transformer.apply_effects(style_preset['effects'])
            
        # Add text if provided
        if 'text' in request_data:
            draw = ImageDraw.Draw(transformer.get_image())
            text_config = request_data.get('text_config', {})
            # Add text drawing logic here based on your requirements
            # Example: draw.text((x, y), request_data['text'], font=font, fill=fill_color)
        
        # Save and return
        image = transformer.get_image()
        filename = generate_unique_filename('banner.png')
        filepath = save_banner(image, filename, app.config['UPLOAD_FOLDER'])
        
        return create_banner_response(filepath, width, height)
        
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        app.logger.error(f"Banner generation error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)