from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_user_and_course_and_enrollment():
    # Create admin
    res = client.post("/users/", json={"name":"Admin","email":"a@a.com","role":"admin"})
    admin_id = res.json()["id"]
    assert res.status_code == 200

    # Create student
    res = client.post("/users/", json={"name":"Student","email":"s@s.com","role":"student"})
    student_id = res.json()["id"]
    assert res.status_code == 200

    # Admin creates course
    res = client.post("/courses/?role=admin", json={"title":"Math","code":"M101"})
    course_id = res.json()["id"]
    assert res.status_code == 200

    # Student enrolls
    res = client.post("/enrollments/", json={"user_id":student_id,"course_id":course_id,"role":"student"})
    enrollment_id = res.json()["id"]
    assert res.status_code == 200

    # Student cannot enroll twice
    res = client.post("/enrollments/", json={"user_id":student_id,"course_id":course_id,"role":"student"})
    assert res.status_code == 400

    # Admin sees all enrollments
    res = client.get("/enrollments/?role=admin")
    assert res.status_code == 200
    assert len(res.json()) == 1

    # Deregister
    res = client.delete(f"/enrollments/{enrollment_id}?role=student")
    assert res.status_code == 200
