from flask import Flask, render_template, request, redirect, url_for  
import csv
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from langchain import HuggingFaceHub, LLMChain
from langchain.prompts import PromptTemplate

# Loading HuggingfaceApi Key
load_dotenv()

app = Flask(__name__)

# Load and read csv file .
with open("items.csv") as file:
    lines = csv.reader(file)
    documents = []
    metadatas = []
    ids = []
    id = 1

    for i, line in enumerate(lines):
        if i == 0:
            continue
        documents.append(line[1])
        metadatas.append({"item_id": line[0]})
        ids.append(str(id))
        id += 1

# Created a database client and collection using the chromadb library, 
# then fed the collection with data.
chroma_client = chromadb.Client()
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")
collection = chroma_client.create_collection(name="my_collection")
collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

# Homepage
@app.route('/')
def hello_world():
    return render_template('index.html')

# Route to handle button clicks and redirect accordingly
@app.route('/redirect', methods=['POST'])
def redirect_page():
    page = request.form['page']
    if page == 'calculator':
        return redirect(url_for('calculator'))
    elif page == 'question_answering':
        return redirect(url_for('question_answering'))
    elif page == 'search':
        return redirect(url_for('index'))  # Bu "/search" adresine yönlendirsin
    else:
        return 'Invalid page'


# Vector search 
@app.route('/search/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form['search_query']
        results = search_and_return_results(search_query)
        return render_template('vector_search.html', search_query=search_query, results=results)
    return render_template('vector_search.html', search_query=None, results=None)

# This function searches for results in the collection using the search query parameter
# Prints the most similar 5 results based on the specified query."
def search_and_return_results(search_query):
    results = collection.query(
        query_texts=[search_query],
        n_results=5,
        include=['documents']
    )
    return results['documents']

# Calculator
@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.route('/calculate', methods=['GET','POST'])
def calculate():
    if 'num1' in request.form and 'num2' in request.form and 'operator' in request.form:
        num1 = request.form['num1']
        num2 = request.form['num2']
        operator = request.form['operator']

        try:
            num1 = float(num1)
            num2 = float(num2)
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    return render_template('calculator.html', result="Can't divide to zero")
                result = num1 / num2
            else:
                return render_template('calculator.html', result="Invalid operator!")
        except ValueError:
            return render_template('calculator.html', result="Invalid number!")
        
        return render_template('calculator.html', result=result)
    else:
        return render_template('calculator.html', result="Numbers missing!")


#A question-answering application that works using the HuggingFace model; operates by responding to queries formatted as 'How does it work?
@app.route('/question_answering')
def question_answering():
    return render_template('question_answering.html')

hub_llm = HuggingFaceHub(repo_id="google/gemma-1.1-7b-it", model_kwargs={'temperature':0.8, 'max_new_tokens':2000})

prompt = PromptTemplate(
    input_variables=["text-generation"],
    template="{text-generation}",
)

hub_chain = LLMChain(prompt=prompt, llm=hub_llm, verbose=True)

# The result is added to the HTML template line by line and displayed to the user.
@app.route('/generate', methods=['POST'])
def generate():
    question = request.form['question']
    output = hub_chain.run(question)
    output_with_newlines = output.split('\n')  
    return render_template('question_answering.html', question=question, output=output_with_newlines)

if __name__ == '__main__':
    app.run(debug=True)
