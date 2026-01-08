from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy.ext.declarative import declarative_base

# ============================================
# QADAM 1.1: Database URL (DOIM SHUNDAY!)
# ============================================

SQLALCHEMY_DATABASE_URL="sqlite:///./todosapp.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin123@localhost:5433/TodoApplicationDatabase"
# ESLAB QOLING:
# sqlite:///./FILENAME.db
#          └─ Bu qism o'zgaradi (loyihaga qarab)

# ============================================
# QADAM 1.2: Engine yaratish
# ============================================

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
#     connect_args={"check_same_thread": False}  # ← Faqat SQLite uchun!
# )

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# YODDA SAQLANG:
# - SQLite → check_same_thread=False KERAK
# - PostgreSQL/MySQL → Bu qator KERAK EMAS

# ============================================
# QADAM 1.3: SessionLocal (DOIM SHUNDAY!)
# ============================================
SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)
# ============================================
# QADAM 1.4: Base (DOIM SHUNDAY!)
# ============================================
Base = declarative_base()

# BU FAYL TUGADI!
# Endi HECH QACHON o'zgartirmaysiz!