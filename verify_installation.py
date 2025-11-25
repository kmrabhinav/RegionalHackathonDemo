"""
VoyageAI - Installation Verification Script
Checks if all dependencies and configurations are correct
"""

import sys
import os

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ⚠ Warning: Python 3.8+ recommended")
        return False
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = {
        'streamlit': 'Streamlit',
        'openai': 'OpenAI',
        'psycopg2': 'PostgreSQL (psycopg2-binary)',
        'pymongo': 'MongoDB (pymongo)',
        'reportlab': 'ReportLab',
        'pandas': 'Pandas',
        'numpy': 'NumPy'
    }
    
    print("\nChecking dependencies...")
    all_installed = True
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"✓ {name}")
        except ImportError:
            print(f"✗ {name} - NOT INSTALLED")
            all_installed = False
    
    return all_installed

def check_env_file():
    """Check if .env file exists"""
    print("\nChecking configuration...")
    if os.path.exists('.env'):
        print("✓ .env file found")
        return True
    else:
        print("⚠ .env file not found (optional for demo mode)")
        print("  Run: cp .env.example .env")
        return False

def check_databases():
    """Check database connectivity"""
    print("\nChecking database connections...")
    
    # PostgreSQL
    try:
        import psycopg2
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='postgres',
            user='postgres',
            password='postgres'
        )
        conn.close()
        print("✓ PostgreSQL connection successful")
        pg_available = True
    except Exception as e:
        print("⚠ PostgreSQL not available (optional for demo mode)")
        pg_available = False
    
    # MongoDB
    try:
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
        client.server_info()
        print("✓ MongoDB connection successful")
        mongo_available = True
    except Exception as e:
        print("⚠ MongoDB not available (optional for demo mode)")
        mongo_available = False
    
    return pg_available, mongo_available

def check_azure_config():
    """Check Azure OpenAI configuration"""
    print("\nChecking Azure OpenAI configuration...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except:
        pass
    
    api_key = os.getenv('AZURE_OPENAI_API_KEY')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    
    if api_key and api_key != 'your-azure-openai-api-key':
        print("✓ Azure OpenAI API key configured")
        azure_configured = True
    else:
        print("⚠ Azure OpenAI not configured (optional for demo mode)")
        azure_configured = False
    
    return azure_configured

def check_project_structure():
    """Check if all required files exist"""
    print("\nChecking project structure...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'backend/orchestrator.py',
        'backend/agents.py',
        'backend/rag_system.py',
        'backend/database.py',
        'backend/mock_apis.py',
        'config/settings.py',
        'utils/pdf_generator.py'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ {file} - MISSING")
            all_exist = False
    
    return all_exist

def main():
    """Run all checks"""
    print("=" * 60)
    print("VoyageAI - Installation Verification")
    print("=" * 60)
    
    # Run checks
    python_ok = check_python_version()
    deps_ok = check_dependencies()
    env_exists = check_env_file()
    pg_ok, mongo_ok = check_databases()
    azure_ok = check_azure_config()
    structure_ok = check_project_structure()
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    if python_ok and deps_ok and structure_ok:
        print("✓ READY FOR DEMO MODE")
        print("  Run: streamlit run app.py")
        print("\n✓ Application will work with mock data")
    else:
        print("✗ INSTALLATION INCOMPLETE")
        print("  Run: pip install -r requirements.txt")
    
    if env_exists and azure_ok:
        print("\n✓ READY FOR AI MODE")
        print("  Azure OpenAI integration enabled")
    else:
        print("\n⚠ Azure OpenAI not configured")
        print("  Edit .env file to enable AI features")
    
    if pg_ok and mongo_ok:
        print("\n✓ READY FOR FULL MODE")
        print("  Database persistence enabled")
    else:
        print("\n⚠ Databases not available")
        print("  Start PostgreSQL and MongoDB for persistence")
    
    print("\n" + "=" * 60)
    print("Quick Start Commands")
    print("=" * 60)
    print("1. Demo Mode (no setup needed):")
    print("   streamlit run app.py")
    print("\n2. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("\n3. Setup databases:")
    print("   python setup_database.py")
    print("\n4. Configure Azure:")
    print("   cp .env.example .env")
    print("   # Edit .env with your credentials")
    print("=" * 60)

if __name__ == "__main__":
    main()
