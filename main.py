import os
import sys
import uuid
from config import embeddings
from logger_util import setup_logger
from utils.document_loader import load_and_split_pdfs
from utils.routing import route_decision
from graph_state import GraphState
from langchain_community.vectorstores import Chroma
from langgraph.graph import StateGraph, END

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
    try:
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

        logger.info("Retriever initialized successfully")
        return vectorstore.as_retriever()

    except Exception as e:
        logger.error("Failed to initialize retriever: %s", str(e), exc_info=True)
        raise


def build_workflow():
    try:
        logger.info("Building the LangGraph...")
        workflow = StateGraph(GraphState)

        # Register nodes
        workflow.add_node("router", router_agent)
        workflow.add_node("article_search", article_search_agent)
        workflow.add_node("case_law", case_law_agent)
        workflow.add_node("historical_context", historical_context_agent)
        workflow.add_node("synthesizer", synthesizer_agent)

        # Define entry & routing
        workflow.set_entry_point("router")
        workflow.add_conditional_edges("router", route_decision, {
            "article_search": "article_search",
            "case_law": "case_law",
            "historical_context": "historical_context",
            "synthesizer": "synthesizer"
        })

        # Define transitions
        workflow.add_edge("article_search", "synthesizer")
        workflow.add_edge("case_law", "synthesizer")
        workflow.add_edge("historical_context", "synthesizer")
        workflow.add_edge("synthesizer", END)

        app = workflow.compile()
        logger.info("Graph compiled successfully.")
        return app
    except Exception as e:
        logger.error("Error building graph: %s", str(e), exc_info=True)
        sys.exit(1)


def run_query(app, retriever, query):
    logger.info("Running workflow with query: %s", query)
    inputs = {"query": query, "retriever": retriever}
    final_state = {}

    try:
        for s in app.stream(inputs):
            logger.debug("Current State Keys: %s", list(s.keys()))
            final_state.update(s)

        if "synthesizer" in final_state:
            return final_state["synthesizer"]["final_answer"]
        elif "__end__" in final_state:
            return final_state["__end__"]["final_answer"]
        else:
            logger.warning("No final answer produced. Keys: %s", final_state.keys())
            return "No answer could be generated."
    except Exception as e:
        logger.error("Error during workflow execution: %s", str(e), exc_info=True)
        return f"Error: {e}"


def main():
    pdf_files = [
        r"D:\BTP-1\pdf\20240716890312078.pdf",
        r"D:\BTP-1\pdf\EighthSchedule_19052017.pdf",
        r"D:\BTP-1\pdf\part3.pdf"
    ]

    logger.info("Initializing retriever...")
    retriever = get_retriever(pdf_files)

    logger.info("Compiling workflow...")
    app = build_workflow()

    # --- Interactive loop ---
    logger.info("Entering interactive query mode. Type 'q' or 'quit' to exit.")
    while True:
        try:
            query = input("\nEnter your question: ").strip()
            if query.lower() in {"q", "quit", "exit"}:
                logger.info("Exiting application.")
                break

            if not query:
                continue

            answer = run_query(app, retriever, query)
            print("\n--- Final Answer ---\n")
            print(answer)
            print("\n--------------------\n")

        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received. Exiting.")
            break
        except Exception as e:
            logger.error("Unexpected error: %s", str(e), exc_info=True)


if __name__ == "__main__":
    main()
