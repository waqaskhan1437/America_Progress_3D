import json
import os
from PIL import Image, ImageDraw
import math
import random

os.makedirs("/tmp/frames", exist_ok=True)

LOTTIE_COLORS = {
    'rocket': [(255, 100, 50), (255, 150, 80), (255, 200, 120)],
    'globe': [(30, 100, 200), (40, 120, 220), (60, 140, 240)],
    'people': [(100, 200, 100), (150, 220, 150), (80, 180, 80)],
    'building': [(150, 150, 170), (180, 180, 200), (130, 130, 150)],
    'tech': [(100, 200, 255), (150, 220, 255), (80, 180, 240)],
    'nature': [(50, 200, 100), (80, 220, 120), (40, 180, 80)],
    'space': [(50, 50, 100), (80, 80, 150), (100, 100, 180)],
    'education': [(200, 150, 50), (220, 180, 80), (180, 130, 40)],
    'industry': [(120, 120, 130), (150, 150, 160), (100, 100, 110)],
    'celebration': [(255, 200, 50), (255, 220, 100), (255, 180, 30)],
    'star': [(255, 230, 100), (255, 250, 150), (255, 200, 50)],
    'heart': [(255, 100, 130), (255, 130, 150), (255, 80, 110)],
    'fire': [(255, 100, 30), (255, 150, 60), (255, 200, 100)],
    'water': [(50, 150, 255), (80, 180, 255), (100, 200, 255)],
    'earth': [(139, 90, 43), (160, 110, 60), (120, 80, 40)],
    'lightning': [(255, 255, 100), (255, 255, 150), (255, 240, 80)],
    'music': [(200, 100, 255), (220, 130, 255), (180, 80, 240)],
    'default': [(100, 150, 255), (130, 180, 255), (80, 130, 240)]
}

def get_animation_for_keyword(keyword):
    keyword = keyword.lower()
    mapping = {
        'start': 'rocket', 'begin': 'rocket', 'intro': 'star', 'launch': 'rocket',
        'world': 'globe', 'global': 'globe', 'earth': 'globe', 'country': 'globe', 'nation': 'globe',
        'people': 'people', 'community': 'people', 'population': 'people', 'human': 'people',
        'building': 'building', 'construction': 'building', 'city': 'building', 'architecture': 'building',
        'tech': 'tech', 'technology': 'tech', 'computer': 'tech', 'digital': 'tech', 'ai': 'tech',
        'nature': 'nature', 'environment': 'nature', 'tree': 'nature', 'forest': 'nature',
        'space': 'space', 'galaxy': 'space', 'universe': 'space', 'nasa': 'space', 'rocket': 'space',
        'education': 'education', 'school': 'education', 'learning': 'education', 'study': 'education',
        'industry': 'industry', 'factory': 'industry', 'manufacturing': 'industry', 'business': 'industry',
        'celebrate': 'celebration', 'party': 'celebration', 'success': 'celebration', 'achievement': 'celebration',
        'star': 'star', 'best': 'star', 'top': 'star', 'favorite': 'star',
        'love': 'heart', 'heart': 'heart', 'care': 'heart', 'emotion': 'heart',
        'fire': 'fire', 'hot': 'fire', 'flame': 'fire',
        'water': 'water', 'ocean': 'water', 'sea': 'water', 'river': 'water',
        'earth': 'earth', 'land': 'earth', 'ground': 'earth', 'mountain': 'earth',
        'power': 'lightning', 'electric': 'lightning', 'energy': 'lightning', 'electricity': 'lightning',
        'music': 'music', 'song': 'music', 'audio': 'music', 'sound': 'music'
    }
    for key, value in mapping.items():
        if key in keyword:
            return value
    return 'default'

def create_animated_frame(frame_num, scene, total_frames, scene_index, total_scenes, width=1920, height=1080):
    keywords_text = scene.get('description', '') + ' ' + scene.get('title', '') + ' ' + ' '.join(scene.get('keywords', []))
    
    anim_key = 'default'
    for kw in keywords_text.split():
        found = get_animation_for_keyword(kw)
        if found != 'default':
            anim_key = found
            break
    
    colors = LOTTIE_COLORS.get(anim_key, LOTTIE_COLORS['default'])
    
    img = Image.new('RGB', (width, height), (10, 10, 25))
    draw = ImageDraw.Draw(img)
    
    # Animated gradient background
    for y in range(0, height, 2):
        ratio = y / height
        wave = math.sin(frame_num * 0.02 + y * 0.005) * 15
        r = int(10 + ratio * 25 + wave)
        g = int(10 + ratio * 15 + wave * 0.5)
        b = int(30 + ratio * 60 + wave)
        draw.line([(0, y), (width, y)], fill=(max(0, r), max(0, g), min(255, b)))
    
    # Floating particles
    for i in range(30):
        x = int((frame_num * 3 + i * 73) % width)
        y = int(height/2 + math.sin(frame_num * 0.05 + i * 0.5) * height * 0.4 + i * 20)
        size = 2 + (i % 4)
        alpha = int(80 + math.sin(frame_num * 0.1 + i) * 40)
        draw.ellipse([x-size, y-size, x+size, y+size], fill=colors[i % 3])
    
    # Central animated element
    cx, cy = width // 2, height // 2 - 30
    pulse = 1 + math.sin(frame_num * 0.15) * 0.15
    radius = int(180 * pulse)
    
    # Rotating rings
    for ring in range(4):
        ring_radius = radius + ring * 50
        ring_speed = 0.03 * (1 if ring % 2 else -1)
        for i in range(40):
            angle = (i / 40) * 2 * math.pi + frame_num * ring_speed
            x = cx + int(math.cos(angle) * ring_radius)
            y = cy + int(math.sin(angle) * ring_radius)
            size = 6 - ring
            if size > 0:
                draw.ellipse([x-size, y-size, x+size, y+size], fill=colors[ring % 3])
    
    # Glowing orb
    for i in range(5, 0, -1):
        r = radius // 2 + i * 15
        alpha = 80 - i * 15
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=colors[0])
    
    # Inner glow
    inner_pulse = 1 + math.sin(frame_num * 0.2) * 0.2
    inner_r = int(60 * inner_pulse)
    draw.ellipse([cx-inner_r, cy-inner_r, cx+inner_r, cy+inner_r], fill=(255, 255, 255))
    
    # Animated character
    bounce = int(math.sin(frame_num * 0.3) * 15)
    char_cx, char_cy = cx, cy - 250 + bounce
    
    # Head
    draw.ellipse([char_cx-35, char_cy-70, char_cx+35, char_cy], fill=(255, 220, 180))
    # Body
    draw.ellipse([char_cx-20, char_cy, char_cx+20, char_cy+50], fill=colors[0])
    # Arms (waving)
    wave_angle = math.sin(frame_num * 0.4) * 40
    draw.line([char_cx+15, char_cy+10, char_cx+50+int(wave_angle), char_cy-10], fill=(255, 220, 180), width=8)
    draw.line([char_cx-15, char_cy+10, char_cx-50-int(wave_angle), char_cy+20], fill=(255, 220, 180), width=8)
    # Legs
    draw.ellipse([char_cx-15, char_cy+50, char_cx+15, char_cy+75], fill=(50, 50, 150))
    
    # Title animation
    title_y = 80 + int(math.sin(frame_num * 0.08) * 8)
    title = f"✨ {scene.get('title', 'Scene')} ✨"
    draw.text((width // 2, title_y), title, fill=(255, 255, 255), anchor="mm", font_size=72)
    
    # Description with fade in
    desc = scene.get('description', '')
    fade_progress = min((frame_num % 30) / 25, 1)
    visible_chars = int(len(desc) * fade_progress)
    display_desc = desc[:visible_chars]
    draw.text((width // 2, height - 180), display_desc, fill=(200, 200, 220), anchor="mm", font_size=42)
    
    # Keywords as animated tags
    keywords = scene.get('keywords', [])[:6]
    for i, kw in enumerate(keywords):
        tag_x = 150 + i * 280
        tag_y = height - 100 + int(math.sin(frame_num * 0.1 + i) * 5)
        draw.rounded_rectangle([tag_x, tag_y, tag_x + 200, tag_y + 40], radius=15, fill=colors[i % 3])
        draw.text((tag_x + 100, tag_y + 20), f"#{kw}", fill=(255, 255, 255), anchor="mm", font_size=22)
    
    # Scene counter
    draw.text((width - 100, 60), f"Scene {scene_index + 1}/{total_scenes}", fill=(150, 150, 180), anchor="mm", font_size=28)
    
    # Timer
    seconds = frame_num // 30
    mins = seconds // 60
    secs = seconds % 60
    draw.text((100, 60), f"{mins:02d}:{secs:02d}", fill=(150, 150, 180), anchor="mm", font_size=28)
    
    # Progress bar
    bar_width = width - 300
    progress = frame_num / total_frames
    draw.rounded_rectangle([150, height - 50, 150 + bar_width, height - 20], radius=10, fill=(40, 40, 60))
    draw.rounded_rectangle([150, height - 50, 150 + int(bar_width * progress), height - 20], radius=10, fill=colors[0])
    
    return img

def main():
    script_json = os.environ.get('VIDEO_SCRIPT', '{"title":"Dynamic Video","scenes":[{"title":"Welcome","description":"Amazing animated video","keywords":["star","celebrate"]},{"title":"Explore","description":"Discover new horizons","keywords":["globe","world"]},{"title":"Achieve","description":"Reach for the stars","keywords":["rocket","start"]},{"title":"Celebrate","description":"Success and joy","keywords":["celebration","heart"]}],"duration":30}')
    
    try:
        script = json.loads(script_json)
    except:
        script = {"title": "Dynamic Video", "scenes": [{"title": "Welcome", "description": "Welcome!", "keywords": ["star"]}], "duration": 30}
    
    title = script.get('title', 'Video')
    scenes = script.get('scenes', [])
    duration = script.get('duration', 30)
    total_frames = duration * 30
    
    if not scenes:
        scenes = [{"title": "Welcome", "description": "Welcome!", "keywords": ["star"]}]
    
    print(f"Generating: {title}")
    print(f"Scenes: {len(scenes)}, Duration: {duration}s, Frames: {total_frames}")
    
    frames_per_scene = max(1, total_frames // len(scenes))
    
    for frame in range(total_frames):
        scene_index = min(frame // frames_per_scene, len(scenes) - 1)
        scene = scenes[scene_index]
        
        img = create_animated_frame(frame, scene, total_frames, scene_index, len(scenes))
        img.save(f"/tmp/frames/frame_{frame:05d}.png")
        
        if (frame + 1) % 150 == 0:
            print(f"  Progress: {frame + 1}/{total_frames} frames")
    
    print(f"Done! Generated {total_frames} frames")

if __name__ == "__main__":
    main()
