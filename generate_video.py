import json
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math
import random

os.makedirs("/tmp/frames", exist_ok=True)

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def create_background(draw, width, height, frame_num, bg_type, palette):
    c1 = hex_to_rgb(palette[0]) if len(palette) > 0 else (20, 20, 40)
    c2 = hex_to_rgb(palette[1]) if len(palette) > 1 else (40, 40, 80)
    c3 = hex_to_rgb(palette[2]) if len(palette) > 2 else (60, 60, 120)

    if bg_type == 'gradient_dark':
        for y in range(0, height, 4):
            ratio = y / height
            blend = tuple(int(c1[i] + (c2[i] - c1[i]) * ratio) for i in range(3))
            draw.rectangle([0, y, width, y+4], fill=blend)
    
    elif bg_type == 'gradient_light':
        for y in range(0, height, 4):
            ratio = y / height
            blend = tuple(int(min(255, c2[i]*1.5 + (c3[i] - c2[i]) * ratio)) for i in range(3))
            draw.rectangle([0, y, width, y+4], fill=blend)
            
    elif bg_type == 'space':
        draw.rectangle([0, 0, width, height], fill=(5, 5, 15))
        # Moving stars
        for i in range(100):
            sz = (i % 3) + 1
            x = (int(math.sin(i*123.4) * 10000) + frame_num * sz) % width
            y = int(math.cos(i*321.4) * 10000) % height
            alpha = int(128 + math.sin(frame_num*0.1 + i)*127)
            draw.ellipse([x, y, x+sz, y+sz], fill=(255,255,255))
            
    elif bg_type == 'tech_grid':
        draw.rectangle([0, 0, width, height], fill=c1)
        grid_sz = 100
        offset_x = (frame_num * 2) % grid_sz
        offset_y = (frame_num * 2) % grid_sz
        for x in range(-grid_sz, width, grid_sz):
            draw.line([(x+offset_x, 0), (x+offset_x, height)], fill=c2, width=2)
        for y in range(-grid_sz, height, grid_sz):
            draw.line([(0, y+offset_y), (width, y+offset_y)], fill=c2, width=2)
            
    elif bg_type == 'particles':
        draw.rectangle([0, 0, width, height], fill=c1)
        for i in range(40):
            r = 10 + (i%5)*10
            x = (int(math.sin(i*11)*width) + frame_num*(i%3+1)) % width
            y = (int(math.cos(i*13)*height) + int(math.sin(frame_num*0.05 + i)*50)) % height
            draw.ellipse([x-r, y-r, x+r, y+r], fill=c2)
            
    elif bg_type == 'geometric':
        draw.rectangle([0, 0, width, height], fill=c1)
        for i in range(5):
            x = cx = width//2 + int(math.sin(frame_num*0.02 + i)*300)
            y = cy = height//2 + int(math.cos(frame_num*0.03 + i)*200)
            sz = 200 + i*50
            draw.polygon([
                (x, y-sz), (x+sz*0.86, y+sz*0.5), (x-sz*0.86, y+sz*0.5)
            ], outline=c2, width=10)
            
    elif bg_type == 'nature':
        draw.rectangle([0, 0, width, height], fill=c1)
        for i in range(3):
            y_offset = height - 200 - i*150
            for x in range(0, width, 10):
                y = y_offset + math.sin(x*0.005 + frame_num*0.05 + i)*100
                draw.rectangle([x, y, x+10, height], fill=c2 if i%2==0 else c3)
                
    elif bg_type == 'abstract':
        draw.rectangle([0, 0, width, height], fill=c1)
        w = int(width/2 + math.sin(frame_num*0.05)*width/4)
        draw.ellipse([width//4-w, height//4-w, width//4+w, height//4+w], fill=c2)
        w2 = int(width/2 + math.cos(frame_num*0.04)*width/4)
        draw.ellipse([width*3//4-w2, height*3//4-w2, width*3//4+w2, height*3//4+w2], fill=c3)
        
    else:
        # Default gradient
        draw.rectangle([0, 0, width, height], fill=(30, 30, 40))

def draw_text_centered(draw, text, y, max_w, font=None, fill=(255,255,255), size=60):
    # Simplified without external font
    draw.text((1920//2, y), text, fill=fill, anchor="mm", font_size=size)

def crossfade(img1, img2, alpha):
    return Image.blend(img1, img2, alpha)

def create_scene_frame(frame_num, scene_local_frame, scene, total_scene_frames, width=1920, height=1080):
    palette = scene.get('colorPalette', ['#1a1a2e', '#16213e', '#e94560'])
    bg_type = scene.get('backgroundType', 'gradient_dark')
    title = scene.get('title', '')
    desc = scene.get('description', '')
    
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Background
    create_background(draw, width, height, frame_num, bg_type, palette)
    
    # Dark overlay for text readability (bottom third)
    overlay_h = 250
    draw.rectangle([0, height-overlay_h, width, height], fill=(0,0,0))
    for y in range(height-overlay_h-100, height-overlay_h):
        alpha = int(((y - (height-overlay_h-100)) / 100) * 200)
        # We can't do alpha shapes easily in pure PIL RGB, so we fake it:
    
    # Main Title (fades out halfway)
    fade_title = 1.0
    half = total_scene_frames / 2
    if scene_local_frame > half:
        fade_title = max(0, 1.0 - (scene_local_frame - half) / (total_scene_frames * 0.1))
    
    if fade_title > 0:
        c1 = hex_to_rgb(palette[-1]) if palette else (255,255,255)
        # Blend with background slightly
        textColor = tuple(int(x * fade_title) for x in (255,255,255))
        draw_text_centered(draw, title.upper(), height//2 - 100, width-200, fill=textColor, size=90)

    # Subtitle / VoiceOver narration
    draw_text_centered(draw, desc, height - 125, width-200, fill=(220, 220, 220), size=46)
    
    return img

def main():
    script_json = os.environ.get('VIDEO_SCRIPT', '')
    try:
        script = json.loads(script_json)
    except:
        script = {
            "title": "Default Video", 
            "scenes": [
                {
                    "title": "Welcome", 
                    "description": "Connecting the world.", 
                    "backgroundType": "space", 
                    "colorPalette": ["#000000", "#111133", "#ffffff"]
                }
            ], 
            "duration": 5
        }
    
    title = script.get('title', 'Video')
    scenes = script.get('scenes', [])
    duration = script.get('duration', 30)
    total_frames = duration * 30
    
    if not scenes:
        scenes = [{"title": "Welcome", "description": "Welcome!", "backgroundType": "gradient_dark", "colorPalette": ["#111", "#333", "#555"]}]
        
    for i, s in enumerate(scenes):
        if 'backgroundType' not in s: 
            types = ['gradient_dark', 'particles', 'geometric', 'tech_grid', 'space', 'nature', 'abstract']
            s['backgroundType'] = types[i % len(types)]
        if 'colorPalette' not in s:
            s['colorPalette'] = ['#1a1a2e', '#0f3460', '#e94560']
    
    frames_per_scene = max(1, total_frames // len(scenes))
    crossfade_duration = 15 # half a second at 30 fps
    
    prev_bg_img = None
    
    for frame in range(total_frames):
        scene_index = min(frame // frames_per_scene, len(scenes) - 1)
        scene = scenes[scene_index]
        scene_local_frame = frame % frames_per_scene
        
        img = create_scene_frame(frame, scene_local_frame, scene, frames_per_scene)
        
        # Crossfade transition logic
        if scene_local_frame < crossfade_duration and scene_index > 0 and prev_bg_img is not None:
             alpha = scene_local_frame / crossfade_duration
             # Blend with the ending frame of previous scene
             img = crossfade(prev_bg_img, img, alpha)
             
        elif scene_local_frame >= frames_per_scene - crossfade_duration:
             # Store this as the tail frame for the next crossfade
             prev_bg_img = img.copy()

        img.save(f"/tmp/frames/frame_{frame:05d}.png")
        
        if (frame + 1) % 150 == 0:
            print(f"Progress: {frame + 1}/{total_frames} frames")
            
    print(f"Generated {total_frames} frames")

if __name__ == "__main__":
    main()
