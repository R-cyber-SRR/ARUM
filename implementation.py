from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

@app.route('/generate-banner', methods=['POST'])
def generate_banner():
    try:
        # Get parameters from request
        text = request.form.get('text', 'Default Text')
        width = int(request.form.get('width', 1200))
        height = int(request.form.get('height', 1300))
        font_size = int(request.form.get('fontSize', 56))
        text_color = request.form.get('textColor', '#FF0000')
        
        # Create new image with white background
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)
        
        # Load a font (make sure this font file exists in your system)
        try:
            font = ImageFont.truetype('arial.ttf', font_size)
        except:
            # Fallback to default font if arial is not available
            font = ImageFont.load_default()
        
        # Calculate text position to center it
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Draw text
        draw.text((x, y), text, fill=text_color, font=font)
        
        # Save the image
        output_path = os.path.join('static', 'generated_banner.png')
        image.save(output_path)
        
        return jsonify({'success': True, 'path': output_path})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # Make sure the static folder exists
    os.makedirs('static', exist_ok=True)
    app.run(debug=True)