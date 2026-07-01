"""
AI Orchestrator Module
Handles the orchestration of multiple AI agents and RAG system
"""

import json
from typing import Dict, List, Any
from datetime import datetime
import openai
from config.settings import Settings

class TravelOrchestrator:
    """
    Main orchestrator that coordinates between RAG system and multiple agents
    """
    
    def __init__(self):
        self.settings = Settings()
        self.client = openai.AzureOpenAI(
            api_key=self.settings.AZURE_OPENAI_API_KEY,
            api_version=self.settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=self.settings.AZURE_OPENAI_ENDPOINT
        )
        self.orchestration_plan = None
        
    def analyze_preferences(self, travel_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze travel preferences and create initial understanding
        """
        prompt = f"""
        Analyze the following travel preferences and provide insights:
        
        Destination: {travel_data.get('destination')}
        Budget: ${travel_data.get('budget')}
        Duration: {travel_data.get('duration')} days
        Interests: {', '.join(travel_data.get('interests', []))}
        Travel Style: {travel_data.get('travel_style')}
        
        Provide a brief analysis of what kind of trip this should be.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.settings.AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "You are an expert travel planner."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            analysis = response.choices[0].message.content
            
            return {
                "status": "success",
                "analysis": analysis,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "error",
                "analysis": f"Mock analysis for {travel_data.get('destination')}",
                "error": str(e)
            }
    
    def create_orchestration_plan(self, travel_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a detailed plan for agent execution
        """
        plan = {
            "destination": travel_data.get('destination'),
            "agents_required": [
                {
                    "agent": "weather_analysis",
                    "priority": 1,
                    "estimated_time": 3,
                    "dependencies": []
                },
                {
                    "agent": "safety_geopolitical",
                    "priority": 1,
                    "estimated_time": 4,
                    "dependencies": []
                },
                {
                    "agent": "flight_options",
                    "priority": 2,
                    "estimated_time": 5,
                    "dependencies": ["weather_analysis"]
                },
                {
                    "agent": "hotel_bookings",
                    "priority": 2,
                    "estimated_time": 4,
                    "dependencies": ["safety_geopolitical"]
                },
                {
                    "agent": "local_transport",
                    "priority": 3,
                    "estimated_time": 3,
                    "dependencies": ["hotel_bookings"]
                },
                {
                    "agent": "shopping_markets",
                    "priority": 4,
                    "estimated_time": 3,
                    "dependencies": []
                },
                {
                    "agent": "language_support",
                    "priority": 4,
                    "estimated_time": 2,
                    "dependencies": []
                },
                {
                    "agent": "local_attractions",
                    "priority": 3,
                    "estimated_time": 4,
                    "dependencies": ["weather_analysis"]
                }
            ],
            "rag_queries_needed": 12,
            "api_calls_needed": 15,
            "estimated_total_time": "30-45 seconds",
            "created_at": datetime.now().isoformat()
        }
        
        self.orchestration_plan = plan
        return plan
    
    def optimize_execution_sequence(self, plan: Dict[str, Any]) -> List[str]:
        """
        Optimize the sequence of agent execution based on dependencies
        """
        agents = plan.get('agents_required', [])
        
        # Sort by priority and dependencies
        sorted_agents = sorted(agents, key=lambda x: (x['priority'], len(x['dependencies'])))
        
        execution_sequence = [agent['agent'] for agent in sorted_agents]
        
        return execution_sequence
    
    def generate_plan_summary(self, travel_data: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary of the orchestration plan
        """
        prompt = f"""
        Create a brief summary of the travel planning approach for:
        Destination: {travel_data.get('destination')}
        Duration: {travel_data.get('duration')} days
        Budget: ${travel_data.get('budget')}
        Style: {travel_data.get('travel_style')}
        
        Explain in 2-3 sentences what our AI agents will focus on.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.settings.AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "You are an expert travel planner."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Our AI agents will comprehensively analyze {travel_data.get('destination')}, focusing on your {travel_data.get('travel_style')} travel style and {', '.join(travel_data.get('interests', [])[:2])} interests."
    
    def validate_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the orchestration plan for completeness and feasibility
        """
        required_agents = ['weather_analysis', 'safety_geopolitical', 'flight_options', 'hotel_bookings']
        
        agents_in_plan = [agent['agent'] for agent in plan.get('agents_required', [])]
        
        missing_agents = [agent for agent in required_agents if agent not in agents_in_plan]
        
        is_valid = len(missing_agents) == 0
        
        return {
            "valid": is_valid,
            "missing_agents": missing_agents,
            "total_agents": len(agents_in_plan),
            "validation_timestamp": datetime.now().isoformat()
        }
