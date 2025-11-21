import os
import struct
from typing import Tuple, Optional


class BMPFile:
    """
    Class for working with BMP files.
    Supports reading and writing BMP files with basic validation.
    """

    BMP_SIGNATURE = b"BM"  # BMP file signature

    def __init__(self, filepath: str):
        """Initializes BMP file object."""
        self.filepath = filepath
        self.is_valid = False
        self.width = 0
        self.height = 0
        self.bit_depth = 0
        self.file_size = 0
        self.data_size = 0

        if os.path.exists(filepath):
            self._validate()

    @staticmethod
    def is_bmp_file(filepath: str) -> bool:
        """Checks if file is a valid BMP file."""
        if not os.path.exists(filepath):
            return False

        if not filepath.lower().endswith(".bmp"):
            return False

        try:
            with open(filepath, "rb") as f:
                signature = f.read(2)
                return signature == BMPFile.BMP_SIGNATURE
        except (IOError, OSError):
            return False

    def _validate(self) -> bool:
        """Validates BMP file and extracts basic information."""
        try:
            with open(self.filepath, "rb") as f:
                signature = f.read(2)
                if signature != self.BMP_SIGNATURE:
                    return False

                self.file_size = struct.unpack("<I", f.read(4))[0]

                f.read(4)

                pixel_data_offset = struct.unpack("<I", f.read(4))[0]

                dib_header_size = struct.unpack("<I", f.read(4))[0]

                self.width = struct.unpack("<I", f.read(4))[0]

                self.height = struct.unpack("<I", f.read(4))[0]

                f.read(2)

                self.bit_depth = struct.unpack("<H", f.read(2))[0]

                compression = struct.unpack("<I", f.read(4))[0]

                self.data_size = self.file_size - pixel_data_offset

                self.is_valid = True
                return True

        except (IOError, OSError, struct.error):
            self.is_valid = False
            return False

    def get_info(self) -> dict:
        """Returns information about BMP file."""
        if not self.is_valid:
            return {"error": "Invalid BMP file"}

        return {
            "filepath": self.filepath,
            "filename": os.path.basename(self.filepath),
            "width": self.width,
            "height": self.height,
            "bit_depth": self.bit_depth,
            "file_size": self.file_size,
            "data_size": self.data_size,
            "resolution": f"{self.width}x{self.height}",
            "color_format": self._get_color_format(),
        }

    def _get_color_format(self) -> str:
        """Returns color format based on bit depth."""
        if self.bit_depth == 1:
            return "Monochrome (1-bit)"
        elif self.bit_depth == 4:
            return "Palette (4-bit)"
        elif self.bit_depth == 8:
            return "Palette (8-bit)"
        elif self.bit_depth == 24:
            return "RGB (24-bit)"
        elif self.bit_depth == 32:
            return "RGBA (32-bit)"
        else:
            return f"Unknown format ({self.bit_depth}-bit)"

    def get_file_size_kb(self) -> float:
        """Returns file size in kilobytes."""
        return self.file_size / 1024

    def get_pixel_count(self) -> int:
        """Returns total number of pixels."""
        return self.width * self.height


class BMPValidator:
    """Validator for checking BMP files."""

    @staticmethod
    def validate_file(filepath: str) -> Tuple[bool, str]:
        """
        Validates file and returns (is_valid, message).
        """
        if not os.path.exists(filepath):
            return False, f"File '{filepath}' does not exist"

        if not filepath.lower().endswith(".bmp"):
            return False, "File must have .bmp extension"

        if not BMPFile.is_bmp_file(filepath):
            return False, "File is not a valid BMP file"

        try:
            bmp = BMPFile(filepath)
            if not bmp.is_valid:
                return False, "BMP file is corrupted or has unknown format"

            if bmp.width <= 0 or bmp.height <= 0:
                return False, "Invalid image dimensions"

            return True, "File validated successfully"
        except Exception as e:
            return False, f"Error during validation: {str(e)}"

    @staticmethod
    def get_supported_formats() -> list:
        """Returns list of supported formats."""
        return ["bmp", "BMP"]

    @staticmethod
    def filter_bmp_files(filepath_list: list) -> list:
        """Filters file list and keeps only BMP files."""
        return [f for f in filepath_list if f.lower().endswith(".bmp")]
