import random
import string
from typing import Tuple, Optional
from PIL import Image, ImageDraw, ImageFilter
import io


class CaptchaGenerator:
    """
    CAPTCHA image generator with various formatting options.
    """

    # CAPTCHA parameters
    CAPTCHA_WIDTH = 200
    CAPTCHA_HEIGHT = 80
    CAPTCHA_LENGTH = 4

    # Colors
    COLORS = [
        (255, 0, 0),  # Red
        (0, 0, 255),  # Blue
        (0, 128, 0),  # Green
        (255, 165, 0),  # Orange
        (128, 0, 128),  # Purple
        (0, 128, 128),  # Turquoise
    ]

    BACKGROUND_COLORS = [
        (240, 240, 240),  # Light gray
        (255, 255, 200),  # Light yellow
        (200, 240, 255),  # Light blue
        (240, 255, 240),  # Light green
        (255, 240, 240),  # Light red
    ]

    def __init__(self):
        """Initializes CAPTCHA generator."""
        self.current_captcha_text = None
        self.current_image = None

    @staticmethod
    def _generate_random_text(length: int = CAPTCHA_LENGTH) -> str:
        """Generates random text for CAPTCHA."""
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))

    @staticmethod
    def _add_noise(image: Image.Image, noise_level: int = 30) -> Image.Image:
        """Adds noise to image."""
        pixels = image.load()
        width, height = image.size

        for _ in range(noise_level):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            color = tuple(random.randint(0, 255) for _ in range(3))
            pixels[x, y] = color

        return image

    @staticmethod
    def _add_lines(image: Image.Image, line_count: int = 3) -> Image.Image:
        """Adds random lines to image."""
        draw = ImageDraw.Draw(image)
        width, height = image.size

        for _ in range(line_count):
            x0 = random.randint(0, width)
            y0 = random.randint(0, height)
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            color = tuple(random.randint(100, 200) for _ in range(3))
            draw.line([(x0, y0), (x1, y1)], fill=color, width=2)

        return image

    @staticmethod
    def _distort_image(image: Image.Image) -> Image.Image:
        """Applies distortion to image."""
        return image.filter(ImageFilter.GaussianBlur(radius=0.5))

    def generate(self) -> Tuple[Image.Image, str]:
        """
        Generates CAPTCHA image with text.
        Returns (Image, text)
        """
        # Generate text
        self.current_captcha_text = self._generate_random_text(self.CAPTCHA_LENGTH)

        # Create image with random background
        bg_color = random.choice(self.BACKGROUND_COLORS)
        image = Image.new("RGB", (self.CAPTCHA_WIDTH, self.CAPTCHA_HEIGHT), bg_color)

        # Draw text
        draw = ImageDraw.Draw(image)

        # Write each character separately with random angle and color
        char_width = self.CAPTCHA_WIDTH // self.CAPTCHA_LENGTH
        font_size = 45

        for i, char in enumerate(self.current_captcha_text):
            x = i * char_width + random.randint(5, 15)
            y = random.randint(10, 25)
            color = random.choice(self.COLORS)

            try:
                from PIL import ImageFont

                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    try:
                        font = ImageFont.truetype(
                            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                            font_size,
                        )
                    except:
                        font = ImageFont.load_default()
            except:
                font = ImageFont.load_default()

            draw.text((x, y), char, fill=color, font=font)

        image = self._add_noise(image, noise_level=40)

        # Add lines
        image = self._add_lines(image, line_count=2)

        # Distortion
        image = self._distort_image(image)

        self.current_image = image
        return image, self.current_captcha_text

    def get_current_image(self) -> Optional[Image.Image]:
        """Returns current CAPTCHA image."""
        return self.current_image

    def get_current_text(self) -> Optional[str]:
        """Returns current CAPTCHA text."""
        return self.current_captcha_text

    def verify(self, user_input: str) -> bool:
        """
        Checks text entered by user.
        Case-insensitive verification.
        """
        if self.current_captcha_text is None:
            return False
        return user_input.upper() == self.current_captcha_text.upper()

    def save_image(self, filepath: str) -> bool:
        """Saves current CAPTCHA image to file."""
        if self.current_image is None:
            return False
        try:
            self.current_image.save(filepath)
            return True
        except Exception as e:
            print(f"Error saving CAPTCHA: {str(e)}")
            return False

    def get_image_as_bytes(self) -> Optional[bytes]:
        """Returns CAPTCHA image as bytes (for embedding in Tkinter)."""
        if self.current_image is None:
            return None

        try:
            img_bytes = io.BytesIO()
            self.current_image.save(img_bytes, format="PNG")
            img_bytes.seek(0)
            return img_bytes.getvalue()
        except Exception as e:
            print(f"Error converting CAPTCHA: {str(e)}")
            return None


captcha_generator = CaptchaGenerator()
