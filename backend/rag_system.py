"""
RAG (Retrieval-Augmented Generation) System
Handles vector database operations and knowledge retrieval
"""

import openai
from typing import List, Dict, Any
import numpy as np
from pymongo import MongoClient
from config.settings import Settings
import json

class RAGSystem:
    """
    RAG system using MongoDB as vector database and Azure OpenAI for embeddings
    """
    
    def __init__(self):
        self.settings = Settings()
        
        # Initialize Azure OpenAI client
        self.client = openai.AzureOpenAI(
            api_key=self.settings.AZURE_OPENAI_API_KEY,
            api_version=self.settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=self.settings.AZURE_OPENAI_ENDPOINT
        )
        
        # Initialize MongoDB connection for vector storage
        try:
            self.mongo_client = MongoClient(self.settings.MONGODB_URI)
            self.db = self.mongo_client[self.settings.MONGODB_DATABASE]
            self.collection = self.db['travel_knowledge']
            self._initialize_knowledge_base()
        except Exception as e:
            print(f"MongoDB connection warning: {e}")
            self.mongo_client = None
            self.db = None
            self.collection = None
    
    def _initialize_knowledge_base(self):
        """Initialize the knowledge base with sample travel insights"""
        
        # Sample unique travel knowledge
        unique_knowledge = [
            {
                "destination": "Bali",
                "category": "hidden_gems",
                "content": "Secret waterfall Tukad Cepung accessible only through narrow canyon. Local guide network knows precise timing when sunlight creates magical beam effect. Best visited 10-11 AM during dry season.",
                "metadata": {"type": "location", "exclusivity": "high"}
            },
            {
                "destination": "Bali",
                "category": "local_secrets",
                "content": "Traditional Balinese healer Mangku Made in Ubud offers authentic healing ceremonies. Family has practiced for 9 generations. Sessions include spiritual cleansing and herbal treatments unknown to tourists.",
                "metadata": {"type": "experience", "exclusivity": "high"}
            },
            {
                "destination": "Bali",
                "category": "best_times",
                "content": "Optimal visit period: Mid-April to early June. Post-rainy season means lush landscapes, fewer crowds than peak July-August. Galungan festival in April offers authentic cultural immersion.",
                "metadata": {"type": "timing", "exclusivity": "medium"}
            },
            {
                "destination": "Paris",
                "category": "hidden_gems",
                "content": "Musée de la Chasse et de la Nature - intimate museum in Marais combining art and natural history. Secret courtyard gardens accessible only to visitors. Curated by renowned designer.",
                "metadata": {"type": "location", "exclusivity": "high"}
            },
            {
                "destination": "Paris",
                "category": "local_secrets",
                "content": "Marché des Enfants Rouges - oldest covered market (1615) frequented by locals. Vendors offer Moroccan, Lebanese, Italian specialties. Visit Tuesday/Saturday mornings for best selection before tourist rush.",
                "metadata": {"type": "food", "exclusivity": "medium"}
            },
            {
                "destination": "Tokyo",
                "category": "hidden_gems",
                "content": "Yanaka district preserves old Tokyo atmosphere. Family-run shops operated for 100+ years. Cat-themed shopping street Yanaka Ginza offers authentic local experience away from tourist centers.",
                "metadata": {"type": "location", "exclusivity": "high"}
            },
            {
                "destination": "Tokyo",
                "category": "local_secrets",
                "content": "Tsukiji Outer Market opens 5 AM. Local fishmongers and restaurants serve breakfast sushi using same fish as high-end establishments at fraction of price. Arrive before 7 AM.",
                "metadata": {"type": "food", "exclusivity": "medium"}
            },
            {
                "destination": "Santorini",
                "category": "hidden_gems",
                "content": "Pyrgos village offers authentic Greek experience without Oia crowds. Kasteli viewpoint provides panoramic sunset views. Local taverna Metaxi Mas serves traditional recipes known only to islanders.",
                "metadata": {"type": "location", "exclusivity": "high"}
            },
            {
                "destination": "Santorini",
                "category": "best_times",
                "content": "Late May and early October ideal. Post-Easter means open establishments, pre-summer crowds. Water temperature suitable, accommodations 40% cheaper than June-September peak.",
                "metadata": {"type": "timing", "exclusivity": "low"}
            },
            {
                "destination": "Dubai",
                "category": "local_secrets",
                "content": "Al Fahidi district morning walking tours with Emirati guides reveal pre-oil Dubai. Traditional wind-tower architecture and pearl diving history. Book through Dubai Culture & Arts Authority for authentic experience.",
                "metadata": {"type": "culture", "exclusivity": "medium"}
            }
        ]
        
        # Check if collection exists and has data
        if self.collection is not None:
            try:
                if self.collection.count_documents({}) == 0:
                    # Add embeddings to knowledge items
                    for item in unique_knowledge:
                        embedding = self._create_embedding(item['content'])
                        item['embedding'] = embedding
                        self.collection.insert_one(item)
                    print(f"Initialized knowledge base with {len(unique_knowledge)} items")
            except Exception as e:
                print(f"Knowledge base initialization warning: {e}")
    
    def _create_embedding(self, text: str) -> List[float]:
        """Create embedding using Azure OpenAI"""
        try:
            response = self.client.embeddings.create(
                model=self.settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Embedding creation warning: {e}")
            # Return dummy embedding for demo
            return [0.1] * 1536
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        vec1_array = np.array(vec1)
        vec2_array = np.array(vec2)
        
        dot_product = np.dot(vec1_array, vec2_array)
        norm1 = np.linalg.norm(vec1_array)
        norm2 = np.linalg.norm(vec2_array)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def retrieve_knowledge(self, query: str, destination: str = None, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant knowledge using RAG
        """
        # Create query embedding
        query_embedding = self._create_embedding(query)
        
        # Mock retrieval if MongoDB not available
        if self.collection is None:
            return self._mock_retrieval(query, destination, top_k)
        
        try:
            # Build MongoDB filter
            filter_query = {}
            if destination:
                filter_query['destination'] = {"$regex": destination, "$options": "i"}
            
            # Retrieve all documents matching filter
            documents = list(self.collection.find(filter_query))
            
            if not documents:
                return self._mock_retrieval(query, destination, top_k)
            
            # Calculate similarity scores
            scored_docs = []
            for doc in documents:
                if 'embedding' in doc:
                    similarity = self._cosine_similarity(query_embedding, doc['embedding'])
                    scored_docs.append({
                        "content": doc['content'],
                        "category": doc['category'],
                        "destination": doc['destination'],
                        "metadata": doc.get('metadata', {}),
                        "similarity_score": similarity
                    })
            
            # Sort by similarity and return top_k
            scored_docs.sort(key=lambda x: x['similarity_score'], reverse=True)
            return scored_docs[:top_k]
            
        except Exception as e:
            print(f"Retrieval warning: {e}")
            return self._mock_retrieval(query, destination, top_k)
    
    def _mock_retrieval(self, query: str, destination: str = None, top_k: int = 5) -> List[Dict[str, Any]]:
        """Mock retrieval for demo purposes"""
        mock_results = [
            {
                "content": f"Exclusive insider tip for {destination or 'this destination'}: Hidden local restaurant known only to residents serves authentic cuisine at exceptional value.",
                "category": "local_secrets",
                "destination": destination or "Unknown",
                "metadata": {"type": "food", "exclusivity": "high"},
                "similarity_score": 0.92
            },
            {
                "content": f"Best time to visit {destination or 'this destination'}: Shoulder season offers 30% savings on accommodation with perfect weather conditions.",
                "category": "best_times",
                "destination": destination or "Unknown",
                "metadata": {"type": "timing", "exclusivity": "medium"},
                "similarity_score": 0.88
            },
            {
                "content": f"Hidden gem in {destination or 'this destination'}: Secluded viewpoint accessible through unmarked trail. Locals gather here for sunset.",
                "category": "hidden_gems",
                "destination": destination or "Unknown",
                "metadata": {"type": "location", "exclusivity": "high"},
                "similarity_score": 0.85
            }
        ]
        
        return mock_results[:top_k]
    
    def add_knowledge(self, destination: str, category: str, content: str, metadata: Dict[str, Any] = None) -> bool:
        """
        Add new knowledge to the database
        """
        if self.collection is None:
            print("MongoDB not available - knowledge not persisted")
            return False
        
        try:
            embedding = self._create_embedding(content)
            
            document = {
                "destination": destination,
                "category": category,
                "content": content,
                "metadata": metadata or {},
                "embedding": embedding,
                "created_at": "2024-01-01"
            }
            
            self.collection.insert_one(document)
            return True
            
        except Exception as e:
            print(f"Add knowledge warning: {e}")
            return False
    
    def get_insights_for_destination(self, destination: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get categorized insights for a specific destination
        """
        categories = ["hidden_gems", "local_secrets", "best_times"]
        insights = {}
        
        for category in categories:
            query = f"{category} for {destination}"
            results = self.retrieve_knowledge(query, destination, top_k=3)
            insights[category] = results
        
        return insights
    
    def enhance_agent_context(self, agent_type: str, travel_data: Dict[str, Any]) -> str:
        """
        Enhance agent context with RAG knowledge
        """
        destination = travel_data.get('destination', '')
        
        # Create query based on agent type
        query_map = {
            'weather_analysis': f"weather patterns and best times for {destination}",
            'local_attractions': f"hidden attractions and must-see places in {destination}",
            'hotel_bookings': f"best areas to stay and accommodation tips for {destination}",
            'shopping_markets': f"local markets and authentic shopping in {destination}",
            'language_support': f"communication tips and local customs in {destination}"
        }
        
        query = query_map.get(agent_type, f"travel tips for {destination}")
        
        # Retrieve relevant knowledge
        knowledge = self.retrieve_knowledge(query, destination, top_k=3)
        
        # Format as context string
        context = "\n".join([f"- {item['content']}" for item in knowledge])
        
        return context
    
    def generate_rag_enhanced_response(self, query: str, context: Dict[str, Any]) -> str:
        """
        Generate AI response enhanced with RAG knowledge
        """
        destination = context.get('destination', '')
        
        # Retrieve relevant knowledge
        relevant_knowledge = self.retrieve_knowledge(query, destination, top_k=3)
        
        # Build context from retrieved knowledge
        knowledge_context = "\n".join([
            f"Insight: {item['content']}" 
            for item in relevant_knowledge
        ])
        
        # Generate response using LLM
        prompt = f"""
        Based on the following exclusive travel insights:
        
        {knowledge_context}
        
        Query: {query}
        Destination: {destination}
        
        Provide a helpful, personalized response incorporating these unique insights.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.settings.AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "You are an expert travel advisor with access to exclusive destination knowledge."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Response generation warning: {e}")
            return f"Based on our exclusive knowledge, {destination} offers unique experiences. {relevant_knowledge[0]['content'] if relevant_knowledge else ''}"
