
---

# AutoHyde RAG

AutoHyde RAG is a sophisticated retrieval-augmented generation (RAG) system that leverages ChromaDB for vector storage and Gemini LLM for text generation. The system retrieves relevant documents, filters them based on keywords, clusters them using the HDBSCAN algorithm, and generates answers using hypothetical documents formed from these clusters.

## Table of Contents
- [AutoHyde RAG](#autohyde-rag)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Steps](#steps)
  - [Usage](#usage)
  - [Workflow](#workflow)
  - [Example Output](#example-output)
    - [Request](#request)
    - [Response](#response)
    - [Output Example Image](#output-example-image)
  - [License](#license)

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package installer)

### Steps

1. **Clone the repository**
   ```sh
   git clone https://github.com/voilentKiller0/Custom-AutoHyde.git
   ```

2. **Create a virtual environment:**
   ```sh
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - **For Windows:**
     ```sh
     venv\Scripts\activate
     ```
   - **For macOS/Linux:**
     ```sh
     source venv/bin/activate
     ```

4. **Install the required packages:**
   ```sh
   pip install -r requirements.txt
   ```

5. **Run the backend server:**
   ```sh
   python app.py
   ```

   The server will run on `0.0.0.0:5000`.

## Usage

To interact with the server, send a POST request to `http://0.0.0.0:5000` with the following JSON payload:

```json
{
  "uuid": 37827,
  "query": "Put your question here"
}
```

## Workflow

1. **Fetch Baseline Documents:**
   Retrieve `baseline_k * exponential` documents from the database.

2. **Extract Keywords:**
   Extract 1 to 5 key phrases or important words from the user query.

3. **Filter Documents:**
   Eliminate all documents that do not contain any of the extracted keywords.

4. **Cluster Documents:**
   Use the HDBSCAN algorithm to cluster the remaining documents.

5. **Generate Hypothetical Documents:**
   Create hypothetical single documents from each cluster.

6. **Generate Answer:**
   Use the generated hypothetical documents to answer the user's query.

![image](https://github.com/voilentKiller0/Custom-AutoHyde/assets/55941465/dc905742-60ae-45e5-9b9b-dbd844ecbe04)


## Example Output

### Request
```json
{
  "uuid" : "1212",
  "query" : "How to design a URL Shortener"
}
```

### Response
```json
{
  "response": "**Step 1: Choose a domain name**\n\nThe domain name of your URL shortening service should be short, easy to remember, and relevant to the service you are providing.\n\n**Step 2: Set up a web server**\n\nThe web server that hosts your URL shortening service should be reliable and able to handle a large number of requests.\n\n**Step 3: Create a database**\n\nThe database that stores the short URLs and their corresponding long URLs should be able to handle a large number of requests and should be able to scale as your service grows.\n\n**Step 4: Develop a short URL generation algorithm**\n\nThe short URL generation algorithm should be efficient and should generate short URLs that are easy to remember and type.\n\n**Step 5: Implement a tracking system**\n\nThe tracking system should track the number of clicks on each short URL. This information can be used to measure the effectiveness of your URL shortening service and to identify which links are most popular."
}
```
---
### Request
```json
{
  "uuid" : "1212",
  "query" : "Design a Real-Time Chat Application"
}
```

### Response
```json
{
  "response": "**Step 1: Define the requirements**\n\nThe first step is to define the requirements for your chat application. This includes things like:\n\n* The number of users that the application will need to support\n* The types of messages that the application will need to handle (text, images, files, etc.)\n* The security features that the application will need\n* The user experience that you want to provide\n\n**Step 2: Choose a technology stack**\n\nOnce you have defined the requirements for your application, you need to choose a technology stack. This includes things like:\n\n* The programming language that you will use\n* The web server that you will use\n* The database that you will use\n* The real-time communication protocol that you will use\n\n**Step 3: Design the database**\n\nThe next step is to design the database for your application. This includes things like:\n\n* The tables that you will need\n* The columns that each table will have\n* The relationships between the tables\n\n**Step 4: Implement the application**\n\nOnce you have designed the database, you can start implementing the application. This includes things like:\n\n* Writing the code for the web server\n* Writing the code for the database\n* Writing the code for the real-time communication protocol\n\n**Step 5: Test the application**\n\nOnce you have implemented the application, you need to test it. This includes things like:\n\n* Testing the application with a small number of users\n* Testing the application with a large number of users\n* Testing the application under different conditions\n\n**Step 6: Deploy the application**\n\nOnce you have tested the application, you can deploy it. This includes things like:\n\n* Uploading the application to a web server\n* Configuring the web server\n* Configuring the database\n\n**Step 7: Monitor the application**\n\nOnce you have deployed the application, you need to monitor it. This includes things like:\n\n* Monitoring the performance of the application\n* Monitoring the security of the application\n* Monitoring the user experience"
}
```
---
### Request
```json
{
  "uuid" : "1212",
  "query" : "How to design a Cache System"
}
```

### Response
```json
{
  "response": "**Steps to Design a Cache System**\n\n1. **Determine the size of the cache.** The size of the cache will depend on the amount of data that needs to be cached and the performance requirements of the application.\n2. **Choose a cache design.** There are a number of different cache designs available, each with its own advantages and disadvantages. The most common cache design is the least recently used (LRU) cache.\n3. **Implement the cache system.** The cache system can be implemented in hardware or software.\n4. **Test the cache system.** The cache system should be tested to ensure that it is working correctly and that it is meeting the performance requirements of the application."
}
```

## Note:
The PDF file in the books folder is converted to vector data and stored in chromaDB using the ingest.py script.
