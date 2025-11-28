from PIL import Image, ImageDraw, ImageFont
import os

class IconGenerator:
    def __init__(self):
        self.size = (64, 64)
        self.background_color = (255, 255, 255)  # White
        self.accent_color = (0, 122, 204)  # Blue
        self.text_color = (44, 62, 80)  # Dark blue-gray
        self.icons_path = "assets/icons/"
        
    def create_icon(self, text, filename, icon_color=None):
        if icon_color is None:
            icon_color = self.accent_color
            
        # Create image with white background
        img = Image.new('RGB', self.size, self.background_color)
        draw = ImageDraw.Draw(img)
        
        # Draw circle background
        circle_margin = 8
        circle_size = (circle_margin, circle_margin, self.size[0]-circle_margin, self.size[1]-circle_margin)
        draw.ellipse(circle_size, fill=icon_color)
        
        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text[:2], font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center the text
        x = (self.size[0] - text_width) // 2
        y = (self.size[1] - text_height) // 2
        
        draw.text((x, y), text[:2], fill=self.background_color, font=font)
        
        # Save icon
        img.save(os.path.join(self.icons_path, filename))
        print(f"Created icon: {filename}")
    
    def generate_all_icons(self):
        # Ensure icons directory exists
        os.makedirs(self.icons_path, exist_ok=True)
        
        # Define icons to create
        icons = [
            ("Dashboard", "dashboard.png", (0, 122, 204)),  # Blue
            ("Sales", "sales.png", (40, 167, 69)),         # Green
            ("Purchase", "purchase.png", (220, 53, 69)),   # Red
            ("Receipts", "receipts.png", (255, 193, 7)),   # Yellow
            ("Ledger", "ledger.png", (111, 66, 193)),      # Purple
            ("Reports", "reports.png", (23, 162, 184)),    # Teal
            ("Users", "users.png", (253, 126, 20)),        # Orange
            ("Settings", "settings.png", (108, 117, 125)), # Gray
            ("Logo", "logo.png", (0, 122, 204)),           # Blue
        ]
        
        for text, filename, color in icons:
            self.create_icon(text, filename, color)

# Run this to generate icons
if __name__ == "__main__":
    generator = IconGenerator()
    generator.generate_all_icons()