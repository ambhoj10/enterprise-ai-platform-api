from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

import os

from dotenv import load_dotenv

from langchain_openai import AzureChatOpenAI
from langsmith import traceable

# ======================================================
# LOAD ENV VARIABLES
# ======================================================

load_dotenv()

# ======================================================
# FASTAPI APP
# ======================================================

app = FastAPI(
    title="Enterprise Secure AI Platform API",
    description="Production-ready secure enterprise AI backend",
    version="5.0"
)

# ======================================================
# SECURITY CONFIG
# ======================================================

ENTERPRISE_API_KEY = os.getenv("ENTERPRISE_API_KEY")

# ======================================================
# AZURE OPENAI MODEL
# ======================================================

llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    temperature=0
)

# ======================================================
# AUTHENTICATION FUNCTION
# ======================================================

def verify_api_key(x_api_key: str = Header(...)):

    if x_api_key != ENTERPRISE_API_KEY:

        raise HTTPException(
            status_code=401,
            detail="Unauthorized API Key"
        )

# ======================================================
# REQUEST SCHEMAS
# ======================================================

class AIRequest(BaseModel):

    question: str

class EvaluationRequest(BaseModel):

    question: str
    ai_response: str

class PromptComparisonRequest(BaseModel):

    question: str
    prompt_1: str
    prompt_2: str

# ======================================================
# RESPONSE SCHEMAS
# ======================================================

class AIResponse(BaseModel):

    agent: str
    question: str
    answer: str

class EvaluationResponse(BaseModel):

    evaluation_type: str
    result: str

# ======================================================
# ROOT ENDPOINT
# ======================================================

@app.get("/")
def home():

    return {
        "message": "Enterprise Secure AI Platform API is running"
    }

# ======================================================
# GENERAL AI ASSISTANT
# ======================================================

@app.post("/ask-ai", response_model=AIResponse)
@traceable
def ask_ai(
    request: AIRequest,
    x_api_key: str = Header(...)
):

    verify_api_key(x_api_key)

    try:

        prompt = f'''
You are an enterprise AI assistant.

User Question:
{request.question}

Provide:
- professional response
- technical explanation
- enterprise-style answer
'''

        response = llm.invoke(prompt)

        return AIResponse(
            agent="General AI Assistant",
            question=request.question,
            answer=response.content
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ======================================================
# CLOUDOPS AGENT
# ======================================================

@app.post("/cloudops-agent", response_model=AIResponse)
@traceable
def cloudops_agent(
    request: AIRequest,
    x_api_key: str = Header(...)
):

    verify_api_key(x_api_key)

    try:

        prompt = f'''
You are an AI CloudOps Agent.

Analyze this cloud infrastructure issue.

Issue:
{request.question}

Provide:
- incident summary
- root cause analysis
- severity level
- remediation steps
'''

        response = llm.invoke(prompt)

        return AIResponse(
            agent="CloudOps Agent",
            question=request.question,
            answer=response.content
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ======================================================
# SECURITY AGENT
# ======================================================

@app.post("/security-agent", response_model=AIResponse)
@traceable
def security_agent(
    request: AIRequest,
    x_api_key: str = Header(...)
):

    verify_api_key(x_api_key)

    try:

        prompt = f'''
You are an Enterprise Security AI Agent.

Analyze the following enterprise security scenario.

Scenario:
{request.question}

Provide:
- security assessment
- vulnerabilities
- governance considerations
- remediation recommendations
'''

        response = llm.invoke(prompt)

        return AIResponse(
            agent="Security Agent",
            question=request.question,
            answer=response.content
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ======================================================
# ANALYTICS AGENT
# ======================================================

@app.post("/analytics-agent", response_model=AIResponse)
@traceable
def analytics_agent(
    request: AIRequest,
    x_api_key: str = Header(...)
):

    verify_api_key(x_api_key)

    try:

        prompt = f'''
You are an Enterprise Analytics AI Agent.

Analyze this enterprise analytics scenario.

Scenario:
{request.question}

Provide:
- analytics architecture
- Azure services involved
- pipeline recommendations
- optimization suggestions
'''

        response = llm.invoke(prompt)

        return AIResponse(
            agent="Analytics Agent",
            question=request.question,
            answer=response.content
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ======================================================
# RESPONSE EVALUATION PIPELINE
# ======================================================

@app.post("/evaluate-response", response_model=EvaluationResponse)
@traceable
def evaluate_response(
    request: EvaluationRequest,
    x_api_key: str = Header(...)
):

    verify_api_key(x_api_key)

    try:

        evaluation_prompt = f'''
You are an enterprise AI evaluation system.

Evaluate this AI response.

Question:
{request.question}

AI Response:
{request.ai_response}

Evaluate:
- correctness
- completeness
- hallucination risk
- enterprise quality

Provide:
- evaluation summary
- quality score out of 10
- improvement recommendations
'''

        response = llm.invoke(evaluation_prompt)

        return EvaluationResponse(
            evaluation_type="AI Response Evaluation",
            result=response.content
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ======================================================
# HEALTH CHECK
# ======================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "Enterprise Secure AI Platform API",
        "authentication": "Enabled",
        "observability": "LangSmith Enabled"
    }