from contextlib import asynccontextmanager
import re

from fastapi import FastAPI, Request
from pydantic import BaseModel, ConfigDict, Field
from transformers import pipeline


MODEL = "Helsinki-NLP/opus-mt-en-fr"
SOURCE_TOKENS = 250


@asynccontextmanager
async def lifespan(app: FastAPI):
    translator = pipeline("translation", model=MODEL, device=-1)
    app.state.tokenizer = translator.tokenizer
    app.state.translator = translator
    yield


app = FastAPI(title="Tradução do inglês para o francês", lifespan=lifespan)


class TranslationInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    text: str = Field(min_length=1, max_length=20000)


class TranslationOutput(BaseModel):
    translation: str


def split_text(text, tokenizer):
    if len(tokenizer.tokenize(text)) <= SOURCE_TOKENS:
        return [text]

    # Corta perto do meio, de preferência entre palavras.
    middle = len(text) // 2
    boundary = text.rfind(" ", middle // 2, middle)
    cut = boundary if boundary > 0 else middle
    return split_text(text[:cut].strip(), tokenizer) + split_text(text[cut:].strip(), tokenizer)


@app.post("/translate", response_model=TranslationOutput)
def translate(body: TranslationInput, request: Request):
    state = request.app.state
    paragraphs = re.split(r"\r?\n(?:[ \t]*\r?\n)+", body.text)
    translations = []
    for paragraph in paragraphs:
        chunks = split_text(paragraph.strip(), state.tokenizer)
        results = state.translator(chunks, batch_size=4)
        translations.append(" ".join(result["translation_text"] for result in results))
    return {"translation": "\n\n".join(translations)}
