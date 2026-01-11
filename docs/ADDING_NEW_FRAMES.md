# How to Add New Frames for Virtual Try-On

The Virtual Try-On system is dynamic. This means you do not need to change any code to add new glasses. You simply need to upload the correct 3D files in the Admin Panel.

## Prerequisite: The 3D Model
The system **CANNOT** automatically turn a 2D photo of glasses into a 3D model. You must have a **3D file** for the frame.
- **Accepted Formats:** `.glb` (Recommended) or `.gltf`.
- **File Size:** Keep under 2MB for fast loading on mobile data.
- **Reference Setup:** 
  - The model should be centered at `(0,0,0)`.
  - The bridge of the nose (where it sits) should be roughly at the origin.
  - The scale should be in appropriate units (usually meters or centimeters).

---

## Step-by-Step Guide

### 1. Open the Admin Panel
1. Go to `http://your-domain.com/admin` (e.g., `http://localhost:8000/admin`).
2. Log in with your Superuser credentials.

### 2. Locate "Virtual_Tryon"
Scroll to the **Virtual_Tryon** section and click on **Spectacle Frames**.

### 3. Add a New Frame
1. Click the **"Add Spectacle frame"** button (top right).
2. **Variant:** Select the existing product variant (e.g., "Ray-Ban Aviator - Gold") you want to attach this 3D model to.
   - *Note: If the product handles multiple colors but has the same shape, you still need to create a SpectacleFrame entry for each variant color if you want them all to work.*
3. **Model file:** Click "Choose File" and upload your `.glb` file.

### 4. Initial Fit Settings (Defaults)
Leave the settings as default for the first try:
- **Scaling factor:** `1.0`
- **Offset x:** `0.0`
- **Offset y:** `0.0`
- **Offset z:** `0.0` (Use this to move glasses forward/backward)

Click **SAVE**.

---

## How to Check & "Fit" the Frame

Once saved, the frame will **immediately** appear in the Virtual Try-On list on the website. Now you need to check if it fits correctly on a face.

1. Open the Virtual Try-On page.
2. Allow the camera and wait for your face to be detected.
3. Scroll to the new frame you just added.
4. observe the fit:
   - **Too Big/Small?** → Adjust **Scaling factor**.
     - *Example:* If huge, try `0.1` or `0.01`. If tiny, try `10.0`.
   - **Too High/Low?** → Adjust **Offset y**.
     - Positive values move it UP.
     - Negative values move it DOWN.
   - **Too Left/Right?** → Adjust **Offset x** (Rarely needed if model is centered).
   - **Floating too far away?** → Adjust **Offset z**.
     - Negative values usually move it closer to the face/ears.

### Tuning Process
1. Keep the Try-On page open in one tab.
2. Keep the Admin Page (Edit Spectacle Frame) open in another tab.
3. Make a change in Admin (e.g., change Scale to `1.1`).
4. Click **Save**.
5. Refresh the Try-On page and select the frame again to see the difference.
6. Repeat until perfect.

---

## Troubleshooting

### "The card shows 'Error' or keeps loading"
- The `.glb` file might be corrupted.
- The file URL might be inaccessible (404).
- Creating a `SpectacleFrame` without uploading a file.

### "The glasses are facing the wrong way"
- We currently support standard orientation. If your model is rotated 90 degrees, you will need to open it in a 3D editor (like Blender), rotate it, and export it again.
- *Future Update:* We can add "Rotation X/Y/Z" fields to the Admin to handle this without 3D editing.
