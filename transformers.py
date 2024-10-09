from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
import numpy as np
from typing import Tuple, List, Dict, Any, Optional
import colorsys
import random

class BannerTransformer:
    """
    A class to handle various image transformations for banner generation
    """
    
    def __init__(self, image: Image.Image):
        """
        Initialize the transformer with an image
        
        Args:
            image (PIL.Image): The input image to transform
        """
        self.image = image
        self.width, self.height = image.size
        
    def apply_gradient(self, 
                      start_color: str, 
                      end_color: str, 
                      direction: str = 'horizontal') -> None:
        """
        Apply a gradient background to the image
        
        Args:
            start_color (str): Starting color in hex format (#RRGGBB)
            end_color (str): Ending color in hex format (#RRGGBB)
            direction (str): 'horizontal' or 'vertical'
        """
        # Convert hex to RGB
        start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
        end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
        
        # Create gradient array
        if direction == 'horizontal':
            gradient = np.linspace(0, 1, self.width)
            gradient = np.tile(gradient, (self.height, 1))
        else:
            gradient = np.linspace(0, 1, self.height)
            gradient = np.tile(gradient, (self.width, 1)).T
            
        # Create gradient image
        gradient_image = Image.new('RGBA', (self.width, self.height))
        draw = ImageDraw.Draw(gradient_image)
        
        for x in range(self.width):
            for y in range(self.height):
                factor = gradient[y, x]
                r = int(start_rgb[0] * (1 - factor) + end_rgb[0] * factor)
                g = int(start_rgb[1] * (1 - factor) + end_rgb[1] * factor)
                b = int(start_rgb[2] * (1 - factor) + end_rgb[2] * factor)
                draw.point((x, y), fill=(r, g, b, 255))
                
        # Composite gradient with original image
        self.image = Image.alpha_composite(gradient_image, self.image)
        
    def apply_texture(self, 
                     texture_type: str = 'noise', 
                     opacity: float = 0.2) -> None:
        """
        Apply a texture overlay to the image
        
        Args:
            texture_type (str): Type of texture ('noise', 'grain', 'paper')
            opacity (float): Opacity of the texture (0-1)
        """
        texture = Image.new('RGBA', (self.width, self.height))
        
        if texture_type == 'noise':
            # Create random noise
            noise = np.random.randint(0, 255, (self.height, self.width), dtype=np.uint8)
            texture = Image.fromarray(noise, 'L')
        elif texture_type == 'grain':
            # Create film grain effect
            noise = np.random.normal(127, 20, (self.height, self.width))
            noise = np.clip(noise, 0, 255).astype(np.uint8)
            texture = Image.fromarray(noise, 'L')
        elif texture_type == 'paper':
            # Create paper texture
            texture = self._create_paper_texture()
            
        # Convert to RGBA and set opacity
        texture = texture.convert('RGBA')
        texture.putalpha(int(255 * opacity))
        
        # Composite texture with original image
        self.image = Image.alpha_composite(self.image, texture)
        
    def apply_overlay(self, 
                     color: str, 
                     opacity: float = 0.3) -> None:
        """
        Apply a color overlay to the image
        
        Args:
            color (str): Color in hex format (#RRGGBB)
            opacity (float): Opacity of the overlay (0-1)
        """
        overlay = Image.new('RGBA', (self.width, self.height))
        draw = ImageDraw.Draw(overlay)
        
        # Convert hex to RGB
        r, g, b = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        
        # Draw overlay
        draw.rectangle([(0, 0), (self.width, self.height)], 
                      fill=(r, g, b, int(255 * opacity)))
                      
        # Composite overlay with original image
        self.image = Image.alpha_composite(self.image, overlay)
        
    def apply_effects(self, effects: Dict[str, Any]) -> None:
        """
        Apply multiple effects based on configuration
        
        Args:
            effects (dict): Dictionary of effects and their parameters
        """
        for effect, params in effects.items():
            if effect == 'blur':
                self.apply_blur(params.get('radius', 2))
            elif effect == 'shadow':
                self.apply_drop_shadow(
                    params.get('offset', (5, 5)),
                    params.get('shadow_color', '#000000'),
                    params.get('blur_radius', 3)
                )
            elif effect == 'border':
                self.apply_border(
                    params.get('width', 2),
                    params.get('color', '#000000')
                )
            elif effect == 'glow':
                self.apply_glow(
                    params.get('spread', 20),
                    params.get('intensity', 0.5)
                )
                
    def apply_blur(self, radius: int = 2) -> None:
        """
        Apply gaussian blur to the image
        
        Args:
            radius (int): Blur radius
        """
        self.image = self.image.filter(ImageFilter.GaussianBlur(radius))
        
    def apply_drop_shadow(self, 
                         offset: Tuple[int, int] = (5, 5),
                         shadow_color: str = '#000000',
                         blur_radius: int = 3) -> None:
        """
        Apply drop shadow to the image
        
        Args:
            offset (tuple): Shadow offset (x, y)
            shadow_color (str): Shadow color in hex format
            blur_radius (int): Shadow blur radius
        """
        # Create shadow image
        shadow = Image.new('RGBA', self.image.size, (0, 0, 0, 0))
        shadow.paste(self.image, offset)
        shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))
        
        # Convert shadow color
        r, g, b = tuple(int(shadow_color[i:i+2], 16) for i in (1, 3, 5))
        
        # Apply shadow color
        shadow_data = shadow.getdata()
        new_data = [(r, g, b, a) for (_, _, _, a) in shadow_data]
        shadow.putdata(new_data)
        
        # Create new image with shadow
        final_image = Image.new('RGBA', self.image.size, (0, 0, 0, 0))
        final_image = Image.alpha_composite(final_image, shadow)
        final_image = Image.alpha_composite(final_image, self.image)
        
        self.image = final_image
        
    def apply_border(self, 
                    width: int = 2, 
                    color: str = '#000000') -> None:
        """
        Apply border to the image
        
        Args:
            width (int): Border width
            color (str): Border color in hex format
        """
        draw = ImageDraw.Draw(self.image)
        
        # Convert color
        r, g, b = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        
        # Draw border
        draw.rectangle([(0, 0), (self.width-1, self.height-1)], 
                      outline=(r, g, b, 255), 
                      width=width)
                      
    def apply_glow(self, 
                  spread: int = 20, 
                  intensity: float = 0.5) -> None:
        """
        Apply outer glow effect
        
        Args:
            spread (int): Glow spread distance
            intensity (float): Glow intensity (0-1)
        """
        # Create glow layer
        glow = self.image.filter(ImageFilter.GaussianBlur(spread))
        enhancer = ImageEnhance.Brightness(glow)
        glow = enhancer.enhance(intensity)
        
        # Composite glow with original
        self.image = Image.alpha_composite(glow, self.image)
        
    def _create_paper_texture(self) -> Image.Image:
        """
        Create a paper-like texture
        
        Returns:
            PIL.Image: Paper texture image
        """
        texture = Image.new('L', (self.width, self.height))
        pixels = texture.load()
        
        # Generate base noise
        for x in range(self.width):
            for y in range(self.height):
                noise = random.randint(200, 255)
                pixels[x, y] = noise
                
        # Apply subtle variations
        texture = texture.filter(ImageFilter.GaussianBlur(1))
        
        return texture
        
    def get_image(self) -> Image.Image:
        """
        Get the transformed image
        
        Returns:
            PIL.Image: The transformed image
        """
        return self.image

class StylePresets:
    """
    Predefined style presets for banners
    """
    
    @staticmethod
    def modern() -> Dict[str, Any]:
        return {
            'gradient': {
                'start_color': '#4361ee',
                'end_color': '#3f37c9',
                'direction': 'horizontal'
            },
            'effects': {
                'shadow': {
                    'offset': (5, 5),
                    'blur_radius': 3
                },
                'border': {
                    'width': 0
                }
            }
        }
        
    @staticmethod
    def vintage() -> Dict[str, Any]:
        return {
            'overlay': {
                'color': '#f4a261',
                'opacity': 0.3
            },
            'texture': {
                'type': 'paper',
                'opacity': 0.2
            },
            'effects': {
                'border': {
                    'width': 5,
                    'color': '#e76f51'
                }
            }
        }
        
    @staticmethod
    def minimalist() -> Dict[str, Any]:
        return {
            'gradient': {
                'start_color': '#ffffff',
                'end_color': '#f8f9fa',
                'direction': 'vertical'
            },
            'effects': {
                'border': {
                    'width': 2,
                    'color': '#2b2d42'
                }
            }
        }
        
    @staticmethod
    def bold() -> Dict[str, Any]:
        return {
            'gradient': {
                'start_color': '#2b2d42',
                'end_color': '#8d99ae',
                'direction': 'horizontal'
            },
            'effects': {
                'glow': {
                    'spread': 20,
                    'intensity': 0.6
                }
            }
        }

# Example usage:
"""
from PIL import Image
from transformers import BannerTransformer, StylePresets

# Create base image
image = Image.new('RGBA', (800, 400), (255, 255, 255, 0))

# Initialize transformer
transformer = BannerTransformer(image)

# Apply style preset
style = StylePresets.modern()

# Apply transformations
if 'gradient' in style:
    transformer.apply_gradient(**style['gradient'])
if 'texture' in style:
    transformer.apply_texture(**style['texture'])
if 'overlay' in style:
    transformer.apply_overlay(**style['overlay'])
if 'effects' in style:
    transformer.apply_effects(style['effects'])

# Get final image
final_image = transformer.get_image()
final_image.save('banner.png')
"""