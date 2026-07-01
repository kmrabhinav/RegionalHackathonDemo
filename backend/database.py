"""
Database Manager Module
Handles PostgreSQL for operational data and MongoDB for vector storage
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from pymongo import MongoClient
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from config.settings import Settings

class DatabaseManager:
    """
    Manages both PostgreSQL (operational data) and MongoDB (vector data)
    """
    
    def __init__(self):
        self.settings = Settings()
        self._initialize_postgresql()
        self._initialize_mongodb()
    
    def _initialize_postgresql(self):
        """Initialize PostgreSQL connection and create tables"""
        try:
            self.pg_conn = psycopg2.connect(
                host=self.settings.POSTGRES_HOST,
                port=self.settings.POSTGRES_PORT,
                database=self.settings.POSTGRES_DATABASE,
                user=self.settings.POSTGRES_USER,
                password=self.settings.POSTGRES_PASSWORD
            )
            self._create_tables()
            print("PostgreSQL connected successfully")
        except Exception as e:
            print(f"PostgreSQL connection warning: {e}")
            self.pg_conn = None
    
    def _initialize_mongodb(self):
        """Initialize MongoDB connection"""
        try:
            self.mongo_client = MongoClient(self.settings.MONGODB_URI)
            self.mongo_db = self.mongo_client[self.settings.MONGODB_DATABASE]
            print("MongoDB connected successfully")
        except Exception as e:
            print(f"MongoDB connection warning: {e}")
            self.mongo_client = None
            self.mongo_db = None
    
    def _create_tables(self):
        """Create necessary PostgreSQL tables"""
        if self.pg_conn is None:
            return
        
        try:
            cursor = self.pg_conn.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    email VARCHAR(255) UNIQUE,
                    name VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            """)
            
            # Travel Plans table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS travel_plans (
                    plan_id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(user_id),
                    destination VARCHAR(255) NOT NULL,
                    budget DECIMAL(10, 2),
                    duration INTEGER,
                    travel_style VARCHAR(50),
                    interests TEXT[],
                    status VARCHAR(50) DEFAULT 'draft',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Agent Executions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agent_executions (
                    execution_id SERIAL PRIMARY KEY,
                    plan_id INTEGER REFERENCES travel_plans(plan_id),
                    agent_name VARCHAR(100) NOT NULL,
                    status VARCHAR(50),
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    result_summary TEXT,
                    error_message TEXT
                )
            """)
            
            # RAG Queries table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rag_queries (
                    query_id SERIAL PRIMARY KEY,
                    plan_id INTEGER REFERENCES travel_plans(plan_id),
                    query_text TEXT NOT NULL,
                    destination VARCHAR(255),
                    results_count INTEGER,
                    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Bookings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bookings (
                    booking_id SERIAL PRIMARY KEY,
                    plan_id INTEGER REFERENCES travel_plans(plan_id),
                    booking_type VARCHAR(50) NOT NULL,
                    provider VARCHAR(255),
                    booking_reference VARCHAR(255),
                    price DECIMAL(10, 2),
                    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    travel_date DATE,
                    status VARCHAR(50) DEFAULT 'pending'
                )
            """)
            
            # User Preferences table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    preference_id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(user_id),
                    preference_type VARCHAR(100),
                    preference_value TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            self.pg_conn.commit()
            cursor.close()
            print("PostgreSQL tables created/verified successfully")
            
        except Exception as e:
            print(f"Table creation warning: {e}")
            if self.pg_conn:
                self.pg_conn.rollback()
    
    # ==================== Travel Plan Operations ====================
    
    def create_travel_plan(self, user_id: int, travel_data: Dict[str, Any]) -> Optional[int]:
        """Create a new travel plan"""
        if self.pg_conn is None:
            return None
        
        try:
            cursor = self.pg_conn.cursor()
            
            cursor.execute("""
                INSERT INTO travel_plans 
                (user_id, destination, budget, duration, travel_style, interests, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING plan_id
            """, (
                user_id,
                travel_data.get('destination'),
                travel_data.get('budget'),
                travel_data.get('duration'),
                travel_data.get('travel_style'),
                travel_data.get('interests', []),
                'created'
            ))
            
            plan_id = cursor.fetchone()[0]
            self.pg_conn.commit()
            cursor.close()
            
            return plan_id
            
        except Exception as e:
            print(f"Create travel plan error: {e}")
            if self.pg_conn:
                self.pg_conn.rollback()
            return None
    
    def get_travel_plan(self, plan_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a travel plan by ID"""
        if self.pg_conn is None:
            return None
        
        try:
            cursor = self.pg_conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT * FROM travel_plans WHERE plan_id = %s
            """, (plan_id,))
            
            plan = cursor.fetchone()
            cursor.close()
            
            return dict(plan) if plan else None
            
        except Exception as e:
            print(f"Get travel plan error: {e}")
            return None
    
    def update_travel_plan_status(self, plan_id: int, status: str) -> bool:
        """Update travel plan status"""
        if self.pg_conn is None:
            return False
        
        try:
            cursor = self.pg_conn.cursor()
            
            cursor.execute("""
                UPDATE travel_plans 
                SET status = %s, updated_at = CURRENT_TIMESTAMP
                WHERE plan_id = %s
            """, (status, plan_id))
            
            self.pg_conn.commit()
            cursor.close()
            
            return True
            
        except Exception as e:
            print(f"Update travel plan error: {e}")
            if self.pg_conn:
                self.pg_conn.rollback()
            return False
    
    # ==================== Agent Execution Operations ====================
    
    def log_agent_execution(self, plan_id: int, agent_name: str, status: str, 
                           result_summary: str = None, error_message: str = None) -> bool:
        """Log agent execution details"""
        if self.pg_conn is None:
            return False
        
        try:
            cursor = self.pg_conn.cursor()
            
            cursor.execute("""
                INSERT INTO agent_executions 
                (plan_id, agent_name, status, start_time, result_summary, error_message)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP, %s, %s)
            """, (plan_id, agent_name, status, result_summary, error_message))
            
            self.pg_conn.commit()
            cursor.close()
            
            return True
            
        except Exception as e:
            print(f"Log agent execution error: {e}")
            if self.pg_conn:
                self.pg_conn.rollback()
            return False
    
    def get_agent_executions(self, plan_id: int) -> List[Dict[str, Any]]:
        """Get all agent executions for a plan"""
        if self.pg_conn is None:
            return []
        
        try:
            cursor = self.pg_conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT * FROM agent_executions 
                WHERE plan_id = %s 
                ORDER BY start_time DESC
            """, (plan_id,))
            
            executions = cursor.fetchall()
            cursor.close()
            
            return [dict(exe) for exe in executions]
            
        except Exception as e:
            print(f"Get agent executions error: {e}")
            return []
    
    # ==================== RAG Query Operations ====================
    
    def log_rag_query(self, plan_id: int, query_text: str, 
                     destination: str, results_count: int) -> bool:
        """Log RAG query for analytics"""
        if self.pg_conn is None:
            return False
        
        try:
            cursor = self.pg_conn.cursor()
            
            cursor.execute("""
                INSERT INTO rag_queries 
                (plan_id, query_text, destination, results_count)
                VALUES (%s, %s, %s, %s)
            """, (plan_id, query_text, destination, results_count))
            
            self.pg_conn.commit()
            cursor.close()
            
            return True
            
        except Exception as e:
            print(f"Log RAG query error: {e}")
            if self.pg_conn:
                self.pg_conn.rollback()
            return False
    
    # ==================== Synthetic Data Generation ====================
    
    def generate_synthetic_users(self, count: int = 10) -> List[Dict[str, Any]]:
        """Generate synthetic user data"""
        import random
        
        first_names = ["John", "Emma", "Michael", "Sophia", "William", "Olivia", "James", "Ava", "Robert", "Isabella"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        
        users = []
        
        for i in range(count):
            user = {
                "email": f"{first_names[i % 10].lower()}.{last_names[i % 10].lower()}{i}@example.com",
                "name": f"{random.choice(first_names)} {random.choice(last_names)}",
                "created_at": datetime.now().isoformat(),
                "last_login": datetime.now().isoformat()
            }
            users.append(user)
        
        return users
    
    def generate_synthetic_travel_plans(self, user_id: int, count: int = 5) -> List[Dict[str, Any]]:
        """Generate synthetic travel plans"""
        import random
        
        destinations = ["Bali", "Paris", "Tokyo", "New York", "Dubai", "Santorini", "Barcelona", "Maldives"]
        styles = ["Budget", "Comfort", "Luxury", "Adventure", "Romantic"]
        interests = ["Adventure", "Culture", "Food", "Nature", "Beaches", "History", "Shopping"]
        
        plans = []
        
        for i in range(count):
            plan = {
                "user_id": user_id,
                "destination": random.choice(destinations),
                "budget": random.randint(1000, 10000),
                "duration": random.randint(3, 14),
                "travel_style": random.choice(styles),
                "interests": random.sample(interests, k=random.randint(2, 4)),
                "status": random.choice(["draft", "planning", "confirmed", "completed"]),
                "created_at": datetime.now().isoformat()
            }
            plans.append(plan)
        
        return plans
    
    def insert_synthetic_data(self, users: List[Dict[str, Any]], 
                            plans: List[Dict[str, Any]]) -> bool:
        """Insert synthetic data into database"""
        if self.pg_conn is None:
            print("PostgreSQL not available - synthetic data not inserted")
            return False
        
        try:
            cursor = self.pg_conn.cursor()
            
            # Insert users
            for user in users:
                cursor.execute("""
                    INSERT INTO users (email, name, created_at, last_login)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (email) DO NOTHING
                """, (user['email'], user['name'], user['created_at'], user['last_login']))
            
            # Insert travel plans
            for plan in plans:
                cursor.execute("""
                    INSERT INTO travel_plans 
                    (user_id, destination, budget, duration, travel_style, interests, status, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    plan['user_id'], plan['destination'], plan['budget'],
                    plan['duration'], plan['travel_style'], plan['interests'],
                    plan['status'], plan['created_at']
                ))
            
            self.pg_conn.commit()
            cursor.close()
            
            print(f"Inserted {len(users)} users and {len(plans)} travel plans")
            return True
            
        except Exception as e:
            print(f"Insert synthetic data error: {e}")
            if self.pg_conn:
                self.pg_conn.rollback()
            return False
    
    # ==================== MongoDB Operations ====================
    
    def store_agent_result(self, agent_name: str, plan_id: int, result: Dict[str, Any]) -> bool:
        """Store detailed agent results in MongoDB"""
        if self.mongo_db is None:
            return False
        
        try:
            collection = self.mongo_db['agent_results']
            
            document = {
                "agent_name": agent_name,
                "plan_id": plan_id,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
            
            collection.insert_one(document)
            return True
            
        except Exception as e:
            print(f"Store agent result error: {e}")
            return False
    
    def get_agent_result(self, agent_name: str, plan_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve agent result from MongoDB"""
        if self.mongo_db is None:
            return None
        
        try:
            collection = self.mongo_db['agent_results']
            
            result = collection.find_one({
                "agent_name": agent_name,
                "plan_id": plan_id
            }, sort=[("timestamp", -1)])
            
            if result:
                result.pop('_id', None)  # Remove MongoDB ID
                return result
            
            return None
            
        except Exception as e:
            print(f"Get agent result error: {e}")
            return None
    
    def close_connections(self):
        """Close all database connections"""
        if self.pg_conn:
            self.pg_conn.close()
            print("PostgreSQL connection closed")
        
        if self.mongo_client:
            self.mongo_client.close()
            print("MongoDB connection closed")
