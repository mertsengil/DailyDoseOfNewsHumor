import os
from groq import Groq
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

os.environ["GROQ_API_KEY"] = """TYPE YOUR GROQ_API_KEY"""
client = Groq()


def fun_w_lang(text):
    chat = ChatGroq(temperature=0.7, model_name="llama3-70b-8192")
    prompt = ChatPromptTemplate.from_messages([("human","""Please read this text and give us a funny summary. Your task is to make this text more funny and entertaining. Create a humorous paragraph that will actually make people laugh. You should add funny jokes about this article to summary. Don't write the translation. 
                                                           Important Note: Understand the language in which the news is written and create your whole summary in that language!
                                                           Another Note: Just write a text, don't add anything like title, translation, explanation!
                                                           news: {text}
                                                           Funny text in language of the given text: """)])

    chain = prompt | chat
    fun_text = "".join(chunk.content for chunk in chain.stream({"text": f"""{text}"""}))
    return fun_text


def generate_funny_summary(news):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""
                
                 Prompt: Please read this news and give us a short and funny summary. Analyze the tone, context, and semantic content of news articles to identify potential comedic elements. The reader should burst out laughing! Prepare an entertaining summary in Turkish by making clever jokes about the news. Important note: Understand the language in which the news is written and create your summary in that language.
                
                 news: {news} 
                 
                 funny summary:
    """,
            }
        ],
        model="llama3-70b-8192",
        temperature=0.7,
        max_tokens=4096,
        top_p=1,
        stop=None,
    )

    response = chat_completion.choices[0].message.content
    #SEND TO SECOND AI FUNCTION (langchain) TO IMPROVE THE RESPONSE
    funny_response = fun_w_lang(response)
    return funny_response
