import streamlit as st
import time
from datetime import datetime
import json
from typing import List, Dict, Any
from backend.orchestrator import TravelOrchestrator
from backend.agents import AgentManager
from backend.rag_system import RAGSystem
from backend.database import DatabaseManager
from utils.pdf_generator import PDFGenerator
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="VoyageAI - AI Travel Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(to bottom right, #f8fafc, #f1f5f9, #e2e8f0);
    }
    
    .stButton>button {
        background: linear-gradient(to right, #0ea5e9, #06b6d4);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.5);
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(14, 165, 233, 0.1);
        margin: 1rem 0;
    }
    
    .agent-card {
        background: rgba(255, 255, 255, 0.7);
        padding: 1rem;
        border-radius: 0.75rem;
        margin: 0.5rem 0;
        border-left: 4px solid;
    }
    
    .progress-step {
        display: inline-block;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        border-radius: 2rem;
        font-size: 0.875rem;
        font-weight: 600;
    }
    
    .step-completed {
        background: linear-gradient(to right, #0ea5e9, #06b6d4);
        color: white;
    }
    
    .step-current {
        background: rgba(14, 165, 233, 0.2);
        color: #0ea5e9;
        border: 2px solid #0ea5e9;
    }
    
    .step-upcoming {
        background: rgba(148, 163, 184, 0.1);
        color: #94a3b8;
    }
    
    .gradient-text {
        background: linear-gradient(to right, #0ea5e9, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .insight-card {
        background: white;
        padding: 1.25rem;
        border-radius: 0.75rem;
        border: 2px solid #0ea5e9;
        margin: 0.75rem 0;
    }
    
    .badge {
        display: inline-block;
        padding: 0.375rem 0.75rem;
        margin: 0.25rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        background: rgba(14, 165, 233, 0.1);
        color: #0ea5e9;
        border: 1px solid #0ea5e9;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .badge-selected {
        background: linear-gradient(to right, #0ea5e9, #06b6d4);
        color: white;
        border-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 'welcome'
    
if 'travel_data' not in st.session_state:
    st.session_state.travel_data = {}
    
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = TravelOrchestrator()
    
if 'agent_manager' not in st.session_state:
    st.session_state.agent_manager = AgentManager()
    
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = RAGSystem()
    
if 'db_manager' not in st.session_state:
    st.session_state.db_manager = DatabaseManager()

# Progress Indicator
def show_progress():
    steps = [
        ("welcome", "🌟 Welcome"),
        ("collection", "📋 Details"),
        ("orchestrator", "🧠 Planning"),
        ("execution", "⚡ Execution"),
        ("results", "✅ Results")
    ]
    
    current_idx = next((i for i, (step, _) in enumerate(steps) if step == st.session_state.step), 0)
    
    progress_html = '<div style="text-align: center; margin: 2rem 0;">'
    for idx, (step, label) in enumerate(steps):
        if idx < current_idx:
            class_name = "progress-step step-completed"
        elif idx == current_idx:
            class_name = "progress-step step-current"
        else:
            class_name = "progress-step step-upcoming"
        
        progress_html += f'<span class="{class_name}">{label}</span>'
        
        if idx < len(steps) - 1:
            if idx < current_idx:
                progress_html += '<span style="color: #0ea5e9; margin: 0 0.5rem;">━━</span>'
            else:
                progress_html += '<span style="color: #cbd5e1; margin: 0 0.5rem;">╌╌</span>'
    
    progress_html += '</div>'
    st.markdown(progress_html, unsafe_allow_html=True)

# Screen 1: Welcome
def show_welcome():
    st.markdown('<h1 style="text-align: center; font-size: 3rem; margin-top: 2rem;">🌍</h1>', unsafe_allow_html=True)
    st.markdown('<h1 class="gradient-text" style="text-align: center; font-size: 2.5rem;">Welcome to VoyageAI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #64748b; font-size: 1.125rem; margin-bottom: 3rem;">Your intelligent travel companion powered by advanced AI agents and RAG technology</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>✨ AI Orchestration</h3>
            <p style="color: #64748b;">Multiple specialized agents work together to craft your perfect journey</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🌐 Unique Insights</h3>
            <p style="color: #64748b;">RAG-powered knowledge base with exclusive destination information</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🛡️ Smart Planning</h3>
            <p style="color: #64748b;">Real-time weather, geopolitical analysis, and safety recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(148, 163, 184, 0.1); padding: 2rem; border-radius: 1rem; margin: 2rem 0;">
        <h3 style="color: #0ea5e9; margin-bottom: 1rem;">How It Works</h3>
        <ol style="color: #475569; line-height: 1.8;">
            <li><strong style="color: #0ea5e9;">Share</strong> your travel preferences and requirements</li>
            <li><strong style="color: #0ea5e9;">AI orchestrator</strong> analyzes and creates a personalized plan</li>
            <li><strong style="color: #0ea5e9;">Specialized agents</strong> gather real-time data (weather, flights, hotels)</li>
            <li><strong style="color: #0ea5e9;">Receive</strong> comprehensive itinerary with downloadable PDF</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Start Planning Your Journey", use_container_width=True):
            st.session_state.step = 'collection'
            st.rerun()

# Screen 2: Data Collection
def show_data_collection():
    st.markdown('<h1 class="gradient-text" style="text-align: center; font-size: 2rem;">Tell Us About Your Dream Trip</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #64748b; margin-bottom: 2rem;">Our AI will use this information to create a personalized travel plan</p>', unsafe_allow_html=True)
    
    with st.form("travel_form"):
        # Destination
        destination = st.text_input("📍 Destination", placeholder="e.g., Bali, Indonesia", help="Where do you want to go?")
        
        col1, col2 = st.columns(2)
        with col1:
            budget = st.text_input("💰 Budget (USD)", placeholder="e.g., 3000", help="Total budget for the trip")
        with col2:
            duration = st.text_input("📅 Duration (days)", placeholder="e.g., 7", help="How many days?")
        
        # Interests
        st.markdown("### ❤️ Interests (select multiple)")
        interests_options = ["Adventure", "Culture", "Food", "Nature", "Beaches", "History", 
                            "Shopping", "Photography", "Wellness", "Wildlife", "Nightlife", "Sports"]
        
        # Create a grid of checkboxes for interests
        cols = st.columns(4)
        selected_interests = []
        for idx, interest in enumerate(interests_options):
            with cols[idx % 4]:
                if st.checkbox(interest, key=f"interest_{interest}"):
                    selected_interests.append(interest)
        
        # Travel Style
        st.markdown("### ✈️ Travel Style")
        travel_style = st.radio(
            "Select your preferred style:",
            ["Budget", "Comfort", "Luxury", "Adventure", "Romantic"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # Submit button
        submitted = st.form_submit_button("Continue to Planning →", use_container_width=True)
        
        if submitted:
            if destination and budget and duration and len(selected_interests) > 0 and travel_style:
                st.session_state.travel_data = {
                    'destination': destination,
                    'budget': budget,
                    'duration': duration,
                    'interests': selected_interests,
                    'travel_style': travel_style
                }
                st.session_state.step = 'orchestrator'
                st.rerun()
            else:
                st.error("Please fill in all fields and select at least one interest!")

# Screen 3: Orchestrator
def show_orchestrator():
    st.markdown('<h1 style="text-align: center;">🧠</h1>', unsafe_allow_html=True)
    st.markdown('<h1 class="gradient-text" style="text-align: center; font-size: 2rem;">AI Orchestrator at Work</h1>', unsafe_allow_html=True)
    destination = st.session_state.travel_data.get('destination', 'your destination')
    st.markdown(f'<p style="text-align: center; color: #64748b; margin-bottom: 2rem;">Planning your perfect trip to {destination}</p>', unsafe_allow_html=True)
    
    planning_steps = [
        "Analyzing travel preferences",
        "Accessing RAG knowledge base for unique insights",
        "Identifying required agent capabilities",
        "Creating multi-agent orchestration plan",
        "Optimizing agent execution sequence"
    ]
    
    progress_container = st.container()
    
    with progress_container:
        step_placeholders = [st.empty() for _ in range(len(planning_steps))]
        
        for idx, step in enumerate(planning_steps):
            # Show pending state for all
            for i in range(len(planning_steps)):
                if i < idx:
                    step_placeholders[i].markdown(f"""
                    <div style="padding: 1rem; margin: 0.5rem 0; background: rgba(14, 165, 233, 0.05); 
                         border-radius: 0.5rem; border-left: 4px solid #0ea5e9;">
                        <span style="color: #0ea5e9;">✓</span> <strong>{planning_steps[i]}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                elif i == idx:
                    step_placeholders[i].markdown(f"""
                    <div style="padding: 1rem; margin: 0.5rem 0; background: rgba(6, 182, 212, 0.1); 
                         border-radius: 0.5rem; border-left: 4px solid #06b6d4;">
                        <span style="color: #06b6d4;">⟳</span> <strong>{planning_steps[i]}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    step_placeholders[i].markdown(f"""
                    <div style="padding: 1rem; margin: 0.5rem 0; background: rgba(148, 163, 184, 0.05); 
                         border-radius: 0.5rem; border-left: 4px solid #cbd5e1;">
                        <span style="color: #94a3b8;">○</span> <span style="color: #94a3b8;">{planning_steps[i]}</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            time.sleep(1)
        
        # Show all complete
        for i in range(len(planning_steps)):
            step_placeholders[i].markdown(f"""
            <div style="padding: 1rem; margin: 0.5rem 0; background: rgba(14, 165, 233, 0.05); 
                 border-radius: 0.5rem; border-left: 4px solid #0ea5e9;">
                <span style="color: #0ea5e9;">✓</span> <strong>{planning_steps[i]}</strong>
            </div>
            """, unsafe_allow_html=True)
    
    # Summary card
    st.markdown("""
    <div style="background: linear-gradient(to right, rgba(14, 165, 233, 0.05), rgba(6, 182, 212, 0.05)); 
         padding: 2rem; border-radius: 1rem; border: 2px solid #0ea5e9; margin: 2rem 0;">
        <h3 style="color: #0ea5e9; margin-bottom: 1rem;">🧠 Orchestration Plan Ready</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Agents Required", "8")
    with col2:
        st.metric("RAG Queries", "12")
    with col3:
        st.metric("API Calls", "15")
    with col4:
        st.metric("Estimated Time", "30-45s")
    
    if st.button("Deploy Agents →", use_container_width=True):
        st.session_state.step = 'execution'
        st.rerun()

# Screen 4: Agent Execution
def show_agent_execution():
    st.markdown('<h1 class="gradient-text" style="text-align: center; font-size: 2rem;">Agents Executing Your Plan</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #64748b; margin-bottom: 2rem;">Multiple specialized agents are gathering real-time data for your trip</p>', unsafe_allow_html=True)
    
    agents = [
        {"name": "Weather Analysis", "icon": "☁️", "color": "#3b82f6"},
        {"name": "Safety & Geopolitical", "icon": "🌐", "color": "#10b981"},
        {"name": "Flight Options", "icon": "✈️", "color": "#8b5cf6"},
        {"name": "Hotel Bookings", "icon": "🏨", "color": "#f59e0b"},
        {"name": "Local Transport", "icon": "🚗", "color": "#eab308"},
        {"name": "Shopping & Markets", "icon": "🛍️", "color": "#ec4899"},
        {"name": "Language Support", "icon": "🗣️", "color": "#6366f1"},
        {"name": "Local Attractions", "icon": "📍", "color": "#14b8a6"}
    ]
    
    col1, col2 = st.columns(2)
    
    agent_placeholders = []
    for idx, agent in enumerate(agents):
        with col1 if idx % 2 == 0 else col2:
            agent_placeholders.append(st.empty())
    
    # Simulate agent execution
    for idx, agent in enumerate(agents):
        # Show queued state
        for i, placeholder in enumerate(agent_placeholders):
            if i < idx:
                placeholder.markdown(f"""
                <div class="agent-card" style="border-left-color: {agents[i]['color']}; 
                     background: rgba(14, 165, 233, 0.05);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 1.5rem;">{agents[i]['icon']}</span>
                            <strong style="margin-left: 0.5rem;">{agents[i]['name']}</strong>
                        </div>
                        <span style="color: #0ea5e9;">✓ Complete</span>
                    </div>
                    <div style="margin-top: 0.5rem; background: #e0f2fe; height: 8px; border-radius: 4px;">
                        <div style="background: linear-gradient(to right, #0ea5e9, #06b6d4); 
                             width: 100%; height: 100%; border-radius: 4px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            elif i == idx:
                placeholder.markdown(f"""
                <div class="agent-card" style="border-left-color: {agents[i]['color']}; 
                     background: rgba(6, 182, 212, 0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 1.5rem;">{agents[i]['icon']}</span>
                            <strong style="margin-left: 0.5rem;">{agents[i]['name']}</strong>
                        </div>
                        <span style="color: #06b6d4;">⟳ Running...</span>
                    </div>
                    <div style="margin-top: 0.5rem; background: #e0f2fe; height: 8px; border-radius: 4px;">
                        <div style="background: linear-gradient(to right, #0ea5e9, #06b6d4); 
                             width: 50%; height: 100%; border-radius: 4px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                placeholder.markdown(f"""
                <div class="agent-card" style="border-left-color: {agents[i]['color']}; 
                     background: rgba(148, 163, 184, 0.05);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 1.5rem;">{agents[i]['icon']}</span>
                            <strong style="margin-left: 0.5rem; color: #94a3b8;">{agents[i]['name']}</strong>
                        </div>
                        <span style="color: #94a3b8;">Queued</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        time.sleep(0.8)
    
    # Show all complete
    for i, placeholder in enumerate(agent_placeholders):
        placeholder.markdown(f"""
        <div class="agent-card" style="border-left-color: {agents[i]['color']}; 
             background: rgba(14, 165, 233, 0.05);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-size: 1.5rem;">{agents[i]['icon']}</span>
                    <strong style="margin-left: 0.5rem;">{agents[i]['name']}</strong>
                </div>
                <span style="color: #0ea5e9;">✓ Complete</span>
            </div>
            <div style="margin-top: 0.5rem; background: #e0f2fe; height: 8px; border-radius: 4px;">
                <div style="background: linear-gradient(to right, #0ea5e9, #06b6d4); 
                     width: 100%; height: 100%; border-radius: 4px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Summary
    st.markdown("""
    <div style="background: linear-gradient(to right, rgba(14, 165, 233, 0.1), rgba(6, 182, 212, 0.1)); 
         padding: 2rem; border-radius: 1rem; margin: 2rem 0;">
        <h3 style="color: #0ea5e9;">All Agents Completed Successfully! ✨</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total API Calls", "23")
    with col2:
        st.metric("RAG Retrievals", "12")
    with col3:
        st.metric("Processing Time", "38s")
    
    if st.button("View Results →", use_container_width=True):
        st.session_state.step = 'results'
        st.rerun()

# Screen 5: Results
def show_results():
    st.markdown('<h1 class="gradient-text" style="text-align: center; font-size: 2rem;">Your Personalized Travel Plan</h1>', unsafe_allow_html=True)
    destination = st.session_state.travel_data.get('destination', 'your destination')
    st.markdown(f'<p style="text-align: center; color: #64748b; margin-bottom: 2rem;">AI-Generated Itinerary for {destination}</p>', unsafe_allow_html=True)
    
    # Travel Summary
    st.markdown("### 📊 Travel Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📍 Destination", st.session_state.travel_data.get('destination'))
    with col2:
        st.metric("📅 Duration", f"{st.session_state.travel_data.get('duration')} days")
    with col3:
        st.metric("💰 Budget", f"${st.session_state.travel_data.get('budget')}")
    with col4:
        st.metric("✈️ Style", st.session_state.travel_data.get('travel_style'))
    
    st.markdown("**Interests:** " + ", ".join(st.session_state.travel_data.get('interests', [])))
    
    # RAG Insights
    st.markdown("---")
    st.markdown("### 🧠 Exclusive Destination Insights")
    st.markdown('<p style="color: #64748b; margin-bottom: 1rem;">Powered by our proprietary RAG knowledge base with insider information</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="insight-card">
            <h4>📖 Hidden Gems</h4>
            <p style="color: #64748b; font-size: 0.9rem;">Secret waterfall accessible only through local guide network. Exclusive beach cove known to locals. Traditional cooking class with family recipes.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-card">
            <h4>📅 Best Times to Visit</h4>
            <p style="color: #64748b; font-size: 0.9rem;">Optimal weather: Mid-April to early June. Avoid monsoon: July-September. Festival season: March brings authentic cultural experiences.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="insight-card">
            <h4>🌐 Local Secrets</h4>
            <p style="color: #64748b; font-size: 0.9rem;">Morning markets open at 5 AM with freshest produce. Sunset viewpoint behind temple - locals only spot. Traditional healer offers authentic wellness treatments.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Agent Results
    st.markdown("---")
    st.markdown("### 🤖 Detailed Agent Reports")
    
    with st.expander("☁️ Weather Analysis", expanded=False):
        st.markdown("""
        - **Current Conditions**: Sunny, 28°C (82°F)
        - **7-Day Forecast**: Mostly sunny with occasional clouds
        - **Best Time**: Early morning (6-9 AM) and late afternoon (4-7 PM)
        - **UV Index**: High (8/10) - sunscreen recommended
        - **Humidity**: 65% average
        """)
    
    with st.expander("🌐 Safety & Geopolitical", expanded=False):
        st.markdown("""
        - **Safety Rating**: 4.5/5 - Very Safe
        - **Travel Advisories**: None active
        - **Local Stability**: Stable political climate
        - **Health Requirements**: Standard vaccinations recommended
        - **Emergency Contacts**: Embassy +XX-XXX-XXXX
        """)
    
    with st.expander("✈️ Flight Options", expanded=False):
        st.markdown("""
        - **Best Price**: $850 round trip (Economy)
        - **Airlines**: Emirates, Singapore Airlines, Qatar Airways
        - **Flight Duration**: 14 hours (1 stop)
        - **Best Deals**: Tuesday/Wednesday departures
        - **Airport**: International Airport (XXX)
        """)
    
    with st.expander("🏨 Hotel Bookings", expanded=False):
        st.markdown("""
        - **Luxury Option**: Ocean Resort & Spa ($280/night)
        - **Mid-Range**: Seaside Hotel ($120/night)
        - **Budget**: Beachfront Hostel ($35/night)
        - **Recommended**: Based on your '{style}' preference
        - **Amenities**: Pool, WiFi, Breakfast included
        """.format(style=st.session_state.travel_data.get('travel_style', 'Comfort')))
    
    with st.expander("🚗 Local Transport", expanded=False):
        st.markdown("""
        - **Airport Transfer**: $25 (shared), $50 (private)
        - **Daily Rental**: Scooter ($10/day), Car ($40/day)
        - **Ride-hailing**: Available - Grab, GoJek
        - **Public Transport**: Bus system ($1/ride)
        - **Bike Rental**: $5/day for exploring
        """)
    
    with st.expander("🛍️ Shopping & Markets", expanded=False):
        st.markdown("""
        - **Main Market**: Traditional crafts and souvenirs
        - **Night Market**: Friday-Sunday, 6 PM - 11 PM
        - **Shopping District**: Modern malls with international brands
        - **Bargaining**: Expected at markets (start at 50%)
        - **Must-Buy**: Local textiles, handcrafted jewelry
        """)
    
    with st.expander("🗣️ Language Support", expanded=False):
        st.markdown("""
        - **Primary Language**: Local language
        - **English Proficiency**: Moderate in tourist areas
        - **Essential Phrases**: "Hello", "Thank you", "How much?"
        - **Translation Apps**: Google Translate works offline
        - **Cultural Tips**: Respectful greetings appreciated
        """)
    
    with st.expander("📍 Local Attractions", expanded=False):
        st.markdown("""
        - **Top Rated**: Ancient Temple Complex (4.8★)
        - **Nature**: Waterfall Trek (3 hours)
        - **Cultural**: Traditional Dance Show (evening)
        - **Adventure**: Snorkeling & Diving
        - **Relaxation**: Spa & Wellness Centers
        """)
    
    # Download Options
    st.markdown("---")
    st.markdown("### 📥 Download Your Travel Plan")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Download PDF", use_container_width=True):
            pdf_gen = PDFGenerator()
            pdf_path = pdf_gen.generate_itinerary(st.session_state.travel_data)
            with open(pdf_path, 'rb') as f:
                st.download_button(
                    label="💾 Save PDF",
                    data=f,
                    file_name=f"voyage_ai_itinerary_{destination.replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )
    
    with col2:
        if st.button("📊 Download CSV", use_container_width=True):
            df = pd.DataFrame([st.session_state.travel_data])
            csv = df.to_csv(index=False)
            st.download_button(
                label="💾 Save CSV",
                data=csv,
                file_name=f"voyage_ai_data_{destination.replace(' ', '_')}.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("💻 Download JSON", use_container_width=True):
            json_data = json.dumps(st.session_state.travel_data, indent=2)
            st.download_button(
                label="💾 Save JSON",
                data=json_data,
                file_name=f"voyage_ai_data_{destination.replace(' ', '_')}.json",
                mime="application/json"
            )
    
    # Action Buttons
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Plan Another Trip", use_container_width=True):
            st.session_state.step = 'welcome'
            st.session_state.travel_data = {}
            st.rerun()
    
    with col2:
        if st.button("✏️ Refine This Plan", use_container_width=True):
            st.session_state.step = 'collection'
            st.rerun()

# Main App
def main():
    # Header
    st.markdown('<h1 class="gradient-text" style="text-align: center; font-size: 3rem; margin: 1rem 0;">VoyageAI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #64748b; font-size: 1.125rem; margin-bottom: 2rem;">Your AI-Powered Travel Orchestrator</p>', unsafe_allow_html=True)
    
    # Progress Indicator
    show_progress()
    
    # Route to appropriate screen
    if st.session_state.step == 'welcome':
        show_welcome()
    elif st.session_state.step == 'collection':
        show_data_collection()
    elif st.session_state.step == 'orchestrator':
        show_orchestrator()
    elif st.session_state.step == 'execution':
        show_agent_execution()
    elif st.session_state.step == 'results':
        show_results()

if __name__ == "__main__":
    main()
