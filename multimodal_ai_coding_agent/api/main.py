from fastapi import FastAPI, UploadFile, File
from .agents.code_writer import CodeWriter
from agents.visual_inspector import VisualInspector
from agents.code_executor import CodeExecutor

app = FastAPI()

writer = CodeWriter()
inspector = VisualInspector()
executor = CodeExecutor()

@app.post("/generate-code/")
async def generate_code(prompt: str):
    code = writer.generate_code(prompt)
    return {"generated_code": code}

@app.post("/analyze-image/")
async def analyze_image(file: UploadFile = File(...)):
    image_path = f"temp/{file.filename}"
    with open(image_path, "wb") as buffer:
        buffer.write(await file.read())
    analysis = inspector.analyze_image(image_path)
    return {"analysis": analysis}

@app.post("/execute-code/")
async def execute_code(code: str, language: str = "python"):
    output = executor.run_code(code, language)
    return {"execution_output": output}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
