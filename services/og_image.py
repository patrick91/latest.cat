import io
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


class OGImageGenerator:
    """Service for generating Open Graph images using static background + text overlay"""

    WIDTH = 1200
    HEIGHT = 630
    SCALE = 2  # Render at 2x for better quality

    # Colors from the design system
    PINK = "#ffe6e6"
    DARK = "#121212"

    def __init__(self):
        self.fonts_dir = Path(__file__).parent.parent / "fonts"
        self.heading_font_path = self.fonts_dir / "PPWoodland-Heavy.ttf"
        self.body_font_path = self.fonts_dir / "NeueMontreal-Regular.ttf"

        # Load the static background image
        self.background_path = (
            Path(__file__).parent.parent / "static" / "og-background.png"
        )

    def _load_background(self) -> Image.Image:
        """Load and scale the background image"""
        if self.background_path.exists():
            bg = Image.open(self.background_path)
            # Scale to 2x for high-quality rendering
            return bg.resize(
                (self.WIDTH * self.SCALE, self.HEIGHT * self.SCALE), Image.LANCZOS
            )
        else:
            # Fallback: create a simple pink background
            return Image.new(
                "RGB", (self.WIDTH * self.SCALE, self.HEIGHT * self.SCALE), self.PINK
            )

    def generate_home_image(self) -> bytes:
        """Generate OG image for the home page"""
        text_color = self.DARK

        # Load background at 2x scale
        img = self._load_background()
        draw = ImageDraw.Draw(img)

        width = self.WIDTH * self.SCALE
        height = self.HEIGHT * self.SCALE

        try:
            # Load fonts at 2x size
            heading_font = ImageFont.truetype(
                str(self.heading_font_path), 120 * self.SCALE
            )
            subheading_font = ImageFont.truetype(
                str(self.body_font_path), 48 * self.SCALE
            )
        except OSError:
            # Fallback to default font if custom fonts aren't available
            heading_font = ImageFont.load_default()
            subheading_font = ImageFont.load_default()

        # Draw "latest.cat" heading
        heading_text = "latest.cat"
        heading_bbox = draw.textbbox((0, 0), heading_text, font=heading_font)
        heading_width = heading_bbox[2] - heading_bbox[0]
        heading_x = (width - heading_width) // 2

        draw.text(
            (heading_x, 180 * self.SCALE),
            heading_text,
            fill=text_color,
            font=heading_font,
        )

        # Draw subheading
        line1 = "Find the latest version of"
        line2 = "your favourite software"

        for i, line in enumerate([line1, line2]):
            bbox = draw.textbbox((0, 0), line, font=subheading_font)
            line_width = bbox[2] - bbox[0]
            x = (width - line_width) // 2
            y = (340 + (i * 60)) * self.SCALE
            draw.text((x, y), line, fill=text_color, font=subheading_font)

        # Resize to target size with high-quality downsampling
        img = img.resize((self.WIDTH, self.HEIGHT), Image.LANCZOS)

        # Convert to bytes
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()

    def generate_software_image(self, software_name: str, version: str) -> bytes:
        """Generate OG image for a software page"""
        text_color = self.DARK

        # Load background at 2x scale
        img = self._load_background()
        draw = ImageDraw.Draw(img)

        width = self.WIDTH * self.SCALE
        height = self.HEIGHT * self.SCALE

        try:
            # Load fonts at 2x size - use heading font (PP Woodland) for all text
            text_font = ImageFont.truetype(str(self.heading_font_path), 48 * self.SCALE)
            version_font = ImageFont.truetype(
                str(self.heading_font_path), 72 * self.SCALE
            )
            site_font = ImageFont.truetype(str(self.heading_font_path), 40 * self.SCALE)
        except OSError:
            # Fallback to default font if custom fonts aren't available
            text_font = ImageFont.load_default()
            version_font = ImageFont.load_default()
            site_font = ImageFont.load_default()

        # Draw "latest version of [software] is"
        line1 = f"latest version of {software_name} is"
        line1_bbox = draw.textbbox((0, 0), line1, font=text_font)
        line1_width = line1_bbox[2] - line1_bbox[0]
        line1_x = (width - line1_width) // 2

        draw.text(
            (line1_x, 220 * self.SCALE),
            line1,
            fill=text_color,
            font=text_font,
        )

        # Draw version number (larger)
        version_bbox = draw.textbbox((0, 0), version, font=version_font)
        version_width = version_bbox[2] - version_bbox[0]
        version_x = (width - version_width) // 2

        draw.text(
            (version_x, 290 * self.SCALE),
            version,
            fill=text_color,
            font=version_font,
        )

        # Draw "latest.cat" at bottom
        site_text = "latest.cat"
        site_bbox = draw.textbbox((0, 0), site_text, font=site_font)
        site_width = site_bbox[2] - site_bbox[0]
        site_x = (width - site_width) // 2

        draw.text(
            (site_x, 500 * self.SCALE),
            site_text,
            fill=text_color,
            font=site_font,
        )

        # Resize to target size with high-quality downsampling
        img = img.resize((self.WIDTH, self.HEIGHT), Image.LANCZOS)

        # Convert to bytes
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()
