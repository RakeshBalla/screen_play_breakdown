import json

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

def save_result(result, output_path):
    """Save the result to a JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4)

# Example text
input_text = """INT. MINISTER'S HOUSE - NIGHT
SUPERIMPOSE: 2016
The FOREST MINISTER is watching TV, which is playing a
commercial of CHINTHAN BABA's Cola-flavored Goumuutram. He is
flanked by VASU, who seems like he is waiting on the FOREST
MINISTER, but can't do anything about it.
FOREST MINISTER
Edi popularity roju roju ki ee
pichi janallo perigipotundi kani aa
pichodu maatram dorakatledhu.6.
VASU
Popularity peregadam to vaadilo
nijamgaane daivuni punindhi
anukuntunnaadu saar
FOREST MINISTER
Sarele vigraham dorikina taravaatha
vaadini sajeeva samaadhiloki
pampudhaam. Dabbu flow aagadu.
The FOREST MINISTER pulls out a his wallet and hands a purple
parchment - a brand new 2,000 rupee note.
FOREST MINISTER
Deeni valla mana jeevitaalu
maarutaayi...pub ki velli
ivvu...appude manaki kavaalsindhi
dorukuddhi...pani jagratta.
VASU is smiling and staring at the note.
VASU"""

# Process the text
result = process_input(input_text)

# Save the result
output_path = "output.json"
save_result(result, output_path)
print(f"Result saved to {output_path}")