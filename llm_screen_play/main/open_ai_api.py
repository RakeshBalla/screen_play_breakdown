import os
import dotenv
import re
import json


# Load environment variables
dotenv.load_dotenv()
api_key_ge = os.getenv("GEMINI_API_KEY")


from openai import OpenAI

client = OpenAI(
    api_key=api_key_ge,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

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
        5. If an element (e.g., parentheticals, shot directions, superimpose) is not present, omit it from the JSON for that scene.
        6. Ensure the output is valid JSON with clear, consistent formatting.

        **Output Format**:
        ```json
        {{
        "scenes": [
            {{
            "scene_number": <number>,
            "slugline": {{
                "type": <string>,        // e.g., INT. or EXT.
                "location": <string>,    // e.g., OFFICE - NIGHT
                "time_of_day": <string>  // e.g., NIGHT, DAY, EVENING
            }},
            "action_lines": [<string>, ...],
            "dialogue": [
                {{
                "character": <string>,
                "extension": <string|null>,      // e.g., (O.S.), (V.O.)
                "parenthetical": <string|null>,  // e.g., (whispering)
                "text": <string>
                }},
                ...
            ],
            "transitions": [<string>, ...],       // e.g., CUT TO:, DISSOLVE TO:
            "shot_directions": [<string>, ...],   // e.g., CLOSE UP, WIDE SHOT
            "superimpose": [<string>, ...]        // e.g., SUPER: "10 YEARS LATER"
            }},
            ...
        ]
        }}
        ```
        Provide the parsed JSON output for the given screenplay text.
    """
    return prompt1, sys_prompt


def get_prompt_production_categories(content_text):
    sys_prompt = "You are an expert in screenplay analysis and production planning. "
    prompt1 = f"""
        Given a screenplay scene in JSON format, extract and categorize production-related elements into the following predefined categories: CAST, CAST INFO, 
        EXTRAS, PROPS, LOCATION DETAILS,\SCREEN TITLES, CAMERA, SOUND, LIGHTS, ELECTRICS, STUNTS, MUSIC, 
        COSTUMES, MAKEUP, HAIR, VEHICLES,ANIMALS, NUDITY, GREENERY, SET, SET DRESSING, CONSTRUCTION, SCENE DETAILS, MECHANICAL FX, 
        OPTICAL FX, VISUAL FX, SOUND FX, SPECIAL FX, SPECIAL EQUIPMENT, MISC.
        Your task is to analyze the scene's slugline, action lines, dialogue, transitions, and 
        superimpose fields to identify and assign relevant elements to these categories.
        **Input Scene JSON**:
        ```json
        {content_text}
        ```
        **Instructions**:
        1. Analyze the provided JSON scene, including slugline, action lines, dialogue, transitions, and superimpose fields.
        2. Extract and categorize elements into the specified production categories based on the scene's content:
        - **CAST**: Named characters appearing in the scene (e.g., SURESH, mute BUM).
        - **CAST INFO**: Specific details about characters (e.g., descriptions, roles, or traits like "mute").
        - **EXTRAS**: Background or non-speaking characters (if mentioned).
        - **PROPS**: Physical objects used in the scene (e.g., chillams, radio, mannequin torso).
        - **LOCATION DETAILS**: Specific details about the setting (e.g., platform, tree, ruined temple state).
        - **SCREEN TITLES**: Text overlays like superimpose (e.g., "2009.").
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
        - **SET**: Set pieces or structures (e.g., platform, ruined temple).
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

def get_llm_response(content_text):
    prompt, sys_prompt = get_prompt_structure_recognition(content_text)
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {"role": "system", "content": sys_prompt},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    answer = response.choices[0].message.content
    # print(answer)
    final_response = []
    formattted_res = extract_and_save_json(answer)
    scenes_data = formattted_res.get('scenes', [])
    for scene_ in scenes_data:
        scene_number = scene_.get('scene_number', 'temp_scene')
        scene_result = {'scene_number': scene_number, "structure_recognition":scene_}
        prompt2, sys_prompt2 = get_prompt_production_categories(scene_)
        print('@@@@@@@@@@@@@@@@@@@@')
        production_categories_response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {"role": "system", "content": sys_prompt2},
                {
                    "role": "user",
                    "content": prompt2
                }
            ]
        )
        production_categories_response = production_categories_response.choices[0].message.content  
        production_categories_response = extract_and_save_json(production_categories_response)
        scene_result['production_categories'] = production_categories_response
        print('production_categories_response:', production_categories_response)
        final_response.append(scene_result)
    return answer, formattted_res, final_response