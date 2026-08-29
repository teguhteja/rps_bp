import cv2
import numpy as np
import os
from glob import glob

def get_thickness(alpha_channel):
    dist = cv2.distanceTransform((alpha_channel > 128).astype(np.uint8), cv2.DIST_L2, 3)
    mask = alpha_channel > 128
    if not np.any(mask):
        return 0
    return np.mean(dist[mask])

def process_signatures(sign_dir="sign", target_name="venny.png"):
    target_path = os.path.join(sign_dir, target_name)
    if not os.path.exists(target_path):
        print(f"Error: Target {target_path} not found.")
        return

    target_img = cv2.imread(target_path, cv2.IMREAD_UNCHANGED)
    if target_img is None or target_img.shape[2] != 4:
        print("Target image must be RGBA.")
        return

    target_h, target_w = target_img.shape[:2]
    target_alpha = target_img[:, :, 3]
    target_thickness = get_thickness(target_alpha)
    
    # Get median BGR color of target signature
    mask = target_alpha > 128
    target_bgr = np.median(target_img[mask], axis=0)[:3]
    
    print(f"Target '{target_name}': size={target_w}x{target_h}, thickness={target_thickness:.2f}, color={target_bgr}")

    for img_path in glob(os.path.join(sign_dir, "*.png")):
        if os.path.basename(img_path) == target_name:
            continue
            
        print(f"Processing '{os.path.basename(img_path)}'...")
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        if img is None or img.shape[2] != 4:
            print(f"Skipping {img_path}, not an RGBA image.")
            continue

        # Resize to match target
        resized = cv2.resize(img, (target_w, target_h), interpolation=cv2.INTER_AREA)
        
        current_thickness = get_thickness(resized[:, :, 3])
        print(f"  Original thickness (after resize): {current_thickness:.2f}")

        # Find best morphological operation
        best_img = resized
        best_diff = abs(current_thickness - target_thickness)
        
        # Try dilating (making thicker)
        for k_size in [2, 3, 4]:
            kernel = np.ones((k_size, k_size), np.uint8)
            dilated_alpha = cv2.dilate(resized[:, :, 3], kernel, iterations=1)
            t = get_thickness(dilated_alpha)
            diff = abs(t - target_thickness)
            if diff < best_diff:
                best_diff = diff
                best_img = resized.copy()
                best_img[:, :, 3] = dilated_alpha

        # Try eroding (making thinner)
        for k_size in [2, 3]:
            kernel = np.ones((k_size, k_size), np.uint8)
            eroded_alpha = cv2.erode(resized[:, :, 3], kernel, iterations=1)
            t = get_thickness(eroded_alpha)
            diff = abs(t - target_thickness)
            if diff < best_diff:
                best_diff = diff
                best_img = resized.copy()
                best_img[:, :, 3] = eroded_alpha

        # Apply target color to the signature strokes to match "black sign" color
        final_alpha = best_img[:, :, 3]
        best_img[final_alpha > 0, 0] = target_bgr[0]  # B
        best_img[final_alpha > 0, 1] = target_bgr[1]  # G
        best_img[final_alpha > 0, 2] = target_bgr[2]  # R

        # Overwrite the image
        cv2.imwrite(img_path, best_img)
        print(f"  Saved '{os.path.basename(img_path)}' with matched size, thickness, and color.")

if __name__ == "__main__":
    process_signatures()
