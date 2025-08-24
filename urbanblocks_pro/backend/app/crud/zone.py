from urbanblocks_pro.backend.app.db.session import SessionLocal
from urbanblocks_pro.backend.app.models.zone import Zone

def create_zone(name, geom_wkt):
    db = SessionLocal()
    zone = Zone(name=name, geom=f'SRID=4326;{geom_wkt}')
    db.add(zone)
    db.commit()
    db.refresh(zone)
    db.close()
    return zone

def get_zones():
    db = SessionLocal()
    zones = db.query(Zone).all()
    db.close()
    return zones