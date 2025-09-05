from logger_util import setup_logger

logger = setup_logger(__name__)

def case_law_agent(state):
    """Agent to retrieve relevant case law based on query keywords."""
    logger.info("Case Law Agent invoked.")

    query = state.get("query", "")
    logger.debug(f"Query received for case law search: '{query}'")

    try:
        if "privacy" in query.lower() or "puttaswamy" in query.lower():
            state["relevant_cases"] = [
                "K.S. Puttaswamy v. Union of India (2017) - Right to Privacy under Article 21."
            ]
            logger.info("Found relevant case law on privacy.")
        else:
            state["relevant_cases"] = []
            logger.info("No relevant case law found for this query.")
    except Exception as e:
        logger.exception(f"Error while processing case law agent for query: {query}")
        state["relevant_cases"] = []

    return state
