"""
Prompt repository and heuristic mappings for script analysis.
"""

EMOTION_KEYWORDS = {
    "suspense": ["dark", "shadow", "unknown", "crept", "waiting", "danger", "mystery", "silent", "whisper", "abyss"],
    "awe": ["immense", "vast", "glorious", "cosmos", "ancient", "wondrous", "magnificent", "endless", "galaxy"],
    "sorrow": ["lost", "fallen", "tragedy", "extinct", "tears", "lonely", "desolate", "faded", "ruins"],
    "action": ["chase", "struck", "explosion", "erupted", "swift", "battle", "surged", "collapsed", "storm"],
    "curiosity": ["discovered", "revealed", "unlocked", "puzzle", "question", "delving", "searching", "hidden"]
}

MUSIC_STYLE_MAP = {
    "suspense": ("Dark Ambient / Drone", (60, 85), ["Sub-bass synth", "Dissonant Cello", "Prepared Piano", "Atmospheric Pads"]),
    "awe": ("Orchestral Hybrid / Celestial", (75, 100), ["Full String Ensemble", "Brass Swells", "Female Choir", "Modular Synths"]),
    "sorrow": ("Neoclassical Minimalist", (50, 70), ["Solo Cello", "Upright Piano", "Soft Violins", "Subtle Reverb Trails"]),
    "action": ("Cinematic Percussive Hybrid", (110, 140), ["Taiko Drums", "Low Brass", "Aggressive Synth Bass", "Staccato Strings"]),
    "curiosity": ("Pulse / Micro-Textural", (85, 110), ["Marimba", "Pizzicato Strings", "Analog Arpeggiator", "Woodwinds"])
}
