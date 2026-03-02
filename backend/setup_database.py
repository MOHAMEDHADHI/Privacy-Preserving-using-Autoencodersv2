"""
Complete database setup script
Creates all tables and verifies connection
"""
from database import engine, Base, SessionLocal
import models
from sqlalchemy import inspect

def setup_database():
    print("=" * 60)
    print("DATABASE SETUP")
    print("=" * 60)
    
    # Test connection
    print("\n1. Testing database connection...")
    try:
        with engine.connect() as conn:
            print("   ✅ Connected to PostgreSQL successfully")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return False
    
    # Create tables
    print("\n2. Creating tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("   ✅ Tables created successfully")
    except Exception as e:
        print(f"   ❌ Table creation failed: {e}")
        return False
    
    # Verify tables
    print("\n3. Verifying tables...")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    expected_tables = [
        'users',
        'datasets',
        'latent_vectors',
        'model_results',
        'privacy_attack_results'
    ]
    
    for table in expected_tables:
        if table in tables:
            print(f"   ✅ {table}")
        else:
            print(f"   ❌ {table} - MISSING")
    
    # Show table details
    print("\n4. Table schemas:")
    for table in expected_tables:
        if table in tables:
            columns = inspector.get_columns(table)
            print(f"\n   {table}:")
            for col in columns:
                print(f"      - {col['name']}: {col['type']}")
    
    print("\n" + "=" * 60)
    print("DATABASE SETUP COMPLETE")
    print("=" * 60)
    print("\nYou can now:")
    print("  1. Start the server: python backend/main.py")
    print("  2. Test the API: python backend/test_upload_latent.py")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    setup_database()
