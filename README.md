# VoyageAI - AI-Powered Holiday Travel Planner

A comprehensive AI-powered travel planning application demonstrating advanced agentic orchestration, RAG (Retrieval-Augmented Generation) knowledge retrieval, and multi-agent execution workflows.

## 🌟 Features

### Core Capabilities
- **AI Orchestration**: Intelligent coordination of multiple specialized agents
- **RAG-Powered Knowledge**: Unique destination insights from proprietary knowledge base
- **Multi-Agent Execution**: 8 specialized agents working in parallel
- **Real-time Progress Tracking**: Visual feedback on agent execution
- **Comprehensive Reporting**: Downloadable PDF, CSV, and JSON outputs

### Specialized Agents
1. **Weather Analysis Agent** - Climate patterns and optimal visit times
2. **Safety & Geopolitical Agent** - Travel advisories and safety ratings
3. **Flight Options Agent** - Best flight deals and booking recommendations
4. **Hotel Bookings Agent** - Accommodation options matching preferences
5. **Local Transport Agent** - Transportation solutions and navigation
6. **Shopping & Markets Agent** - Local markets and authentic shopping
7. **Language Support Agent** - Translation and communication tips
8. **Local Attractions Agent** - Curated activities and hidden gems

## 🏗️ Architecture

```
voyage-ai-planner/
├── app.py                      # Main Streamlit application
├── backend/
│   ├── __init__.py
│   ├── orchestrator.py         # AI orchestration logic
│   ├── agents.py               # All specialized agents
│   ├── rag_system.py           # RAG implementation
│   ├── database.py             # Database management
│   └── mock_apis.py            # Mock API implementations
├── config/
│   ├── __init__.py
│   └── settings.py             # Configuration settings
├── utils/
│   ├── __init__.py
│   └── pdf_generator.py        # PDF generation utilities
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── setup_database.py           # Database initialization script
```

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL 12+ (optional, for persistent storage)
- MongoDB 4.4+ (optional, for vector storage)
- Azure OpenAI API access (optional, mock mode available)

## 🚀 Installation

### 1. Clone the Repository
```bash
cd voyage-ai-planner
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
```

Edit `.env` file with your configuration:
```env
# Azure OpenAI (required for full functionality)
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002

# Database (optional - works without for demo)
POSTGRES_HOST=localhost
POSTGRES_DATABASE=voyage_ai
MONGODB_URI=mongodb://localhost:27017/
```

### 5. Initialize Database (Optional)
```bash
python setup_database.py
```

## 💻 Running the Application

### Start the Streamlit App
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Demo Mode
The application works without external services using mock data:
- Mock APIs simulate real-world responses
- In-memory storage when databases unavailable
- Synthetic RAG knowledge base

## 📱 User Interface Flow

### 1. Welcome Screen
- Introduction to VoyageAI capabilities
- Feature highlights with animated cards
- "How It Works" explanation

### 2. Data Collection Screen
- Destination input
- Budget and duration selection
- Multi-select interests (Adventure, Culture, Food, etc.)
- Travel style selector (Budget, Comfort, Luxury, Adventure, Romantic)

### 3. Orchestrator Screen
- Real-time planning steps visualization
- RAG knowledge base queries
- Agent capability identification
- Orchestration plan creation

### 4. Agent Execution Screen
- Parallel agent execution with progress bars
- Real-time status updates for each agent
- Visual representation of agent workflows
- Completion summary with metrics

### 5. Results Screen
- Comprehensive travel summary
- RAG-powered unique insights
- Detailed agent reports (expandable)
- Download options (PDF, CSV, JSON)
- Options to refine or plan another trip

## 🧠 RAG System

### Knowledge Base
The RAG system maintains proprietary travel knowledge:
- **Hidden Gems**: Secret locations known to locals
- **Best Times to Visit**: Optimal periods based on multiple factors
- **Local Secrets**: Insider tips from destination experts

### Vector Storage
- MongoDB for vector embeddings
- Azure OpenAI for text embeddings
- Cosine similarity for retrieval
- Context-aware knowledge enhancement

### Custom Chunking Strategy
- Destination-specific knowledge chunks
- Category-based indexing (gems, secrets, timing)
- Metadata-rich embeddings for better retrieval

## 🤖 Agent Architecture

### Base Agent Class
All agents inherit from `BaseAgent`:
```python
class BaseAgent:
    def __init__(self, agent_name: str)
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]
    def get_status(self) -> Dict[str, Any]
```

### Agent Manager
Coordinates all agents:
- Sequential or parallel execution
- Result aggregation
- Status monitoring
- Error handling

### Mock APIs
Each agent uses mock APIs for demonstration:
- Weather API (OpenWeather-style)
- Flight Search API (Skyscanner-style)
- Hotel Booking API (Booking.com-style)
- Safety Info API (travel.state.gov-style)
- Translation API (Google Translate-style)

## 🗄️ Database Schema

### PostgreSQL Tables

#### users
```sql
user_id (PK), email, name, created_at, last_login
```

#### travel_plans
```sql
plan_id (PK), user_id (FK), destination, budget, duration, 
travel_style, interests, status, created_at, updated_at
```

#### agent_executions
```sql
execution_id (PK), plan_id (FK), agent_name, status, 
start_time, end_time, result_summary, error_message
```

#### rag_queries
```sql
query_id (PK), plan_id (FK), query_text, destination, 
results_count, executed_at
```

#### bookings
```sql
booking_id (PK), plan_id (FK), booking_type, provider, 
booking_reference, price, booking_date, travel_date, status
```

### MongoDB Collections

#### travel_knowledge
```json
{
  "destination": "Bali",
  "category": "hidden_gems",
  "content": "Secret waterfall...",
  "metadata": {"type": "location", "exclusivity": "high"},
  "embedding": [0.1, 0.2, ...],
  "created_at": "2024-01-01"
}
```

#### agent_results
```json
{
  "agent_name": "weather_analysis",
  "plan_id": 123,
  "result": {...},
  "timestamp": "2024-01-01T12:00:00"
}
```

## 📊 PDF Generation

The application generates comprehensive PDF itineraries including:
- Travel summary with all preferences
- RAG-powered exclusive insights
- Detailed agent reports
- Practical recommendations
- Professional formatting with ReportLab

## 🛡️ Guardrails & Safety

### Error Handling
- Try-catch blocks around all external calls
- Graceful degradation to mock data
- User-friendly error messages
- Automatic retry mechanisms

### Data Validation
- Input sanitization
- Budget range validation
- Date consistency checks
- Interest selection requirements

### Rate Limiting
- API call throttling
- Database connection pooling
- Timeout configurations

## 🔧 Configuration Options

### Agent Settings
```python
AGENT_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
```

### RAG Settings
```python
RAG_TOP_K = 5  # results per query
RAG_SIMILARITY_THRESHOLD = 0.7
```

### Application Settings
```python
DEBUG_MODE = True
RATE_LIMIT_PER_MINUTE = 60
```

## 🧪 Testing

### Run with Mock Data
```bash
# No external dependencies required
streamlit run app.py
```

### Test Database Setup
```bash
python setup_database.py
```

### Test Individual Components
```python
from backend.agents import WeatherAgent
from backend.rag_system import RAGSystem

# Test weather agent
agent = WeatherAgent()
result = agent.execute({'destination': 'Bali'})

# Test RAG system
rag = RAGSystem()
insights = rag.retrieve_knowledge('hidden gems', 'Bali')
```

## 📈 Performance Considerations

- **Async Operations**: Agents can execute in parallel
- **Caching**: RAG results cached for repeated queries
- **Connection Pooling**: Database connections reused
- **Lazy Loading**: Components initialized on demand

## 🎯 Hackathon Tips (From Requirements)

1. **Initial 10 Minutes**: Individual thinking time
2. **Problem Analysis**: Who, what, why, when, where
3. **Explode the Problem**: Look beyond given statement
4. **Advanced RAG**: Custom chunking, indexing, embedding
5. **Agentic Strategy**: Tools, reasoning, ReAct, MCP
6. **UI/UX Strategy**: Conversational flow, progress tracking
7. **Data Strategy**: Operational, training, synthetic data
8. **Integration**: REST API or direct Python calls
9. **Architecture**: Clear building blocks and flow
10. **Guardrails**: Failsafe mechanisms and human control

## 🚧 Future Enhancements

- [ ] Real-time collaboration features
- [ ] User authentication and profiles
- [ ] Trip comparison functionality
- [ ] Mobile app version
- [ ] Integration with real booking APIs
- [ ] Multi-language support
- [ ] Social sharing features
- [ ] AI-powered budget optimization
- [ ] Real-time currency conversion
- [ ] Weather alerts and notifications

## 📝 License

This project is created for educational and demonstration purposes.

## 🤝 Contributing

This is a hackathon demonstration project. Feel free to use it as a reference for:
- AI agent orchestration patterns
- RAG system implementation
- Streamlit application design
- Multi-agent workflows

## 📧 Support

For questions or issues, please refer to:
- Azure OpenAI Documentation: https://learn.microsoft.com/azure/ai-services/openai/
- Streamlit Documentation: https://docs.streamlit.io/
- ReportLab Documentation: https://www.reportlab.com/docs/

## 🎓 Learning Resources

- **RAG Systems**: Understanding vector databases and semantic search
- **Agent Orchestration**: Coordinating multiple AI agents effectively
- **Streamlit**: Building interactive data applications
- **Azure OpenAI**: Enterprise AI implementation

---

**Built with ❤️ for AI Hackathon Regional Level**

*Demonstrating the power of agentic AI, RAG knowledge systems, and intelligent orchestration in real-world travel planning scenarios.*
