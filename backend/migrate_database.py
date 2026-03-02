"""
Migrate database to add missing columns
"""
from database import engine
from sqlalchemy import text

def migrate_database():
    print("=" * 60)
    print("DATABASE MIGRATION")
    print("=" * 60)
    
    with engine.connect() as conn:
        # Add missing columns to latent_vectors
        print("\n1. Updating latent_vectors table...")
        try:
            conn.execute(text("ALTER TABLE latent_vectors ADD COLUMN IF NOT EXISTS labels TEXT"))
            conn.execute(text("ALTER TABLE latent_vectors ADD COLUMN IF NOT EXISTS sigma DOUBLE PRECISION"))
            conn.commit()
            print("   ✅ Added labels and sigma columns")
        except Exception as e:
            print(f"   ⚠️  Columns may already exist: {e}")
        
        # Add missing columns to model_results
        print("\n2. Updating model_results table...")
        try:
            conn.execute(text("ALTER TABLE model_results ADD COLUMN IF NOT EXISTS precision DOUBLE PRECISION"))
            conn.execute(text("ALTER TABLE model_results ADD COLUMN IF NOT EXISTS recall DOUBLE PRECISION"))
            conn.execute(text("ALTER TABLE model_results ADD COLUMN IF NOT EXISTS f1_score DOUBLE PRECISION"))
            conn.execute(text("ALTER TABLE model_results ADD COLUMN IF NOT EXISTS sigma DOUBLE PRECISION"))
            conn.commit()
            print("   ✅ Added precision, recall, f1_score, and sigma columns")
        except Exception as e:
            print(f"   ⚠️  Columns may already exist: {e}")
        
        # Verify columns
        print("\n3. Verifying latent_vectors columns...")
        result = conn.execute(text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'latent_vectors'
            ORDER BY ordinal_position
        """))
        for row in result:
            print(f"   - {row[0]}: {row[1]}")
        
        print("\n4. Verifying model_results columns...")
        result = conn.execute(text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'model_results'
            ORDER BY ordinal_position
        """))
        for row in result:
            print(f"   - {row[0]}: {row[1]}")
    
    print("\n" + "=" * 60)
    print("MIGRATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    migrate_database()
