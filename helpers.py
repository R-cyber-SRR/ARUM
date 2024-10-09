import os
import uuid
import json
from datetime import datetime
from typing import Dict, Tuple, Optional, Any
from PIL import Image, ImageDraw, ImageFont
import re
from werkzeug.utils import secure_filename

class BannerGenerationError(Exception):
    """Custom exception for banner generation errors"""
    pass

def generate_unique_filename(original_filename: str) -> str:
    """
    Generate a unique filename for storing banners
    
    Args:
        original_filename (str): Original filename
        
    Returns:
        str: Unique filename with timestamp and UUID
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    filename = secure_filename(original_filename)
    name, ext = os.path.splitext(filename)
    return f"banner_{timestamp}_{unique_id}{ext}"

def validate_banner_params(params: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate banner generation parameters
    
    Args:
        params (dict): Dictionary containing banner parameters
        
    Returns:
        tuple: (is_valid, error_message)
    """
    required_params = ['text', 'width', 'height', 'fontSize', 'textColor']
    
    # Check for required parameters
    for param in required_params:
        if param not in params:
            return False, f"Missing required parameter: {param}"
    
    # Validate dimensions
    try:
        width = int(params['width'])
        height = int(params['height'])
        font_size = int(params['fontSize'])
        
        if not (300 <= width <= 2000):
            return False, "Width must be between 300 and 2000 pixels"
        if not (100 <= height <= 1000):
            return False, "Height must be between 100 and 1000 pixels"
        if not (12 <= font_size <= 120):
            return False, "Font size must be between 12 and 120 pixels"
            
    except ValueError:
        return False, "Invalid numeric values for dimensions or font size"
    
    # Validate text
    if not params['text'].strip():
        return False, "Banner text cannot be empty"
    if len(params['text']) > 100:
        return False, "Banner text must be less than 100 characters"
        
    # Validate color (hex format)
    if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', params['textColor']):
        return False, "Invalid color format. Use hex color (e.g., #FF0000)"
        
    return True, ""

def clean_text(text: str) -> str:
    """
    Clean and sanitize text for banner generation
    
    Args:
        text (str): Input text
        
    Returns:
        str: Cleaned text
    """
    # Remove any HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def get_font_path(style: str = 'modern') -> str:
    """
    Get the appropriate font path based on style
    
    Args:
        style (str): Banner style (modern, vintage, minimalist, bold)
        
    Returns:
        str: Path to font file
    """
    # Define font mappings (adjust paths according to your project structure)
    font_mapping = {
        'modern': 'fonts/Roboto-Regular.ttf',
        'vintage': 'fonts/PlayfairDisplay-Regular.ttf',
        'minimalist': 'fonts/Montserrat-Light.ttf',
        'bold': 'fonts/Oswald-Bold.ttf'
    }
    
    # Get the base path of your application
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Get the font path or default to modern
    font_file = font_mapping.get(style, font_mapping['modern'])
    
    # Construct the full path
    font_path = os.path.join(base_path, 'static', font_file)
    
    # Check if font exists, if not use system font
    if not os.path.exists(font_path):
        return "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # Default system font
        
    return font_path

def save_banner(image: Image.Image, filename: str, output_dir: str) -> str:
    """
    Save the generated banner to the filesystem
    
    Args:
        image (PIL.Image): Generated banner image
        filename (str): Filename for the banner
        output_dir (str): Directory to save the banner
        
    Returns:
        str: Path to saved banner
    """
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Construct full path
        filepath = os.path.join(output_dir, filename)
        
        # Save the image
        image.save(filepath, 'PNG', quality=95, optimize=True)
        
        return filepath
        
    except Exception as e:
        raise BannerGenerationError(f"Failed to save banner: {str(e)}")

def create_banner_response(filepath: str, width: int, height: int) -> Dict[str, Any]:
    """
    Create the response dictionary for the banner API
    
    Args:
        filepath (str): Path to the generated banner
        width (int): Banner width
        height (int): Banner height
        
    Returns:
        dict: Response dictionary
    """
    return {
        'banner_url': f'/static/banners/{os.path.basename(filepath)}',
        'width': width,
        'height': height,
        'timestamp': datetime.now().isoformat(),
        'success': True
    }

def get_banner_style_config(style: str) -> Dict[str, Any]:
    """
    Get configuration for different banner styles
    
    Args:
        style (str): Banner style name
        
    Returns:
        dict: Style configuration
    """
    styles = {
        'modern': {
            'background_color': '#4361ee',
            'gradient': True,
            'gradient_colors': ['#4361ee', '#3f37c9'],
            'shadow': True,
            'border_radius': 10,
        },
        'vintage': {
            'background_color': '#f4a261',
            'texture': True,
            'border': True,
            'border_color': '#e76f51',
            'border_width': 5,
        },
        'minimalist': {
            'background_color': '#ffffff',
            'stroke': True,
            'stroke_color': '#2b2d42',
            'stroke_width': 2,
        },
        'bold': {
            'background_color': '#2b2d42',
            'gradient': True,
            'gradient_colors': ['#2b2d42', '#8d99ae'],
            'shadow': True,
        }
    }
    
    return styles.get(style, styles['modern'])

def apply_style_effects(draw: ImageDraw, image: Image.Image, config: Dict[str, Any]) -> Image.Image:
    """
    Apply style effects to the banner
    
    Args:
        draw (ImageDraw): PIL ImageDraw object
        image (Image.Image): PIL Image object
        config (dict): Style configuration
        
    Returns:
        Image.Image: Processed image with effects
    """
    if config.get('gradient'):
        # Create gradient background
        from PIL import ImageDraw
        width, height = image.size
        for i in range(height):
            color = _interpolate_color(
                config['gradient_colors'][0],
                config['gradient_colors'][1],
                i / height
            )
            draw.line([(0, i), (width, i)], fill=color)
            
    if config.get('texture'):
        # Apply texture overlay
        texture = Image.new('RGBA', image.size, (255, 255, 255, 30))
        image = Image.alpha_composite(image, texture)
        
    if config.get('border'):
        # Draw border
        draw.rectangle(
            [(0, 0), image.size],
            outline=config['border_color'],
            width=config['border_width']
        )
        
    return image

def _interpolate_color(color1: str, color2: str, factor: float) -> str:
    """
    Interpolate between two colors
    
    Args:
        color1 (str): First color in hex format
        color2 (str): Second color in hex format
        factor (float): Interpolation factor (0-1)
        
    Returns:
        str: Interpolated color in hex format
    """
    # Convert hex to RGB
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
    
    # Interpolate
    r = int(r1 + factor * (r2 - r1))
    g = int(g1 + factor * (g2 - g1))
    b = int(b1 + factor * (b2 - b1))
    
    return f'#{r:02x}{g:02x}{b:02x}'