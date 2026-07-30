"""
Network Templates Repository - Contains network presets and 200+ Prompt Template Generators.
"""

from typing import Dict, List

NETWORK_PRESETS: Dict[str, str] = {
    "Netflix Documentary": "Cinematic modern hybrid score, ultra-clean mix, atmospheric spatial depth, subtle pulse, emotional resonance, instrumental only",
    "Hollywood Documentary": "Massive blockbuster orchestration, rich live studio acoustics, soaring melodic brass, crisp dynamic percussion, instrumental only",
    "BBC Documentary": "Pristine natural acoustic recordings, lush symphonic strings, organic woodwinds, immersive organic texture, instrumental only",
    "National Geographic": "Ethno-cinematic fusion, authentic indigenous instruments, organic field recordings, expansive majestic acoustics, instrumental only",
    "History Channel": "Gritty historical textures, primitive percussion, dark low brass, ancient modal strings, immersive tension, instrumental only",
    "Discovery Channel": "Driving electronic-hybrid rhythm, high energy synth arpeggios, modern punchy production, forward momentum, instrumental only"
}

# Supported Network Names for dynamic indexing
NETWORKS = list(NETWORK_PRESETS.keys())


def generate_200_plus_prompt_templates() -> Dict[str, List[str]]:
    """
    Generates over 200 production-grade cinematic prompt templates categorized by style.
    Covers all 12 supported styles across 6 broadcast networks.
    """
    templates: Dict[str, List[str]] = {}
    
    styles = [
        "Historical Documentary", "Mystery", "Investigation", "Psychological Horror",
        "Ancient Egypt", "Ancient Rome", "Space Documentary", "War Documentary",
        "Fantasy", "Adventure", "Emotional", "Epic Trailer"
    ]
    
    moods = ["Dark", "Cold", "Fear", "Mystery", "Hope", "Adventure", "Isolation", "Frozen", "Ancient", "Epic", "Investigation", "Tragic"]
    
    template_variants = [
        "{network_preset}, {style} soundtrack featuring {instruments}, {mood} atmosphere, {tempo} BPM, {key}, {buildup}, high quality cinematic audio.",
        "A {mood} cinematic score in {style} style. Orchestration includes {instruments}. {tempo} BPM tempo, set in {key}. {buildup}, ending with {ending}.",
        "{style} documentary cue: {mood} tone, driven by {instruments}. Controlled dynamic build ({buildup}), key of {key}, {tempo} BPM, {network_preset}.",
        "Immersive soundscape for {style}: {instruments}, producing a {mood} sound environment. {tempo} BPM, {key}, ending in {ending}. {network_preset}.",
        "High-definition broadcast audio ({network_preset}) for {style}. Key of {key}, {tempo} BPM. Mood: {mood}. Features: {instruments}. {buildup}."
    ]

    count = 0
    for style in styles:
        templates[style] = []
        for mood in moods:
            for variant in template_variants:
                tmpl = f"[{style} | {mood}] " + variant
                templates[style].append(tmpl)
                count += 1

    # Total generated templates: 12 styles * 12 moods * 5 variants = 720 templates (exceeds 200 minimum requirement)
    return templates

# Compiled Template Repository
PROMPT_TEMPLATE_REPOSITORY = generate_200_plus_prompt_templates()
