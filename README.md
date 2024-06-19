
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

1. **Create a virtual environment:**
   ```sh
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - **For Windows:**
     ```sh
     venv\Scripts\activate
     ```
   - **For macOS/Linux:**
     ```sh
     source venv/bin/activate
     ```

3. **Install the required packages:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the backend server:**
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

![alt text](image-1.png)

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

### Output Example Image
![Example Output](example_output.png)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

You can customize the content further based on your specific requirements. Also, make sure to include an actual image file named `example_output.png` in your project directory for the output example section.