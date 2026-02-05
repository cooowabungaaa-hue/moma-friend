from PIL import Image
import os
import sys
import argparse

try:
    from rembg import remove
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False

def process_images(input_path, rows=2, cols=2, names=None, tolerance=30, output_dir=None):
    if not output_dir:
        output_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load image
    try:
        img = Image.open(input_path)
        img = img.convert("RGBA")
    except Exception as e:
        print(f"Failed to load image at {input_path}: {e}")
        return

    width, height = img.size
    print(f"Image loaded: {width}x{height}")

    cell_w = width // cols
    cell_h = height // rows

    # Default names if not provided
    if not names:
        names = [f"pose_{i}_{j}.png" for i in range(rows) for j in range(cols)]
    
    # Grid processing
    for i in range(rows):
        for j in range(cols):
            idx = i * cols + j
            if idx >= len(names):
                break
                
            filename = names[idx]
            if not filename.endswith(".png"):
                filename += ".png"
                
            # Define crop box (left, upper, right, lower)
            box = (j * cell_w, i * cell_h, (j + 1) * cell_w, (i + 1) * cell_h)
            
            # Crop
            cropped = img.crop(box)
            
            # Remove background
            if REMBG_AVAILABLE:
                cropped = remove(cropped)
            else:
                datas = cropped.getdata()
                newData = []
                for item in datas:
                    # Check for white (R,G,B all high)
                    if item[0] > 255 - tolerance and item[1] > 255 - tolerance and item[2] > 255 - tolerance:
                        newData.append((255, 255, 255, 0))
                    else:
                        newData.append(item)
                cropped.putdata(newData)
            
            # Trim transparent borders
            bbox = cropped.getbbox()
            if bbox:
                cropped = cropped.crop(bbox)

            # Save
            save_path = os.path.join(output_dir, filename)
            cropped.save(save_path, "PNG")
            print(f"Saved {filename}")

def main():
    parser = argparse.ArgumentParser(description="Process a character sheet into individual poses.")
    parser.add_argument("input", help="Path to the input image sheet")
    parser.add_argument("--rows", type=int, default=2, help="Number of rows in the grid")
    parser.add_argument("--cols", type=int, default=2, help="Number of columns in the grid")
    parser.add_argument("--names", help="Comma-separated list of output filenames")
    parser.add_argument("--tolerance", type=int, default=30, help="Brightness tolerance for background removal (0-255)")
    parser.add_argument("--outdir", help="Output directory (defaults to script directory)")

    args = parser.parse_args()

    names = None
    if args.names:
        names = [s.strip() for s in args.names.split(",")]
    
    # Generic processing
    process_images(args.input, args.rows, args.cols, names, args.tolerance, args.outdir)

if __name__ == "__main__":
    main()
