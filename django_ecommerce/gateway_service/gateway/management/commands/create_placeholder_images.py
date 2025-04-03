from django.core.management.base import BaseCommand
import os
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

class Command(BaseCommand):
    help = 'Generate placeholder images for products'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Generating placeholder images...'))
        
        # Define the base path for static images
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        static_img_dir = base_dir / 'static' / 'img'
        
        # Create directory if it doesn't exist
        os.makedirs(static_img_dir, exist_ok=True)
        
        # Generate placeholder images for different product types
        self.generate_image(static_img_dir / 'book.jpg', "Book", (400, 600), (130, 70, 180))
        self.generate_image(static_img_dir / 'laptop.jpg', "Laptop", (600, 400), (70, 130, 180))
        self.generate_image(static_img_dir / 'mobile.jpg', "Mobile", (400, 800), (70, 180, 130))
        self.generate_image(static_img_dir / 'clothes.jpg', "Clothes", (600, 600), (180, 130, 70))
        self.generate_image(static_img_dir / 'placeholder.jpg', "Product", (500, 500), (120, 120, 120))
        
        self.stdout.write(self.style.SUCCESS('All placeholder images generated successfully!'))
    
    def generate_image(self, path, text, size, color):
        """Generate a simple placeholder image with text"""
        # Create a new image with the specified size and color
        img = Image.new('RGB', size, color=color)
        draw = ImageDraw.Draw(img)
        
        # Try to create a font, falling back to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except IOError:
            font = ImageFont.load_default()
        
        # Add text to the center of the image
        text_width, text_height = draw.textsize(text, font=font) if hasattr(draw, 'textsize') else (200, 40)
        position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
        
        # Draw the text in white
        draw.text(position, text, fill=(255, 255, 255), font=font)
        
        # Save the image
        img.save(path)
        
        self.stdout.write(f"Generated {path.name}") 