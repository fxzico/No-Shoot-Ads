# Professional Watermark Removal Pipeline
**For no-shoot ad production — frame-by-frame inpainting, ProRes output, Premiere-ready**

---

## Overview

Remove watermarks from source footage using **pixel-to-pixel intelligent inpainting** (not blur).

**Algorithms:**
- CPU: OpenCV Telea (fast, good for small regions like watermarks)
- GPU: ProPainter (slower, excellent for complex/large regions)

**Output:** ProRes 422 HQ (.mov) for lossless intermediate editing

---

## GPU Setup (One-Time)

### RTX 4060 / 3060 / 3080 / 4090

```bash
# 1. Verify NVIDIA driver
nvidia-smi

# 2. Install CUDA Toolkit 11.8 from:
# https://developer.nvidia.com/cuda-11-8-0-download-archive

# 3. Install PyTorch with CUDA support
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# 4. Verify CUDA in Python
python -c "import torch; print('CUDA:', torch.cuda.is_available())"
```

---

## Method 1: OpenCV Telea (CPU — Ready Now)

**Speed:** 45 min for 18x 4-sec videos  
**Quality:** Professional px-to-px inpainting  
**No GPU required**

### Script Template

```python
#!/usr/bin/env python3
import cv2
import numpy as np
import ffmpeg
import os
from pathlib import Path

VIDEO_DIR = "path/to/Videos"
OUTPUT_DIR = "path/to/Clean"
WATERMARK_BOX = (x, y, width, height)  # Bottom-right corner location

def create_watermark_mask(frame_shape, box):
    """Binary mask for watermark region"""
    h, w = frame_shape[:2]
    x, y, bw, bh = box
    mask = np.zeros((h, w), dtype=np.uint8)
    x1, y1 = max(0, x-5), max(0, y-5)
    x2, y2 = min(w, x+bw+5), min(h, y+bh+5)
    mask[y1:y2, x1:x2] = 255
    return mask

def inpaint_frame_telea(frame, mask):
    """Telea inpainting algorithm"""
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask_dilated = cv2.dilate(mask, kernel, iterations=1)
    return cv2.inpaint(frame, mask_dilated, 3, cv2.INPAINT_TELEA)

def process_video_frame_by_frame(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    frame_dir = Path("C:/tmp/frames_clean")
    frame_dir.mkdir(exist_ok=True, parents=True)
    
    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        mask = create_watermark_mask(frame.shape, WATERMARK_BOX)
        try:
            frame_clean = inpaint_frame_telea(frame, mask)
        except Exception as e:
            print(f"Frame {frame_idx}: {e}")
            frame_clean = frame
        
        cv2.imwrite(str(frame_dir / f"frame_{frame_idx:05d}.png"), frame_clean)
        frame_idx += 1
        
        if frame_idx % 20 == 0:
            pct = int(100 * frame_idx / frame_count)
            print(f"  {frame_idx}/{frame_count} ({pct}%)")
    
    cap.release()
    
    # Reassemble with FFmpeg
    (
        ffmpeg
        .input(str(frame_dir / "frame_%05d.png"), framerate=fps)
        .output(output_path, c_v="prores_ks", profile_v="3", c_a="aac", q_scale_v=9)
        .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
    )
    
    import shutil
    shutil.rmtree(frame_dir)

os.makedirs(OUTPUT_DIR, exist_ok=True)
videos = sorted([f for f in os.listdir(VIDEO_DIR) if f.endswith(".mp4")])

for idx, video in enumerate(videos, 1):
    video_path = os.path.join(VIDEO_DIR, video)
    name = video.replace(".mp4", "")
    output_path = os.path.join(OUTPUT_DIR, f"{name}_clean.mov")
    
    if os.path.exists(output_path):
        print(f"[{idx}] SKIP {name}")
        continue
    
    process_video_frame_by_frame(video_path, output_path)
```

### Run It

```bash
cd /path/to/project
python watermark_removal_telea.py
```

---

## Method 2: ProPainter (GPU — Better Quality)

**Speed:** 4–6 hours for 18 videos  
**Quality:** Excellent for complex backgrounds  
**Requires:** RTX 3060 or better

### Setup

```bash
# 1. Clone ProPainter
cd C:/tmp
git clone https://github.com/sczhou/ProPainter.git
cd ProPainter

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download pretrained model
# https://huggingface.co/sczhou/ProPainter/blob/main/propainter.pth
# Save to: C:/tmp/ProPainter/pretrained_models/propainter.pth

# 4. Test GPU
python -c "import torch; print(f'GPU: {torch.cuda.is_available()}')"
```

### Batch Script

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, "C:/tmp/ProPainter")

from core.utils import flow_warp, pad_forward_backward, pad_divide
from models.propainter import ProPainter
import torch
import cv2
import numpy as np
from pathlib import Path

# Load model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = ProPainter(
    num_frames=6,
    inject_frames=5,
    n_layers=18,
    c_dim=96,
    depth_dim=10,
    backbone="swin2"
).to(device)

checkpoint = torch.load("C:/tmp/ProPainter/pretrained_models/propainter.pth", map_location=device)
model.load_state_dict(checkpoint["state_dict"])
model.eval()

def create_mask(frame_shape, box):
    """Watermark mask"""
    h, w = frame_shape[:2]
    x, y, bw, bh = box
    mask = np.zeros((h, w), dtype=np.uint8)
    x1, y1 = max(0, x-5), max(0, y-5)
    x2, y2 = min(w, x+bw+5), min(h, y+bh+5)
    mask[y1:y2, x1:x2] = 1
    return mask

# Process video...
```

---

## Choosing the Right Method

| Factor | Telea | ProPainter |
|--------|-------|-----------|
| Setup time | 2 min | 30 min |
| GPU required | No | Yes (RTX 3060+) |
| Speed | Fast (45m) | Slow (4-6h) |
| Quality | Good | Excellent |
| Watermark complexity | Simple (logos, text) | Complex (patterns) |

**Recommendation:** Start with **Telea** for speed. If results show artifacts, switch to **ProPainter**.

---

## Integration with No-Shoot Ads

### Input

```json
{
  "project": "EmbroCare",
  "source_videos": "F:/Downloads/Manan/Videos with Water mark",
  "output_videos": "F:/Downloads/Manan/Clean clips",
  "watermark_box": [1600, 900, 300, 150],
  "method": "telea"
}
```

### Output

```
F:/Downloads/Manan/Clean clips/
  1st_shot_clean.mov
  2nd_shot_clean.mov
  ...
  18th_shot_clean.mov
```

All ProRes 422 HQ, ready for Premiere conform → AE graphics → final export.

---

## QC Checklist

- [ ] Watermark fully removed (no residual text/logo)
- [ ] No obvious seams or blurring at removal edges
- [ ] Colors match surrounding pixels
- [ ] Texture naturally blends (not plastic-looking)
- [ ] No temporal artifacts (flickering frame-to-frame)

---

## Troubleshooting

**Q: Telea results show blur**
A: Increase kernel size or dilate iterations. Reduce to see if it's the algorithm choice.

**Q: ProPainter runs out of memory**
A: Split video into chunks (first 100 frames, next 100, etc.). Reassemble in Premiere.

**Q: Watermark partially remains**
A: Expand WATERMARK_BOX (increase width/height by 20px).

**Q: Colors don't match**
A: Use ProPainter instead (better content understanding).

---

## References

- OpenCV Telea: `cv2.inpaint(..., cv2.INPAINT_TELEA)`
- ProPainter: https://github.com/sczhou/ProPainter
- FFmpeg ProRes: https://trac.ffmpeg.org/wiki/Encode/ProRes
