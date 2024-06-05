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

token="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" #insert hugging face token here


login(token=token) 
model_name = "mistralai/Mixtral-8x7B-Instruct-v0.1" 

'''
Used for quantizing model if running locally.

bnb_config = BitsAndBytesConfig (  
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
)'''

#Few shot examples

examples = [{"input": """The nature of the personal data,
  in particular whether special categories of personal data are processed, pursuant to Section B of Article 9.
  The purpose of the processing shall be determined in that legal basis or, as regards the processing referred to in point (e) of Article 1
 """,
  "output": """ ["Article(9)(b)", "Article(1)(e)"] """,},

    {"input": """The controller shall facilitate the exercise of data subject rights under Articles 15 to 22. 2In the cases referred to in Article 11(2), the controller shall not refuse to act on the request of the data subject for exercising his or her rights under Articles 15 to 22, unless the controller demonstrates that it is not in a position to identify the data subject.
 """,
  "output": """ [""Article(15)" ,"Article(16)", "Article(17)", "Article(18)", "Article(19)", "Article(20)", "Article(21)"  "Article(22)", "Article (11)(2)"] """,},
    
    {"input": """In such cases, Articles 15 to 20 shall not apply except where the data subject, for the purpose of exercising his or her rights under those articles, provides additional information enabling his or her identification.
 """,
  "output": """ ["Article(15)" ,"Article(16)", "Article(17)", "Article(18)", "Article(19)", "Article(20)"] """,},

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
      
      {"input": """Without prejudice to Article 55, the supervisory authority of the main establishment or of the single establishment of the controller or processor shall be competent to act as lead supervisory authority for the cross-border processing carried out by that controller or processor in accordance with the procedure provided in Article 60.
 """,
  "output": """ ["Article(55)", "Article(60)"]
  """,},
      
 ]
example_prompt= PromptTemplate(
    input_variables=["input", "output"], template="input: {input}\n{output}"
)
example_prompt.format(**examples[0])

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix= "Return a list only of all the articles referenced in the last input",
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

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap = 100)
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
    articles = vec_db.similarity_search("What articles are referenced",)
    full_article = " ".join(a.page_content for a in articles)


    
    '''
    Used in combination with commented code above. Pipeline for running the model locally with hugging face
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=100, top_k=50, temperature=0.1)
    llm = HuggingFacePipeline(pipeline=pipe)'''
    
    llm= HuggingFaceEndpoint(
        repo_id=model_name, max_new_tokens=512, temperature=0.05, huggingfacehub_api_token=token)
    

    chain = prompt|llm
    print (chain.invoke(full_article))

vec_db =html_to_vector_db("https://gdpr-info.eu/art-6-gdpr/")
query(vec_db) 