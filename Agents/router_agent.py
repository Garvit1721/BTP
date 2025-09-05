from config import llm
from logger_util import setup_logger
from graph_state import GraphState, router_parser
from langchain_core.prompts import PromptTemplate

logger = setup_logger(__name__)

def router_agent(state: GraphState):
    print("---ROUTER AGENT: Analyzing Query---")
    query = state["query"]

    logger.info("Router Agent started")
    logger.debug(f"Received query: {query}")

    prompt = PromptTemplate(
        template="""Based on the user's query, determine which agents to activate.
        Only respond with a JSON object that matches the schema: {format_instructions}

        User Query: {query}
        """,
        input_variables=["query"],
        partial_variables={"format_instructions": router_parser.get_format_instructions()}
    )

    try:
        chain = prompt | llm | router_parser
        routing_decision = chain.invoke({"query": query})
        print(f"Routing Decision: {routing_decision.reasoning}")
        logger.info("Routing decision successfully generated")
        logger.debug(f"Routing decision reasoning: {routing_decision.reasoning}")
        logger.debug(f"Routing decision object: {routing_decision.dict()}")

        state["routing_decision"] = routing_decision.dict()
    except Exception as e:
        logger.error(f"Error during routing decision: {e}", exc_info=True)
        state["routing_decision"] = {"error": str(e)}

    logger.info("Router Agent finished")
    return state
