import os
import sys
from config import embeddings
from logger_util import setup_logger
from utils.document_loader import load_and_split_pdfs
from utils.routing import route_decision
from graph_state import GraphState
from langchain_community.vectorstores import Chroma
from langgraph.graph import StateGraph, END
import chainlit as cl

# Agents
from Agents.router_agent import router_agent
from Agents.article_search_agent import article_search_agent
from Agents.case_law_agent import case_law_agent
from Agents.historical_context_agent import historical_context_agent
from Agents.synthesizer_agent import synthesizer_agent

# Persistent storage path for Chroma DB
CHROMA_DIR = "./chroma_store"

# Logger setup
logger = setup_logger(__name__)


def get_retriever(pdf_files):
    """Load existing vectorstore if available, else create and persist."""
    if os.path.exists(CHROMA_DIR):
        logger.info("Loading existing Chroma DB from %s", CHROMA_DIR)
        vectorstore = Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=embeddings
        )
    else:
        logger.info("Creating new Chroma DB...")
        docs = load_and_split_pdfs(pdf_files)
        logger.info("Loaded and split %d documents", len(docs))

        vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=CHROMA_DIR
        )
        vectorstore.persist()
        logger.info("Persisted new Chroma DB at %s", CHROMA_DIR)

    return vectorstore.as_retriever()


def build_workflow():
    """Build and compile the LangGraph workflow."""
    workflow = StateGraph(GraphState)

    # Register nodes
    workflow.add_node("router", router_agent)
    workflow.add_node("article_search", article_search_agent)
    workflow.add_node("case_law", case_law_agent)
    workflow.add_node("historical_context", historical_context_agent)
    workflow.add_node("synthesizer", synthesizer_agent)

    # Entry point
    workflow.set_entry_point("router")
    workflow.add_conditional_edges("router", route_decision, {
        "article_search": "article_search",
        "case_law": "case_law",
        "historical_context": "historical_context",
        "synthesizer": "synthesizer"
    })

    # Transitions
    workflow.add_edge("article_search", "synthesizer")
    workflow.add_edge("case_law", "synthesizer")
    workflow.add_edge("historical_context", "synthesizer")
    workflow.add_edge("synthesizer", END)

    return workflow.compile()


def run_query(app, retriever, query):
    """Run workflow for a single query and return final answer."""
    inputs = {"query": query, "retriever": retriever}
    final_state = {}

    for s in app.stream(inputs):
        final_state.update(s)

    if "synthesizer" in final_state:
        return final_state["synthesizer"]["final_answer"]
    elif "__end__" in final_state:
        return final_state["__end__"]["final_answer"]
    else:
        return "No answer could be generated."


# --- Chainlit Handlers ---
retriever = None
workflow_app = None


@cl.on_chat_start
async def start_chat():
    global retriever, workflow_app

    pdf_files = [
        r"D:\BTP-1\pdf\20240716890312078.pdf",
        r"D:\BTP-1\pdf\EighthSchedule_19052017.pdf",
        r"D:\BTP-1\pdf\part3.pdf"
    ]

    logger.info("Initializing retriever...")
    retriever = get_retriever(pdf_files)

    logger.info("Compiling workflow...")
    workflow_app = build_workflow()

    await cl.Message(content="Hi 👋! I’m your Indian Constitution Assistant. Ask me anything about articles, cases, or historical context.").send()


@cl.on_message
async def handle_message(message: cl.Message):
    query = message.content.strip()
    logger.info("Received query: %s", query)

    answer = run_query(workflow_app, retriever, query)

    await cl.Message(content=answer).send()
