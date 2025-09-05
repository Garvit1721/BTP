from typing import TypedDict, List, Any
from logger_util import setup_logger
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser

# Setup logger
logger = setup_logger(__name__)

class GraphState(TypedDict):
    """Represents the state shared across agents in the LangGraph workflow."""
    query: str
    relevant_articles: List[str]
    relevant_cases: List[str]
    historical_context: List[str]
    final_answer: str
    routing_decision: dict
    retriever: Any


class RouterOutput(BaseModel):
    """Schema for Router Agent output with routing decisions and reasoning."""
    route_to_article_search: bool = Field(description="Route to Article Search Agent")
    route_to_case_law: bool = Field(description="Route to Case Law Agent")
    route_to_historical_context: bool = Field(description="Route to Historical Context Agent")
    reasoning: str = Field(description="Reasoning for routing")

    def log_decision(self):
        """Log the routing decision in a structured way."""
        logger.info("Router decision taken:")
        logger.info(f"  → Article Search: {self.route_to_article_search}")
        logger.info(f"  → Case Law: {self.route_to_case_law}")
        logger.info(f"  → Historical Context: {self.route_to_historical_context}")
        logger.info(f"  → Reasoning: {self.reasoning}")


# Output parser for Router Agent
router_parser = PydanticOutputParser(pydantic_object=RouterOutput)

# Example usage with logging
def parse_router_output(output_text: str) -> RouterOutput:
    """Parses router agent output and logs the decision."""
    logger.debug("Parsing router agent output...")
    result = router_parser.parse(output_text)
    result.log_decision()
    return result
