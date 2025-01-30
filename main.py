from fastapi import FastAPI, File, UploadFile
import pandas as pd
import openai
from io import BytesIO

app = FastAPI()

openai.api_key = "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"

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))
    return {"message": "File uploaded successfully", "columns": df.columns.tolist()}

@app.post("/ask/")
async def ask_question(question: str, file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))
    
    # Convert DataFrame to string for AI processing
    context = df.to_string()
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Answer questions based on the provided Excel data."},
                  {"role": "user", "content": f"Data: {context} \n\nQuestion: {question}"}]
    )
    return {"answer": response["choices"][0]["message"]["content"]}

