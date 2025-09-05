import os
import uuid
from dotenv import load_dotenv
from logger_util import setup_logger
from logger_context import call_id_var
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

# Setup logger
logger = setup_logger(__name__)
call_id_var.set(str(uuid.uuid4()))

# --- Load environment variables ---
logger.info("Loading environment variables from .env file...")
load_dotenv()

# --- API Setup ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    logger.error("GROQ_API_KEY not found in environment variables!")
else:
    logger.info("Successfully loaded GROQ_API_KEY.")

# --- LLM Setup ---
try:
    logger.info("Initializing ChatGroq LLM (llama-3.3-70b-versatile)...")
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=GROQ_API_KEY)
    logger.info("ChatGroq LLM initialized successfully.")
except Exception as e:
    logger.exception(f"Failed to initialize ChatGroq LLM: {e}")
    raise

# --- Embeddings Setup ---
try:
    logger.info("Loading HuggingFace sentence-transformers/all-MiniLM-L6-v2 embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': False}
    )
    logger.info("HuggingFace embeddings initialized successfully.")
except Exception as e:
    logger.exception(f"Failed to initialize HuggingFace embeddings: {e}")
    raise
