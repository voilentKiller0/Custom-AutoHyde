from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser


KEYWORD_EXTRACTION_PROMPT = """
Your goal is to extract a list of keywords from an input phrase, sentence, or several sentences.

- You can only generate 1 to 5 keywords.
- Keywords should be nouns, issues, concepts, entities, topics, objects.
- Keywords can be include synonyms, but should not be too general
- Keywords should not include verbs, prepositions, pronouns
- If keywords are short form or abbreviation, expand them to full form.
- Each keyword can only be one word long.
- If the input is just a single word, return that word as the only keyword.

{format_instructions}

The input is:
{input}
"""


class KeywordListSchema(BaseModel):
    keywordList: list[str] = Field(description="list of one-word keywords based on a given phrase")

parser = JsonOutputParser(pydantic_object=KeywordListSchema)

def getKeyWords(llm, text):
    prompt = ChatPromptTemplate.from_template(
        template=KEYWORD_EXTRACTION_PROMPT,
        intput_variables = ["input"],
        partial_variables = {
            'format_instructions': parser.get_format_instructions()
        }
    )

    keyword_extraction_chain = (
        {'input': RunnablePassthrough()}
        | prompt
        | llm
        | parser
    )

    keywords = keyword_extraction_chain.invoke(text)['keywordList']
    print (f"\n>>> Keywords extracted: {keywords}\n")
    return keywords