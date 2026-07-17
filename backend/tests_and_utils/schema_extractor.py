from sqlalchemy import inspect
from db_connector import get_engine

def extract_schema_info() -> str:
    """
    Extracts tables, columns, types, primary keys, and foreign keys from the database
    and formats them as a clean text string for LLM injection.
    """
    engine = get_engine()
    inspector = inspect(engine)
    
    schema_lines = []
    
    # Get all table names
    table_names = inspector.get_table_names()
    
    for table_name in table_names:
        schema_lines.append(f"Table: {table_name}")
        
        # Get columns
        columns = inspector.get_columns(table_name)
        schema_lines.append("  Columns:")
        for col in columns:
            col_name = col['name']
            col_type = col['type']
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            
            # Check if primary key
            pk = " (PK)" if col.get('primary_key', 0) > 0 else ""
            
            schema_lines.append(f"    - {col_name} ({col_type}) {nullable}{pk}")
            
        # Get foreign keys
        foreign_keys = inspector.get_foreign_keys(table_name)
        if foreign_keys:
            schema_lines.append("  Foreign Keys:")
            for fk in foreign_keys:
                referred_table = fk['referred_table']
                referred_cols = ", ".join(fk['referred_columns'])
                schema_lines.append(f"    - {', '.join(fk['constrained_columns'])} -> {referred_table}({referred_cols})")
                
        schema_lines.append("") # Empty line between tables
        
    return "\n".join(schema_lines)

if __name__ == "__main__":
    try:
        schema_text = extract_schema_info()
        print("Successfully extracted database schema:\n")
        print("="*60)
        print(schema_text)
        print("="*60)
    except Exception as e:
        print(f"Error extracting schema: {e}")
