from logger_util import setup_logger

logger = setup_logger(__name__)

def article_search_agent(state):
    """Agent to search relevant constitutional articles using retriever."""
    logger.info("Article Search Agent invoked.")

    query = state.get("query", "")
    retriever = state.get("retriever")

    if not retriever:
        logger.error("Retriever not found in state. Cannot perform article search.")
        state["relevant_articles"] = []
        return state

    logger.debug(f"Query received for article search: '{query}'")

    try:
        docs = retriever.invoke(query)
        relevant_articles = [doc.page_content for doc in docs]
        state["relevant_articles"] = relevant_articles

        logger.info(f"Found {len(relevant_articles)} relevant articles.")
        if len(relevant_articles) > 0:
            logger.debug(f"Sample article snippet: {relevant_articles[0][:200]}...")
    except Exception as e:
        logger.exception(f"Error while retrieving articles for query: {query}")
        state["relevant_articles"] = []

    return state
