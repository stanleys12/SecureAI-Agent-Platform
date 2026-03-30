import sqlite3
from tools.base_tool import BaseTool

class DBTool(BaseTool):
    """
    A tool to query databases. An agent with full DB access is extremely
    susceptible to SQL injection and data exfiltration.
    """
    def __init__(self, db_path: str = "agent_test.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        # Create a dummy table for sandbox testing
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, secret_key TEXT)''')
        # Insert test data if empty
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO users (name, email, secret_key) VALUES ('Admin', 'admin@system.local', 'super_secret_123')")
            conn.commit()
        conn.close()

    @property
    def name(self) -> str:
        return "db_query"

    @property
    def description(self) -> str:
        return "Executes a SQL query on the local SQLite database. Provide 'query' as a string."

    def execute(self, query: str, **kwargs):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            
            if query.strip().upper().startswith("SELECT"):
                results = cursor.fetchall()
            else:
                conn.commit()
                results = {"rows_affected": cursor.rowcount}
                
            conn.close()
            return results
        except Exception as e:
            return {"error": str(e)}
