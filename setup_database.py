"""
Database Setup Script
Initializes PostgreSQL and MongoDB with schema and sample data
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import DatabaseManager
from backend.rag_system import RAGSystem

def setup_databases():
    """
    Set up all databases with schema and initial data
    """
    print("=" * 60)
    print("VoyageAI Database Setup")
    print("=" * 60)
    
    # Initialize database manager
    print("\n1. Initializing database connections...")
    db_manager = DatabaseManager()
    
    # Generate and insert synthetic data
    print("\n2. Generating synthetic data...")
    
    # Generate 10 synthetic users
    users = db_manager.generate_synthetic_users(count=10)
    print(f"   Generated {len(users)} users")
    
    # Generate travel plans for first user
    travel_plans = db_manager.generate_synthetic_travel_plans(user_id=1, count=5)
    print(f"   Generated {len(travel_plans)} travel plans")
    
    # Insert into database
    print("\n3. Inserting synthetic data into PostgreSQL...")
    success = db_manager.insert_synthetic_data(users, travel_plans)
    
    if success:
        print("   ✓ Synthetic data inserted successfully")
    else:
        print("   ✗ Failed to insert synthetic data (PostgreSQL may not be running)")
    
    # Initialize RAG system
    print("\n4. Initializing RAG knowledge base...")
    rag_system = RAGSystem()
    print("   ✓ RAG system initialized with travel knowledge")
    
    # Test RAG retrieval
    print("\n5. Testing RAG retrieval...")
    test_results = rag_system.retrieve_knowledge("hidden gems", "Bali", top_k=3)
    print(f"   Retrieved {len(test_results)} knowledge items")
    
    if test_results:
        print("\n   Sample retrieval:")
        print(f"   - {test_results[0].get('content', 'N/A')[:100]}...")
    
    # Close connections
    db_manager.close_connections()
    
    print("\n" + "=" * 60)
    print("Database setup completed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Configure your .env file with Azure OpenAI credentials")
    print("2. Start PostgreSQL and MongoDB services if not running")
    print("3. Run: streamlit run app.py")
    print("=" * 60)

if __name__ == "__main__":
    setup_databases()
