from urbanblocks_pro.backend.app.db.session import Base, engine
from urbanblocks_pro.backend.app.models.zone import Zone

def init_db():
    print("📦 Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created")

if __name__ == "__main__":
    init_db()
