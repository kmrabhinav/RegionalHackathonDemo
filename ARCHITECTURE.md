# VoyageAI - Architecture Documentation

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        STREAMLIT UI LAYER                        │
│  ┌─────────────┬──────────────┬─────────────┬─────────────┐    │
│  │  Welcome    │  Collection  │ Orchestrator│  Execution  │    │
│  │   Screen    │    Screen    │   Screen    │   Screen    │    │
│  └─────────────┴──────────────┴─────────────┴─────────────┘    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   ORCHESTRATION LAYER                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Travel Orchestrator                          │  │
│  │  • Analyze Preferences                                    │  │
│  │  • Create Execution Plan                                  │  │
│  │  • Optimize Agent Sequence                                │  │
│  │  • Validate Plan                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                    ▼                 ▼
┌─────────────────────────┐  ┌──────────────────────┐
│    RAG SYSTEM           │  │   AGENT MANAGER      │
│  • Vector Storage       │  │  • Execute Agents    │
│  • Knowledge Retrieval  │  │  • Monitor Status    │
│  • Semantic Search      │  │  • Aggregate Results │
│  • Context Enhancement  │  │  • Error Handling    │
└───────┬─────────────────┘  └──────────┬───────────┘
        │                               │
        ▼                               ▼
┌─────────────────┐          ┌──────────────────────┐
│  MongoDB        │          │  8 Specialized Agents│
│  (Vector DB)    │          │  ┌─────────────────┐ │
│  • Embeddings   │          │  │ Weather         │ │
│  • Knowledge    │          │  │ Safety          │ │
│    Base         │          │  │ Flights         │ │
└─────────────────┘          │  │ Hotels          │ │
                             │  │ Transport       │ │
┌─────────────────┐          │  │ Shopping        │ │
│  PostgreSQL     │          │  │ Language        │ │
│  • Users        │◄─────────┤  │ Attractions     │ │
│  • Plans        │          │  └─────────────────┘ │
│  • Executions   │          └──────────┬───────────┘
│  • RAG Queries  │                     │
└─────────────────┘                     ▼
                             ┌──────────────────────┐
┌─────────────────┐          │   MOCK APIs          │
│  Azure OpenAI   │          │  • Weather API       │
│  • GPT-4        │          │  • Flight API        │
│  • Embeddings   │          │  • Hotel API         │
│  • Chat         │          │  • Safety API        │
└─────────────────┘          │  • Translation API   │
                             │  • Geo API           │
                             └──────────────────────┘
                                        │
                                        ▼
                             ┌──────────────────────┐
                             │   OUTPUT LAYER       │
                             │  • PDF Generator     │
                             │  • CSV Export        │
                             │  • JSON Export       │
                             └──────────────────────┘
```

## Component Details

### 1. UI Layer (Streamlit)

**Purpose**: User interaction and visualization

**Screens**:
- **Welcome**: Introduction and feature showcase
- **Collection**: Travel preference gathering
- **Orchestrator**: Planning visualization
- **Execution**: Agent progress tracking
- **Results**: Comprehensive itinerary display

**Technologies**:
- Streamlit 1.29.0
- Custom CSS styling
- Session state management

### 2. Orchestration Layer

**Purpose**: Coordinate all AI operations

**Components**:
- **TravelOrchestrator**
  - Analyzes user preferences using Azure OpenAI
  - Creates detailed agent execution plan
  - Optimizes execution sequence based on dependencies
  - Validates plan completeness
  - Generates human-readable summaries

**Key Methods**:
```python
analyze_preferences(travel_data) -> Dict
create_orchestration_plan(travel_data) -> Dict
optimize_execution_sequence(plan) -> List
validate_plan(plan) -> Dict
```

### 3. RAG System

**Purpose**: Provide unique destination knowledge

**Architecture**:
```
User Query → Create Embedding → Vector Search → 
Retrieve Top-K → Rank by Similarity → Return Results
```

**Components**:
- **Embedding Generation**: Azure OpenAI text-embedding-ada-002
- **Vector Storage**: MongoDB with embedded vectors
- **Similarity Search**: Cosine similarity calculation
- **Context Enhancement**: Augment agent contexts with RAG knowledge

**Knowledge Categories**:
- Hidden Gems (high exclusivity)
- Local Secrets (medium exclusivity)
- Best Times to Visit (low-medium exclusivity)

**Retrieval Strategy**:
```python
# Custom chunking based on destination and category
chunks = {
  "destination": "Bali",
  "category": "hidden_gems",
  "content": "...",
  "metadata": {"type": "location", "exclusivity": "high"}
}

# Indexing with embeddings
embedding = create_embedding(content)
store_with_embedding(chunk, embedding)

# Retrieval
query_embedding = create_embedding(user_query)
results = vector_search(query_embedding, top_k=5)
```

### 4. Agent System

**Purpose**: Execute specialized travel planning tasks

**Agent Architecture**:
```python
class BaseAgent:
    - agent_name: str
    - status: str
    - progress: int
    - result: Dict
    
    def execute(context) -> Dict
    def get_status() -> Dict
```

**8 Specialized Agents**:

1. **WeatherAgent**
   - Current weather conditions
   - 7-day forecast
   - Best visit times
   - UV index and recommendations

2. **SafetyAgent**
   - Safety ratings
   - Travel advisories
   - Health requirements
   - Emergency contacts

3. **FlightAgent**
   - Flight search
   - Price comparison
   - Best booking times
   - Airline recommendations

4. **HotelAgent**
   - Accommodation search
   - Price filtering by travel style
   - Neighborhood analysis
   - Amenity filtering

5. **TransportAgent**
   - Airport transfers
   - Local transport options
   - Rental services
   - Navigation tips

6. **ShoppingAgent**
   - Local markets
   - Shopping districts
   - Bargaining tips
   - Payment methods

7. **LanguageAgent**
   - Common phrases
   - Translation tools
   - Cultural tips
   - Communication strategies

8. **AttractionsAgent**
   - Interest-based filtering
   - Top-rated attractions
   - Day trip options
   - Booking recommendations

**Execution Flow**:
```
Agent Manager → Select Agent → Load Context → 
Execute Task → Update Progress → Store Result → 
Return to Manager
```

### 5. Database Layer

**PostgreSQL (Operational Data)**:
- User accounts and preferences
- Travel plan storage
- Agent execution logs
- RAG query analytics
- Booking records

**MongoDB (Vector Data)**:
- Vector embeddings
- Travel knowledge base
- Agent detailed results
- Unstructured data storage

**Schema Design Philosophy**:
- Normalized relational data in PostgreSQL
- Flexible document storage in MongoDB
- Foreign key relationships for referential integrity
- Indexes on frequently queried fields

### 6. Mock API Layer

**Purpose**: Simulate external services for demo

**Available APIs**:
- Weather API (OpenWeather-style)
- Flight Search API (Skyscanner-style)
- Hotel Booking API (Booking.com-style)
- Safety Information API (travel.state.gov-style)
- Translation API (Google Translate-style)
- Geolocation API (Google Maps-style)
- Currency Exchange API
- Email API

**Mock Data Strategy**:
- Randomized realistic data
- Consistent with user inputs
- Appropriate variance
- Timestamp inclusion

### 7. Output Generation

**PDF Generation**:
- ReportLab library
- Professional formatting
- Multi-page layout
- Tables and images
- Custom styling

**CSV Export**:
- Pandas DataFrame
- Structured data format
- Easy spreadsheet import

**JSON Export**:
- Complete data structure
- API-ready format
- Developer-friendly

## Data Flow

### 1. User Input Flow
```
User Input → Validation → Session State → 
Orchestrator → Plan Creation
```

### 2. RAG Query Flow
```
Agent Request → Query Formation → Embedding Generation → 
Vector Search → Similarity Ranking → Context Enhancement
```

### 3. Agent Execution Flow
```
Plan Ready → Sequential/Parallel Launch → 
Progress Tracking → Result Collection → 
Database Storage → UI Update
```

### 4. Output Generation Flow
```
All Agents Complete → Data Aggregation → 
Format Selection → Document Generation → 
Download Link → User Download
```

## Security Considerations

### Data Protection
- Environment variables for credentials
- No hardcoded API keys
- Secure database connections
- Input sanitization

### Error Handling
- Try-catch blocks at every external call
- Graceful degradation to mock data
- User-friendly error messages
- Logging for debugging

### Rate Limiting
- API call throttling
- Database connection pooling
- Timeout configurations
- Retry mechanisms with exponential backoff

## Scalability

### Horizontal Scaling
- Stateless application design
- Database connection pooling
- Caching layer potential
- Load balancer ready

### Vertical Scaling
- Efficient memory usage
- Lazy loading of components
- Query optimization
- Index utilization

### Performance Optimization
- Vector search optimization
- Database query caching
- Async agent execution
- Result memoization

## Monitoring & Observability

### Logging
- Agent execution times
- RAG query performance
- API call success rates
- Error tracking

### Metrics
- User journey completion rates
- Agent success rates
- RAG relevance scores
- System response times

### Debugging
- Detailed error messages
- Stack trace logging
- Request/response logging
- State inspection

## Deployment Architecture

### Local Development
```
Python Virtual Environment → Streamlit Dev Server →
Local PostgreSQL → Local MongoDB
```

### Production Deployment (Recommended)
```
Container (Docker) → Streamlit Cloud / AWS / Azure →
Managed PostgreSQL (RDS / Azure DB) →
MongoDB Atlas
```

### Environment Configuration
```
Development: .env.development
Staging: .env.staging
Production: .env.production
```

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| UI | Streamlit 1.29.0 | Interactive web application |
| AI/ML | Azure OpenAI GPT-4 | Chat completion and reasoning |
| Embeddings | Azure OpenAI Ada-002 | Vector embeddings |
| Relational DB | PostgreSQL 12+ | Structured operational data |
| Vector DB | MongoDB 4.4+ | Vector storage and search |
| PDF | ReportLab 4.0 | Document generation |
| Data | Pandas, NumPy | Data processing |
| Language | Python 3.8+ | Core application logic |

## Integration Points

### External Services (Optional)
- Azure OpenAI API
- PostgreSQL Database
- MongoDB Database

### Internal Services
- Orchestrator ↔ Agent Manager
- Agent Manager ↔ Agents
- Agents ↔ Mock APIs
- Orchestrator ↔ RAG System
- RAG System ↔ MongoDB
- All Components ↔ PostgreSQL

## Configuration Management

### Settings Hierarchy
1. Environment Variables (.env)
2. Default Values (settings.py)
3. Runtime Configuration (session state)

### Key Configuration Areas
- API credentials
- Database connections
- Agent timeouts
- RAG parameters
- Rate limits

## Error Recovery

### Agent Failure
- Retry with exponential backoff
- Fall back to mock data
- Continue with other agents
- Report in final summary

### Database Failure
- In-memory fallback
- User notification
- Graceful degradation
- Automatic reconnection attempt

### API Failure
- Mock data substitution
- Cached result usage
- User transparency
- Error logging

---

This architecture supports the hackathon requirements for:
✅ Advanced RAG implementation
✅ Multi-agent orchestration
✅ Custom chunking and indexing
✅ MCP-style agent coordination
✅ Comprehensive UI/UX flow
✅ Multiple data sources
✅ Failsafe mechanisms
✅ Downloadable outputs
