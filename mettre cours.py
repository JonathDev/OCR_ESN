# Module 1
def sentence_to_token(sentence):
    
    # Token list
    tokens = sentence.split(" ")
    #print(tokens)
    
    # Size of sentence
    size = len(tokens)
    #print(size)
    
    # End 
    return{'input_sentence': sentence,
           'tokens': tokens,
           'size': size}

# Module 2
def extract_token(tokens):
    
    start_token = tokens[0]
    #print(start_token)
    
    end_token = tokens[-1]
    #print(end_token)
    
    return{'start_token': start_token,
           'end_token': end_token}

# Module 3
from random import randint, sample
def random_tokens_to_sentence(tokens, size):
    
    random_sentence = sample(population=tokens, k=size)
    
    return{'random_sentence': random_sentence}

# Main
res_module1 = sentence_to_token(sentence="aujourd'hui il fait beau à Tours, et c'est l'anniversaire de Kaelig :) !!!!")
print(f"La phrase d'origine est : {res_module1['input_sentence']}")
print(f"La liste de tokens est : {res_module1['tokens']}")
print(f"La taille de la phrase est : {res_module1['size']}")

print('\n------------------------------\n')

res_module2 = extract_token(tokens=res_module1['tokens'])
print(f"Le premier token de la phrase est : {res_module2['start_token']}")
print(f"Le dernier token de la phrase est : {res_module2['end_token']}")

print('\n------------------------------\n')

res_module3 = random_tokens_to_sentence(tokens=res_module1['tokens'], size=res_module1['size'])
print(f"La phrase aléatoire est : {res_module3['random_sentence']}")
print('\n------------------------------\n')