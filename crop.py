import random

from PIL import Image
import numpy as np
from sklearn.cluster import KMeans


def get_random_crops(img, crop_size=720):
    assert img.size == (1600, 1600), "Image must be 1600x1600"

    region_centers = {
        "top_left": (400, 400),
        "top_right": (1200, 400),
        "bottom_left": (400, 1200),
        "bottom_right": (1200, 1200),
        "center": (800, 800),
    }

    crops = []

    for cx, cy in region_centers.values():
        # Choose a random top-left offset within ~±100px around the center
        offset_x = random.randint(cx - 100, cx + 100) - crop_size // 2
        offset_y = random.randint(cy - 100, cy + 100) - crop_size // 2

        # Clamp to image bounds
        offset_x = max(0, min(offset_x, img.width - crop_size))
        offset_y = max(0, min(offset_y, img.height - crop_size))

        box = (offset_x, offset_y, offset_x + crop_size, offset_y + crop_size)
        crop = img.crop(box)
        crop_resized = crop.resize((1080, 1080), resample=Image.LANCZOS)
        crops.append(crop_resized)

    random.shuffle(crops)
    return crops


def get_bars_color(img: Image.Image, num_clusters=4, skip_top_n=3, pick_from_n=1):
    """
    Pick a subtle, less prominent color from the image.
    - skip_top_n: how many most dominant colors to skip
    - pick_from_n: how many of the next less-dominant to consider randomly
    """
        # 1) shrink for speed
    small = img.resize((100, 100))
    pixels = np.array(small).reshape(-1, 3)

    # 2) k-means – use int for n_init to support old sklearn
    kmeans = KMeans(
        n_clusters=num_clusters,
        n_init=10,          # <-- int works on every sklearn version
        random_state=0
    )
    labels = kmeans.fit_predict(pixels)
    counts = np.bincount(labels)

    # 3) sort clusters by pixel count (descending)
    ordered = np.argsort(-counts)

    # 4) candidates: anything after the top `skip_top_n`
    candidates = ordered[skip_top_n:skip_top_n + pick_from_n]
    chosen = random.choice(candidates)

    # 5) convert centre to ints
    color = tuple(int(c) for c in kmeans.cluster_centers_[chosen])

    return color
