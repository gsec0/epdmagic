from io import BytesIO
from PIL import Image, ImageOps

# Target display resolution
TARGET_W = 800
TARGET_H = 480

# Fixed 6-colour ePaper palette
PALETTE = [
    (0, 0, 0),        # Black
    (255, 255, 255),  # White
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    (255, 0, 0),      # Red
    (255, 255, 0),    # Yellow
]

# Convert PALETTE to a flat list for Pillow (R,G,B,R,G,B,...)
PALETTE_FLAT = sum(PALETTE, ())


def process_image(data: bytes) -> bytes:
    # Load image from bytes
    with Image.open(BytesIO(data)) as im:
        # Convert to RGB
        im = im.convert("RGB")

        # Scale while keeping aspect ratio
        im.thumbnail((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)

        # Create a new white background image and paste the resized image centered
        background = Image.new("RGB", (TARGET_W, TARGET_H), (255, 255, 255))
        left = (TARGET_W - im.width) // 2
        top = (TARGET_H - im.height) // 2
        background.paste(im, (left, top))
        im = background

        # Create a Pillow palette image
        palette_image = Image.new("P", (1, 1))
        palette_image.putpalette(PALETTE_FLAT + (0, 0, 0) * (256 - len(PALETTE)))

        # Quantize to 6 colours using the palette with dithering
        im = im.quantize(palette=palette_image, dither=Image.FLOYDSTEINBERG)

        # Save to BMP in bytes
        output = BytesIO()
        im.save(output, format="BMP")
        return output.getvalue()
