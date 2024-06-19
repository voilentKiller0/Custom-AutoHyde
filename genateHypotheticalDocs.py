from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser


HYPOTHETICAL_DOCUMENT_PROMPT = """
Your instruction is to generate a single hypothetical document from an input.
- This hypothetical document must be similar in style, tone and voice as examples you are provided with.
- This hypothetical document must appear like it was written by the same author as the examples you are provided with.
- This hypothetical document must also be similar in length with the examples you are provided with.

{format_instructions}

### EXAMPLES ###
Below are some examples of hypothetical documents, all written by the same author, in pairs of <Input> and <Hypothetical Document>:

{ref_documents}

### INSTRUCTION ###
Now generate a new hypothetical document. 

<Input>
{input}
<Hypothetical Document>

"""


class HypotheticalDocumentSchema(BaseModel):
    hypotheticalDocument: str = Field(description="a hypothetical document given an input word, phrase or question")

parser = JsonOutputParser(pydantic_object=HypotheticalDocumentSchema)


def generateHypotheticalDocs(llm, cat_dict, text):
    print(f"\n>>> Generating Hypothetical Documents for each Doc Cluster...\n")
    
    hypo_docs = list()
    
    prompt = ChatPromptTemplate.from_template(
        template=HYPOTHETICAL_DOCUMENT_PROMPT,
        intput_variables = ["input", "ref_documents"],
        partial_variables = {
            'format_instructions': parser.get_format_instructions()
        }
    )

    hypothetical_document_chain = (
        {'input': RunnablePassthrough(), 'ref_documents': RunnablePassthrough()}
        | prompt
        | llm
        | parser
    )


    cat_ii = 1
    for cat in cat_dict.keys():

        ref_doc_string = ""
        doc_ii = 1
        hypo_doc = hypothetical_document_chain.invoke(
            {'input': text, 'ref_documents': ref_doc_string}
        )['hypotheticalDocument']
        
        hypo_docs.append(hypo_doc)
        
        cat_ii += 1
        
    print(f">>> ...{len(hypo_docs)} Hypothetical Docs generated\n")
        
    return hypo_docs