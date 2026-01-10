import os
import io
import numpy as np
import trimesh
from PIL import Image
from skimage import measure
from shapely.geometry import Polygon
from django.core.files.base import ContentFile
import logging

logger = logging.getLogger(__name__)

def remove_background_simple(image, threshold=240):
    """
    Simple heuristic: Convert whiteish pixels to transparent.
    """
    img = image.convert("RGBA")
    data = np.array(img)
    
    # Check for white background (R>threshold and G>threshold and B>threshold)
    red, green, blue, alpha = data.T
    white_areas = (red > threshold) & (green > threshold) & (blue > threshold)
    
    # Set alpha to 0 for white areas
    data[..., 3][white_areas.T] = 0
    
    return Image.fromarray(data)

def generate_3d_glass_model(image_file, extrusion_depth=0.02):
    """
    Converts a 2D image of glasses into a 3D GLB model.
    1. Removes background (AI or Simple).
    2. Generates a mesh by extruding the silhouette.
    3. Applies the original image as a texture to the front face.
    """
    try:
        # Load Image
        input_image = Image.open(image_file).convert("RGBA")
        
        # Check if image already has transparency (simple heuristic)
        # If > 5% of pixels are transparent/translucent, assume BG is already gone.
        np_img = np.array(input_image)
        alpha_channel = np_img[..., 3]
        
        has_transparency = np.mean(alpha_channel < 250) > 0.05
        
        if has_transparency:
            logger.info("Image appears to have transparency already. Skipping background removal.")
            removed_bg_image = input_image
        else:
            # 1. Remove Background
            try:
                from rembg import remove
                
                # Pass the image bytes to rembg
                img_byte_arr = io.BytesIO()
                input_image.save(img_byte_arr, format='PNG')
                img_bytes = img_byte_arr.getvalue()
                
                output_data = remove(img_bytes)
                removed_bg_image = Image.open(io.BytesIO(output_data)).convert("RGBA")
                logger.info("Used rembg for background removal")
                
            except BaseException as e:
                logger.warning(f"rembg failed or not installed ({e}), using simple fallback")
                removed_bg_image = remove_background_simple(input_image)
        
        # Get Alpha channel for contour detection
        alpha = np.array(removed_bg_image)[..., 3]
        
        # 2. Find Contours
        # Level 127 (0.5)
        contours = measure.find_contours(alpha, 127)
        
        if not contours:
            logger.error("No contours found in image")
            return None

        # Find largest contour (the frame)
        largest_contour = max(contours, key=lambda x: len(x))
        
        # Simplify contour
        w, h = removed_bg_image.size
        
        # Convert to shapely polygon format
        # Invert Y to make it upright in 3D
        poly_points = [(c[1], h - c[0]) for c in largest_contour]
        
        # Simplify using shapely
        poly = Polygon(poly_points).simplify(1.0, preserve_topology=True)
        
        if not poly.is_valid or poly.is_empty:
            logger.error("Invalid polygon generated")
            return None

        # 3. Extrude
        # Center the polygon
        bounds = poly.bounds # (minx, miny, maxx, maxy)
        cx = (bounds[0] + bounds[2]) / 2
        cy = (bounds[1] + bounds[3]) / 2
        
        # Normalize scale (make it approx 14cm wide = 0.14m)
        current_width = bounds[2] - bounds[0]
        if current_width == 0: return None
        
        target_width = 0.15 # 15cm standard glasses width
        scale_factor = target_width / current_width
        
        # Translate to origin
        from shapely import affinity
        poly = affinity.translate(poly, -cx, -cy)
        # Scale
        poly = affinity.scale(poly, xfact=scale_factor, yfact=scale_factor)
        
        # Create Mesh using Trimesh
        # height is thickness. 5mm = 0.005m
        mesh = trimesh.creation.extrude_polygon(poly, height=0.005)
        
        # ADDED: Apply Curvature (Bend)
        # Real glasses are curved. We apply a parabolic bend: Z -= X^2 * factor.
        # This wraps the glasses around the face.
        vertices = mesh.vertices
        # X coordinates are vertices[:, 0]
        # We assume X is centered around 0 (which it is from previous steps)
        # Bending factor: determined empirically. 
        # For width ~0.15m, X ranges [-0.075, 0.075]. X^2 ~ 0.005.
        # We want edge Z to bend back by ~2cm (0.02m).
        # 0.02 = 0.005 * k  =>  k = 4.0.
        bend_factor = 4.0
        
        # Apply shift to Z based on X
        # Note: Extrusion axis is Z. We bend along Z based on X.
        vertices[:, 2] -= np.square(vertices[:, 0]) * bend_factor
        
        # Update mesh vertices
        mesh.vertices = vertices
        
        # 4. UV Mapping
        min_x, min_y, _ = mesh.bounds[0]
        max_x, max_y, _ = mesh.bounds[1]
        width_m = max_x - min_x
        height_m = max_y - min_y
        
        uvs = np.zeros((len(mesh.vertices), 2))
        
        for i, v in enumerate(mesh.vertices):
            # v is (x, y, z)
            # Map X from [min_x, max_x] to [0, 1]
            u = (v[0] - min_x) / width_m
            # Map Y from [min_y, max_y] to [0, 1]
            v_coord = (v[1] - min_y) / height_m
            uvs[i] = [u, v_coord]
            
        # Create Material
        material = trimesh.visual.texture.SimpleMaterial(image=removed_bg_image)
        mesh.visual = trimesh.visual.TextureVisuals(uv=uvs, image=removed_bg_image, material=material)
        
        # 5. Export
        glb_data = mesh.export(file_type='glb')
        
        return ContentFile(glb_data, name="model.glb")

    except Exception as e:
        logger.error(f"Failed to generate 3D model: {str(e)}")
        # Start Debugging: Return nothing
        return None
