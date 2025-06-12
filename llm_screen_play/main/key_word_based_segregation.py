import re
import json

def parse_screenplay(text):
    # Regex patterns
    slugline_pattern = r'^(\d+)\s*(INT\.|EXT\.|INT\./EXT\.|I/E)\s+([A-Z\s\-.,&]+?)\s*(?:-\s*([A-Z\s\-.,&]+))?\s*-\s*(DAY|NIGHT|EVENING|MORNING|CONTINUOUS|NIGHTFADE|DUSK|DAWN)$'
    transition_pattern = r'^(CUT TO:|FADE OUT:|FADE IN:|DISSOLVE TO:|WIPE TO:|MATCH CUT TO:)$'
    character_pattern = r'^\s*([A-Z\s]+)(?:\s*\((V\.O\.|O\.S\.|O\.C\.)\))?\s*$'
    parenthetical_pattern = r'^\s*\(([a-zA-Z\s,]+)\)\s*$'
    shot_direction_pattern = r'^(CLOSE ON|ANGLE ON|WIDE SHOT|POV|PAN TO|ZOOM IN|TRACKING SHOT):'
    superimpose_pattern = r'^SUPERIMPOSE:\s*(.+)$'

    # Keywords
    time_of_day_keywords = ["DAY", "NIGHT", "EVENING", "MORNING", "CONTINUOUS", "NIGHTFADE", "DUSK", "DAWN"]
    transition_keywords = ["CUT TO:", "FADE OUT:", "FADE IN:", "DISSOLVE TO:", "WIPE TO:", "MATCH CUT TO:"]

    scenes = []
    current_scene = None
    current_dialogue = None
    lines = text.strip().split('\n')
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # Slugline with Scene Number
        slug_match = re.match(slugline_pattern, line)
        if slug_match:
            if current_scene:
                scenes.append(current_scene)
            current_scene = {
                "scene_number": int(slug_match.group(1)),
                "slugline": {
                    "type": slug_match.group(2),
                    "location": slug_match.group(3).strip() + (f" - {slug_match.group(4).strip()}" if slug_match.group(4) else ""),
                    "time_of_day": slug_match.group(5)
                },
                "action_lines": [],
                "dialogue": [],
                "transitions": [],
                "shot_directions": [],
                "superimpose": []
            }
            i += 1
            continue

        # Transition
        if re.match(transition_pattern, line):
            if current_scene:
                current_scene["transitions"].append(line)
            i += 1
            continue

        # Shot Direction
        if re.match(shot_direction_pattern, line):
            if current_scene:
                current_scene["shot_directions"].append(line)
            i += 1
            continue

        # Superimpose
        if re.match(superimpose_pattern, line):
            if current_scene:
                current_scene["superimpose"].append(re.match(superimpose_pattern, line).group(1))
            i += 1
            continue

        # Character Name
        char_match = re.match(character_pattern, line)
        if char_match:
            current_dialogue = {
                "character": char_match.group(1).strip(),
                "extension": char_match.group(2) if char_match.group(2) else None,
                "parenthetical": None,
                "text": ""
            }
            i += 1
            # Check for parenthetical
            if i < len(lines) and re.match(parenthetical_pattern, lines[i].strip()):
                current_dialogue["parenthetical"] = re.match(parenthetical_pattern, lines[i].strip()).group(1)
                i += 1
            # Collect dialogue lines
            dialogue_lines = []
            while i < len(lines) and not re.match(slugline_pattern, lines[i]) and not re.match(transition_pattern, lines[i]) and not re.match(character_pattern, lines[i]) and not re.match(shot_direction_pattern, lines[i]) and not re.match(superimpose_pattern, lines[i]):
                dialogue_lines.append(lines[i].strip())
                i += 1
            current_dialogue["text"] = " ".join(dialogue_lines).strip()
            if current_scene and current_dialogue["text"]:
                current_scene["dialogue"].append(current_dialogue)
            continue

        # Action Line
        if current_scene:
            current_scene["action_lines"].append(line)
        i += 1

    if current_scene:
        scenes.append(current_scene)

    return {"scenes": scenes}


import re
import json

def extract_production_categories(scene):
    # Keyword and regex lists
    category_keywords = {
        "CAST": [],
        "CAST_INFO": ["mute", "bum", "man", "woman", r"in his \d+s", r"in her \d+s"],
        "EXTRAS": ["extras", "background", "crowd", "group", "goons"],
        "PROPS": ["chillams", "radio", "mannequin", "briefcase", "idol", "jewelry", "cell phones", "money", "weed", "ring", "chair", "tv"],
        "LOCATION_DETAILS": ["platform", "tree", "ruins", "gates", "stairs", "hallway", "room"],
        "SCREEN_TITLES": [],
        "CAMERA": ["close", "angle", "wide", "pov", "pan", "zoom", "tracking"],
        "SOUND": ["radio", "sirens", "sound", "voice"],
        "LIGHTS": ["nightfade", "night", "day", "dusk", "dawn", "light", "sidelight"],
        "ELECTRICS": ["radio", "tv", "sidelight"],
        "STUNTS": ["run", "fight", "fall", "chase"],
        "MUSIC": ["gita", "music", "song", "radio"],
        "COSTUMES": ["rags", "tattered", "dishevelled", "costume"],
        "MAKEUP": ["dishevelled", "bleeding", "makeup"],
        "HAIR": ["dishevelled", "hair"],
        "VEHICLES": ["car", "truck", "bike", "vehicle"],
        "ANIMALS": ["dog", "cat", "horse", "animal"],
        "NUDITY": ["nude", "naked", "bare"],
        "GREENERY": ["tree", "forest", "grass", "bush"],
        "SET": ["platform", "temple", "room", "gates"],
        "SET_DRESSING": ["mannequin", "torso", "chair", "tv"],
        "CONSTRUCTION": ["platform", "temple", "ruins", "gates"],
        "SCENE_DETAILS": ["smoking", "dancing", "surveying", "rummaging"],
        "MECHANICAL_FX": ["explosion", "fog", "smoke"],
        "OPTICAL_FX": ["flash", "fade"],
        "VISUAL_FX": ["explosion", "smoke"],
        "SOUND_FX": ["sirens", "explosion"],
        "SPECIAL_FX": ["smoke", "fog"],
        "SPECIAL_EQUIPMENT": ["radio", "chillam", "briefcase"],
        "MISC": []
    }

    # Initialize output
    result = {
        "scene_number": scene.get("scene_number", "unknown"),
        "production_categories": {
            category: [] for category in category_keywords.keys()
        }
    }

    # Combine all relevant text for analysis
    text_to_analyze = []
    text_to_analyze.extend(scene.get("action_lines", []))
    text_to_analyze.append(scene.get("slugline", {}).get("location", ""))
    text_to_analyze.append(scene.get("slugline", {}).get("time_of_day", ""))
    for dialogue in scene.get("dialogue", []):
        text_to_analyze.append(dialogue.get("text", ""))
        if dialogue.get("parenthetical"):
            text_to_analyze.append(dialogue["parenthetical"])

    # CAST: From dialogue and named entities in action lines
    cast = set()
    for dialogue in scene.get("dialogue", []):
        cast.add(dialogue["character"])
    name_pattern = r'\b([A-Z][A-Z\s]+)\b'
    for line in scene.get("action_lines", []):
        matches = re.findall(name_pattern, line)
        cast.update([m.strip() for m in matches if m.strip() not in ["THE", "A", "AN"]])
    result["production_categories"]["CAST"] = list(cast)

    # CAST_INFO: Character descriptions
    cast_info_pattern = r'\b(?:' + '|'.join(category_keywords["CAST_INFO"]) + r')\b'
    for line in scene.get("action_lines", []):
        matches = re.findall(cast_info_pattern, line, re.IGNORECASE)
        result["production_categories"]["CAST_INFO"].extend(matches)

    # SCREEN_TITLES: From superimpose
    result["production_categories"]["SCREEN_TITLES"] = scene.get("superimpose", [])

    # Other categories: Keyword-based matching
    for category, keywords in category_keywords.items():
        if category in ["CAST", "CAST_INFO", "SCREEN_TITLES"]:
            continue
        for line in text_to_analyze:
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', line, re.IGNORECASE):
                    if keyword not in result["production_categories"][category]:
                        result["production_categories"][category].append(keyword)

    # MISC: Catch-all for unmatched terms (optional, can be expanded)
    result["production_categories"]["MISC"] = []

    return result


import json

def process_screenplay(screenplay_text):
    # Step 1: Structure Recognition
    structure_result = parse_screenplay(screenplay_text)
    
    # Step 2: Production Categories for each scene
    final_response = []
    for scene in structure_result.get("scenes", []):
        scene_result = {
            "scene_number": scene["scene_number"],
            "structure_recognition": scene,
            "production_categories": extract_production_categories(scene)["production_categories"]
        }
        final_response.append(scene_result)
    
    return final_response

# Example usage
if __name__ == "__main__":
    screenplay_text = """
    4.
    16 EXT. ROAD - NIGHT
    SURESH and the mute BUM are surveying the accident spot - the two men from the front of the car are dead. The car's blinking sidelight lights up SURI's bleeding face, who lay on the road almost dead. SURI barely musters the strength to ask them for help. The mute BUM wants to, but SURESH stops him, and points at SURI...or rather his gold ring.
    CUT TO:
    17 EXT. RUINED TEMPLE - NIGHT
    The bums are rummaging through their loot - jewelry, money, cell phones, and the green briefcase. SURESH opens the briefcase and finds a curious-looking antique idol. He thinks it is worthless, and gives it to the mute BUM, grabbing the rest. The BUM gratefully accepts it, immediately playing with it like a toy. Police sirens can be heard from the highway. SURESH is perturbed. He pockets as much loot as possible and scrambles. The BUM has the idol and the green briefcase with him.
    CUT TO:
    18 INT. MINISTER'S HOUSE - DAY
    A goon runs past the opulent gates, stairs, hallway and enters a vast room which has the FOREST MINISTER, a man in his 60s, with imposing presence and stature, lays his feet on SURESH. They are surrounded by the minister's goons, a woman sitting on a chair and watching TV, with the minister's LEAD GOON standing close to the FOREST MINISTER.
    FOREST MINISTER SURESH
    Ekkada raa aa vigraham? Saar... nenu nijam cheptunaanu, paniki raadhani aa moogodiki ichesaanu saar... naa daggara ivvi tappinchi inkem leevu
    FOREST MINISTER
    Vaadekkada?
    SURESH
    Telidhu saar...
    LEAD GOON
    Ekkada dorkatledu...
    """
    result = process_screenplay(screenplay_text)
    print(json.dumps(result, indent=4, ensure_ascii=False))

# # Example usage
# if __name__ == "__main__":
#     screenplay_text = """
#     4.
#     16 EXT. ROAD - NIGHT
#     SURESH and the mute BUM are surveying the accident spot - the two men from the front of the car are dead. The car's blinking sidelight lights up SURI's bleeding face, who lay on the road almost dead. SURI barely musters the strength to ask them for help. The mute BUM wants to, but SURESH stops him, and points at SURI...or rather his gold ring.
#     CUT TO:
#     17 EXT. RUINED TEMPLE - NIGHT
#     The bums are rummaging through their loot - jewelry, money, cell phones, and the green briefcase. SURESH opens the briefcase and finds a curious-looking antique idol. He thinks it is worthless, and gives it to the mute BUM, grabbing the rest. The BUM gratefully accepts it, immediately playing with it like a toy. Police sirens can be heard from the highway. SURESH is perturbed. He pockets as much loot as possible and scrambles. The BUM has the idol and the green briefcase with him.
#     CUT TO:
#     18 INT. MINISTER'S HOUSE - DAY
#     A goon runs past the opulent gates, stairs, hallway and enters a vast room which has the FOREST MINISTER, a man in his 60s, with imposing presence and stature, lays his feet on SURESH. They are surrounded by the minister's goons, a woman sitting on a chair and watching TV, with the minister's LEAD GOON standing close to the FOREST MINISTER.
#     FOREST MINISTER SURESH
#     Ekkada raa aa vigraham? Saar... nenu nijam cheptunaanu, paniki raadhani aa moogodiki ichesaanu saar... naa daggara ivvi tappinchi inkem leevu
#     FOREST MINISTER
#     Vaadekkada?
#     SURESH
#     Telidhu saar...
#     LEAD GOON
#     Ekkada dorkatledu...
#     """
#     result = parse_screenplay(screenplay_text)
#     print(json.dumps(result, indent=4, ensure_ascii=False))