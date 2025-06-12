import os
import uuid
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core import PromptTemplate
import logging
from datetime import datetime
import time


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set OpenAI API key
open_ai_key = "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"
os.environ["OPENAI_API_KEY"] = open_ai_key
pdf_file_path = "/home/ntlpt19/Downloads/Ak_For_Testing-current_draft_2024-07-23_5_26pm.pdf"

# gpt_model = "gpt-4o-mini-2024-07-18"
# gpt_model = "gpt-4.1-mini-2025-04-14"
gpt_model = "gpt-4.1-nano-2025-04-14"
# gpt_model = "gpt-4o-2024-11-20"

# Define prompts
#summary need to have scean number also
SUMMARY_PROMPT1 = PromptTemplate(
    """You are a screenwriting analysis assistant tasked with generating a detailed, scene-wise summary of the provided screenplay chunk for 'Thella Kaagitham.' The chunk is written in Tinglish (Telugu language represented using English words and script, e.g., 'Andharu Asha body ni paadi meedha ethukuni smasaanaaniki velthunte' meaning 'Everyone is carrying Asha's body on a bier to the cremation ground'). Interpret the Tinglish text as Telugu dialogue or descriptions and summarize it in clear, standard English in approximately {word_limit} words. Ensure a comprehensive breakdown of all scenes or logical narrative segments within the chunk, capturing every critical element without omitting anything essential.

    **Guidelines for the Summary:**
    - **Tinglish Interpretation**: Treat the input as Telugu language written in English script. Translate and interpret the dialogue and descriptions into standard English, preserving the intended meaning, tone, and context. For example, 'Andharu Asha body ni paadi meedha ethukuni smasaanaaniki velthunte' should be understood as 'Everyone is carrying Asha's body on a bier to the cremation ground.'
    - **Scene-Wise Breakdown**: Divide the chunk into individual scenes or logical narrative segments based on shifts in location, time, or action. For each scene/segment:
        - Assign a descriptive title in English (e.g., 'Scene 1: Asha's Funeral Procession').
        - Summarize the key events, character interactions, and narrative progression in standard English.
        - Highlight main characters involved, their motivations, and any development in their arcs.
        - Note significant themes, tonal shifts, or emotional beats (e.g., grief, tension, hope).
        - Include notable dialogue (translated into standard English) or action lines that drive the story or reveal character.
        - Specify the setting and its relevance to the scene (e.g., cultural or emotional significance).
    - **Comprehensiveness**: Ensure no major plot points, characters, themes, settings, or other critical details are missed. Capture subtext, foreshadowing, or cultural nuances (e.g., Telugu traditions) explicitly.
    - **Word Limit**: Distribute the {word_limit} words across scenes to balance detail and conciseness, prioritizing clarity and completeness.
    - **Structure**: Present the summary as a numbered or bulleted list of scenes/segments for clarity, with each entry clearly labeled and detailed in standard English.
    - **Context**: If the chunk references earlier or later parts of the screenplay, note any implied connections or unresolved elements.
    - **Avoid Misinterpretation**: Do not respond with messages like 'I can't continue the text.' Instead, focus on generating a complete, accurate summary based on the provided Tinglish input.

    Screenplay Chunk:
    {chunk_text}
    """
)

SUMMARY_PROMPT2 = PromptTemplate(
    """You are a screenwriting analysis assistant tasked with generating a detailed, scene-wise summary of the provided screenplay chunk for 'Thella Kaagitham.' The chunk is written in Tinglish (Telugu language represented using English words and script, e.g., 'Andharu Asha body ni paadi meedha ethukuni smasaanaaniki velthunte' meaning 'Everyone is carrying Asha's body on a bier to the cremation ground'). Interpret the Tinglish text as Telugu dialogue or descriptions and summarize it in clear, standard English in approximately {word_limit} words. Ensure a comprehensive breakdown of all scenes or logical narrative segments within the chunk, capturing every critical element without omitting anything essential.

    **Guidelines for the Summary:**
    - **Tinglish Interpretation**: Treat the input as Telugu language written in English script. Translate and interpret the dialogue and descriptions into standard English, preserving the intended meaning, tone, and context. For example, 'Andharu Asha body ni paadi meedha ethukuni smasaanaaniki velthunte' should be understood as 'Everyone is carrying Asha's body on a bier to the cremation ground.'
    - just summarise the context in english
    Screenplay Chunk:
    {chunk_text}
    """
)

SUMMARY_PROMPT3 = PromptTemplate(
    """You are a screenwriting analysis assistant tasked with generating a detailed, scene-wise extractive summary of the provided screenplay chunk for 'Thella Kaagitham.' The chunk is written in Tinglish (Telugu language represented using English words and script, e.g., 'Andharu Asha body ni paadi meedha ethukuni smasaanaaniki velthunte' meaning 'Everyone is carrying Asha's body on a bier to the cremation ground'). Your task is to identify the key sentences in each scene that capture the essential plot points, dialogue, and descriptions, translate them directly into standard English, and present them as the summary for that scene. Ensure that you cover all scenes or logical narrative segments within the chunk, capturing every critical element without omitting anything essential.

**Guidelines for the Summary:**
- **Tinglish Interpretation**: Treat the input as Telugu language written in English script. Translate the selected key sentences directly into standard English, preserving the original wording as much as possible while ensuring grammatical correctness in English.
- **Scene Breakdown**: Divide the screenplay chunk into its constituent scenes or logical narrative segments. For each segment, list the translated key sentences that best represent the main actions, emotions, plot advancements, character dialogue, and important descriptions.
- **Comprehensiveness**: Ensure your summary includes all critical elements of each scene, such as plot developments, character actions, and significant dialogue.
- **Extractive Focus**: Prioritize selecting and translating actual sentences or phrases from the original text rather than generating new content. If no direct sentences are suitable, you may paraphrase minimally to ensure clarity while staying as close to the original as possible.

**Example of Tinglish Interpretation**:
- Original: 'Andharu Asha body ni paadi meedha ethukuni smasaanaaniki velthunte'
- Translation: 'Everyone is carrying Asha's body on a bier to the cremation ground'

**Note**:
- Make sure you have covered all the provided scenes.
- Depending on the input length, adjust the summarization scene by scene to ensure clarity and conciseness.
Screenplay Chunk:
{chunk_text}
"""
)

SUMMARY_PROMPT4 = PromptTemplate(
    """You are a screenwriting analysis assistant tasked with generating a detailed, scene-wise extractive summary of the provided screenplay chunk from a Movie. The chunk is written in Tinglish (Telugu language represented using English words and script, e.g., 'Andharu Asha body ni paadi meedha ethukuni smasaanaaniki velthunte' meaning 'Everyone is carrying Asha's body on a bier to the cremation ground'). Your task is to comprehensively cover **every scene or logical narrative segment** in the chunk by selecting and translating all key sentences into standard English, ensuring no critical plot points, dialogue, or descriptions are omitted. The summary will be used for subsequent coverage and plot hole analyses, so completeness is critical.

    **Guidelines for the Summary:**
    - **Tinglish Interpretation**: Treat the input as Telugu language written in English script. Translate all selected key sentences directly into standard English, preserving the original wording as much as possible while ensuring grammatical correctness and fidelity to the intended meaning, tone, and context.
    - **Comprehensive Scene Breakdown**: Identify and summarize **every scene or logical narrative segment** in the chunk. For each segment, extract and translate the most representative sentences that capture all essential elements, including plot developments, character actions, emotions, dialogue, and significant descriptions.
    - **Exhaustive Coverage**: Ensure the summary includes **all content** from the input chunk. Do not omit any scenes, plot points, or critical details, as the summary must provide a complete foundation for later coverage and plot hole reports.
    - **Extractive Focus**: Prioritize selecting and translating actual sentences or phrases from the original text rather than generating new content. If no direct sentences are suitable, minimally paraphrase to ensure clarity while staying as close to the original as possible.
    - **Structure**: Organize the summary by scenes or narrative segments, labeling each with a brief descriptive title (e.g., 'Scene 1: Asha's Funeral Procession'). List the translated key sentences for each segment, ensuring they collectively represent the full scope of the scene.

    **Example of Tinglish Interpretation**:
    - Original: 'Andharu Asha body ni paadi meedha ethukuni smasaanaaniki velthunte'
    - Translation: 'Everyone is carrying Asha's body on a bier to the cremation ground'
    
    
    **Output Format**:
    For each scene or segment:
    - **Scene/Segment Title**: [Descriptive title]
    - **Summary**: [Translated key sentences covering all critical plot points, dialogue, and descriptions]
                    
    Screenplay Chunk:
    {chunk_text}
    """
    )


SUMMARY_PROMPT = PromptTemplate(
    """You are a helpful assistant summarizing a movie screenplay written in Tinglish (Telugu written in English script). Read the given screenplay chunk carefully and summarize it **scene by scene**.

        **Instructions:**
        - Translate any important sentences from Tinglish to clear, simple English.
        - For each scene or major part of the story, give a **short but complete summary** that covers the main actions, emotions, and dialogues.
        - Make sure **no scene or event is skipped**. Cover everything briefly and clearly.

        **Output Format:**
        For each scene:
        - **Scene Title**: [Short title for the scene]
        - **Summary**: [8-10 brief sentences that explain what happens in this part]

        **Example Tinglish Line**:  
        - 'Andharu Asha body ni paadi meedha ethukuni smasaanaaniki velthunte'  
        - **Translated**: 'Everyone is carrying Asha's body on a bier to the cremation ground'

        Now, summarize the following:

        Screenplay Chunk:
        {chunk_text}
        """
        )


COVERAGE_PROMPT = PromptTemplate(
    """You are an AI-powered screenplay analyst tasked with generating a comprehensive coverage report for the screenplay from a Movie based on the provided chunk summaries. Follow the structure below, ensuring all sections are detailed, expressive, and insightful. Use the chunk summaries to infer the narrative flow and make informed decisions about dividing the story into distinct acts or segments.

    1. **Coverage Report Header Information:**
        * Screenplay Title: <Get Movie Name from Summary>
        * Writer(s): Unknown
        * Submitted By: Unknown
        * Form: Feature Screenplay
        * Pages: {page_count}
        * Created: {current_date}
        * Genre: Drama
        * Circa: Contemporary
        * Location: Unknown
        * Budget: Medium
        * Analyst: AJA Engine

    2. **Logline:**
        Craft a concise, compelling logline (1-2 sentences) that encapsulates the entire screenplay’s core conflict, stakes, and thematic essence.

    3. **Overall Impression:**
        Provide a vivid assessment of the screenplay’s strengths, weaknesses, thematic resonance, emotional impact, and any overarching issues. Paint a clear picture of the screenplay’s potential and challenges, using expressive language to convey its narrative and emotional weight.

    4. **Synopsis (Dynamic Act Breakdown):**
        Divide the screenplay into meaningful narrative segments (e.g., acts or key story phases) based on the chunk summaries, determining the structure dynamically to reflect the story’s natural progression. Assign descriptive titles to each segment (e.g., 'The Setup & Inciting Incident (Scenes 1-42)', 'Rising Action & First Major Complication (Scenes 43-62)') and provide an elaborate, detailed synopsis for each. Include:
        - Specific plot points, character arcs, and thematic developments.
        - Scene or page ranges (estimated based on chunk summaries).
        - Key turning points, conflicts, or emotional beats.
        Ensure the synopsis is comprehensive, capturing the full scope of the story’s evolution across all segments.

    5. **Comments (Detailed Analysis):**
        Provide an in-depth, expressive analysis for each of the following categories. Use vivid, specific language to explain observations, citing examples from the summaries where possible. Elaborate on what works, what doesn’t, and why, ensuring each point is thoroughly explored:
        - **Overall Theme/Core Idea**: Discuss the central theme and its execution, including its emotional and intellectual resonance.
        - **Character Development**: Analyze character arcs, motivations, and relatability, highlighting strengths and gaps.
        - **Conflict**: Evaluate the nature, intensity, and resolution of conflicts, both internal and external.
        - **Structure & Pacing**: Assess the narrative flow, act transitions, and pacing, noting any lulls or rushed moments.
        - **Plot Holes & Logic Gaps**: Identify inconsistencies or unresolved elements, explaining their impact.
        - **Tonal Consistency & Dialogue**: Examine tone shifts and dialogue authenticity, with examples of strengths or weaknesses.
        - **Thematic Coherence**: Evaluate how well the themes are woven throughout the narrative.
        - **Well-Roundedness**: Discuss the balance of characters, plot, and themes in creating a cohesive story.
        - **Cinematic Quality**: Analyze visual storytelling, imagery, and potential for cinematic adaptation.
        - **Formatting (General)**: Comment on adherence to screenplay formatting standards.
        - **Action Lines Externalization**: Assess how effectively action lines convey character emotions and story dynamics.
        - **Tense**: Evaluate consistency in narrative tense and its impact on immersion.

    6. **Market Potential:**
        - **Strengths**: Highlight elements that enhance commercial viability (e.g., unique premise, strong characters).
        - **Weaknesses**: Identify barriers to marketability (e.g., niche appeal, budget concerns).

    7. **Genre Fidelity:**
        Assess how well the screenplay adheres to or innovatively blends the Drama genre, citing specific elements that align with or deviate from genre expectations.

    8. **Ratings Grid:**
        Rate each category on a scale: 1ST CLASS, Solid, Not bad, Weak. Provide a brief justification for each rating:
        - Concept, Story, Structure, Protagonist, Antagonist, Stakes, Characters, Dialogue, Scenes, Pacing, Theme, Tone, Writing Style, Marketability, Formatting, Grammar, Title.

    9. **Script Recommendation:**
        Choose one: PASS, CONSIDER, RECOMMEND, DEVELOPMENT NEEDED. Justify the recommendation based on the analysis.

    10. **Final Thoughts and Suggestions:**
        Summarize the screenplay’s overall status and potential. Provide actionable, category-specific suggestions for improvement, structured as follows:
        - **Tonal Consistency**: Suggestions to enhance or maintain tone.
        - **Stronger Character Arcs**: Recommendations for deepening character development.
        - **Structural Refinements**: Ideas to improve pacing or narrative flow.
        - **Conflict Enhancement**: Ways to heighten stakes or clarify conflicts.
        - **Dialogue Polish**: Suggestions for more authentic or impactful dialogue.
        - **Thematic Clarity**: Recommendations to strengthen thematic resonance.
        - **Market Appeal**: Strategies to broaden commercial viability.
        Ensure each suggestion is specific, practical, and tied to the analysis.

    Screenplay Chunk Summaries:
    {chunk_summaries}
    """
)

PLOT_HOLE_PROMPT = PromptTemplate(
    """You are a screenwriting analysis assistant tasked with analyzing the provided screenplay chunk summaries from a Movie. to generate a comprehensive Plot Hole Report. Based on the narrative content in the summaries, dynamically identify and categorize plot holes or inconsistencies into relevant issue types (e.g., Narrative Issues, Character Issues, Logical Issues, Timeline Issues, Thematic Issues, Medical/Legal Inaccuracies, Convenient Coincidences, or other story-specific categories). Ensure the report is thorough, with strongly articulated, detailed explanations for each issue.

    **Structure of the Plot Hole Report:**
    For each identified issue, provide:
    - **Title**: A clear, descriptive name for the issue (e.g., "Unresolved Subplot in Act 2").
    - **Category**: Specify the type of issue (e.g., Narrative, Character, Logical, Timeline, Thematic, Medical/Legal, Coincidence, or a custom category relevant to the story).
    - **Description**: Provide an in-depth, expressive explanation of the issue, including:
        - **What the Issue Is**: Clearly describe the plot hole or inconsistency, referencing specific elements from the chunk summaries.
        - **Location**: Indicate where the issue appears (e.g., specific chunk, estimated scene/page range, or narrative segment).
        - **Impact**: Explain how the issue affects the story’s coherence, audience engagement, or emotional resonance, using vivid language to underscore its significance.
        - **Potential Fix**: Suggest a specific, actionable solution to address the issue, enhancing the narrative’s integrity.

    **Guidelines:**
    - Dynamically determine issue categories based on the content of the chunk summaries, ensuring relevance to the story’s unique structure and themes.
    - Prioritize significant issues that disrupt narrative flow, character credibility, or logical consistency.
    - Use strong, persuasive language to articulate why each issue matters and how it detracts from the screenplay’s quality.
    - If no issues are found in a category, explicitly state so and provide a brief justification.
    - Conclude with a brief overall assessment of the screenplay’s narrative integrity based on the identified issues.

    Screenplay Chunk Summaries:
    {chunk_summaries}
    """
)

def chunk_documents(documents, pages_per_chunk=50):
    """Chunk documents into groups of approximately 100 pages."""
    chunks = []
    current_chunk = []
    current_page_count = 0

    for doc in documents:
        # Estimate pages based on word count (assuming ~250 words per page)
        word_count = len(doc.text.split())
        estimated_pages = word_count // 250 + 1
        current_page_count += estimated_pages

        if current_page_count > pages_per_chunk and current_chunk:
            chunks.append({
                'text': '\n'.join([d.text for d in current_chunk]),
                'page_count': current_page_count - estimated_pages
            })
            current_chunk = [doc]
            current_page_count = estimated_pages
        else:
            current_chunk.append(doc)

    if current_chunk:
        chunks.append({
            'text': '\n'.join([d.text for d in current_chunk]),
            'page_count': current_page_count
        })

    return chunks


def generate_summary(chunk_text, word_limit):
    """Generate a summary for a chunk with dynamic word limit."""
    # llm = OpenAI(model=gpt_model)
    print('generate_summary >>>>>>>>>>>')
    llm = OpenAI(
        model=gpt_model,
        temperature=0.0,
        # max_tokens=word_limit,  # or 500 if you want a fixed size
        top_p=1.0,
        # frequency_penalty=0.5,
        # presence_penalty=0.5
    #     model_kwargs={
    #     "user": "Thella_Kaagitham"
    # }
    )
    # word_limit = 30000
    # print('word_limit >>>>>>>>>>>', word_limit)
    prompt = SUMMARY_PROMPT.format(chunk_text=chunk_text)#, word_limit=word_limit)
    model_start = time.time()
    response = llm.complete(prompt)
    total_duration = time.time() - model_start
    print(f"[{datetime.now()}] Time taken ==> {total_duration:.2f} seconds.")
    # print(response.text)
    return response.text

def generate_coverage_report(chunk_summaries, total_page_count):
    """Generate coverage report using chunk summaries."""
    print('generate_coverage_report >>>>>>>>>>>')

    llm = OpenAI(
        model=gpt_model,
        temperature=0.0,
        # max_tokens=word_limit,  # or 500 if you want a fixed size
        top_p=1.0,
        # frequency_penalty=0.5,
        # presence_penalty=0.5
    )
    current_date = datetime.now().strftime("%Y-%m-%d")
    prompt = COVERAGE_PROMPT.format(chunk_summaries=chunk_summaries, page_count=total_page_count, current_date=current_date)
    # Call Gemini-based LLM function
    model_start = time.time()
    response = llm.complete(prompt)
    total_duration = time.time() - model_start
    print(f"[{datetime.now()}] Time taken ==> {total_duration:.2f} seconds.")
    return response.text

def generate_plot_hole_report(chunk_summaries):
    """Generate plot hole report using chunk summaries."""
    print('generate_plot_hole_report >>>>>>>>>>>')

    llm = OpenAI(
        model=gpt_model,
        temperature=0.0,
        # max_tokens=word_limit,  # or 500 if you want a fixed size
        top_p=1.0,
        # frequency_penalty=0.5,
        # presence_penalty=0.5
    )
    prompt = PLOT_HOLE_PROMPT.format(chunk_summaries=chunk_summaries)
    model_start = time.time()
    response = llm.complete(prompt)
    total_duration = time.time() - model_start
    print(f"[{datetime.now()}] Time taken ==> {total_duration:.2f} seconds.")
    return response.text

def save_final_report(coverage_report, plot_hole_report):
    output_path1 = "final_screenplay_coverage_report.txt"
    output_path2 = "final_screenplay_plot_hole_report.txt"
    
    """Save the combined coverage and plot hole reports to a text file."""
    with open(output_path1, 'w', encoding='utf-8') as f:
        f.write("=== Final Screenplay Analysis Report ===\n\n")
        f.write("##Coverage Report\n")
        f.write(coverage_report)
    logger.info(f"Final report saved to {output_path1}")

    with open(output_path2, 'w', encoding='utf-8') as f:
        f.write("=== Final Screenplay Analysis Report ===\n\n")
        f.write("\n\n## Plot Hole Report\n")
        f.write(plot_hole_report)
    logger.info(f"Final report saved to {output_path2}")



def main():
    try:
        # Load PDF
        logger.info("Loading PDF...")
        documents = SimpleDirectoryReader(input_files=[pdf_file_path]).load_data()
        logger.info(f"Loaded {len(documents)} documents")

        # Chunk documents
        logger.info("Chunking documents...")
        chunks = chunk_documents(documents)
        logger.info(f"Created {len(chunks)} chunks")

        # Calculate dynamic word limit for summaries (e.g., aim for ~100-200 words per chunk)
        total_chunks = len(chunks)
        base_word_limit = 150
        word_limit = max(50, min(200, base_word_limit // max(1, total_chunks // 5)))  # Adjust based on chunk count

        # Generate summaries for each chunk
        chunk_summaries = []
        total_page_count = 0
        for i, chunk in enumerate(chunks):
            logger.info(f"Generating summary for chunk {i+1}/{len(chunks)}...")
            summary = generate_summary(chunk['text'], word_limit)
            chunk_summaries.append(f"Chunk {i+1} Summary ({chunk['page_count']} pages):\n{summary}")
            total_page_count += chunk['page_count']
            logger.info(f"Generated summary for chunk {i+1}")

        # Combine summaries
        combined_summaries = "\n\n".join(chunk_summaries)
        with open('combined_summaries.txt', 'w', encoding='utf-8') as f:
            f.write("=== Final Summaries ===\n\n")
            f.write(combined_summaries)

        # Generate final reports
        logger.info("Generating combined coverage report...")
        combined_coverage = generate_coverage_report(combined_summaries, total_page_count)
        logger.info("Generating combined plot hole report...")
        combined_plot_hole = generate_plot_hole_report(combined_summaries)

        # Save final report
        save_final_report(combined_coverage, combined_plot_hole)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()