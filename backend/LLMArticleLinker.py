from langchain_core.prompts import PromptTemplate
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_community.llms import HuggingFaceEndpoint
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFacePipeline
from langchain_community.vectorstores import FAISS
from huggingface_hub import login 
from transformers import AutoModelForCausalLM, BitsAndBytesConfig, AutoTokenizer,pipeline
import requests
from bs4 import BeautifulSoup

token=HFTOKEN #insert hugging face token here


login(token=token) 
model_name = HF_TOKEN #Insert hugging face token here if using endpoints

'''
Used for quantizing model if running locally.

bnb_config = BitsAndBytesConfig (  
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
)'''

#Few shot examples

examples = [

    {"input": """The controller shall facilitate the exercise of data subject rights under Articles 15 to 22. 2In the cases referred to in Article 11(2), the controller shall not refuse to act on the request of the data subject for exercising his or her rights under Articles 15 to 22, unless the controller demonstrates that it is not in a position to identify the data subject.
 """,
  "output": """ [""Article(15)" ,"Article(16)", "Article(17)", "Article(18)", "Article(19)", "Article(20)", "Article(21)"  "Article(22)", "Article (11)(2)"] """,},
    

       {"input": """1Information provided under Articles 13 and 14 and any communication and any actions taken under Articles 15 to 22 and 34 shall be provided free of charge. 2Where requests from a data subject are manifestly unfounded or excessive, in particular because of their repetitive character, the controller may either:
charge a reasonable fee taking into account the administrative costs of providing the information or communication or taking the action requested; or
refuse to act on the request.
3The controller shall bear the burden of demonstrating the manifestly unfounded or excessive character of the request.
 """,
  "output": """ ["Article(13)", "Article(14)", "Article(15)" ,"Article(16)", "Article(17)", "Article(18)", "Article(19)", "Article(20)", "Article(21)"  "Article(22)", "Article(34)" ]
  """,},
       
       {"input": """the tasks of any data protection officer designated in accordance with Article 37 or any other person or entity in charge of the monitoring compliance with the binding corporate rules within the group of undertakings, or group of enterprises engaged in a joint economic activity, as well as monitoring training and complaint-handling;
 """,
  "output": """ ["Article(37)"]
  """,},
       
      {"input": """Each supervisory authority shall be competent for the performance of the tasks assigned to and the exercise of the powers conferred on it in accordance with this Regulation on the territory of its own Member State.
1Where processing is carried out by public authorities or private bodies acting on the basis of point (c) or (e) of Article 6(1), the supervisory authority of the Member State concerned shall be competent. 2In such cases Article 56 does not apply.
Supervisory authorities shall not be competent to supervise processing operations of courts acting in their judicial capacity.
 """,
  "output": """ ["Article(6)(1)(c)", "Article(6)(1)(e)", "Article (56)"]
  """,},
      
      {"input": """to order the rectification or erasure of personal data or restriction of processing pursuant to Articles 16, 17 and 18 and the notification of such actions to recipients to whom the personal data have been disclosed pursuant to Article 17(2) and Article 19;
 """,
  "output": """ ["Article(16)", "Article(17)", "Article(18)", "Article(17)(2)", "Article(19)"]
  """,},
      
      {"input": """1The delegation of power referred to in Article 12(8) and Article 43(8) may be revoked at any time by the European Parliament or by the Council. 2A decision of revocation shall put an end to the delegation of power specified in that decision. 3It shall take effect the day following that of its publication in the Official Journal of the European Union or at a later date specified therein. 4It shall not affect the validity of any delegated acts already in force.
 """,
  "output": """ ["Article (12)(8)", "Article (43)(8)"]
  """,},
      
      {"input": """The Commission shall, on an ongoing basis, monitor developments in third countries and international organisations that could affect the functioning of decisions adopted pursuant to paragraph 3 of this Article and decisions adopted on the basis of Article 25(6) of Directive 95/46/EC.
 """,
  "output": """ ["Directive 95/46/EC Article 25(6)"]
  """,},
      
      {"input": """Without prejudice to Article 55, the supervisory authority of the main establishment or of the single establishment of the controller or processor shall be competent to act as lead supervisory authority for the cross-border processing carried out by that controller or processor in accordance with the procedure provided in Article 60.
 """,
  "output": """ ["Article(55)", "Article(60)"]
  """,},
      
          {"input": """In the absence of a decision pursuant to Article 45(3), a controller or processor may transfer personal data to a third country or an international organisation only if the controller or processor has provided appropriate safeguards, and on condition that enforceable data subject rights and effective legal remedies for data subjects are available.
The appropriate safeguards referred to in paragraph 1 may be provided for, without requiring any specific authorisation from a supervisory authority, by:
a legally binding and enforceable instrument between public authorities or bodies;
binding corporate rules in accordance with Article 47;
standard data protection clauses adopted by the Commission in accordance with the examination procedure referred to in Article 93(2);
standard data protection clauses adopted by a supervisory authority and approved by the Commission pursuant to the examination procedure referred to in Article 93(2);
an approved code of conduct pursuant to Article 40 together with binding and enforceable commitments of the controller or processor in the third country to apply the appropriate safeguards, including as regards data subjects’ rights; or
an approved certification mechanism pursuant to Article 42 together with binding and enforceable commitments of the controller or processor in the third country to apply the appropriate safeguards, including as regards data subjects’ rights.
Subject to the authorisation from the competent supervisory authority, the appropriate safeguards referred to in paragraph 1 may also be provided for, in particular, by:
contractual clauses between the controller or processor and the controller, processor or the recipient of the personal data in the third country or international organisation; or
provisions to be inserted into administrative arrangements between public authorities or bodies which include enforceable and effective data subject rights.
The supervisory authority shall apply the consistency mechanism referred to in Article 63 in the cases referred to in paragraph 3 of this Article.
1Authorisations by a Member State or supervisory authority on the basis of Article 26(2) of Directive 95/46/EC shall remain valid until amended, replaced or repealed, if necessary, by that supervisory authority. 2Decisions adopted by the Commission on the basis of Article 26(4) of Directive 95/46/EC shall remain in force until amended, replaced or repealed, if necessary, by a Commission Decision adopted in accordance with paragraph 2 of this Article.
 """,
  "output": """ ["Article (45)(3)", "Article (47)", "Article (93)(2)", "Article (40)", "Article (42)", "Article (63)", "Directive 95/46/EC Article 26(2)", "Directive 95/46/EC Article 26(4)"] """,},

{"input": """Where personal data relating to a data subject are collected from the data subject, the controller shall, at the time when personal data are obtained, provide the data subject with all of the following information:
the identity and the contact details of the controller and, where applicable, of the controller’s representative;
the contact details of the data protection officer, where applicable;
the purposes of the processing for which the personal data are intended as well as the legal basis for the processing;
where the processing is based on point (f) of Article 6(1), the legitimate interests pursued by the controller or by a third party;
the recipients or categories of recipients of the personal data, if any;
where applicable, the fact that the controller intends to transfer personal data to a third country or international organisation and the existence or absence of an adequacy decision by the Commission, or in the case of transfers referred to in Article 46 or 47, or the second subparagraph of Article 49(1), reference to the appropriate or suitable safeguards and the means by which to obtain a copy of them or where they have been made available.
In addition to the information referred to in paragraph 1, the controller shall, at the time when personal data are obtained, provide the data subject with the following further information necessary to ensure fair and transparent processing:
the period for which the personal data will be stored, or if that is not possible, the criteria used to determine that period;
the existence of the right to request from the controller access to and rectification or erasure of personal data or restriction of processing concerning the data subject or to object to processing as well as the right to data portability;
where the processing is based on point (a) of Article 6(1) or point (a) of Article 9(2), the existence of the right to withdraw consent at any time, without affecting the lawfulness of processing based on consent before its withdrawal;
the right to lodge a complaint with a supervisory authority;
whether the provision of personal data is a statutory or contractual requirement, or a requirement necessary to enter into a contract, as well as whether the data subject is obliged to provide the personal data and of the possible consequences of failure to provide such data;
the existence of automated decision-making, including profiling, referred to in Article 22(1) and (4) and, at least in those cases, meaningful information about the logic involved, as well as the significance and the envisaged consequences of such processing for the data subject.
Where the controller intends to further process the personal data for a purpose other than that for which the personal data were collected, the controller shall provide the data subject prior to that further processing with information on that other purpose and with any relevant further information as referred to in paragraph 2.
Paragraphs 1, 2 and 3 shall not apply where and insofar as the data subject already has the information.
 """,
  "output": """ ["Article (6)(1)(f)", " Article (46)", "Article (47)", "Article (49)(1)", "Article (6)(1)(a)", "Article (9)(2)(a)", "Article (22)(1)", Article (22)(4)"] """,},
      
 ]
example_prompt= PromptTemplate(
    input_variables=["input", "output"], template="input: {input}\noutput:{output}"
)
example_prompt.format(**examples[0])

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix= "return a list of consisting of only ALL of the articles listed in the last input.",
    suffix="input: {input}\nOutput",
    input_variables=["input"],
)

#Code commented out but can be used for quantization when running model locally.
'''
model= AutoModelForCausalLM.from_pretrained(model_name, quantization_config=bnb_config, device_map ="auto")
tokenizer = AutoTokenizer.from_pretrained(model_name)
'''

#Using embedding model for embedding, its possible to use mixtral for this but it requires running it locally to my knowledge
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")

def html_to_vector_db(path) -> FAISS:  
    """
    Function that takes html content from path and turns into vector database
    The html is parsed and only the actual article text is turned into a vector database

    :param path: the path the html should be taken from
    :return: returns a FAISS vector database
    """ 
    webp = requests.get(path)
    html = webp.text
    soup = BeautifulSoup(html, "html.parser") 
    content = soup.find("ol")
    #Retrieves the text in the ordered list, this is where the body of GDPR content is stored in the html files. 
    txt_content = content.get_text() 
    #1000 is chosen fror the chunk size because smaller chunks seem to increase the probability of hallucination 
    splitter = RecursiveCharacterTextSplitter(chunk_size= 500, chunk_overlap = 100)
    #Creation of a new document containing 
    data = splitter.create_documents([txt_content])
    article = splitter.split_documents(data)
    #Vector database is created from the document 
    vec_db = FAISS.from_documents(article, embeddings)
    
    return vec_db




def query(vec_db):
    ''' 
    Function for actual interaction with the model
    '''
    #Using similarity search to return relevant chunks.
    articles = vec_db.similarity_search("Article _", 8)
    full_article = " ".join(a.page_content for a in articles)
    print(full_article)


    
    '''
    Used in combination with commented code above. Pipeline for running the model locally with hugging face
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=100, top_k=50, temperature=0.1)
    llm = HuggingFacePipeline(pipeline=pipe)'''
    
    #Have only briefly played around with the parameters but this seems to be the most promising result
    llm= HuggingFaceEndpoint(
        repo_id=model_name, max_new_tokens=512, temperature=0.05, repetition_penalty=1.25, huggingfacehub_api_token=token)
    

    chain = prompt|llm
    print (chain.invoke(full_article))

vec_db =html_to_vector_db("https://gdpr-info.eu/art-12-gdpr/")
query(vec_db) 
