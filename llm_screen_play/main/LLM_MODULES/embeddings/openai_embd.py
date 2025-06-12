import openai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Set your OpenAI API key

import openai
open_ai_key = "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"

# Set your OpenAI API key
openai.api_key = open_ai_key  # Replace with your actual key


# # Call the text-embedding-3-small model
# response = openai.embeddings.create(
#     model="text-embedding-3-small",
#     input=sentence1
# )

# # Extract the embedding
# embedding_vector = response.data[0].embedding
# print("Embedding vector length:", len(embedding_vector))
# print("First 10 values:", embedding_vector[:10])



sentence1 = """
        1st year class room lo Nani ni teacher gaa choopincham. Nani
        class loki raagaane students andharu silent, dull ayipoyaaru.
        STUDENTS
        Enti sir eeroju kooda class ah?
        Ani andharu arusthunnaru gola gaa...
        NANI
        Nenu meeku cheppaboyedhi Maths
        class kaadhu, dhanikantey important
        class. Okasaari aa notebook ivvu!
        Ani adagaganey oka student thana notebook ni ichaaru. Aa
        pusthakam lo nunchi oka thella Kaagithaanni chinchi, dhanni
        students ki choopisthu...
        Idhenti?
        NANI (CONT’D)
        Ani adigadu...
        STUDENT 1
        Thella kaagitham sir.
        No..!
        NANI
        STUDENT 2
        White paper sir.
        NANI
        Idhi white paper kaadhu..idhi mee
        life!
        Andharu okka saarigaa class theesukunnaadanna chiraaku nunchi
        kothadhedho cheppabothunnadu anna aathrutha tho vinadam
        modhalupettaaru,
        NANI (CONT’D)
        Meeru vinnadhi correct ey, ee
        intermediate stage anedhi edhaithe
        undho adhi pure gaa, clean gaa unna
        thella kaagitham laantidhi.
    """

sentence2 = """
        ippudu meerandharu em
        chusthunnaaru? Aa Red machcha
        maathramey kanapaduthundhi,
        migilinadhantha mayamayipothundhi.
        White gaa unnantha varake dheeniki
        value, dheeni meedha oka red
        machcha padindhi anukondi,
        dheeniki inka value undadhu. Ikkada
        Red ante thappu. Teenage chedunu
        aakarshisthundhi. Ee vayasulo
        evaraina edhaina cheyoddhu ante
        chestharu! Choododdhu ante
        choostharu! Velloddhu ante
        velthaaru!
        Andharu vintunnaru...
        NANI (CONT’D)
        Meeru edhaina chese mundhu okatiki
        padhi sarlu idhi thappaa kaadha ani
        alochinchandi. Thella kaagitham la
        Inter lo adugupettina meeru adhe
        thella Kaagitham la bayatapadithe
        mee life happy gaa untundhi. Alaa
        kaakunda edhaina Red machcha
        padindhi ante dhaani effect
        lifelong vuntundhi.
        Ventane pakka nundi oka Bus velthunna shabdham
        vinapaduthundhi. Andharu vintunnaru.
        NANI (CONT’D)
        Idhi nenu cheppina class kaadhu,
        maa intermediate lo naaku Madhava
        rao master ani oka aayana
        cheppaaru. Nenu cheppe Maths class
        kanna meeku idhe important.
        Nani white paper theesi table meedha pettaadu. Pillalandharu
        shraddhagaa vinnaaru. Nani Class complete chesi bayataki
        velthunte oka abbayi cheyyi pattukunnaadu.
        STUDENT
        Sir, naa jeevitham lo red macha
        """


sentence3 = """
    amu chethilo andharu 20 roopayilu pettaaru...okadu dabbulu
    isthu...
    OKADU
    Uchhala poti lo ninnu kottevaade
    ledu raa, kaani edho oka roju ninnu
    odisthaa.
    RAMU
    Nannu..Nuvvu..
    Ani navvi, Shiva dull gaa undadam chusi...
    RAMU (CONT’D)
    Entraa alaa ayipoyaav?
    SHIVA
    Naa rendu roopayilu poyaayi
    kadhaa...!
    RAMU
    Rey Shiva... manam best friends
    raa...! Nenu gelisthey nuvvu
    gelichinattu! Idhigo neeku sagam…
    naaku sagam! Padha school ki time
    avthundhi.
    Shiva happy reaction.
"""

sentence4 = """
INT. GNANASARASWATHI TEMPLE - DAY
Lopala pradhakshanalu chesthunna shots.
SHIVA
Rey bava ee gullo pradakshanalu
chesthe baagaa chaduvastaadhani
entha mandhi moddhulu Vachhaaro
chudaraa.
Ani laavuga unna oka ammayini chupisthu,
SHIVA (CONT’D)
Aa Shashikala ni chudu, adhi
pradakshanalu kaadhu kadhaa porlu
dhandaalu pettina dhaaniki chadhuvu
raadhu.
RAMU
Oorukoraa vintaaru!
CUT:
3C
EXT. GNANASARASWATHI TEMPLE - DAY
Iddharu bayatiki vachhaaru, Shiva gaadu aadi naalugu cup la
carriage teesukoni Ramu dhaggariki vachhi,
SHIVA
Entra vethukuthunnaav?
RAMU
Naa box ikkade pettaanu,
ekkadundhi?
Ani dhooranga unna thana box ni chusi box teesukunnaadu.
CUT:7.
3D
INT. SCHOOL CLASS ROOM-A SECTION - DAY
Zilla parishath unnatha paathashaala ane board meedha open
chesaam. Padho tharagathi A section ane class room lo open
chesthe students andharu kindha kurchunnaaru, Maths sir class
chepthu board meedha raasinavi explain chesthu,
SIR
Functions naalugu rakaalu...! Into
function, onto function, Common
function, one one function.
Andharu note chesukuntunnaaru.
SIR (CONT’D)
Andharu raasukunnaaru kadhaa.
Andharu okesaari,
STUDENTS
Raasukunnaam sir.
Board meedha cheripi students vaipu thirige sariki Shiva
padukovatam chusi ramu kangaaru ga
RAMU
Rey...Sir chusthunnaaru raa,
le raa.
Annaadu, Shiva lechi atu itu chusthu
"""


sentences = [sentence1, sentence2, sentence3, sentence4]
# Generate sentence embeddings from OpenAI
response = openai.embeddings.create(
    model="text-embedding-3-small",
    input=sentences
)

# Extract sentence embeddings
embeddings = [item.embedding for item in response.data]

# Function to find the most relevant sentence for a given question
def get_relevant_sentence(question, sentences, embeddings):
    # Get embedding for the question
    question_response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=[question]
    )
    question_embedding = np.array(question_response.data[0].embedding).reshape(1, -1)

    # Convert all sentence embeddings to numpy array
    sentence_embeddings = np.array(embeddings)

    # Compute cosine similarities
    similarities = cosine_similarity(question_embedding, sentence_embeddings)[0]

    # Get index of most similar sentence
    most_relevant_idx = np.argmax(similarities)
    return sentences[most_relevant_idx], similarities[most_relevant_idx]

# Example question
question = "1st year class room ki evaru vacharu , valla peru enti"

# Find relevant sentence
relevant_sentence, similarity_score = get_relevant_sentence(question, sentences, embeddings)

# Print results
print("Question:", question)
print("Most relevant sentence:", relevant_sentence)
print("Similarity score:", similarity_score)

# Optional: Display all sentence similarity scores
print("\nAll sentences and similarity scores:")
'''for i, sent in enumerate(sentences):
    sim = cosine_similarity(
        [np.array(response.data[0].embedding)],
        [embeddings[i]]
    )[0][0]
    print(f"Sentence {i+1}: {sent}")
    print(f"Similarity Score: {sim:.4f}")
    print()
'''