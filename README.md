# Indian Constitution Assistant

A sophisticated AI-powered assistant that helps users query and understand the Constitution of India using a multi-agent system built with LangGraph, LangChain, and Chainlit.

## 🌟 Features

- **Multi-Agent Architecture**: Specialized agents for different types of constitutional queries
- **Intelligent Routing**: Smart query analysis to determine the most relevant information sources
- **Document Retrieval**: Vector-based search through constitutional articles and amendments
- **Case Law Integration**: Access to relevant legal precedents and landmark cases
- **Historical Context**: Background information on constitutional amendments and provisions
- **Interactive Chat Interface**: User-friendly web interface powered by Chainlit
- **Persistent Knowledge Base**: ChromaDB vector store for efficient document retrieval

## 🏗️ Architecture

The system uses a graph-based workflow with the following agents:

1. **Router Agent**: Analyzes incoming queries and routes them to appropriate specialized agents
2. **Article Search Agent**: Retrieves relevant constitutional articles using vector similarity search
3. **Case Law Agent**: Provides relevant legal cases and precedents
4. **Historical Context Agent**: Offers historical background and context for constitutional provisions
5. **Synthesizer Agent**: Combines information from all agents to generate comprehensive answers

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- GROQ API key (for LLM access)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd indian-constitution-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Prepare PDF documents**
   Place your constitutional documents in the `pdf/` directory. The system expects:
   - `20240716890312078.pdf` (Main constitution document)
   - `EighthSchedule_19052017.pdf` (Eighth Schedule)
   - `part3.pdf` (Part III - Fundamental Rights)

### Usage

#### Web Interface (Recommended)
```bash
chainlit run app.py
```
Then open your browser and navigate to the provided URL (typically `http://localhost:8000`).

#### Command Line Interface
```bash
python main.py
```

## 📁 Project Structure

```
├── Agents/
│   ├── article_search_agent.py    # Vector-based article retrieval
│   ├── case_law_agent.py          # Legal case precedents
│   ├── historical_context_agent.py # Historical background
│   ├── router_agent.py            # Query routing logic
│   └── synthesizer_agent.py       # Response synthesis
├── utils/
│   ├── document_loader.py         # PDF processing utilities
│   └── routing.py                 # Routing decision logic
├── logs/                          # Application logs
├── chroma_store/                  # Vector database storage
├── pdf/                          # Constitutional documents
├── app.py                        # Chainlit web interface
├── main.py                       # CLI interface
├── config.py                     # Configuration and model setup
├── graph_state.py               # State management
├── logger_util.py               # Logging utilities
├── logger_context.py           # Logging context
├── logging_config.yaml         # Logging configuration
└── requirements.txt            # Python dependencies
```

## 🔧 Configuration

### Model Configuration
The system uses:
- **LLM**: Llama 3.3 70B (via GROQ)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Vector Store**: ChromaDB with persistent storage

### Logging
Comprehensive logging is configured via `logging_config.yaml`:
- Console and file logging
- Contextual logging with call IDs
- Separate handling for external libraries

## 📊 Agent Details

### Router Agent
- Analyzes user queries using LLM reasoning
- Makes routing decisions based on query content
- Supports multiple agent activation for complex queries

### Article Search Agent
- Uses vector similarity search on constitutional documents
- Retrieves most relevant article excerpts
- Handles PDF document processing and chunking

### Case Law Agent
- Currently includes landmark cases like K.S. Puttaswamy v. Union of India
- Extensible framework for adding more legal precedents
- Keyword-based case matching

### Historical Context Agent
- Provides background on constitutional amendments
- Includes information about abrogated provisions (e.g., Article 370)
- Contextualizes constitutional changes over time

### Synthesizer Agent
- Combines information from all activated agents
- Generates coherent, comprehensive responses
- Maintains context and relevance across different information sources

## 🛠️ Extending the System

### Adding New Documents
1. Place PDF files in the `pdf/` directory
2. Update the file paths in `main.py` or `app.py`
3. Delete the `chroma_store/` directory to rebuild the vector database

### Adding New Case Law
Modify `Agents/case_law_agent.py` to include additional cases:
```python
if "your_keyword" in query.lower():
    state["relevant_cases"] = [
        "New Case Name v. Respondent (Year) - Brief description."
    ]
```

### Customizing Agent Behavior
Each agent can be independently modified to change its behavior, data sources, or response format.

## 📝 Example Queries

- "What is Article 21 of the Constitution?"
- "Tell me about the right to privacy"
- "What happened to Article 370?"
- "Explain fundamental rights in India"
- "Cases related to freedom of speech"

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This assistant is for educational and informational purposes only. It should not be considered as legal advice. Always consult qualified legal professionals for legal matters.

## 🐛 Troubleshooting

### Common Issues

1. **ChromaDB Import Error**
   ```bash
   pip install --upgrade chromadb
   ```

2. **GROQ API Issues**
   - Verify your API key is correct
   - Check your GROQ account usage limits

3. **PDF Loading Errors**
   - Ensure PDF files exist at specified paths
   - Check file permissions

4. **Memory Issues**
   - Reduce chunk size in `document_loader.py`
   - Consider using a smaller embedding model

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the logs in the `logs/` directory for detailed error information
- Review the console output for immediate debugging

## 🔮 Future Enhancements

- [ ] Integration with more legal databases
- [ ] Support for regional language queries
- [ ] Advanced legal reasoning capabilities
- [ ] Citation and reference tracking
- [ ] Integration with legal document standards
- [ ] REST API endpoints
- [ ] Advanced search filters and faceting
