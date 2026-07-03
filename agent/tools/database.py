import sqlite3
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Find root project path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_DIR = os.path.join(BASE_DIR, 'database')
DB_PATH = os.path.join(DB_DIR, 'medmate.db')

def get_connection():
    """Returns a SQLite connection, ensuring parent directory exists."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the SQLite tables for medications and reminders."""
    logger.info("Initializing database...")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Create medications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                dose TEXT NOT NULL,
                frequency TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT,
                notes TEXT
            )
        """)

        # Create reminders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                medication_name TEXT NOT NULL,
                reminder_time TEXT NOT NULL,
                FOREIGN KEY (medication_name) REFERENCES medications(name) ON DELETE CASCADE
            )
        """)
        conn.commit()
        logger.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize database: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

def add_medication_db(name: str, dose: str, frequency: str, start_date: str, end_date: str = None, notes: str = None) -> bool:
    """Inserts a medication into the database using parameterized queries."""
    # Sanitize and validate inputs
    name = name.strip().lower()
    if not name or not dose or not frequency or not start_date:
        logger.error("Invalid arguments passed to add_medication_db.")
        return False

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO medications (name, dose, frequency, start_date, end_date, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, dose, frequency, start_date, end_date, notes))
        conn.commit()
        logger.info(f"Added medication: {name}")
        return True
    except sqlite3.IntegrityError:
        logger.warning(f"Medication {name} already exists. Updating details instead.")
        try:
            cursor.execute("""
                UPDATE medications 
                SET dose = ?, frequency = ?, start_date = ?, end_date = ?, notes = ?
                WHERE name = ?
            """, (dose, frequency, start_date, end_date, notes, name))
            conn.commit()
            logger.info(f"Updated medication: {name}")
            return True
        except sqlite3.Error as e:
            logger.error(f"Failed to update medication {name}: {e}")
            conn.rollback()
            return False
    except sqlite3.Error as e:
        logger.error(f"Failed to add medication {name}: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def remove_medication_db(name: str) -> bool:
    """Removes a medication and its reminders from the database using parameterized queries."""
    name = name.strip().lower()
    if not name:
        return False

    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Enable foreign keys to trigger cascade delete if supported, 
        # or delete from reminders manually
        cursor.execute("DELETE FROM reminders WHERE medication_name = ?", (name,))
        cursor.execute("DELETE FROM medications WHERE name = ?", (name,))
        conn.commit()
        logger.info(f"Removed medication: {name}")
        return True
    except sqlite3.Error as e:
        logger.error(f"Failed to remove medication {name}: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def list_medications_db() -> list:
    """Returns all medications currently in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM medications ORDER BY name ASC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Failed to list medications: {e}")
        return []
    finally:
        conn.close()

def add_reminder_db(medication_name: str, reminder_time: str) -> bool:
    """Adds a reminder for a medication using parameterized queries."""
    medication_name = medication_name.strip().lower()
    reminder_time = reminder_time.strip()
    if not medication_name or not reminder_time:
        return False

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO reminders (medication_name, reminder_time)
            VALUES (?, ?)
        """, (medication_name, reminder_time))
        conn.commit()
        logger.info(f"Added reminder for {medication_name} at {reminder_time}")
        return True
    except sqlite3.Error as e:
        logger.error(f"Failed to add reminder for {medication_name}: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def list_reminders_db() -> list:
    """Returns all reminders currently in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM reminders ORDER BY reminder_time ASC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Failed to list reminders: {e}")
        return []
def remove_reminder_db(reminder_id: int) -> bool:
    """Removes a reminder by its ID using parameterized queries."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
        conn.commit()
        logger.info(f"Removed reminder ID: {reminder_id}")
        return True
    except sqlite3.Error as e:
        logger.error(f"Failed to remove reminder {reminder_id}: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def clear_all_data_db() -> bool:
    """Clears all data from medications and reminders. Primarily for test usage."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM reminders")
        cursor.execute("DELETE FROM medications")
        conn.commit()
        logger.info("Cleared all data from database.")
        return True
    except sqlite3.Error as e:
        logger.error(f"Failed to clear database: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
