from logger_util import setup_logger

logger = setup_logger(__name__)

def historical_context_agent(state):
    """Agent to provide historical context for constitutional amendments or articles."""
    logger.info("Historical Context Agent invoked.")

    query = state.get("query", "")
    logger.debug(f"Query received for historical context: '{query}'")

    try:
        if "article 370" in query.lower() or "abrogated" in query.lower():
            state["historical_context"] = [
                "Article 370 was a temporary provision for Jammu and Kashmir, abrogated on August 5, 2019."
            ]
            logger.info("Found historical context for Article 370.")
        else:
            state["historical_context"] = []
            logger.info("No relevant historical context found for this query.")
    except Exception as e:
        logger.exception(f"Error in historical context agent for query: {query}")
        state["historical_context"] = []

    return state
