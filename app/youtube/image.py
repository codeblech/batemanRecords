from PIL import Image
from app.config import console


def crop_square_from_horizontal_middle(image: Image.Image) -> Image.Image:
    """
    Crop image to a centered square based on the shorter side.
    For landscape images (width >= height), this crops horizontally from the center.
    """
    width, height = image.size
    console.print(
        f"Thumbnail crop input size: [bold]{width}x{height}[/bold]"
    )
    if width == height:
        console.print("Thumbnail is already square. Skipping crop")
        return image.copy()

    if width > height:
        left = (width - height) // 2
        top = 0
        right = left + height
        bottom = height
    else:
        left = 0
        top = (height - width) // 2
        right = width
        bottom = top + width

    console.print(
        f"Cropping thumbnail with box: left={left}, top={top}, right={right}, bottom={bottom}"
    )
    return image.crop((left, top, right, bottom))
