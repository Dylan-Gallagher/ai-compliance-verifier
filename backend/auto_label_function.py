import pandas as pd 
import random
import string
import json
#Master entity dictionary. 
master_dict = {"ORG": 
            {"provider", "providers", "distributor", "deployer", "operator", "notifying authority", "conformity assessment body", "notified body", "market surveillance authority", "testing experimentation facilities", "researchers", "importer", "the Commission", "businesses", "government", "the Member states", "EU, Digital Europe Programme", "Horizon Europe", "SMEs", "start-ups", "notified bodies", "AI on demand platform", "microenterprises", "laboratories","accredited pursuant", "expert panels", "expert laboratories", "reference laboratories",  "the AI Office", "European Artificial Intelligence Board", "scientific panel", "scientific community", "advisory forum",  "EuroHPC Joint Undertaking***", "The Board", "national competent authorities", "standing sub-groups", "standing subgroup", "market surveillance authorities", "notifying authorities",  "Administrative Cooperation Group",  "(ADCO)", "the Commission", "international", "organisation", "High-Level Expert Group", "Union", "international organisations", "law enforcement", "cloud computing centres"},
            "PER": {"authorised representative", "competent authorities", "stakeholders", "malicious third parties", "representatives of the Member States", "natural persons", "learners", "teachers", "persons", "person"}, "DAT": {"training data", "validation data", "testing data", "input data", "biometric data", "special categories of personal data", "sensitive operational data", "high quality datasets", "high quality data", "health data", "datasets", "performance metrics", "text and data mining", "trade secrets", "confidential business information", "inputs", "machine-based", "sensitive personal data", "personal data"},
            "LOC": {"European digital innovation hubs", "Testing and Experimentation facilities"},
            "SYS": {"post-market monitoring system", "emotion recognition system", "biometric categorisation system", "remote biometric identification system", "real-time remote biometric identification", "post remote biometric identification system", "high-risk AI systems", "AI systems", "risk management system", "quality management system", "pre-training", "synthetic data generation", "fine-tuning", "conformity assessment", "AI system", "AI systems", "systems", "traditional software systems", "models", "infrastructure", "monitoring water pressure", "fire alarm controlling systems"},
            "ACT": {"placing on the market", "making available on the market", "putting into service", "substantial modification", "development", "data sharing", "training", "validation", "testing", "access to data", "provision of high-quality data", "bias detection", "bias correction", "post market monitoring", "automatic recording", "placed on the market", "put it into service", "evaluate", "interpretation of the outputs", "technical and scientific support", "conformity assessment", "integrate stakeholders", "effective implementation", "enforcement", "build up central expertise", "contribute stakeholder input", "contributing to guidance", "issuing opinions", "market evaluations", "prototyping activities", "generation of content", "documentation", "provision of information", "postmarket monitoring", "report to the relevant authorities", "developments", "inference", "predictions", "drafting", "recruitment", "employment", "workers management", "self-employment", "selection of persons", "promotion", "termination", "individual behaviour", "monitoring", "evaluation", "evaluating", "monitoring", "Failure", "malfunctioning"},
            "SPA": {"publicly accessible space", "European common data spaces", "European health data space", "digital single market**", "AI ecosystem", "virtual environments", "physical environments"},
            "STA": {"harmonised standard", "state of the art"},
            "ALG": {"AI", "Artificial Intelligence", "artificial intelligence", "biometric identification", "biometric verification", "profiling", "artificial intelligence algorithms", "system behaviour", "algorithms", "Components", "Algorithms", "componets"},
            "PRO": {"conformity assessment", "assessment", "evaluate", "human oversight measures", "governance framework", "democratic processes", "electoral processes", "data governance", "democratic processes", "legally binding requirements", "civic discourse", "programming approaches", "situations"},
            "HAR": {"reasonably foreseeable misuse",  "potential significantly negative effects","systemic risk", "the dissemination of illegal", "false, or discriminatory content", "false", "discriminatory content"},
            "MAR": {"CE marking of conformity", "CE marking"},
            "DOC": {"instructions for use", "common specification", "documentation", "Union harmonisation legislation"," Regulation (EU) 2017/745", "Regulation (EU) 2017/746", "Article 30 of Regulation (EU) 2019/1020", "Article 33 of Regulation (EU) 2019/1020", "regulation", "2019 Ethics Guidelines", "Union law", "Guidelines", "Charter", "Guidelines of HLEG", "regulation"},
            "ETH": {"human oversight", "transparency", "public interest", "non-discriminatory", "trustful", "accountable", "privacy-preserving", "secure", "transparent", "trustworthy", "institutional governance", "fundamental rights and freedoms of natural persons", "public interest", "traceability", "compliance", "safety", "health", "Cybersecurity", "data poisoning", "AI value chain", "transparency measures", "copyright and related rights", "model reliability", "model fairness", "model security",  "cybersecurity protection",  "transparency towards the public", "deep fakes", "Consent of subjects", "human agency", "oversight", "legal certainty", "safety", "privacy", "transparency", "diversity", "non-discrimination", "fairness", "environmental well-being", "accountability", "ethical principles", "coherent", "human-centric", "human dignity", "personal autonomy", "media literacy", "digital skills", "terms of the work", "personal traits", "characteristics", "contractual relationships", "high-risk", "career prospects", "livelihoods", "workers’ rights", "rights", "safety components", "risks", "physical integrity"}


            }

label2id  = {
            "O" :   0,
            "B-ORG":1,
            "B-PER":2,
            "B-SYS":3,
            "B-ACT":4,
            "B-SPA":5,
            "B-STA":6,
            "B-ALG":7,
            "B-PRO":8,
            "B-HAR":9,
            "B-MAR":10,
            "B-DOC":11,
            "B-ETH":12,
            "I-ORG":13,
            "I-PER":14,
            "I-SYS":15,
            "I-ACT":16,
            "I-SPA":17,
            "I-STA":18,
            "I-ALG":19,
            "I-PRO":20,
            "I-HAR":21,
            "I-MAR":22,
            "I-DOC":23,
            "I-ETH":24}

id2label = {
            0:"O",   
            1:"B-ORG",
            2:"B-PER",
            3:"B-SYS",
            4:"B-ACT",
            5:"B-SPA",
            6:"B-STA",
            7:"B-ALG",
            8:"B-PRO",
            9:"B-HAR",
            10:"B-MAR",
            11:"B-DOC",
            12:"B-ETH",
            13:"I-ORG",
            14:"I-PER",
            15:"I-SYS",
            16:"I-ACT",
            17:"I-SPA",
            18:"I-STA",
            19:"I-ALG",
            20:"I-PRO",
            21:"I-HAR",
            22:"I-MAR",
            23:"I-DOC",
            24:"I-ETH"}


USED_IDS = []

#I opted to go with a dictionary of sets rather than lists as they have a lookup time of O(1).
#changes all strings in set to lowercase 
def set_to_lower():
    for entity in master_dict.copy():
        strings = master_dict[entity]   
        for string in strings.copy():
            master_dict[entity].remove(string)
            master_dict[entity].add(string.lower())
            
            
def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

'''
This function searches every key in the dictionary and
then checks if the lower case version of the current string is in the set of that master entity.
If it finds a matching entity it will return it to the autolabel program, if not it will return false.
'''
def dict_search (ner_tags, curr_string, curr_index, prefix):
    for entity in master_dict:
        if curr_string.lower() in master_dict[entity]:
            tag = prefix + str(entity)
            ner_tags[curr_index] = tag
            return str(entity)
    return "false"
 
 #Takes in token, list of tokens, and index of token to be split 
 #splits tokens with brackets/punctuation/whatever else and makes those seperate tokens.    
def punc_split(token, tokens, index, startpunc,endpunc):
    
    last_element = token[len(token)-1]
    first_element = token[0]
    #Checks if this is the root of the word
    root = True
    
    if first_element in ('(', '[', '{') and token not in ('(', '[', '{'):
        root = False
        startpunc +=1
        punc_split(token[1:len(token)], tokens, index, startpunc, endpunc)
        tokens.insert (index, first_element)
    if last_element in (',', ';', ':', ')', ']', '}') and token not in (',', ';', ':', ')', ']', '}') and root == True:
        root = False
        tokens.insert(index+1, last_element)
        punc_split(token[0:len(token)-1], tokens, index,startpunc, endpunc)
        
    if root == True:
        tokens[index] = token 
        
    return tokens
    
#This function works on the scale of a sentence it splits the sentence into tokens using space as the delimeter then assigns NER tags to each token
def auto_label(sentence):
    tokens = sentence.split()
    ner_tags = []
    
    #Splitting punctuation into seperate words for the sake of cleaner training data
    for token in tokens:
        ner_tags.append(0)
        #Filling Ner_tag array, since labelling function relies on tokens having a default ner_tag value 
        tokens = punc_split(token, tokens, tokens.index(token), 0, 0)
    
    #Labelling loop
    for index in range (len(tokens)):
        #Loop that checks if ner_tag at the current token index == 0, if it is then run label, if not then skip
        if ner_tags[index] == 0:
            label(tokens, ner_tags, index, index, "" )
    return_list = []
    return_list.append(tokens)
    return_list.append(ner_tags)
    
    return return_list
        
'''
Recursive labelling function, 
it takes in the list of tokens, ner tags, current index and starting index along with the current string
It passes up the current string + the string stored in the current index of the tokens list 
then recursively calls itself on the next index of the tokens list until it reaches the end
by that point current string + string will be the start index + the rest of the sentence following it
the search_dict function is then called and attempts to match the current_string, if it cannot do so "false"
is returned which is received by the iteration of the function that called it, 
that function then itself attempts to match it's current string 
which would be from the start index to the current_index (rest of the sentence - 1 token)
if the match is found dict_search returns the entity name and the function recursively adds "I-" to it
returning to the start index which will add "B-" and finally return
if the match is not found even after solely the token in the start index is searched it will label itself as "O"
'''

def label(tokens, ner_tags, curr_index, start_index, curr_string):
    prefix = ""
    #Adding new word onto old one
    string = tokens[curr_index]
    if curr_index >= 511:
        return "false"
    #If starting word then the full string is equal to the word
    if curr_index == start_index:
        curr_string = string
        #Prefixes based on whether its the beginning of an entity
        prefix = "B-"
         
    else:
        curr_string += " " + string
        prefix ="I-"
        
    next_index = curr_index +1
    
    if next_index < len(tokens):
        found_match = label(tokens, ner_tags, next_index, start_index, curr_string)
    else:
        found_match = dict_search (ner_tags, curr_string, curr_index, prefix)
        if curr_index == start_index:
            if found_match == "false":
                tag = "O"
            else:
                tag = prefix + found_match          
            ner_tags[curr_index] = tag
        return found_match
    
    if found_match != "false":
        tag = prefix + found_match          
        ner_tags[curr_index] = tag
        return found_match      
    else:
        tag = dict_search (ner_tags, curr_string, curr_index, prefix)
        if curr_index != start_index:
            return tag
        else: 
            if tag == "false":
                ner_tags[curr_index] = "O"
            
            
def paragraph_to_labeled_sentences(paragraph):
    sentences = paragraph.split(".")
    for i in range(len(sentences)):
        sentences[i] = sentences[i].lstrip()
    tokens_list = []
    tags_list = []
    #Needed when returning ints e.g training data.
    int_tags_list = []
     
    for sentence in sentences:
        #for the sake of context length and not hitting the recursion limit because the punctuation in the AI act draft is unique to say the least.
        if len(sentence) >= 511:
            
            long_sentence = ' '.join([str(word) for word in sentence])
            split_sentences = str(long_sentence.split(','))
            sentences += split_sentences
            
        return_list = auto_label(sentence)
        tokens_list.append(return_list[0])
        tags_list.append(return_list[1])
                
      #lines needed for functionality when an int output is needed (e.g hugging face training data)
      #for tag in return_list[1]: 
          # int_tags.append(label2id.get(tag))
      #int_tags_list.append(int_tags)
            
                
    
    return tokens_list, tags_list, sentences


def label_studio_format(tokens_list, tag_lists, sentences):
    
    start = 0;
    end = 0;
    text = "";
    label = ""; 
    output = "";
    entity = False
    sentence_index = 0;
    
 
    for sentence in sentences:
        output += f"""{{  
  "data": {{
  "text": "{sentence}"
  }},
    "predictions": [{{
      "result": ["""
        
        tag_list = tag_lists[sentence_index]    
        index = 0
        entity = False
        
        for index in range (len(tag_list)):
            tag = tag_list[index]

            if tag[0] == "B":
                id = get_random_string(10)
                start = sentence.find(tokens_list[sentence_index][index])
                label = tag[2:len(tag)]
                end =  start + len(tag)
                text = tokens_list[sentence_index][index]
                index +=1
                if index < len(tag_list):
                    curr_tag = tag_list[index]
                entity = True
                
                
                while(curr_tag[0] == "I" and index < len(tag_list)):    
                    
                    text = text + " " + tokens_list[sentence_index][index]
                    end = end + len(curr_tag)
                    index+=1
                    if index < len(tag_list):
                        curr_tag = tag_list[index]

            
                output += f"""            
      {{
        "value": {{
          "start": {start},
          "end": {end},
          "text": "{text}",
          "labels": [
          "{label}"
          ]
        }},
          "id": {id},
          "from_name": "label",
          "to_name": "text",
          "type": "labels",
          "origin": "manual"
        }},"""
                    
                index +=1
        if entity:
                output += """  
         ]
   }]
}, 
  """
        sentence_index +=1
    output = "[" + output + "]"
    
    return output


def is_alphanumeric_without_hyphen(word):
    return (word.replace('-', '').replace('/', '').replace('\\', '').isalnum())

def get_character_index(word_list, target_word_index):
    if target_word_index < 0 or target_word_index >= len(word_list):
        return -1  # Invalid index


    character_index = 0
    for i in range(target_word_index):
        word = word_list[i]
        if word.isalnum():  # If the word contains only alphanumeric characters
            character_index += len(word) + 1
        elif (("-" in word or "/" in word or "\\" in word) and is_alphanumeric_without_hyphen(word)):
            character_index += len(word) + 1
        else:
            character_index += len(word)  # Add the length of the punctuation or bracket

    return character_index


def better_studio(tokens_list, tag_lists, sentences):
    output = []
    i = 0
    for i in range(len(sentences)):
        output.append({})
        output[len(output) - 1]["id"] = 2
        output[len(output)-1]["data"] = {"text" : sentences[i]}
        # if ("environments and to a capability of AI systems to derive models and/or algorithms from " in sentences[i]):
            # print("A")
        output[len(output) - 1]["predictions"] = [{}]

        entity_starts = []
        for j in range(len(tag_lists[i])):
            if tag_lists[i][j][0] == "B":
                entity_starts.append(j)

        output[len(output) - 1]["predictions"][0]["result"] = []
        if (len(entity_starts) == 0):
            break


        for k in range(len(entity_starts)):
            output[len(output) - 1]["predictions"][0]["result"].append({})
            output[len(output) - 1]["predictions"][0]["result"][k]["value"] = {}
            span = 0

            next_tag_index = entity_starts[k] + 1
            while next_tag_index < len(tag_lists[i]) and (tag_lists[i][next_tag_index][0] == "I"):
                next_tag_index += 1
            span = (next_tag_index-1) - entity_starts[k]
            start_index = get_character_index(tokens_list[i], entity_starts[k])

            output[len(output) - 1]["predictions"][0]["result"][k]["value"]["start"] = start_index

            end_index = get_character_index(tokens_list[i], entity_starts[k])
            for l in range(span+1):
                end_index += len(tokens_list[i][entity_starts[k] + l])
            end_index += span #Counting spaces
            output[len(output) - 1]["predictions"][0]["result"][k]["value"]["end"] = end_index
            output[len(output) - 1]["predictions"][0]["result"][k]["value"]["text"] = sentences[i][start_index:end_index]
            output[len(output) - 1]["predictions"][0]["result"][k]["value"]["labels"] = [tag_lists[i][entity_starts[k]].replace("B-", "")]

            id = get_random_string(16)
            while id in USED_IDS:
                id = get_random_string(16)
            USED_IDS.append(id)
            output[len(output) - 1]["predictions"][0]["result"][k]["id"] = id
            output[len(output) - 1]["predictions"][0]["result"][k]["from_name"] = "label"
            output[len(output) - 1]["predictions"][0]["result"][k]["to_name"] = "text"
            output[len(output) - 1]["predictions"][0]["result"][k]["type"] = "labels"
            output[len(output) - 1]["predictions"][0]["result"][k]["origin"] = "auto"


    return output





def filter_text(text):
    oldlen = len(text)
    newlen = oldlen -1
    while newlen < oldlen:
        oldlen = newlen
        text = text.replace("  ", " ")
        newlen = len(text)
    return text

set_to_lower()



#Reads from the ai act parsed by Dylans parsing function.              
with open ("ai_act/ai-act.txt", "r", encoding='utf-8') as ai_act:
    full_text = ai_act.read()
    full_text = filter_text(full_text)
    paragraphs = full_text.split("\n")
    for i in range(len(paragraphs)):
        paragraphs[i] = paragraphs[i].replace("\n", "")
        while len(paragraphs[i]) != 0 and (paragraphs[i][0] == " "):
            paragraphs[i] = paragraphs[i][1:]

    i = 0
    output_list = []
    for paragraph in paragraphs:
        if (paragraph != ""):
            token_list, tags_list, sentences = paragraph_to_labeled_sentences(paragraph)
            output_list = output_list + better_studio(token_list, tags_list, sentences)
        
    # Outputs the tokens and ner tags into training data jsonl
    with open(f'training-data-final.json', mode='w') as json_file:
        json.dump(output_list, json_file, indent=4)
    i+=1
