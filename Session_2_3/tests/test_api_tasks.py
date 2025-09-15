def test_create_list_update_delete_task(client):
    # create a user
    u = client.post("/users", json={"email": "t@t.com", "full_name": "Tester"}).json()
    uid = u["id"]

    # create a task
    t = client.post("/tasks", json={"user_id": uid, "title": "First"}).json()
    tid = t["id"]
    assert t["completed"] is False

    # list tasks by user
    lst = client.get(f"/tasks?user_id={uid}").json()
    assert any(item["id"] == tid for item in lst)

    # mark done
    updated = client.patch(f"/tasks/{tid}", json={"completed": True}).json()
    assert updated["completed"] is True

    # delete
    resp = client.delete(f"/tasks/{tid}")
    assert resp.status_code == 204

    # verify gone
    lst2 = client.get(f"/tasks?user_id={uid}").json()
    assert all(item["id"] != tid for item in lst2)