from PIL import Image
import sys

def remove_white_background(input_path, output_path, tolerance=30):
    img = Image.open(input_path)
    img = img.convert("RGBA")
    datas = img.getdata()
    
    # Simple thresholding might kill the eyes or wool.
    # Let's try a flood fill approach from corners if possible, 
    # but PIL doesn't have a simple flood fill for alpha.
    # Instead, we will iterate.
    # Actually, simpler approach for "White background" renders:
    # If pixel is very close to white, make it transparent.
    
    newData = []
    for item in datas:
        # Check for white (R,G,B all high)
        if item[0] > 255 - tolerance and item[1] > 255 - tolerance and item[2] > 255 - tolerance:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    
    img.putdata(newData)
    img.save(output_path, "PNG")
    print(f"Saved transparent image to {output_path}")

if __name__ == "__main__":
    try:
        remove_white_background("moma-chan.png", "moma-chan-transparent.png")
    except Exception as e:
        print(f"Error: {e}")
