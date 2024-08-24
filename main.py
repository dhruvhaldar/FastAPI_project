from fastapi import FastAPI, Form, Response
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Union
import os

app = FastAPI()

class ScriptRequest(BaseModel):
    script_type: str
    content: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = """
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Script Generator</title>
            <!-- Tailwind CSS -->
            <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        </head>
        <body class="bg-gray-100 flex items-center justify-center min-h-screen">
            <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-lg">
                <h1 class="text-2xl font-bold text-center mb-6">Script Generator</h1>
                <form action="/generate_script" method="post">
                    <div class="mb-4">
                        <label for="script_type" class="block text-gray-700 font-medium mb-2">Select Script Type:</label>
                        <select id="script_type" name="script_type" class="block w-full mt-1 p-2 border border-gray-300 rounded-md">
                            <option value="python">Python</option>
                            <option value="bash">Bash</option>
                        </select>
                    </div>
                    
                    <div class="mb-4">
                        <label for="script_content" class="block text-gray-700 font-medium mb-2">Script Content:</label>
                        <textarea id="script_content" name="script_content" rows="10" class="block w-full mt-1 p-2 border border-gray-300 rounded-md"></textarea>
                    </div>
                    
                    <div class="text-center">
                        <input type="submit" value="Generate Script" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded cursor-pointer">
                    </div>
                </form>
            </div>
        </body>
    </html>
    """
    return html_content

@app.post("/generate_script", response_class=HTMLResponse)
def generate_script(script_type: str = Form(...), script_content: str = Form(...)):
    if script_type == "python":
        filename = "generated_script.py"
        script = f"# Python Script\n{script_content}"
    elif script_type == "bash":
        filename = "generated_script.sh"
        script = f"# Bash Script\n{script_content}"
    else:
        return "Unknown script type selected."
    
    # Save the script to a file
    with open(filename, "w") as file:
        file.write(script)
    
    return f"""
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Generated Script</title>
            <!-- Tailwind CSS -->
            <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        </head>
        <body class="bg-gray-100 flex items-center justify-center min-h-screen">
            <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-lg">
                <h2 class="text-xl font-bold text-center mb-6">Generated {script_type.capitalize()} Script:</h2>
                <pre class="bg-gray-900 text-white p-4 rounded-lg overflow-x-auto">{script}</pre>
                <div class="text-center mt-6">
                    <a href="/download_script/{filename}" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded cursor-pointer">Download Script</a>
                    <a href="/" class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded ml-2 cursor-pointer">Go Back</a>
                </div>
            </div>
        </body>
    </html>
    """

@app.get("/download_script/{filename}", response_class=FileResponse)
def download_script(filename: str):
    file_path = os.path.join(os.getcwd(), filename)
    return FileResponse(path=file_path, filename=filename, media_type='application/octet-stream')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5353)
