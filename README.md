# Introduction 
TODO: Give a short introduction of your project. Let this section explain the objectives or the motivation behind this project. 

# Getting Started
TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:
1.	Installation process
2.	Software dependencies
3.	Latest releases
4.	API references

# Build and Test
TODO: Describe and show how to build your code and run the tests. 

# Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)


Run Locally
1️⃣ Clone the repository
git clone https://TriZettoT3@dev.azure.com/TriZettoT3/OptimizationSoftwareProducts/_git/OSPAI_QNXT_Schema_Analysis


2️⃣ Create a virtual environment
python -m venv .venv
.venv\Scripts\activate                

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the Streamlit app
streamlit run frontend/app.py

Your app will be available at 👉 http://localhost:8501
________________________________________
🐳 Run with Docker
1️⃣ Build and run the container
docker-compose up --build

This will:
Build the Streamlit frontend image
Load your environment variables from .env
Expose the app on port 9400
Visit 👉 http://localhost:9400
2️⃣ Stop the container
docker-compose down