"""
database.py
------------
Handles MySQL database creation and connection for the PyCommerce project.
"""

import os

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error
from mysql.connector.connection import MySQLConnection

# Load environment variables
load_dotenv()

# ==============================
# Database Configuration
# ==============================

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "pycommerce")


# ==============================
# Create Database
# ==============================

def create_database() -> None:
    """
    Create the database if it does not already exist.
    """

    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )

        cursor = connection.cursor()

        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"
        )

        print(f"[SUCCESS] Database '{DB_NAME}' is ready.")

    except Error as e:
        print(f"[ERROR] Failed to create database.")
        print(e)

    finally:

        if cursor is not None:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# ==============================
# Get Connection
# ==============================

def get_connection() -> MySQLConnection | None:
    """
    Returns a MySQL connection object.
    """

    try:

        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():
            return connection

    except Error as e:
        print(f"[ERROR] Database Connection Failed.")
        print(e)

    return None


# ==============================
# Close Connection
# ==============================

def close_connection(connection: MySQLConnection | None) -> None:
    """
    Close database connection safely.
    """

    if connection and connection.is_connected():
        connection.close()
        print("[SUCCESS] Database connection closed.")

