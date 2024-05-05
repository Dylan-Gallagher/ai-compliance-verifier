# Deployed ethical-ai
## Frontend
Running on ReactJS at https://group22.sprinty.tech/

## Backend
Running an api server on Python Flask at https://group22.api.sprinty.tech/

# Running the project
## Frontend
`cd app` - Change directory to app(frontend) folder  
`npm i` - Install all the dependencies  
`npm start` - Start the frontend on localhost:3000

## Backend
`cd backend` - Change directory to backend folder  
`pip install -r server-requirements.txt` - Install all the server dependencies  
`python server.py` - Start the backend server on localhost:8000

Opon landing on the main page, the user has two options: either visualise the Knowledge Graph of the EU AI Act or upload their own AI model documentation.

## Knowledge Graph
The Knowledge Graph is a visual representation of all key elements of the EU AI Act and the relationships between them. The user can easily navigate the graph either via the computer mouse/touch pad, or by using the buttons located at the bottom of the page (arrows, zoom in/out, full-screen).
In addition, the “Physics Option” button allows for features such as the Enable/Disable Physics, which allows the user to make the entities move around the screen or stop them, the Strong Repulsion button, which widens the space between the entities for a clearer view and the Burnes-Hut Layout button, which returns the graph to its initial state.
Moreover, the entities are colour-coded based on their group, with a legend on the right side of the screen. This allows the user to easily view the different entities. Hovering with the mouse over an entity will prompt a tag to appear, containing details about its respective entity.

## Uploading the Model Documentation
A user may upload their model documentation from their computer in order to generate a knowledge graph based on it, or obtain a compliance score. Once the document is uploaded, the user may navigate the knowledge graph the same way as described in the previous section. In addition, the search bar allows the user to search for specific entities by typing words related to them and clicking on “Update Graph”. The user may also select a specific group of entities to be shown from the dropdown selection bar.
A user may see the uploaded documentation by clicking ”Show Documentation”, where all the entities detected will be highlighted.
Lastly, the user can see the compliance score by clicking on “Get Compliance Score”. This will be shown as a percentage, which represents how well the AI model complies to the EU AI Act’s regulation. A list of recommendations will be shown of how the AI model and its documentation can be improved and be more compliant with the EU AI Act.

## Other Functions
Clicking on “IBM Research” at the top of the page will redirect the user to the start page of the app, where they can choose to upload more documents.
The “About” button will redirect the user to a page with information regarding the team who created the app, including contact information.
Lastly, the Github icon in the upper left corner will take the user to the Github repository containing all the code for the app itself.
