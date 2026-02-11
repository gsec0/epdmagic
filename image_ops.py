from io import BytesIO
from PIL import Image, ImageOps

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


def process_image(data: bytes, target_w: int, target_h: int) -> bytes:
    # Load image from bytes
    with Image.open(BytesIO(data)) as im:
        # Convert to RGB
        im = im.convert("RGB")

        # Determine orientations
        target_is_landscape = target_w >= target_h
        image_is_landscape = im.width >= im.height

        # Rotate if orientations don't match (anti-clockwise 90 degrees)
        if target_is_landscape != image_is_landscape: # v0.2.0 rotate the input image to match the target orientation
            im = im.rotate(90, expand=True)

        # Scale while keeping aspect ratio
        im.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)

        # Create a new white background image and paste the resized image centered
        background = Image.new("RGB", (target_w, target_h), (255, 255, 255))
        left = (target_w - im.width) // 2
        top = (target_h - im.height) // 2
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
