"""
Script pour initialiser les tables NocoDB à partir du schéma défini

Ce script crée toutes les tables nécessaires pour Mail2Tickets dans NocoDB.
Il peut être exécuté plusieurs fois (idempotent).
"""
import json
import sys
from pathlib import Path

# Ajouter le dossier src au path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.config import config
from utils.logger import get_logger

logger = get_logger("setup_nocodb")


def load_schema():
    """Charge le schéma de base de données"""
    schema_path = Path(__file__).parent.parent / "docs" / "database_schema.json"
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def print_schema_info(schema):
    """Affiche les informations du schéma"""
    db_schema = schema["database_schema"]
    print(f"\n{'='*60}")
    print(f"  {db_schema['name']}")
    print(f"  Version: {db_schema['version']}")
    print(f"{'='*60}\n")
    
    print(f"Tables à créer ({len(db_schema['tables'])} tables):\n")
    
    for table in db_schema['tables']:
        print(f"  📋 {table['name']}")
        print(f"     Description: {table['description']}")
        print(f"     Colonnes: {len(table['columns'])}")
        if 'indexes' in table:
            print(f"     Index: {len(table['indexes'])}")
        print()


def generate_sql_statements(schema):
    """Génère les statements SQL pour PostgreSQL"""
    db_schema = schema["database_schema"]
    statements = []
    
    # Ordre de création (en tenant compte des FK)
    table_order = [
        "categories",
        "clients",
        "sites", 
        "configuration_items",
        "tickets",
        "ticket_comments",
        "email_threads"
    ]
    
    tables_by_name = {t["name"]: t for t in db_schema["tables"]}
    
    for table_name in table_order:
        if table_name not in tables_by_name:
            continue
            
        table = tables_by_name[table_name]
        
        # CREATE TABLE
        cols = []
        for col in table["columns"]:
            col_def = f'  "{col["name"]}" {col["type"]}'
            
            if col.get("primary_key"):
                col_def += " PRIMARY KEY"
            
            if col.get("auto_increment") and "INTEGER" in col["type"]:
                col_def = f'  "{col["name"]}" SERIAL PRIMARY KEY'
            
            if col.get("unique") and not col.get("primary_key"):
                col_def += " UNIQUE"
            
            if col.get("nullable") is False:
                col_def += " NOT NULL"
            
            if "default" in col:
                default = col["default"]
                if default == "CURRENT_TIMESTAMP":
                    col_def += " DEFAULT CURRENT_TIMESTAMP"
                elif isinstance(default, bool):
                    col_def += f" DEFAULT {str(default).upper()}"
                elif isinstance(default, str):
                    col_def += f" DEFAULT '{default}'"
                else:
                    col_def += f" DEFAULT {default}"
            
            cols.append(col_def)
        
        create_stmt = f'CREATE TABLE IF NOT EXISTS "{table_name}" (\n'
        create_stmt += ',\n'.join(cols)
        create_stmt += '\n);'
        statements.append(create_stmt)
        
        # CREATE INDEXES
        if "indexes" in table:
            for idx in table["indexes"]:
                idx_name = f'{table_name}_{idx["name"]}'
                unique = "UNIQUE " if idx.get("unique") else ""
                cols_str = ', '.join([f'"{c}"' for c in idx["columns"]])
                idx_stmt = f'CREATE {unique}INDEX IF NOT EXISTS "{idx_name}" ON "{table_name}" ({cols_str});'
                statements.append(idx_stmt)
        
        statements.append("")  # Ligne vide entre tables
    
    return statements


def save_sql_file(statements):
    """Sauvegarde les statements SQL dans un fichier"""
    sql_path = Path(__file__).parent.parent / "scripts" / "create_tables.sql"
    
    with open(sql_path, 'w', encoding='utf-8') as f:
        f.write("-- Mail2Tickets Database Schema\n")
        f.write("-- Auto-generated from database_schema.json\n")
        f.write("-- PostgreSQL\n\n")
        f.write('\n'.join(statements))
    
    logger.info(f"SQL file saved to: {sql_path}")
    return sql_path


def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("  Mail2Tickets - NocoDB Setup")
    print("="*60 + "\n")
    
    # Charger le schéma
    logger.info("Loading database schema...")
    schema = load_schema()
    
    # Afficher les informations
    print_schema_info(schema)
    
    # Générer les SQL statements
    logger.info("Generating SQL statements...")
    statements = generate_sql_statements(schema)
    
    # Sauvegarder le fichier SQL
    sql_path = save_sql_file(statements)
    
    print("\n" + "="*60)
    print("  Configuration NocoDB")
    print("="*60 + "\n")
    print(f"  Base URL: {config.NOCODB_BASE_URL or 'NOT CONFIGURED'}")
    print(f"  Project ID: {config.NOCODB_PROJECT_ID or 'NOT CONFIGURED'}")
    print(f"  API Token: {'***' + config.NOCODB_API_TOKEN[-4:] if config.NOCODB_API_TOKEN else 'NOT CONFIGURED'}")
    
    print("\n" + "="*60)
    print("  Instructions")
    print("="*60 + "\n")
    
    print("1. Le fichier SQL a été généré:")
    print(f"   {sql_path}")
    print()
    print("2. Pour créer les tables dans NocoDB/PostgreSQL:")
    print()
    print("   Option A - Via NocoDB UI:")
    print("   - Connectez-vous à votre instance NocoDB")
    print("   - Créez un nouveau projet ou utilisez un existant")
    print("   - Utilisez l'interface pour créer les tables manuellement")
    print()
    print("   Option B - Via PostgreSQL direct:")
    print("   - Connectez-vous à votre base PostgreSQL")
    print(f"   - Exécutez: psql -U postgres -d your_database -f {sql_path}")
    print()
    print("   Option C - Via API NocoDB:")
    print("   - Utilisez l'API NocoDB pour créer les tables")
    print("   - Consultez: https://docs.nocodb.com/developer-resources/rest-apis")
    print()
    print("3. Après création des tables:")
    print("   - Notez le Project ID dans votre .env")
    print("   - Générez un API Token dans NocoDB")
    print("   - Configurez NOCODB_BASE_URL, NOCODB_API_TOKEN, NOCODB_PROJECT_ID")
    print()
    print("4. Vérifiez que les tables sont accessibles:")
    print("   python scripts/test_nocodb_connection.py")
    print()
    
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
