# -*- coding: utf-8 -*-
import os
from settings import BEST_FILE, SKIN_FILE

def load_best():
    try:
        if os.path.exists(BEST_FILE):
            with open(BEST_FILE, 'r', encoding='utf-8') as f:
                return int(f.read().strip() or 0)
    except:
        pass
    return 0

def save_best(v: int):
    try:
        with open(BEST_FILE, 'w', encoding='utf-8') as f:
            f.write(str(int(v)))
    except:
        pass

def load_skin_index(max_len: int = 5):
    try:
        if os.path.exists(SKIN_FILE):
            with open(SKIN_FILE, "r", encoding="utf-8") as f:
                idx = int(f.read().strip())
                if 0 <= idx < max_len:
                    return idx
    except:
        pass
    return 0

def save_skin_index(idx: int):
    try:
        with open(SKIN_FILE, "w", encoding="utf-8") as f:
            f.write(str(int(idx)))
    except:
        pass
