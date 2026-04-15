"""
America Progress 3D Visualization - Main Render Script
This script creates a cinematic 3D video showing America's journey from colonial times to modern day.
"""

import os
import sys

def create_america_scene():
    """Create America progress scene for Blender"""
    
    blender_script = '''
import bpy
import math

# ============== SETUP ==============
print("Setting up scene...")

# Clear existing scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# ============== TIMELINE DATA ==============
timeline_events = [
    {"year": "1607", "event": "Colonial Beginning", "desc": "Jamestown - First Settlement", "start": 1, "end": 30},
    {"year": "1776", "event": "Independence", "desc": "Declaration of Independence", "start": 31, "end": 60},
    {"year": "1803", "event": "Louisiana Purchase", "desc": "Nation doubles in size", "start": 61, "end": 90},
    {"year": "1865", "event": "Civil War Ends", "desc": "Reconstruction begins", "start": 91, "end": 120},
    {"year": "1900", "event": "Industrial Power", "desc": "Factories & Railroads", "start": 121, "end": 150},
    {"year": "1920", "event": "Roaring Twenties", "desc": "Jazz Age & Prosperity", "start": 151, "end": 180},
    {"year": "1950", "event": "Post-War Era", "desc": "Economic Boom", "start": 181, "end": 210},
    {"year": "2000", "event": "Digital Age", "desc": "Technology Revolution", "start": 211, "end": 240},
    {"year": "2024", "event": "Modern America", "desc": "Innovation Leader", "start": 241, "end": 270},
]

# ============== DEVELOPMENT FACTORS ==============
factors = [
    {"title": "Industrial Innovation", "items": "Steel, Oil, Electricity, Automobiles"},
    {"title": "Immigration", "items": "30M+ Immigrants (1860-1920)"},
    {"title": "Natural Resources", "items": "Oil, Coal, Agriculture"},
    {"title": "Education", "items": "MIT, Stanford, Research"},
    {"title": "Democracy", "items": "Constitution, Rule of Law"},
    {"title": "Capital", "items": "Wall Street, VC Investment"},
]

# ============== CREATE TEXT OVERLAYS ==============
def create_text(text_content, location, scale=1.0):
    bpy.ops.object.text_add()
    text_obj = bpy.context.object
    text_obj.data.body = text_content
    text_obj.location = location
    text_obj.scale = (scale, scale, scale)
    text_obj.rotation_euler = (math.radians(90), 0, 0)
    text_obj.data.align_x = 'CENTER'
    text_obj.data.align_y = 'CENTER'
    text_obj.data.size = 0.3
    text_obj.data.extrude = 0.02
    return text_obj

# Create title
title = create_text("THE RISE OF AMERICA", (0, 3, 8), 2.0)
title.data.size = 1.0
title.data.materials.append(create_material("#FFD700", "TitleMat"))

# Create timeline markers
y_pos = 6
for event in timeline_events:
    text = f"{event['year']}: {event['event']}"
    create_text(text, (-8, y_pos, 8), 0.5)
    y_pos -= 0.7

# ============== CREATE CITY COMPARISON ==============
# Old city representation (left side)
old_city = create_text("1900: Young Nation\nSmall Towns", (-6, 0, 5), 0.8)
old_city.data.materials.append(create_material("#8B4513", "OldCityMat"))

# New city representation (right side)
new_city = create_text("2024: Modern Power\nGlobal Cities", (6, 0, 5), 0.8)
new_city.data.materials.append(create_material("#00FF00", "NewCityMat"))

# ============== CREATE FACTORS DISPLAY ==============
factor_text = "\\n".join([f"• {f['title']}: {f['items']}" for f in factors])
factors_obj = create_text(factor_text, (0, -5, 8), 0.4)

# ============== CREATE SPHERE (AMERICA REPRESENTATION) ==============
bpy.ops.mesh.primitive_uv_sphere_add(radius=3, segments=64, ring_count=32, location=(0, 0, 0))
america_sphere = bpy.context.object
america_sphere.name = "AmericaSphere"

# Add material
mat = bpy.data.materials.new(name="AmericaMat")
mat.use_nodes = True
nodes = mat.node_tree.nodes
bsdf = nodes.get("Principled BSDF")
bsdf.inputs[0].default_value = (0.1, 0.3, 0.8, 1)  # Blue
america_sphere.data.materials.append(mat)

# ============== ANIMATION ==============
# Animate sphere rotation
america_sphere.rotation_euler = (0, 0, 0)
america_sphere.keyframe_insert(data_path="rotation_euler", frame=1)
america_sphere.rotation_euler = (0, 0, math.radians(360))
america_sphere.keyframe_insert(data_path="rotation_euler", frame=270)

# Camera setup
bpy.ops.object.camera_add(location=(0, -15, 8))
camera = bpy.context.object
camera.rotation_euler = (math.radians(65), 0, 0)
bpy.context.scene.camera = camera

# Camera animation
camera.location = (15, -15, 8)
camera.keyframe_insert(data_path="location", frame=1)
camera.location = (-5, -10, 12)
camera.keyframe_insert(data_path="location", frame=135)
camera.location = (0, -15, 8)
camera.keyframe_insert(data_path="location", frame=270)

# ============== LIGHTING ==============
bpy.ops.object.light_add(type='SUN', location=(10, 10, 20))
sun = bpy.context.object
sun.data.energy = 3
sun.rotation_euler = (math.radians(45), math.radians(30), 0)

bpy.ops.object.light_add(type='AREA', location=(0, -10, 10))
area = bpy.context.object
area.data.energy = 500

# ============== RENDER SETTINGS ==============
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 720
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 270
bpy.context.scene.render.filepath = "/tmp/frame_"

print("Scene setup complete!")
'''

def create_material(color_hex, name):
    """Create a material with given color"""
    return f'''
mat = bpy.data.materials.new(name="{name}")
mat.use_nodes = True
nodes = mat.node_tree.nodes
bsdf = nodes.get("Principled BSDF")
bsdf.inputs[0].default_value = {color_hex}
'''

def generate_3d_globe():
    """Generate 3D globe using geojsonto3D"""
    print("Generating 3D globe with countries and cities...")
    
    os.system("""
        cd /tmp
        if [ ! -d "geojsonto3D" ]; then
            git clone --depth 1 https://github.com/martinbaud/geojsonto3D.git
            cd geojsonto3D
            pip install numpy
        fi
        cd geojsonto3D
        python main.py --preset low --enable-cities --enable-border
    """)

def render_animation():
    """Render the animation using Blender"""
    print("Rendering animation with Blender...")
    
    blender_cmd = f"""
        blender -b /tmp/america_scene.blend -a -- --cycles-device CPU
    """
    os.system(blender_cmd)

def create_video():
    """Create video from rendered frames"""
    print("Creating video with FFmpeg...")
    
    ffmpeg_cmd = """
        ffmpeg -framerate 30 -i /tmp/frame_%04d.png -c:v libx264 -pix_fmt yuv420p -y /tmp/america_progress.mp4
    """
    os.system(ffmpeg_cmd)

def main():
    """Main execution flow"""
    print("=" * 50)
    print("America Progress 3D Visualization")
    print("=" * 50)
    
    # Step 1: Generate 3D globe
    print("\\n[1/4] Generating 3D Globe...")
    generate_3d_globe()
    
    # Step 2: Create Blender scene
    print("\\n[2/4] Creating Blender Scene...")
    create_america_scene()
    
    # Step 3: Render animation
    print("\\n[3/4] Rendering Animation...")
    render_animation()
    
    # Step 4: Create video
    print("\\n[4/4] Creating Video...")
    create_video()
    
    print("\\n" + "=" * 50)
    print("DONE! Video saved to: /tmp/america_progress.mp4")
    print("=" * 50)

if __name__ == "__main__":
    main()