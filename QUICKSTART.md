# VoyageAI - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Option 1: Demo Mode (No Setup Required)

Run the application immediately with mock data:

```bash
# 1. Navigate to project directory
cd voyage-ai-planner

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

**That's it!** The app will open at http://localhost:8501

The application works out-of-the-box using:
- Mock APIs for all external services
- In-memory storage
- Synthetic knowledge base

### Option 2: Full Setup (With Azure OpenAI)

For full AI capabilities:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file
cp .env.example .env

# 3. Edit .env with your Azure OpenAI credentials
# Required fields:
#   AZURE_OPENAI_API_KEY=your-key
#   AZURE_OPENAI_ENDPOINT=your-endpoint
#   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4

# 4. Run the app
streamlit run app.py
```

### Option 3: Full Stack (With Databases)

For complete functionality including persistence:

```bash
# 1. Install and start PostgreSQL
# macOS: brew install postgresql && brew services start postgresql
# Ubuntu: sudo apt install postgresql && sudo service postgresql start
# Windows: Download from postgresql.org

# 2. Install and start MongoDB
# macOS: brew install mongodb-community && brew services start mongodb-community
# Ubuntu: Follow https://docs.mongodb.com/manual/installation/
# Windows: Download from mongodb.com

# 3. Create databases
createdb voyage_ai  # PostgreSQL

# 4. Setup .env file
cp .env.example .env
# Edit with your database credentials

# 5. Initialize databases
python setup_database.py

# 6. Run the app
streamlit run app.py
```

## 📱 Using the Application

### Step 1: Welcome Screen
- Read about VoyageAI features
- Click "Start Planning Your Journey"

### Step 2: Enter Your Travel Details
- **Destination**: Where you want to go (e.g., "Bali, Indonesia")
- **Budget**: Total trip budget in USD (e.g., "3000")
- **Duration**: Number of days (e.g., "7")
- **Interests**: Select multiple (Adventure, Culture, Food, etc.)
- **Travel Style**: Choose one (Budget, Comfort, Luxury, Adventure, Romantic)
- Click "Continue to Planning"

### Step 3: Watch AI Planning
- Orchestrator analyzes your preferences
- Creates execution plan for 8 agents
- Shows real-time planning steps
- Click "Deploy Agents" when ready

### Step 4: Agent Execution
- 8 specialized agents gather data:
  * Weather Analysis
  * Safety & Geopolitical Info
  * Flight Options
  * Hotel Bookings
  * Local Transport
  * Shopping & Markets
  * Language Support
  * Local Attractions
- Progress bars show each agent's status
- Click "View Results" when complete

### Step 5: Review Your Itinerary
- See comprehensive travel summary
- Explore RAG-powered unique insights
- Read detailed agent reports
- Download your plan:
  * PDF (complete itinerary)
  * CSV (structured data)
  * JSON (raw data)
- Options:
  * "Plan Another Trip" - Start over
  * "Refine This Plan" - Adjust details

## 🎯 Example Travel Plans to Try

### Beach Paradise (Bali)
- **Destination**: Bali, Indonesia
- **Budget**: 2500
- **Duration**: 10
- **Interests**: Beaches, Wellness, Culture, Food
- **Style**: Comfort

### Urban Explorer (Tokyo)
- **Destination**: Tokyo, Japan
- **Budget**: 4000
- **Duration**: 7
- **Interests**: Culture, Food, Shopping, Photography
- **Style**: Comfort

### Adventure Seeker (Iceland)
- **Destination**: Reykjavik, Iceland
- **Budget**: 3500
- **Duration**: 8
- **Interests**: Adventure, Nature, Photography, Wildlife
- **Style**: Adventure

### Romantic Getaway (Paris)
- **Destination**: Paris, France
- **Budget**: 5000
- **Duration**: 5
- **Interests**: Culture, Food, History, Shopping
- **Style**: Romantic

### Budget Backpacker (Thailand)
- **Destination**: Bangkok, Thailand
- **Budget**: 1500
- **Duration**: 14
- **Interests**: Adventure, Culture, Food, Beaches
- **Style**: Budget

## 🔧 Troubleshooting

### Issue: Port Already in Use
```bash
# Find process using port 8501
lsof -ti:8501 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8501   # Windows

# Or use a different port
streamlit run app.py --server.port 8502
```

### Issue: Module Not Found
```bash
# Reinstall requirements
pip install --upgrade -r requirements.txt

# Or install specific missing module
pip install streamlit
```

### Issue: Database Connection Error
- **PostgreSQL**: Check if service is running
- **MongoDB**: Check if service is running
- **Solution**: App works without databases in demo mode

### Issue: Azure OpenAI Error
- Check API key in .env file
- Verify endpoint URL
- Check deployment name
- **Solution**: App uses mock mode if Azure unavailable

### Issue: PDF Download Not Working
```bash
# Install/reinstall reportlab
pip install --upgrade reportlab
```

## 📊 Understanding the Output

### PDF Itinerary Includes:
- Travel summary with all your inputs
- Exclusive RAG-powered insights
- Detailed reports from all 8 agents
- Practical recommendations
- Professional formatting

### CSV Export Contains:
- Destination
- Budget
- Duration
- Travel style
- Interests list
- Generation timestamp

### JSON Export Contains:
- Complete travel data structure
- All user preferences
- Agent execution metadata
- Timestamp information

## 💡 Pro Tips

1. **Be Specific**: "Bali, Indonesia" is better than just "Bali"
2. **Realistic Budget**: Consider flights, hotels, activities, food
3. **Multiple Interests**: Select 2-4 for balanced recommendations
4. **Try Different Styles**: Each style gives different results
5. **Save PDFs**: Generate and download for offline reference

## 🎓 For Hackathon Participants

This application demonstrates:

### ✅ Required Features
- [x] Advanced RAG with custom chunking
- [x] Multi-agent orchestration
- [x] Agentic UI with progress tracking
- [x] Real-time data gathering
- [x] Downloadable outputs (PDF, CSV, JSON)
- [x] Vector database integration
- [x] Azure OpenAI integration
- [x] PostgreSQL for operational data
- [x] MongoDB for vector storage

### 💡 Learning Points
1. **RAG Implementation**: See `backend/rag_system.py`
2. **Agent Architecture**: See `backend/agents.py`
3. **Orchestration Logic**: See `backend/orchestrator.py`
4. **UI/UX Flow**: See `app.py`
5. **Database Design**: See `backend/database.py`

### 🏆 Presentation Tips
1. Start with the problem statement
2. Show the 5-step user flow
3. Highlight RAG unique insights
4. Demonstrate agent execution
5. Show the final itinerary
6. Explain the architecture
7. Discuss scalability

## 📞 Getting Help

### Documentation
- `README.md` - Complete overview
- `ARCHITECTURE.md` - Technical details
- Code comments - Inline documentation

### Common Questions

**Q: Do I need Azure OpenAI?**
A: No, the app works with mock data for demos.

**Q: Do I need databases?**
A: No, in-memory storage works for demos.

**Q: Can I use other LLMs?**
A: Yes, modify `backend/orchestrator.py` to use other APIs.

**Q: Is this production-ready?**
A: It's a prototype for demonstration and learning.

**Q: Can I deploy this?**
A: Yes, to Streamlit Cloud, AWS, Azure, or any Python host.

## 🎉 You're Ready!

Start exploring VoyageAI and see how AI agents can revolutionize travel planning!

```bash
streamlit run app.py
```

Visit: http://localhost:8501

Happy travels! 🌍✈️🏖️
