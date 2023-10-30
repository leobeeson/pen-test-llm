from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel


from src.clients.runpod_client import RunPodClient


class PromptRequest(BaseModel):
    system_message: str
    n: int
    term_type: str
    theme: str
    instruction: str
    language_prompt: str
    language: str
    negative_examples: list[str]
    blocked_examples: list[str]
    positive_examples: list[str]

app = FastAPI()


url = 'https://hpu7bd6p2i59nb-5000.proxy.runpod.net/api/v1/generate'
run_pod_client = RunPodClient(url=url)

@app.post("/generate/")
async def generate(request: PromptRequest):
    try:
        response = run_pod_client.generate_single_turn_prompt(
            system_message=request.system_message,
            n=request.n,
            terms=request.term_type,
            theme=request.theme,
            instruction=request.instruction,
            language_prompt=request.language_prompt,
            language=request.language,
            negative_examples=request.negative_examples,
            blocked_examples=request.blocked_examples,
            positive_examples=request.positive_examples
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
