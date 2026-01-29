from PIL import Image
import os

def process_images():
    # Input path
    input_path = r"C:/Users/小野明子/.gemini/antigravity/brain/2566ef86-2acf-44b9-981b-d7bb2a006eaa/uploaded_media_1769576486727.jpg"
    output_dir = r"c:/Users/小野明子/Desktop/moma-friend-lp"
    
    # Load image
    try:
        img = Image.open(input_path)
        img = img.convert("RGBA")
    except Exception as e:
        print(f"Failed to load image: {e}")
        return

    width, height = img.size
    print(f"Image loaded: {width}x{height}")

    # Split into 4 quadrants
    # Grid:
    # 0 (Idle) | 1 (Walk)
    # ---------+---------
    # 2 (Eat)  | 3 (Sleep)
    
    mid_x = width // 2
    mid_y = height // 2

    # Define crop boxes (left, upper, right, lower)
    crops = {
        "moma-idle.png": (0, 0, mid_x, mid_y),
        "moma-walk.png": (mid_x, 0, width, mid_y),
        "moma-eat.png": (0, mid_y, mid_x, height),
        "moma-sleep.png": (mid_x, mid_y, width, height)
    }

    white_threshold = 240  # Threshold for "white" or light background

    for filename, box in crops.items():
        # Crop
        cropped = img.crop(box)
        
        # Remove background
        # Since it might be a checkerboard or white, we'll try a generous floodfill or color replacement.
        # Simple method: Replace all pixels close to white/grey with transparent.
        # Better method for "sticker" style: Flood fill from corners? 
        # But corners might be occupied by the character in some views?
        # Let's check corners of the CROP.
        # Usually these 4-up images have whitespace between them.
        
        datas = cropped.getdata()
        newData = []
        
        for item in datas:
            # Check if pixel is light (accounting for potential checkerboard grey/white)
            # Checkerboard usually alternates white (255) and light grey (~204 or ~230)
            # Let's assume anything brighter than 200 in all channels is background for now?
            # Or just use the top-left pixel as reference?
            
            # Simple "Is it white-ish?"
            if item[0] > 230 and item[1] > 230 and item[2] > 230:
                 newData.append((255, 255, 255, 0))
            else:
                 newData.append(item)
        
        cropped.putdata(newData)
        
        # Trim transparent borders (optional but good)
        bbox = cropped.getbbox()
        if bbox:
            cropped = cropped.crop(bbox)

        # Save
        save_path = os.path.join(output_dir, filename)
        cropped.save(save_path, "PNG")
        print(f"Saved {filename}")

if __name__ == "__main__":
    process_images()
