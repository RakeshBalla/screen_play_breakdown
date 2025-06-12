import os
import dotenv
import re
import json
import re



def get_prompt_structure_recognition(content_text):
    sys_prompt = "You are an expert screenplay parser. Given the input screenplay text, parse and structure the content into a JSON object, accurately identifying and categorizing the following elements:"
    prompt1 = f"""
        - **Scene Headings (Sluglines)**: Lines starting with INT., EXT., INT./EXT., or I/E. Extract:
            - Type (INT., EXT., INT./EXT., I/E)
            - Location (primary location and optional sub-location, e.g., "KITCHEN – LIVING ROOM")
            - Time of Day (e.g., DAY, NIGHT, EVENING, CONTINUOUS, etc.)
        - **Action Lines**: Descriptive narrative text between scene headings and dialogue, capturing the scene's actions or descriptions.
        - **Character Names**: Centered, uppercase names above dialogue blocks, identifying the speaker.
        - **Character Names with Extensions**: Include extensions like (V.O.) (voice over), (O.C.) (off-camera), or (O.S.) (off-screen) if present.
        - **Dialogue**: Indented text under a character name, associated with the speaker.
        - **Dual Dialogue**: Two characters with side-by-side dialogue blocks, if present.
        - **Parentheticals**: Performance or delivery notes under character names, e.g., (angry), in parentheses.
        - **Shot Directions**: Specific camera or visual instructions, e.g., CLOSE ON, ANGLE ON.
        - **Superimpose**: Text labeled as SUPERIMPOSE: indicating visual text over an image.
        - **Transitions**: Right-aligned directives like CUT TO:, FADE OUT:, DISSOLVE TO:.

        **Input Text**:
        {content_text}
        ```

        **Instructions**:
        1. Parse the input screenplay text and produce a structured JSON output.
        2. For each scene (identified by scene number and slugline), create a JSON object containing:
        - Scene number
        - Scene heading details (type, location, time of day)
        - Action lines
        - Dialogue blocks (including character name, extensions if any, parentheticals if any, and dialogue text)
        - Transitions
        - Shot directions (if any)
        - Superimpose (if any)
        3. Ensure dialogue is correctly associated with the respective character.
        4. Handle any non-English dialogue accurately, preserving the original text.
        6. Ensure the output is valid JSON with clear, consistent formatting.

        **Output Format**:
        ```json
        {{
            "scene_number": [<number>, ...],
            "slugline": {{
                "type": [<string>, ...],        // e.g., INT. or EXT.
                "location": [<string>, ...],    // e.g., OFFICE - NIGHT
                "time_of_day": [<string>, ...]  // e.g., NIGHT, DAY, EVENING
            }},
            "action_lines": [<string>, ...],
            "dialogue": [
                {{
                "character": [<string>, ...],
                "extension": [<string|null>, ...],      // e.g., (O.S.), (V.O.)
                "parenthetical": [<string|null>, ...],  // e.g., (whispering)
                "text": [<string>, ...]
                }},
                ...
            ],
            "transitions": [<string>, ...],       // e.g., CUT TO:, DISSOLVE TO:
            "shot_directions": [<string>, ...],   // e.g., CLOSE UP, WIDE SHOT
            "superimpose": [<string>, ...]        // e.g., SUPER: "10 YEARS LATER"
        }},
 
        ```
        Provide the parsed JSON output for the given screenplay text.
        Note: Superimpose and Action Lines are two different elements, do not mix them up.generally Superimpose is a text overlay on the screen, while Action Lines describe the actions or events happening in the scene.
    """
    return prompt1, sys_prompt


def extract_and_save_json(response_text):
    """
    Extracts JSON from the response text using regex patterns and saves it as a JSON file.

    Parameters:
        response_text (str): The text response containing the JSON data.
        output_filename (str): Name of the output JSON file (without extension).
    """
    # Define regex patterns for extracting JSON content
    patterns = [
        r"'''<json response>\s*(\{.*?\})\s*'''",
        r"```<json response>\s*(\{.*?\})\s*```",
        r"```json\s*(\{.*?\})\s*```",
        r"'''json\s*(\{.*?\})\s*'''",
        r"\*\*<json response>\*\*\s*(\{.*?\})\s*\*\*<json response>\*\*",
        r"<json response>\s*(\{.*?\})\s*</json response>"
    ]

    extracted_data = None

    # Try to extract JSON content using regex patterns
    for pattern in patterns:
        print(f"Trying pattern: {pattern}")
        match = re.search(pattern, response_text, re.DOTALL)
        if match:
            json_str = match.group(1)  # Extract the JSON string
            try:
                extracted_data = json.loads(json_str)  # Convert to JSON object
                break  # Stop if valid JSON is found
            except json.JSONDecodeError:
                print("Invalid JSON format, trying next pattern...")

    # If no JSON found, set a default error response
    if extracted_data is None:
        extracted_data = {"error": "No valid JSON found in response"}

    return extracted_data


def get_prompt_production_categories_with_word_ids(content_text, word_ids_json):
    sys_prompt = "You are an expert in screenplay analysis and production planning. "
    prompt1 = f"""
        Given a screenplay scene and a word ID mapping, extract and categorize production-related elements into the following predefined categories: CAST, CAST_INFO, 
        EXTRAS, PROPS, LOCATION_DETAILS, SCREEN_TITLES, CAMERA, SOUND, 
        LIGHTS, ELECTRICS, STUNTS, MUSIC, COSTUMES, MAKEUP, HAIR, VEHICLES, 
        ANIMALS, NUDITY, GREENERY, SET, SET_DRESSING, CONSTRUCTION, SCENE_DETAILS, 
        MECHANICAL_FX, OPTICAL_FX, VISUAL_FX, SOUND_FX, SPECIAL_FX, SPECIAL_EQUIPMENT, 
        MISC. Include word IDs for each extracted value.
        **Input**:
        ```json
        {{
        "all_text": {content_text},
        "word_ids": {word_ids_json}
        }}
        ```
        **Instructions**:
        1. Analyze the provided screenplay scene.
        2. Extract and categorize elements into the specified production categories based on the scene's content:
        - **CAST**: Named characters appearing in the scene (e.g., SURESH).
        - **CAST INFO**: Specific details about characters (e.g., descriptions, roles, or traits like "mute").
        - **EXTRAS**: Background or non-speaking characters (if mentioned).
        - **PROPS**: Physical objects used in the scene (e.g., chillams, radio, mannequin torso).
        - **LOCATION DETAILS**: Specific details about the setting. A location is a real, physical place where filming happens.
                                It can be outdoors or indoors, and it's not built for filming — it already exists.('EXT. CENTRAL PARK - DAY', 'A real street in New York City')
        - **SCREEN TITLES**: In a screenplay, screen titles (also known as sluglines, scene headings, or scene titles) tell the reader.
                             Where the scene takes place, When the scene takes place, Whether it's interior (INT.) or exterior (EXT.). eg:('EXT. CENTRAL PARK - DAY')
        - **CAMERA**: Camera movements or shots mentioned (e.g., specific angles or directions).
        - **SOUND**: Audio elements like dialogue, voice-overs, or ambient sounds (e.g., radio Gita).
        - **LIGHTS**: Lighting requirements (e.g., implied by "NIGHTFADE").
        - **ELECTRICS**: Electrical equipment needs (e.g., for radio or lighting).
        - **STUNTS**: Stunt-related actions (if any).
        - **MUSIC**: Music or songs mentioned (e.g., Gita on the radio).
        - **COSTUMES**: Clothing or attire described (e.g., tattered rags).
        - **MAKEUP**: Makeup requirements (e.g., disheveled appearance).
        - **HAIR**: Hair styling needs (if specified).
        - **VEHICLES**: Vehicles mentioned (if any).
        - **ANIMALS**: Animals present (if any).
        - **NUDITY**: Nudity requirements (if any).
        - **GREENERY**: Vegetation or natural elements (e.g., tree).
        - **SET**: A set is a place that is built or constructed specifically for filming — usually inside a studio.
                    It can replicate real places or be completely fictional. (e.g.'INT. SPACESHIP COCKPIT – NIGHT', platform, ruined temple).
        - **SET DRESSING**: Decorative or atmospheric set items (e.g., mannequin in tree).
        - **CONSTRUCTION**: Construction needs for the set (e.g., platform or temple ruins).
        - **SCENE DETAILS**: Additional context or specific actions (e.g., smoking, dancing).
        - **MECHANICAL FX**: Mechanical effects (if any).
        - **OPTICAL FX**: Optical effects (if any).
        - **VISUAL FX**: Visual effects (if any).
        - **SOUND FX**: Sound effects (if any, beyond dialogue or music).
        - **SPECIAL FX**: Special effects (if any).
        - **SPECIAL EQUIPMENT**: Specialized equipment needs (if any).
        - **MISC**: Any other relevant production elements not covered above.
        3. Preserve non-English dialogue text accurately in the relevant categories (e.g., SOUND or MUSIC).
        4. If a category has no relevant elements, include it in the output with an empty array or null value.
        5. Produce a JSON output with the categorized elements, ensuring clear and consistent formatting.
        6. For each extracted element in the categories, include:
            value: The extracted text (e.g., "SURESH", "chillams").
            index_value: A list of word IDs from the word_ids dictionary corresponding to each word in the value. For multi-word values, include IDs for each word. If a word is not found in word_ids, use null for its ID.
        7. For a specific field, if the same value appears multiple times in the input text, extract all occurrences — do not merge or deduplicate them.
        8. When mapping the value to index_value, ensure:
            - Every occurrence is mapped accurately.
            - The correct IDs are assigned based on the specific instance of each word from the word_ids dictionary.
            - Even if a word appears multiple times, do not reuse IDs from earlier occurrences — map each appearance to its own correct ID.
            
        **Output Format**:
        ```json

        {{
        "production_categories": {{
                "CAST": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "CAST_INFO": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "EXTRAS": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "PROPS": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "LOCATION_DETAILS": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "SCREEN_TITLES": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "CAMERA": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "SOUND": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "LIGHTS": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "ELECTRICS": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "STUNTS": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "MUSIC": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "COSTUMES": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "MAKEUP": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "HAIR": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "VEHICLES": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "ANIMALS": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "NUDITY": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "GREENERY": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "SET": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "SET_DRESSING": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "CONSTRUCTION": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "SCENE_DETAILS": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "MECHANICAL_FX": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "OPTICAL_FX": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "VISUAL_FX": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "SOUND_FX": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "SPECIAL_FX": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "SPECIAL_EQUIPMENT": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ],
                "MISC": [
                {{
                    "value": <string>,
                    "index_value": [<number|null>, ...]
                }}
                ]
            }}
        }}
        ```
        Provide the JSON output with production categories for the given scene.
        Note: Try Not to include the context of dialogue or Action Lines in the production categories
        """
    return prompt1, sys_prompt




def get_prompt_production_categories(content_text):
    sys_prompt = "You are an expert in screenplay analysis and production planning. "
    prompt1 = f"""
        Given a screenplay scene and a word ID mapping, extract and categorize production-related elements into the following predefined categories: CAST, CAST_INFO, 
        EXTRAS, PROPS, LOCATION_DETAILS, SCREEN_TITLES, CAMERA, SOUND, 
        LIGHTS, ELECTRICS, STUNTS, MUSIC, COSTUMES, MAKEUP, HAIR, VEHICLES, 
        ANIMALS, NUDITY, GREENERY, SET, SET_DRESSING, CONSTRUCTION, SCENE_DETAILS, 
        MECHANICAL_FX, OPTICAL_FX, VISUAL_FX, SOUND_FX, SPECIAL_FX, SPECIAL_EQUIPMENT, 
        MISC.
        **Input Scene JSON**:
        ```json
        {content_text}
        ```
        **Instructions**:
        1. Analyze the provided screenplay scene.
        2. Extract and categorize elements into the specified production categories based on the scene's content:
        - **CAST**: Named characters appearing in the scene (e.g., SURESH).
        - **CAST INFO**: Specific details about characters (e.g., descriptions, roles, or traits like "mute").
        - **EXTRAS**: Background or non-speaking characters (if mentioned).
        - **PROPS**: Physical objects used in the scene (e.g., chillams, radio, mannequin torso).
        - **LOCATION DETAILS**: Specific details about the setting. A location is a real, physical place where filming happens.
                                It can be outdoors or indoors, and it's not built for filming — it already exists.('EXT. CENTRAL PARK - DAY', 'A real street in New York City')
        - **SCREEN TITLES**: In a screenplay, screen titles (also known as sluglines, scene headings, or scene titles) tell the reader.
                             Where the scene takes place, When the scene takes place, Whether it's interior (INT.) or exterior (EXT.). eg:('EXT. CENTRAL PARK - DAY')
        - **CAMERA**: Camera movements or shots mentioned (e.g., specific angles or directions).
        - **SOUND**: Audio elements like voice-overs, or ambient sounds (e.g., radio Gita).
        - **LIGHTS**: Lighting requirements (e.g., implied by "NIGHTFADE").
        - **ELECTRICS**: Electrical equipment needs (e.g., for radio or lighting).
        - **STUNTS**: Stunt-related actions (if any).
        - **MUSIC**: Music or songs mentioned (e.g., Gita on the radio).
        - **COSTUMES**: Clothing or attire described (e.g., tattered rags).
        - **MAKEUP**: Makeup requirements (e.g., disheveled appearance).
        - **HAIR**: Hair styling needs (if specified).
        - **VEHICLES**: Vehicles mentioned (if any).
        - **ANIMALS**: Animals present (if any).
        - **NUDITY**: Nudity requirements (if any).
        - **GREENERY**: Vegetation or natural elements (e.g., tree).
        - **SET**: A set is a place that is built or constructed specifically for filming — usually inside a studio.
                    It can replicate real places or be completely fictional. (e.g.'INT. SPACESHIP COCKPIT – NIGHT', platform, ruined temple).
        - **SET DRESSING**: Decorative or atmospheric set items (e.g., mannequin in tree).
        - **CONSTRUCTION**: Construction needs for the set (e.g., platform or temple ruins).
        - **SCENE DETAILS**: Additional context or specific actions (e.g., smoking, dancing).
        - **MECHANICAL FX**: Mechanical effects (if any).
        - **OPTICAL FX**: Optical effects (if any).
        - **VISUAL FX**: Visual effects (if any).
        - **SOUND FX**: Sound effects (if any, beyond dialogue or music).
        - **SPECIAL FX**: Special effects (if any).
        - **SPECIAL EQUIPMENT**: Specialized equipment needs (if any).
        - **MISC**: Any other relevant production elements not covered above.
        3. Preserve non-English dialogue text accurately in the relevant categories (e.g., SOUND or MUSIC).
        4. If a category has no relevant elements, include it in the output with an empty array or null value.
        5. Produce a JSON output with the categorized elements, ensuring clear and consistent formatting.
        **Output Format**:
        ```json

            "production_categories": {{
                "CAST": [<string>, ...],
                "CAST_INFO": [<string>, ...],
                "EXTRAS": [<string>, ...],
                "PROPS": [<string>, ...],
                "LOCATION_DETAILS": [<string>, ...],
                "SCREEN_TITLES": [<string>, ...],
                "CAMERA": [<string>, ...],
                "SOUND": [<string>, ...],
                "LIGHTS": [<string>, ...],
                "ELECTRICS": [<string>, ...],
                "STUNTS": [<string>, ...],
                "MUSIC": [<string>, ...],
                "COSTUMES": [<string>, ...],
                "MAKEUP": [<string>, ...],
                "HAIR": [<string>, ...],
                "VEHICLES": [<string>, ...],
                "ANIMALS": [<string>, ...],
                "NUDITY": [<string>, ...],
                "GREENERY": [<string>, ...],
                "SET": [<string>, ...],
                "SET_DRESSING": [<string>, ...],
                "CONSTRUCTION": [<string>, ...],
                "SCENE_DETAILS": [<string>, ...],
                "MECHANICAL_FX": [<string>, ...],
                "OPTICAL_FX": [<string>, ...],
                "VISUAL_FX": [<string>, ...],
                "SOUND_FX": [<string>, ...],
                "SPECIAL_FX": [<string>, ...],
                "SPECIAL_EQUIPMENT": [<string>, ...],
                "MISC": [<string>, ...]
            }}
        ```
        Provide the JSON output with production categories for the given scene.
        Note: Try Not to include the context of dialogue or Action Lines in the production categories
        """
    return prompt1, sys_prompt



def get_prompt_production_categories_revised_itr1(content_text):
    sys_prompt = "You are an expert in screenplay analysis and production planning, focusing on key tangible elements."
    prompt1 = f"""
        Given a screenplay scene, extract and categorize production-related elements into the following 
        predefined categories: CAST, SET, PROPS, STUNTS, VEHICLES, ANIMALS, NUDITY, GREENERY, SOUND.

        **Input Scene JSON**:
        ```json
        {content_text}
        ```
        **Instructions**:
        1. Analyze the provided screenplay scene.
        2. Extract and categorize elements into the specified production categories based on the scene's content:
            - **CAST**: Named characters appearing and speaking or performing significant actions in the scene.
                - *Example : ["SUBBA RAJU", "VEERAYYA", "SULOCHANA"]
            - **SET**: The primary location and time described in the scene header (slugline). This is the overall setting where the scene takes place.
                - *Example: ["EXT. PUB - NIGHT"]
            - **PROPS**: Tangible items characters interact with, handle, or are specifically mentioned as present and significant to the action.
                - *Example: ["lathi", "police belt"]
            - **STUNTS**: Specific physical actions explicitly described that would require specialized performance, coordination, or safety measures (e.g., falls, fights, crashes if detailed).
                - *Example*: ["CHARACTER A JUMPS FROM ROOFTOP"]
            - **VEHICLES**: Any mode of transport mentioned or used by characters in the scene.
                - *Example from a scene like "EXT. PUB - NIGHT..."*: ["car"]
            - **ANIMALS**: Any animals explicitly mentioned as present or directly interacting in the scene.
                - *Example*: ["DOG BARKS IN BACKGROUND"]
            - **NUDITY**: Explicit mentions of nudity of characters.
                - *Example*: ["CHARACTER B IS NUDE"]
            - **GREENERY**: Significant mentions of plants, trees, grass, or specific natural landscape elements that are part of the immediate setting.
                - *Example*: [" overgrown garden", "tall oak tree"]
            - **SOUND**: Specific sound effects, ambient sounds, or significant audio cues mentioned or clearly implied by actions, *excluding spoken dialogue*. These should be distinct sounds, not general descriptions of actions.
                - *Examples*: ["CAR DOOR OPENS AND CLOSES", "FOOTSTEPS ON GRAVEL", "DISTANT SIREN", "PHONE RINGING", "MUSIC FROM RADIO (if the focus is the sound, not the song title for a 'MUSIC' category)"]

        3. Extract the most direct and concise terms for each element.
        4. If a category has no relevant elements, include it in the output with an empty array.
        5. Produce a JSON output with the categorized elements.
        6. Focus strictly on the elements as defined for these specific categories. Do not infer elements that are not explicitly stated or very strongly implied (especially for SOUND).
        7. Do not include character dialogue or general action descriptions unless they directly specify an element for the categories above (e.g., an action line "He picks up the GUN" puts "GUN" in PROPS, or "SOUND of a gunshot" puts "GUNSHOT" in SOUND).
        8. Preserve non-English dialogue text accurately in the relevant categories.

        **Output Format**:
        ```json
        {{
            "production_categories": {{
                "CAST": [<string>, ...],
                "SET": [<string>, ...],
                "PROPS": [<string>, ...],
                "STUNTS": [<string>, ...],
                "VEHICLES": [<string>, ...],
                "ANIMALS": [<string>, ...],
                "NUDITY": [<string>, ...],
                "GREENERY": [<string>, ...],
                "SOUND": [<string>, ...]
            }}
        }}
        ```
        Provide the JSON output with production categories for the given scene.
        """
    return prompt1, sys_prompt


def get_prompt_production_categories_revised(content_text):
    sys_prompt = "You are an expert in screenplay analysis and production planning, focusing on key tangible elements."
    prompt1 = f"""
        Given a screenplay scene, extract and categorize production-related elements into the following 
        predefined categories: CAST, SET, PROPS, STUNTS, VEHICLES, ANIMALS, NUDITY, GREENERY, SOUND.

        **Input Scene JSON**:
        ```json
        {content_text}
        ```
        **Instructions**:
        1. Analyze the provided screenplay scene and preserve the original words from the input scene without altering their context or meaning.
        2. Extract and categorize elements into the specified production categories based on the scene's content:
        - **CAST**: All named characters appearing, speaking, or performing significant actions in the scene, including references such as "man," "brother," "person," or similar. Thoroughly check the scene to ensure all such references are included.
            - *Example*: ["SUBBA RAJU", "VEERAYYA", "SULOCHANA", "MAN", "BROTHER"]
        - **SET**: The primary location and time described in the scene header (slugline). This is the overall setting where the scene takes place. Do not include items or elements from the setting as PROPS.
            - *Example*: ["EXT. PUB - NIGHT"]
        - **PROPS**: Tangible items explicitly mentioned in action lines that characters interact with, handle, or are significant to the scene's action. Do not include items mentioned only in dialogue unless they are explicitly used in the scene's action. Ignore items that are part of the SET (e.g., furniture or fixtures inherent to the location).
            - *Example*: ["lathi", "police belt"]
        - **STUNTS**: Specific physical actions explicitly described that require specialized performance, coordination, or safety measures (e.g., falls, fights, crashes). Exclude simple actions, rushed movements, or casual dialogue references like "he pushed" unless they clearly describe a complex, choreographed, or hazardous action. Challenges between characters (e.g., a race or a tricky maneuver) may qualify as stunts only if they are physically demanding and require coordination.
            - *Example*: ["CHARACTER A JUMPS FROM ROOFTOP", "CHARACTER B PERFORMS A HIGH-SPEED CHASE"]
        - **VEHICLES**: Any mode of transport explicitly mentioned or used by characters in the scene's action.
            - *Example*: ["car"]
        - **ANIMALS**: Any animals explicitly mentioned as present or directly interacting in the scene.
            - *Example*: ["DOG BARKS IN BACKGROUND"]
        - **NUDITY**: Explicit mentions of nudity of characters in the scene's action or description.
            - *Example*: ["CHARACTER B IS NUDE"]
        - **GREENERY**: Significant mentions of plants, trees, grass, or specific natural landscape elements that are part of the immediate setting. Include natural elements like rain, stars, mountains, or other environmental features explicitly mentioned.
            - *Example*: ["overgrown garden", "tall oak tree", "heavy rain", "starlit sky", "rugged mountains"]
        - **SOUND**: Specific sound effects, ambient sounds, or significant audio cues mentioned or strongly implied by actions, *excluding spoken dialogue*. These should be distinct sounds, not general action descriptions. Only include sounds explicitly described in the scene.
            - *Examples*: ["CAR DOOR OPENS AND CLOSES", "FOOTSTEPS ON GRAVEL", "DISTANT SIREN", "PHONE RINGING"]
            
        Please analyze the input scene and follow these detailed instructions strictly:

        1. **Preserve Original Wording**:
        Do not rephrase or alter the original scene content. Extract elements exactly as written in the script.

        2. **Directness and Relevance**:
        * Extract the most direct and concise terms for each element.
        * If a category has no relevant elements, include it in the output with an empty array.
        * Do **not infer or assume** elements that are not explicitly stated or very clearly implied, especially for **SOUND**.

        3. **Dialogue Handling**:
        * Do **not include dialogue lines** themselves.
        * **Only include elements mentioned in the dialogue** if they are **physically used or interacted with in the scene**.
            Example: “He picks up the gun” → "gun" goes to **PROPS**.
        * If something is mentioned in dialogue **but not used or shown**, **ignore it**.
        
        4. **STUNTS** Clarification:
        * Do **not** treat jovial or casual expressions like “he pushed” or “they fell for fun” as stunts.
        * Only include **physically demanding, risky, or choreographed** actions.
        * Actions performed in a rush or with trickiness that imply a challenge may qualify as stunts.
        * Simple, everyday motions **are not** stunts.
        
        5. **PROPS vs. Set**:
        * Only include items **actively used or interacted with** in the scene as **PROPS**.
        * Objects that are not interacted with by the characters—but are instead part of the environment—are considered SET ELEMENTS,
           These may include items like background furniture, wall paintings, decorative lamps, toilets, raised platforms, etc.
        
        6. **GREENERY** Category:
        * Natural elements such as **rain, wind, mountains, trees, stars, rivers, etc.** must be included in the **GREENERY** category.
        
        7. **CAST Identification**:
        * All **named characters** and **generic references** (e.g., "man", "girl", "uncle", "brother", "driver", "cop", etc.) must be listed under **CAST**.
        * Ensure all such references are carefully extracted.
        * Do not include people who are only mentioned in dialogue unless they are actually present in the scene.
        * In other words, only include characters who are visibly participating in the scene.
        * Do not include general or descriptive terms used to narrate the environment— not specific or credited characters. 
        
        8. **Careful Property Detection**:
        * An item mentioned must only be categorized under **PROPS** if it is **visibly or explicitly used** in the action.
        * If the item is **only referenced** in dialogue but not used, **do not include it**.
        
        9. **Output Format**:
            Produce the final output as a structured **JSON**, with each of the five categories clearly listed.

        **Output Format**:
        ```json
        {{
            "production_categories": {{
                "CAST": [<string>, ...],
                "SET": [<string>, ...],
                "PROPS": [<string>, ...],
                "STUNTS": [<string>, ...],
                "VEHICLES": [<string>, ...],
                "ANIMALS": [<string>, ...],
                "NUDITY": [<string>, ...],
                "GREENERY": [<string>, ...],
                "SOUND": [<string>, ...]
            }}
        }}
        ```
        Provide the JSON output with production categories for the given scene.
        """
    return prompt1, sys_prompt



# Sample tokenizer
def tokenize(text):
    return re.findall(r"\b\w+(?:\.\w+)?\b", text)

# Recursive function to walk through nested dict/list and add matched IDs
def enrich_with_ids_struct_recog(data, ids_words):

    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            enriched = enrich_with_ids_struct_recog(value, ids_words)
            result[key] = enriched
        return result

    elif isinstance(data, list):
        enriched_list = []
        for item in data:
            enriched_list.append(enrich_with_ids_struct_recog(item, ids_words))
        return enriched_list

    elif isinstance(data, str):
        tokens = tokenize(data)
        matched_ids = [id for id, word in ids_words.items() if word in tokens]
        return {"value": data, "ids": matched_ids}

    else:
        # For None or unexpected types, just return as is
        return {"value": data, "ids": []}





def group_ids(ids, pair_size=2):
    """Group IDs into lists of specified size (default: pairs)."""
    return [ids[i:i + pair_size] for i in range(0, len(ids), pair_size) if len(ids[i:i + pair_size]) == pair_size]


def process_input(tezt):
    """Process input text into a dictionary with word IDs."""
    tezt = tezt.replace('\n', ' ')
    tezt = tezt.replace('  ', ' ')
    # Split by spaces and remove empty strings
    words = [word for word in tezt.split(' ') if word]
    
    page_dict = {
        "alltext": tezt,
        "words_ids": {}
    }
    # Assign word IDs starting from 1000
    for i, wo in enumerate(words):
        word_id = str(1000 + i)
        page_dict["words_ids"][word_id] = wo
    return page_dict
    
    