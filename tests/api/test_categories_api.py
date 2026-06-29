from tests.factories import category_request_body, create_category, create_product

BASE_URL = "/api/v1/categories"


def test_list_categories_returns_empty_list(client):
    # Arrange
    url = BASE_URL

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    assert response.json() == []


def test_list_categories_returns_created_categories(client, db_session):
    # Arrange
    first = create_category(db_session, name="Electronics", description="Devices")
    second = create_category(db_session, name="Office", description="Office supplies")

    # Act
    response = client.get(BASE_URL)

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 2
    assert payload[0]["id"] == first.id
    assert payload[0]["name"] == "Electronics"
    assert payload[1]["id"] == second.id
    assert payload[1]["name"] == "Office"


def test_get_category_by_id_returns_category(client, db_session):
    # Arrange
    category = create_category(db_session, name="Electronics", description="Devices")

    # Act
    response = client.get(f"{BASE_URL}/{category.id}")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == category.id
    assert payload["name"] == "Electronics"
    assert payload["description"] == "Devices"
    assert "created_at" in payload
    assert "updated_at" in payload


def test_get_category_by_id_returns_404_when_not_found(client):
    # Arrange
    missing_id = 9999

    # Act
    response = client.get(f"{BASE_URL}/{missing_id}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == f"Category {missing_id} was not found."


def test_get_category_by_id_returns_422_for_invalid_path_value(client):
    # Arrange
    invalid_id = 0

    # Act
    response = client.get(f"{BASE_URL}/{invalid_id}")

    # Assert
    assert response.status_code == 422
    payload = response.json()
    assert payload["detail"][0]["loc"][-1] == "category_id"


def test_create_category_returns_201_with_expected_body(client):
    # Arrange
    request_body = category_request_body(name="Electronics", description="Devices and accessories")

    # Act
    response = client.post(BASE_URL, json=request_body)

    # Assert
    assert response.status_code == 201
    payload = response.json()
    assert payload["id"] > 0
    assert payload["name"] == "Electronics"
    assert payload["description"] == "Devices and accessories"
    assert "created_at" in payload
    assert "updated_at" in payload


def test_create_category_returns_409_for_duplicate_name(client, db_session):
    # Arrange
    create_category(db_session, name="Electronics", description="First")
    duplicate_body = category_request_body(name="Electronics", description="Duplicate")

    # Act
    response = client.post(BASE_URL, json=duplicate_body)

    # Assert
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_create_category_returns_422_for_invalid_payload(client):
    # Arrange
    invalid_body = {"name": "", "description": "Invalid due to empty name"}

    # Act
    response = client.post(BASE_URL, json=invalid_body)

    # Assert
    assert response.status_code == 422
    payload = response.json()
    assert payload["detail"][0]["loc"][-1] == "name"


def test_update_category_returns_200_and_updated_body(client, db_session):
    # Arrange
    category = create_category(db_session, name="Electronics", description="Old description")
    update_body = category_request_body(
        name="Consumer Electronics",
        description="Updated description",
    )

    # Act
    response = client.put(f"{BASE_URL}/{category.id}", json=update_body)

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == category.id
    assert payload["name"] == "Consumer Electronics"
    assert payload["description"] == "Updated description"


def test_update_category_returns_404_when_not_found(client):
    # Arrange
    missing_id = 4321
    update_body = category_request_body(
        name="Consumer Electronics",
        description="Updated description",
    )

    # Act
    response = client.put(f"{BASE_URL}/{missing_id}", json=update_body)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == f"Category {missing_id} was not found."


def test_update_category_returns_409_for_duplicate_name(client, db_session):
    # Arrange
    original = create_category(db_session, name="Electronics", description="Original")
    create_category(db_session, name="Office", description="Second")
    duplicate_name_update = category_request_body(name="Office", description="Try duplicate")

    # Act
    response = client.put(f"{BASE_URL}/{original.id}", json=duplicate_name_update)

    # Assert
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_update_category_returns_422_for_validation_error(client, db_session):
    # Arrange
    category = create_category(db_session, name="Electronics", description="Original")
    invalid_name = "x" * 121
    invalid_update = category_request_body(name=invalid_name, description="Too long name")

    # Act
    response = client.put(f"{BASE_URL}/{category.id}", json=invalid_update)

    # Assert
    assert response.status_code == 422
    payload = response.json()
    assert payload["detail"][0]["loc"][-1] == "name"


def test_delete_category_returns_204_and_removes_record(client, db_session):
    # Arrange
    category = create_category(db_session, name="Electronics", description="To delete")

    # Act
    response = client.delete(f"{BASE_URL}/{category.id}")

    # Assert
    assert response.status_code == 204
    check = client.get(f"{BASE_URL}/{category.id}")
    assert check.status_code == 404


def test_delete_category_returns_404_when_not_found(client):
    # Arrange
    missing_id = 5432

    # Act
    response = client.delete(f"{BASE_URL}/{missing_id}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == f"Category {missing_id} was not found."


def test_delete_category_returns_409_when_products_are_assigned(client, db_session):
    # Arrange
    category = create_category(db_session, name="Electronics", description="Has products")
    create_product(
        db_session,
        category_id=category.id,
        name="Category Linked Product",
        sku="CAT-PRD-001",
        stock_quantity=10,
    )

    # Act
    response = client.delete(f"{BASE_URL}/{category.id}")

    # Assert
    assert response.status_code == 409
    assert "Cannot delete category" in response.json()["detail"]
