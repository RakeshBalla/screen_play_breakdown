
from inltk.inltk import get_embedding_vectors
text = 'ਜਿਹਨਾਂ ਤੋਂ ਧਾਤਵੀ ਅਲੌਹ ਦਾ ਆਰਥਕ'
# vectors = get_embedding_vectors(text, 'hi')# // where text is string in <code-of-language>
# setup('<code-of-language>')
from inltk.inltk import setup
setup('hi')

vectors = get_embedding_vectors('भारत', 'hi')
print(vectors[0].shape)

exit('OLLLLLLLL')

# get_embedding_vectors('ਜਿਹਨਾਂ ਤੋਂ ਧਾਤਵੀ ਅਲੌਹ ਦਾ ਆਰਥਕ','pa')
# # [array([-0.894777, -0.140635, -0.030086, -0.669998, ...,  0.859898,  1.940608,  0.09252 ,  1.043363], dtype=float32), array([ 0.290839,  1.459981, -0.582347,  0.27822 , ..., -0.736542, -0.259388,  0.086048,  0.736173], dtype=float32), array([ 0.069481, -0.069362,  0.17558 , -0.349333, ...,  0.390819,  0.117293, -0.194081,  2.492722], dtype=float32), array([-0.37837 , -0.549682, -0.497131,  0.161678, ...,  0.048844, -1.090546,  0.154555,  0.925028], dtype=float32), array([ 0.219287,  0.759776,  0.695487,  1.097593, ...,  0.016115, -0.81602 ,  0.333799,  1.162199], dtype=float32), array([-0.31529 , -0.281649, -0.207479,  0.177357, ...,  0.729619, -0.161499, -0.270225,  2.083801], dtype=float32), array([-0.501414,  1.337661, -0.405563,  0.733806, ..., -0.182045, -1.413752,  0.163339,  0.907111], dtype=float32), array([ 0.185258, -0.429729,  0.060273,  0.232177, ..., -0.537831, -0.51664 , -0.249798,  1.872428], dtype=float32)]
# vectors = get_embedding_vectors('ਜਿਹਨਾਂ ਤੋਂ ਧਾਤਵੀ ਅਲੌਹ ਦਾ ਆਰਥਕ','pa')
# a = len(vectors)

# exit('PLL')
from inltk.inltk import predict_next_words
from inltk.inltk import setup
setup('hi')

text = 'गीक्स फॉर गीक्स एक बेहतरीन टेक्नोलॉजी'
n=3
predict_next_words(text , n, 'hi')


from inltk.inltk import get_embedding_vectors
from warnings import filterwarnings
from IPython.display import display
filterwarnings("ignore")

text = 'गीक्स फॉर गीक्स एक बेहतरीन टेक्नोलॉजी लर्निंग प्लेटफॉर्म है।'
vectors = get_embedding_vectors(text, 'hi')
display(vectors)