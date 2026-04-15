# America Progress 3D Visualization

A 3D animated video showing America's journey from colonial times to modern superpower - highlighting key factors of growth and the transformation of cities.

## Overview

This project creates a cinematic 3D visualization of America's progress:
- Historical timeline from colonization to present
- Key development factors (industrialization, innovation, immigration, etc.)
- Visual comparison of old colonial cities vs modern skylines
- Geographic context on a 3D globe

## Requirements

```bash
pip install numpy opencv-python
```

## Manual Execution

### Step 1: Generate 3D Globe with Countries
```bash
git clone https://github.com/martinbaud/geojsonto3D.git
cd geojsonto3D
pip install numpy
python main.py --preset medium --enable-cities
```

### Step 2: Render Animation
```bash
blender -b america_scene.blend -E CYCLES -s 1 -e 360 -a -- --cycles-device CPU
```

### Step 3: Create Video
```bash
ffmpeg -framerate 30 -i frames/frame_%04d.png -c:v libx264 -pix_fmt yuv420p america_progress.mp4
```

## GitHub Actions

This project includes `.github/workflows/render.yml` which automatically:
1. Installs Blender and dependencies
2. Generates 3D globe
3. Renders animation frames
4. Creates MP4 video
5. Uploads as artifact

## Story Script

The video covers:
1. **Colonial Era (1600s-1776)** - 13 colonies, small settlements
2. **Independence & Expansion (1776-1865)** - Revolution, westward expansion
3. **Industrial Revolution (1865-1900)** - Factories, railroads, immigration
4. **World Power (1900-1950)** - WWI, WWII, economic dominance
5. **Modern America (1950-Present)** - Technology, cities, global influence

## Key Development Factors

- Industrial innovation
- Immigration & diversity
- Natural resources
- Education & research
- Democratic governance
- Capital investment