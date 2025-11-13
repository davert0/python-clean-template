from os.path import defpath

from httpx import AsyncClient


async def test_create_comment(client: AsyncClient):
    user_data = {
        "email": "test@example.com",
        "name": "Test User"
    }
    user_response = await client.post("/users/", json=user_data)
    user_id = user_response.json()["id"]
    
    comment_data = {
        "user_id": user_id,
        "content": "This is a test comment."
    }
    response = await client.post("/comments/", json=comment_data)
    assert response.status_code == 201

    data = response.json()
    assert data["user_id"] == user_id
    assert data["content"] == comment_data["content"]
    assert "post_id" in data
    assert "created_at" in data
    assert "updated_at" in data


async def test_get_all_comments(client: AsyncClient):
    user_data = {"email": "test@example.com", "name": "Test User"}
    user_response = await client.post("/users/", json=user_data)
    user_id = user_response.json()["id"]

    for i in range(3):
        await client.post("/comments/", json={
            "user_id": user_id,
            "content": f"Comment {i}"
        })

    response = await client.get("/comments/all")
    assert response.status_code == 200

    data = response.json()
    assert "comments" in data
    assert isinstance(data["comments"], list)
    assert len(data["comments"]) >= 3
    assert all("content" in c for c in data["comments"])


async def test_get_comments_pagination(client: AsyncClient):
    user_data = {"email": "test@example.com", "name": "Tester"}
    user_response = await client.post("/users/", json=user_data)
    user_id = user_response.json()["id"]

    # Создаём 15 комментариев
    for i in range(15):
        await client.post("/comments/", json={"user_id": user_id, "content": f"Comment {i}"})

    response = await client.get("/comments/?page=2&limit=5&order=desc")
    assert response.status_code == 200

    data = response.json()
    assert "comments" in data
    assert data["page"] == 2
    assert data["limit"] == 5
    assert isinstance(data["comments"], list)
    assert len(data["comments"]) == 5


async def test_update_comment(client: AsyncClient):
    user_data = {
        "email": "test@example.com",
        "name": "Test User"
    }
    user_response = await client.post("/users/", json=user_data)
    user_id = user_response.json()["id"]

    comment_data = {
        "user_id": user_id,
        "content": "This is a test comment."
    }
    create_response = await client.post("/comments/", json=comment_data)
    post_id = create_response.json()["post_id"]

    update_data = {
        "content": "This is an updated test comment."
    }
    response = await client.put(f"/comments/{post_id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["post_id"] == post_id
    assert data["user_id"] == user_id
    assert data["content"] == update_data["content"]
    assert "created_at" in data
    assert "updated_at" in data