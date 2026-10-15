
import time
import traceback
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from src.guardrails import check_scope
from src.retrieval import retrieve
from src.prompts import create_prompt
from src.llm import generate_answer

class RAGState(TypedDict, total=False):
    question: str
    is_in_scope: bool
    answer: str
    context: str
    sources: list
    retrieval_time_ms: float
    generation_time_ms: float

def check_question(state):
    question = state.get("question", "").strip()

    if not question:
        return {
            "is_in_scope": False,
            "answer": "Please enter a question.",
            "sources": [],
            "retrieval_time_ms": 0.0,
            "generation_time_ms": 0.0,
        }

    if check_scope(question):
        return {"is_in_scope": True}

    return {
        "is_in_scope": False,
        "answer": (
            "Sorry, I can only answer questions about "
            "the Islamabad Capital Territory Child Marriage "
            "Restraint Act, 2025."
        ),
        "sources": [],
        "retrieval_time_ms": 0.0,
        "generation_time_ms": 0.0,
    }


def retrieve_documents(state):
    question = state.get("question", "")

    start = time.perf_counter()
    results = retrieve(question, top_k=3)
    retrieval_time = (time.perf_counter() - start) * 1000

    context_parts = []
    sources = []

    for i, item in enumerate(results, start=1):
        text = item.get("text", "")
        section = str(item.get("section", "Unknown"))
        chunk_id = str(item.get("chunk_id", i))
        distance = float(item.get("distance", 0.0))

        if text and text.strip():
            context_parts.append(
                f"Section: {section}\nLegal text: {text}"
            )

        sources.append({
            "text": text,
            "section": section,
            "chunk_id": chunk_id,
            "distance": distance,
        })

    context = "\n\n".join(context_parts)

    print("\nRetrieved chunks:", len(results))
    print("Context length:", len(context))

    return {
        "context": context,
        "sources": sources,
        "retrieval_time_ms": round(retrieval_time, 2),
    }


def generate_response(state):
    question = state.get("question", "")
    context = state.get("context", "").strip()

    if not context:
        return {
            "answer": (
                "I could not find relevant information "
                "in the legal document."
            ),
            "generation_time_ms": 0.0,
        }

    prompt = create_prompt(question, context)

    start = time.perf_counter()
    answer = generate_answer(prompt)
    generation_time = (time.perf_counter() - start) * 1000

    return {
        "answer": answer,
        "generation_time_ms": round(generation_time, 2),
    }


def next_step(state):
    if state.get("is_in_scope", False):
        return "retrieve"
    return "finish"

workflow = StateGraph(RAGState)

workflow.add_node("check", check_question)
workflow.add_node("retrieve", retrieve_documents)
workflow.add_node("generate", generate_response)

workflow.add_edge(START, "check")

workflow.add_conditional_edges(
    "check",
    next_step,
    {
        "retrieve": "retrieve",
        "finish": END,
    },
)

workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

rag_graph = workflow.compile()


def ask_question(question):
    result = rag_graph.invoke({"question": question})

    return {
        "answer": result.get("answer", ""),
        "sources": result.get("sources", []),
        "is_in_scope": result.get("is_in_scope", False),
        "retrieval_time_ms": result.get("retrieval_time_ms", 0.0),
        "generation_time_ms": result.get("generation_time_ms", 0.0),
    }


if __name__ == "__main__":
    print("=" * 50)
    print("PAKISTANI LAW RAG CHATBOT")
    print("=" * 50)

    question = input("\nAsk a question about the law: ")

    try:
        response = ask_question(question)

        print("\nAnswer:")
        print(response["answer"])

        print("\nIn scope:")
        print(response["is_in_scope"])

        print("\nSources:")
        for source in response["sources"]:
            print(source)

        print("\nRetrieval time:", response["retrieval_time_ms"], "ms")
        print("Generation time:", response["generation_time_ms"], "ms")

    except Exception:
        traceback.print_exc()
