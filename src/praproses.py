"""praproses.py: rangkaian praproses SIMUTEH (dipakai ulang mulai P5)."""
import os
import json
import cv2
import numpy as np

PARAM_BAWAAN = {
    "lebar": 640,          # sampling: lebar citra kerja (piksel)
    "gamma": 1.0,          # < 1 mencerahkan, > 1 menggelapkan
    "clahe_clip": 2.0,     # 0 berarti CLAHE tidak dipakai
    "clahe_tile": 8,
    "penapis": "median",   # "none", "rerata", "gaussian", "median"
    "kernel": 3,
    "sigma": 1.0,
    "tajam_k": 0.0,        # 0 berarti tanpa penajaman
}


def praproses(img_bgr, p=None):
    """Urutan: ubah ukuran -> gamma -> CLAHE kanal V -> redam derau -> tajamkan."""
    p = {**PARAM_BAWAAN, **(p or {})}
    img = img_bgr.copy()

    # TODO 1: ubah ukuran agar lebar = p["lebar"], rasio aspek tetap,
    #         gunakan interpolation=cv2.INTER_AREA, simpan ke variabel img
    target_w = p.get("lebar", 640)
    if target_w is not None and target_w > 0:
        h, w = img.shape[:2]
        if w != target_w:
            target_h = int(round(h * (target_w / float(w))))
            img = cv2.resize(img, (target_w, target_h), interpolation=cv2.INTER_AREA)

    # TODO 2: bila p["gamma"] != 1, terapkan koreksi gamma dengan cv2.LUT
    gamma = p.get("gamma", 1.0)
    if gamma != 1.0 and gamma > 0:
        lut = np.clip(255.0 * (np.arange(256) / 255.0) ** gamma, 0, 255).astype(np.uint8)
        img = cv2.LUT(img, lut)

    # TODO 3: bila p["clahe_clip"] > 0, ubah ke HSV, terapkan CLAHE pada
    #         kanal V saja, lalu kembalikan ke BGR
    clahe_clip = p.get("clahe_clip", 0.0)
    if clahe_clip > 0:
        clahe_tile = int(p.get("clahe_tile", 8))
        clahe = cv2.createCLAHE(clipLimit=float(clahe_clip), tileGridSize=(clahe_tile, clahe_tile))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = clahe.apply(hsv[:, :, 2])
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # TODO 4: redam derau sesuai p["penapis"], p["kernel"], p["sigma"]
    penapis = p.get("penapis", "none")
    kernel = int(p.get("kernel", 3))
    if kernel % 2 == 0:
        kernel += 1
    sigma = float(p.get("sigma", 1.0))

    if penapis == "rerata":
        img = cv2.blur(img, (kernel, kernel))
    elif penapis == "gaussian":
        img = cv2.GaussianBlur(img, (kernel, kernel), sigma)
    elif penapis == "median":
        img = cv2.medianBlur(img, kernel)
    elif penapis == "none":
        pass

    # TODO 5: bila p["tajam_k"] > 0, lakukan unsharp masking
    tajam_k = float(p.get("tajam_k", 0.0))
    if tajam_k > 0:
        blur = cv2.GaussianBlur(img, (5, 5), 1.0)
        img = cv2.addWeighted(img, 1.0 + tajam_k, blur, -tajam_k, 0)

    return img


def simpan_param(p, path="../hasil/param_praproses.json"):
    """Menyimpan parameter gabungan bawaan dan kustom ke berkas JSON."""
    dirpath = os.path.dirname(os.path.abspath(path))
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({**PARAM_BAWAAN, **p}, f, indent=2)
