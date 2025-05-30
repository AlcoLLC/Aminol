import os
from PIL import Image
from io import BytesIO
import shutil # shutil.copy2 yerine kendimiz dosya kopyalama yapacağız.

# Target size range in kilobytes
TARGET_MIN_KB = 800
TARGET_MAX_KB = 1200

# JPEG/WebP quality settings
JPEG_QUALITY_MIN = 30
JPEG_QUALITY_MAX = 95

# PNG compression levels (strongest first)
PNG_COMPRESSION_LEVELS = list(range(9, -1, -1))

# Supported image formats
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp')

# Source directory for original images
SOURCE_DIR = "/Aminol/media"

# Target directory for compressed images
COMPRESSED_OUTPUT_DIR = "/Aminol/mediafiles"


def get_file_size_kb(buffer):
    """Return file size in KB from BytesIO buffer"""
    return len(buffer.getvalue()) / 1024

def compress_jpeg(img):
    """Iteratively compress JPEG to target size"""
    # Try to save with original quality first if it's within max, otherwise start from max
    # This can be refined, but for now, we stick to the iterative approach
    best_buffer = None
    best_quality_size_kb = float('inf') # Start with a very large size

    for quality in range(JPEG_QUALITY_MAX, JPEG_QUALITY_MIN - 1, -5):
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=quality, optimize=True)
        size_kb = get_file_size_kb(buffer)
        if TARGET_MIN_KB <= size_kb <= TARGET_MAX_KB:
            return buffer # Found a good size

        # Keep track of the buffer that is smallest but still over TARGET_MIN_KB
        # or the largest if all are under TARGET_MIN_KB
        if best_buffer is None: # First iteration
             best_buffer = buffer
             best_quality_size_kb = size_kb
        elif size_kb < TARGET_MIN_KB: # If current is too small
            if best_quality_size_kb < TARGET_MIN_KB and size_kb > best_quality_size_kb : # if best was also too small, pick the larger of two smalls
                 best_buffer = buffer
                 best_quality_size_kb = size_kb
            elif best_quality_size_kb >= TARGET_MIN_KB: # if best was in acceptable range or larger, and current is too small, stick with best (or update if new best_buffer logic needed)
                pass # Current is too small, and previous best was better or also too small but larger
        elif size_kb > TARGET_MAX_KB: # If current is too large
            if size_kb < best_quality_size_kb: # if current is smaller than previous best (and both are too large)
                 best_buffer = buffer
                 best_quality_size_kb = size_kb
        # This logic might need further refinement if the "closest" is desired.
        # For now, if not in range, it returns the buffer from the lowest quality tried.
    return best_buffer if best_buffer else buffer # Return best attempt or last attempt

def compress_png(img):
    """Iteratively compress PNG to target size"""
    best_buffer = None
    # Similar logic to JPEG can be applied if "closest" is needed rather than just first fit or last resort.
    for level in PNG_COMPRESSION_LEVELS:
        buffer = BytesIO()
        img.save(buffer, format="PNG", optimize=True, compress_level=level)
        size_kb = get_file_size_kb(buffer)
        if TARGET_MIN_KB <= size_kb <= TARGET_MAX_KB:
            return buffer
    return buffer # Return buffer from the last (weakest) compression level tried if not in range

def compress_webp(img):
    """Iteratively compress WebP to target size"""
    # Similar logic to JPEG can be applied
    best_buffer = None
    for quality in range(JPEG_QUALITY_MAX, JPEG_QUALITY_MIN - 1, -5):
        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=quality) # optimize=True is not a param for WEBP save
        size_kb = get_file_size_kb(buffer)
        if TARGET_MIN_KB <= size_kb <= TARGET_MAX_KB:
            return buffer
    return buffer # Return buffer from the lowest quality tried

def process_single_image(original_image_path, compressed_image_save_path):
    """Compress a single image file and save it to the new destination."""
    try:
        # Check if source file exists and is readable
        if not os.path.exists(original_image_path) or not os.access(original_image_path, os.R_OK):
            print(f"⏭ Cannot read file: {original_image_path}")
            return False

        original_size_kb = os.path.getsize(original_image_path) / 1024

        # Skip files that are already in target range (optional, as we are creating a new file)
        # For now, we will try to compress regardless to ensure it's in the target location
        # if TARGET_MIN_KB <= original_size_kb <= TARGET_MAX_KB:
        #     print(f"⏭ Original already in target range: {original_image_path} ({int(original_size_kb)} KB)")
        #     # If already in range, we might just copy it to the destination
        #     os.makedirs(os.path.dirname(compressed_image_save_path), exist_ok=True)
        #     shutil.copy2(original_image_path, compressed_image_save_path)
        #     print(f"✔ Copied (already in range): {original_image_path} to {compressed_image_save_path}")
        #     return True

        # Skip very small files
        if original_size_kb < 50:  # Less than 50KB
            print(f"⏭ File too small to process: {original_image_path} ({int(original_size_kb)} KB)")
            # Optionally, copy small files as is to the destination
            # os.makedirs(os.path.dirname(compressed_image_save_path), exist_ok=True)
            # shutil.copy2(original_image_path, compressed_image_save_path)
            # print(f"📠 Copied (too small): {original_image_path} to {compressed_image_save_path}")
            return False # Or True if copied

        img = Image.open(original_image_path)
        img_format = img.format.upper() if img.format else '' # Handle cases where format might be None

        # Convert to RGB unless PNG (preserves transparency)
        # For WEBP, Pillow might handle RGBA saving better, but let's be explicit.
        if img.mode == 'P' or img.mode == 'LA': # Palette or Luma+Alpha
            # If it has transparency, convert to RGBA. Otherwise, RGB.
            if 'A' in img.mode:
                 img = img.convert("RGBA")
            else:
                 img = img.convert("RGB")
        elif img_format != "PNG" and img.mode == "RGBA": # e.g. a JPEG saved with alpha channel by mistake
             img = img.convert("RGB")
        elif img_format == "PNG" and img.mode != "RGBA" and img.mode != "LA" and img.mode != "P":
            # If it's a PNG but not in a mode that supports transparency well or is paletted,
            # ensure it can be saved properly. This might need more nuanced handling
            # depending on desired output for specific PNG types.
            # For simplicity, if it's not RGBA/LA/P, convert to RGB. If it *should* have alpha, this will lose it.
            if 'A' not in img.mode: # Check if it doesn't have an alpha channel already
                img = img.convert("RGB")


        # Select compression function based on format
        if img_format in ["JPEG", "JPG"]:
            # If original was PNG with transparency and we want JPEG, it must be RGB
            if img.mode == "RGBA":
                img = img.convert("RGB")
            buffer = compress_jpeg(img)
        elif img_format == "PNG":
            buffer = compress_png(img)
        elif img_format == "WEBP":
            buffer = compress_webp(img)
        else:
            # Attempt to save in original format if it's a known one by Pillow but not explicitly handled
            # Or convert to a common format like PNG if format is unknown/problematic
            try:
                print(f"ℹ️ Unsupported explicit format: {img_format}. Trying to save as PNG.")
                img = img.convert("RGBA") # Convert to a safe bet format
                img_format_to_save = "PNG"
                buffer = BytesIO() # Create a new buffer
                img.save(buffer, format=img_format_to_save, optimize=True) # Save as PNG by default
                # Check size, if not in range, apply PNG compression
                size_kb = get_file_size_kb(buffer)
                if not (TARGET_MIN_KB <= size_kb <= TARGET_MAX_KB):
                    buffer = compress_png(img) # Re-compress as PNG with iterations
            except Exception as conv_err:
                print(f"⏭ Error converting/saving unknown format {original_image_path} ({img_format}): {conv_err}")
                return False


        if buffer is None: # Should not happen if compress functions always return a buffer
             print(f"❌ Compression failed to return a buffer for {original_image_path}")
             return False

        # Ensure target directory for the specific file exists
        os.makedirs(os.path.dirname(compressed_image_save_path), exist_ok=True)

        # Write compressed version to the new path
        with open(compressed_image_save_path, "wb") as f_out:
            f_out.write(buffer.getvalue())

        compressed_size_kb = get_file_size_kb(buffer)
        print(f"✔ Compressed: {original_image_path}")
        print(f" ↳ Saved to: {compressed_image_save_path}")
        print(f" 📊 {int(original_size_kb)} KB → {int(compressed_size_kb)} KB")
        return True

    except FileNotFoundError:
        print(f"❌ File not found during processing: {original_image_path}")
        return False
    except UnidentifiedImageError:
        print(f"❌ Cannot identify image file (possibly corrupt or not an image): {original_image_path}")
        return False
    except Exception as e:
        print(f"❌ Error processing {original_image_path}: {e}")
        return False

def is_safe_path(path, base_dir):
    """Ensure path is within the intended base_dir to prevent directory traversal attacks."""
    try:
        abs_base = os.path.abspath(base_dir)
        abs_path = os.path.abspath(path)
        return abs_path.startswith(abs_base)
    except Exception:
        return False

def process_source_directory():
    """Recursively process all valid image files from SOURCE_DIR to COMPRESSED_OUTPUT_DIR."""

    # Safety check for source and target directories
    if not os.path.abspath(SOURCE_DIR).startswith(os.path.abspath("/Aminol")):
        print(f"❌ Security error: Source path {SOURCE_DIR} is not within /Aminol.")
        return
    if not os.path.abspath(COMPRESSED_OUTPUT_DIR).startswith(os.path.abspath("/Aminol")):
        print(f"❌ Security error: Target path {COMPRESSED_OUTPUT_DIR} is not within /Aminol.")
        return

    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Source directory does not exist: {SOURCE_DIR}")
        return
    if not os.path.isdir(SOURCE_DIR):
        print(f"❌ Source path is not a directory: {SOURCE_DIR}")
        return

    # Create the base compressed output directory if it doesn't exist
    if not os.path.exists(COMPRESSED_OUTPUT_DIR):
        try:
            os.makedirs(COMPRESSED_OUTPUT_DIR)
            print(f"📁 Created target directory: {COMPRESSED_OUTPUT_DIR}")
        except Exception as e:
            print(f"❌ Could not create target directory {COMPRESSED_OUTPUT_DIR}: {e}")
            return

    processed_count = 0
    success_count = 0

    try:
        for root, dirs, files in os.walk(SOURCE_DIR):
            # Ensure the current root being walked is safe relative to SOURCE_DIR
            if not is_safe_path(root, SOURCE_DIR):
                print(f"⏭ Skipping unsafe path during walk: {root}")
                continue

            for file in files:
                if file.lower().endswith(IMAGE_EXTENSIONS):
                    original_path = os.path.join(root, file)

                    # Ensure the original file path is safe
                    if not is_safe_path(original_path, SOURCE_DIR):
                        print(f"⏭ Skipping unsafe original file path: {original_path}")
                        continue

                    # Determine the corresponding path in the COMPRESSED_OUTPUT_DIR
                    # This preserves the subdirectory structure from SOURCE_DIR
                    relative_path = os.path.relpath(original_path, SOURCE_DIR)
                    compressed_save_path = os.path.join(COMPRESSED_OUTPUT_DIR, relative_path)

                    # Ensure the target save path is also safe relative to COMPRESSED_OUTPUT_DIR
                    if not is_safe_path(compressed_save_path, COMPRESSED_OUTPUT_DIR):
                        print(f"⏭ Skipping unsafe target save path: {compressed_save_path}")
                        continue

                    if process_single_image(original_path, compressed_save_path):
                        success_count +=1
                    processed_count += 1

    except PermissionError as e:
        print(f"❌ Permission denied during directory processing: {e}")
    except Exception as e:
        print(f"❌ Error during directory processing: {e}")

    print(f"\n🏁 Processing complete. {success_count}/{processed_count} images successfully processed and saved.")

if __name__ == "__main__":
    print(f"🚀 Starting image compression.")
    print(f"📂 Source directory: {SOURCE_DIR}")
    print(f"💾 Target directory for compressed files: {COMPRESSED_OUTPUT_DIR}")
    print(f"📏 Target size range: {TARGET_MIN_KB}-{TARGET_MAX_KB} KB")
    print("-" * 60)

    process_source_directory()