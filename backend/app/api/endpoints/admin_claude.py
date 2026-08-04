"""
Admin Claude Chat API
Provides Claude AI assistance through a secure admin-only endpoint
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import anthropic
import os

router = APIRouter()

# Get Claude client
def get_claude_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Claude API key not configured")
    return anthropic.Anthropic(api_key=api_key)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    conversationHistory: Optional[List[dict]] = None


class ChatResponse(BaseModel):
    response: str


def build_admin_system_prompt() -> str:
    """System prompt for admin Claude chat"""
    return """You are Claude, an expert AI assistant for Project Athena administration.

You have deep knowledge of:
- Project Athena architecture: 4-stage autonomous product intelligence pipeline
- Backend: FastAPI, PostgreSQL, Redis, Celery
- Frontend: Next.js, React, TypeScript
- Agents: Research, Supplier, Validation, Scoring
- APIs: 8 REST endpoints
- Dashboard: Real-time monitoring
- Deployment: Docker, production setup

Your role as an admin assistant:
✓ Explain system architecture and components
✓ Help troubleshoot issues
✓ Suggest optimizations and improvements
✓ Explain code and design decisions
✓ Help with deployment and scaling
✓ Analyze performance and suggest enhancements
✓ Provide best practices and recommendations

When responding:
- Be clear, concise, and technical
- Reference specific files/code when relevant
- Use code examples when helpful
- Provide actionable recommendations
- Focus on what the admin needs to know

You can help with project status, technical questions, debugging, optimization, and administrative tasks."""


@router.post("/api/v1/admin/claude-chat", response_model=ChatResponse)
async def chat_with_claude(request: ChatRequest):
    """
    Chat with Claude about Project Athena
    Admin-only endpoint
    """
    try:
        client = get_claude_client()

        # Build conversation history
        messages = []

        if request.conversationHistory:
            for msg in request.conversationHistory:
                if msg.get("role") in ["user", "assistant"]:
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })

        # Add current message
        messages.append({
            "role": "user",
            "content": request.message
        })

        # Get response from Claude
        response = client.messages.create(
            model="claude-opus-5",
            max_tokens=2048,
            system=build_admin_system_prompt(),
            messages=messages
        )

        return ChatResponse(response=response.content[0].text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Claude: {str(e)}")


@router.get("/api/v1/admin/claude-status")
async def claude_status():
    """Check if Claude API is accessible"""
    try:
        client = get_claude_client()
        # Test with a simple message
        response = client.messages.create(
            model="claude-opus-5",
            max_tokens=10,
            messages=[
                {"role": "user", "content": "Hi"}
            ]
        )
        return {
            "status": "operational",
            "model": "claude-opus-5",
            "message": "Claude API is accessible"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Claude API is not accessible"
        }
