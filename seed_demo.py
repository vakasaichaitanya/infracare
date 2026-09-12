from app.db import SessionLocal, init_db
from app import models
from datetime import datetime

def seed():
    init_db()
    db = SessionLocal()
    
    # Check if reports exist
    if db.query(models.Report).count() > 0:
        print('Database already contains data.')
        db.close()
        return

    # Create demo users
    admin = models.User(id=1, email='admin@infracare.gov', password='password', role=models.UserRole.admin)
    citizen = models.User(id=2, email='citizen@infracare.gov', password='password', role=models.UserRole.citizen)
    officer1 = models.User(id=3, email='officer.rajesh@infracare.gov', password='password', role=models.UserRole.officer)
    officer2 = models.User(id=4, email='officer.priya@infracare.gov', password='password', role=models.UserRole.officer)
    
    db.merge(admin)
    db.merge(citizen)
    db.merge(officer1)
    db.merge(officer2)
    db.commit()

    # Create sample reports
    reports = [
        models.Report(
            title='Severe Pothole & Caved Asphalt',
            description='Large 3ft crater on Outer Circle causing hazardous traffic slowdown and bike skids.',
            category=models.ReportCategory.road,
            severity=models.ReportSeverity.critical,
            latitude=28.6328,
            longitude=77.2195,
            priority='P1',
            priority_reason='Critical severity road hazard',
            status=models.ReportStatus.reported,
            support_count=8
        ),
        models.Report(
            title='Structural Crack on Pedestrian Overbridge',
            description='Expansion joint separation and visible concrete spalling on stairs.',
            category=models.ReportCategory.bridge,
            severity=models.ReportSeverity.high,
            latitude=28.6289,
            longitude=77.2145,
            priority='P2',
            priority_reason='High safety impact on bridge structure',
            status=models.ReportStatus.verified,
            support_count=14
        ),
        models.Report(
            title='Streetlight Cluster Blackout',
            description='Four consecutive light poles non-functional near Janpath crossing, zero nighttime visibility.',
            category=models.ReportCategory.lighting,
            severity=models.ReportSeverity.medium,
            latitude=28.6255,
            longitude=77.2185,
            priority='P3',
            priority_reason='Lighting failure in commercial pedestrian area',
            status=models.ReportStatus.assigned,
            support_count=3
        ),
        models.Report(
            title='Broken Stormwater Drain Grate',
            description='Exposed open drain chamber next to bus shelter, immediate pedestrian risk.',
            category=models.ReportCategory.other,
            severity=models.ReportSeverity.critical,
            latitude=28.6360,
            longitude=77.2240,
            priority='P1',
            priority_reason='High hazard near public transit point',
            status=models.ReportStatus.in_progress,
            support_count=19
        ),
        models.Report(
            title='Faded Road Markings & Missing Signboard',
            description='Speed bump warning sign damaged by tree branch.',
            category=models.ReportCategory.road,
            severity=models.ReportSeverity.low,
            latitude=28.6385,
            longitude=77.2110,
            priority='P4',
            priority_reason='Low urgency maintenance item',
            status=models.ReportStatus.resolved,
            support_count=1
        )
    ]

    for r in reports:
        db.add(r)
    db.commit()

    # Add assignments
    db.add(models.Assignment(report_id=3, officer_id=3))
    db.add(models.Assignment(report_id=4, officer_id=3))
    db.commit()

    print('Database seeded with demo users and realistic SIH infrastructure reports!')
    db.close()

if __name__ == '__main__':
    seed()
