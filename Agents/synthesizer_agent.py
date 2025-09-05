from config import llm
from logger_util import setup_logger
from langchain_core.prompts import PromptTemplate

logger = setup_logger(__name__)

def synthesizer_agent(state):
    print("---SYNTHESIZER AGENT: Composing Final Answer---")
    query = state["query"]

    logger.info("Synthesizer Agent started")
    logger.debug(f"Received query: {query}")

    relevant_articles = "\n".join(state.get("relevant_articles", []))
    relevant_cases = "\n".join(state.get("relevant_cases", []))
    historical_context = "\n".join(state.get("historical_context", []))

    logger.debug(f"Relevant Articles: {relevant_articles}")
    logger.debug(f"Relevant Cases: {relevant_cases}")
    logger.debug(f"Historical Context: {historical_context}")

    full_context = (
        f"User Query: {query}\n\n"
        f"Relevant Articles:\n{relevant_articles}\n\n"
        f"Relevant Cases:\n{relevant_cases}\n\n"
        f"Historical Context:\n{historical_context}"
    )

    prompt = PromptTemplate(
        template="""You are a helpful assistant answering queries about the Constitution of India.
        Use the provided context to formulate a comprehensive and accurate answer.

        Context:
        {context}

        Question: {query}

        Final Answer:""",
        input_variables=["context", "query"]
    )

    try:
        chain = prompt | llm
        final_answer = chain.invoke({"context": full_context, "query": query})

        state["final_answer"] = (
            final_answer.content if hasattr(final_answer, "content") else str(final_answer)
        )
        logger.info("Final answer generated successfully")
        logger.debug(f"Final Answer: {state['final_answer']}")
    except Exception as e:
        logger.error(f"Error in synthesizer agent: {e}", exc_info=True)
        state["final_answer"] = f"Error generating answer: {e}"

    logger.info("Synthesizer Agent finished")
    return state
