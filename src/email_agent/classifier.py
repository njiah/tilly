"""LLM-based email classification using structured output."""
from typing import Literal
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from email_agent.config import MODEL_NAME


class EmailClassification(BaseModel):
    """Structured classification output for an email."""
    category: Literal[
        "newsletter",
        "transactional",
        "personal",
        "work",
        "promotional",
        "needs_reply",
        "spam_like",
    ] = Field(description="Best-fit category for this email")
    suggested_action: Literal[
        "keep_in_inbox",
        "label_only",
        "archive",
    ] = Field(description="What should be done with this email")
    confidence: float = Field(ge=0, le=1, description="Confidence 0-1")
    reasoning: str = Field(description="One-sentence justification")


CLASSIFICATION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an email triage assistant. Classify the email into one category and suggest an action.

Guidelines:
- newsletter: subscriptions, blogs, news digests → suggest archive
- transactional: receipts, confirmations, notifications → suggest archive
- personal: from friends/family → suggest keep_in_inbox
- work: from colleagues or work-related → suggest keep_in_inbox
- promotional: marketing, sales pitches → suggest archive
- needs_reply: clearly expects a response → suggest keep_in_inbox
- spam_like: suspicious or low-quality → suggest archive

Be concise. Output only the structured fields."""),
    ("human", """From: {from_addr}
Subject: {subject}
Preview: {snippet}"""),
])


def get_classifier():
    """Build the classification chain."""
    llm = ChatOllama(model=MODEL_NAME, temperature=0)
    structured_llm = llm.with_structured_output(EmailClassification)
    return CLASSIFICATION_PROMPT | structured_llm


def classify_email(chain, email: dict) -> EmailClassification:
    """Classify a single email."""
    return chain.invoke({
        "from_addr": email["from"],
        "subject": email["subject"],
        "snippet": email["snippet"][:500],  # Truncate for speed
    })