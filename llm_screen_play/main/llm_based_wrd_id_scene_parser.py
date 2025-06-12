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

def get_prompt_structure_recognition_with_wordids(content_text, word_ids):
    sys_prompt = "You are an expert screenplay parser. Given the input screenplay text and a word ID mapping, parse and structure the content into a JSON object, accurately identifying and categorizing the following elements, and include word IDs for each extracted value:"
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

        **Input**:
        ```json
            {{
            "all_text": "{content_text}",
            "word_ids": {word_ids}
            }}
        ```

        **Instructions**:
        1. Parse the screenplay text from `all_text` and produce a structured JSON output.
        2. For each extracted value (e.g., scene number, slugline components, action lines, dialogue, etc.), include:
        - `value`: The extracted text (e.g., "EXT.", "RUINED TEMPLE", dialogue text).
        - `index_value`: A list of word IDs from the `word_ids` dictionary corresponding to each word in the value. For multi-word values, include IDs for each word. If a word is not found in `word_ids`, use `null` for its ID.
        3. For each scene (identified by scene number and slugline), create a JSON object containing:
        - Scene number (with `value` and `index_value`)
        - Scene heading details (type, location, time of day, each with `value` and `index_value`)
        - Action lines (list of objects with `value` and `index_value`)
        - Dialogue blocks (including character name, extensions, parentheticals, and dialogue text, each with `value` and `index_value`)
        - Transitions (list of objects with `value` and `index_value`)
        - Shot directions (if any, with `value` and `index_value`)
        - Superimpose (if any, with `value` and `index_value`)
        4. Ensure dialogue is correctly associated with the respective character.
        5. Handle any non-English dialogue accurately, preserving the original text and mapping to word IDs if available.
        6. If an element (e.g., parentheticals, shot directions, superimpose) is not present, omit it from the JSON for that scene.
        7. Ensure the output is valid JSON with clear, consistent formatting.

        **Output Format**:
        ```json
            {{
            "scenes": [
                {{
                "scene_number": {{
                    "value": [<number>],
                    "index_value": [<number|null>]
                }},
                "slugline": {{
                    "type": {{
                    "value": [<string>],
                    "index_value": [<number|null>]
                    }},
                    "location": {{
                    "value": [<string>],
                    "index_value": [<number|null>, ...]
                    }},
                    "time_of_day": {{
                    "value": [<string>],
                    "index_value": [<number|null>, ...]
                    }}
                }},
                "action_lines": [
                    {{
                    "value": [<string>],
                    "index_value": [<number|null>, ...]
                    }}
                ],
                "dialogue": [
                    {{
                    "character": {{
                        "value": [<string>],
                        "index_value": [<number|null>, ...]
                    }},
                    "extension": {{
                        "value": [<string|null>],
                        "index_value": [<number|null>, ...]
                    }},
                    "parenthetical": {{
                        "value": [<string|null>],
                        "index_value": [<number|null>, ...]
                    }},
                    "text": {{
                        "value": [<string|null>],
                        "index_value": [<number|null>, ...]
                    }}
                    }}
                ],
                "transitions": [
                    {{
                    "value": [<string|null>],
                    "index_value": [<number|null>, ...]
                    }}
                ],
                "shot_directions": [
                    {{
                    "value":[<string|null>],
                    "index_value": [<number|null>, ...]
                    }}
                ],
                "superimpose": [
                    {{
                    "value": [<string|null>],
                    "index_value": [<number|null>, ...]
                    }}
                ]
                }}
            ]
            }}
        ```
        Provide the parsed JSON output for the given screenplay text and word IDs.
            
            """
    return prompt1, sys_prompt

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

def get_prompt_production_categories(content_text, word_ids_json):
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
        6. For each extracted element in the categories, include:
            value: The extracted text (e.g., "SURESH", "chillams").
            index_value: A list of word IDs from the word_ids dictionary corresponding to each word in the value. For multi-word values, include IDs for each word. If a word is not found in word_ids, use null for its ID.
        **Output Format**:
        ```json

        {{
        "scene_number": {{
            "value": <number>,
            "index_value": [<number|null>]
        }},
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
        Note: Try Not to include the context of dialogue or Action Lines in the production categories or 
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


if __name__ == "__main__":
                                                                                                                        

    input_scene = {
        "all_text": """13 EXT. RUINED TEMPLE - NIGHTFADE IN.
                SUPERIMPOSE: 2009. On the edge of a platform in tattered,
                dishevelled rags, two bums, SURESH and a mute BUM, are
                smoking up using chillams and listening to the Gita on the
                radio. The mute BUM is slow-dancing against a female
                mannequin torso stuck in the middle of a tree.
                RADIO (V.O.)
                Jaatasya hi dhruvo martyurdhruvaam
                janma martasya cha
                tasmaadaparihaaryerthe na tvam
                sochitumarhasi. Puttina vaaniki
                maranamu tappadhu. Maraninchina
                vaaniki janmamu tappadhu.
                Anivaaryamagu ee vishayamunu
                goorchi Sokimpa tagadhu.
                SURESH takes the radio and opens a compartment in the back.
                He takes out some weed from it, puts it in his chillam, and
                continues smoking up.
                CUT TO:""",
        "word_ids": {
            "13": 8492,
            "EXT.": 3201,
            "RUINED": 4058,
            "TEMPLE": 9750,
            "NIGHTFADE": 6274,
            "IN": 5120,
            "SUPERIMPOSE": 2749,
            "2009": 1478,
            "On": 8266,
            "the": 3109,
            "edge": 2302,
            "of": 4727,
            "a": 9195,
            "platform": 6083,
            "in": 1002,
            "tattered": 3394,
            "dishevelled": 6889,
            "rags": 2190,
            "two": 3952,
            "bums": 4463,
            "SURESH": 5717,
            "and": 9821,
            "mute": 1086,
            "BUM": 6137,
            "are": 1062,
            "smoking": 4090,
            "up": 9978,
            "using": 7134,
            "chillams": 2957,
            "listening": 7261,
            "to": 1174,
            "Gita": 5409,
            "on": 7451,
            "radio": 1463,
            "The": 6740,
            "slow-dancing": 3297,
            "against": 2223,
            "female": 3812,
            "mannequin": 9641,
            "torso": 7894,
            "stuck": 3533,
            "middle": 7259,
            "tree": 3657,
            "RADIO": 1870,
            "V.O.": 7127,
            "Jaatasya": 1628,
            "hi": 3015,
            "dhruvo": 5746,
            "martyurdhruvaam": 2253,
            "janma": 9490,
            "martasya": 6632,
            "cha": 1455,
            "tasmaadaparihaaryerthe": 5710,
            "na": 8473,
            "tvam": 4918,
            "sochitumarhasi": 6786,
            "Puttina": 3770,
            "vaaniki": 1184,
            "maranamu": 9323,
            "tappadhu": 8125,
            "Maraninchina": 8321,
            "janmamu": 9300,
            "Anivaaryamagu": 2387,
            "ee": 2779,
            "vishayamunu": 6150,
            "goorchi": 8530,
            "Sokimpa": 6242,
            "tagadhu": 5086,
            "takes": 5634,
            "radio": 6321,
            "opens": 3709,
            "compartment": 7628,
            "back": 3310,
            "He": 2897,
            "out": 7981,
            "some": 1722,
            "weed": 3249,
            "from": 9205,
            "it": 4130,
            "puts": 2793,
            "his": 4836,
            "chillam": 1604,
            "continues": 4582,
            "CUT": 7997,
            "TO": 2166
        }
    }
    # prompt, sys_prompt = get_prompt_structure_recognition(input_scene['all_text'])#, input_scene['word_ids'])
    prompt, sys_prompt = get_prompt_production_categories(input_scene['all_text'], input_scene['word_ids'])
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
    print('formattted_res:', formattted_res)