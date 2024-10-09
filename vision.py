from PIL import Image
import io
import base64

def generate_banner(image_path, text):
    # Load image
    image = Image.open(image_path)
    
    # Here you could add text to the image using PIL
    # Example: draw text on image, resize, etc.
    
    # Save to a bytes buffer
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    buf.seek(0)

    return base64.b64encode(buf.read()).decode('utf-8')
