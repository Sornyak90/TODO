from tests.conftest import *  
import uuid

async def test_creat_unauthorized(client, headers_expired_token, headers_invlid):
    """Тест ошибок авторизации при создании задачи (401)"""
   
    # Сценарий 1: Запрос без токена -> 401
    patch_response = await client.post(
        "/tasks/",
        json={"name": "task_name", "status": False}
    )
    assert patch_response.status_code == 401  

    # Сценарий 2: Запрос с неверным токеном -> 401
    patch_response = await client.post(
        "/tasks/",
        json={"name": "task_name", "status": False},
        headers=headers_invlid
    )
    assert patch_response.status_code == 401  

    # Сценарий 3: Запрос с просроченным токеном -> 401
    response = await client.post(
        "/tasks/", 
        json={"name": "task_name", "status": False},  
        headers=headers_expired_token 
    )
    assert response.status_code == 401  

async def test_delete_unauthorized(client, headers_expired_token, headers_invlid):
    # Проверка удаления без авторизации или с неверным токеном
    
    # Попытка удаления без токена -> 401 Unauthorized
    delete_response = await client.delete(f"/tasks/{"task_name"}")
    assert delete_response.status_code == 401 
    
    # Попытка удаления с неверным токеном -> 401 Unauthorized
    delete_response = await client.delete(
        f"/tasks/{"task_name"}",
        headers=headers_invlid
    )
    assert delete_response.status_code == 401 

    # Сценарий 3: Запрос с просроченным токеном -> 401
    delete_response = await client.delete(
        f"/tasks/{"task_name"}",   
        headers=headers_expired_token 
    )
    assert delete_response.status_code == 401 

async def test_getall_unauthorized(client, headers_expired_token, headers_invlid,pagination_params):
    # Сценарий 2: Запрос без токена -> 401 Unauthorized
    response = await client.get(
            "/tasks/", 
            params=pagination_params["first_page"]
        )
    assert response.status_code == 401  
    
    # Сценарий 3: Запрос с неверным токеном -> 401 Unauthorized
    response = await client.get(
            "/tasks/", 
            params=pagination_params["first_page"],
            headers=headers_invlid
        )
    assert response.status_code == 401 

    # Сценарий 3: Запрос с просроченным токеном -> 401
    response = await client.get(
            "/tasks/", 
            params=pagination_params["first_page"],
            headers=headers_expired_token
        )
    assert response.status_code == 401 

async def test_getone_unauthorized(client, headers_expired_token, headers_invlid):
    """Тест доступа к задаче без авторизации -> 401"""
    
    # Сценарий 1: GET запрос без токена
    response = await client.get(f"/tasks/{"task_name"}")
    assert response.status_code == 401  # Не авторизован
    
    # Сценарий 2: GET запрос с неверным токеном
    response = await client.get(
        f"/tasks/{"task_name"}",
        headers=headers_invlid 
    )
    assert response.status_code == 401  # Не авторизован

    # Сценарий 3: GET запрос с просроченным токеном
    response = await client.get(
        f"/tasks/{"task_name"}",
        headers=headers_expired_token 
    )
    assert response.status_code == 401  # Не авторизован

async def test_patch_unauthorized(client, headers_expired_token, headers_invlid):
    """Ошибки авторизации при обновлении (без токена / неверный токен)"""
    
    # Попытка обновления без токена -> 401
    patch_response = await client.patch(
        "/tasks/",
        json={"name": "task_name", "status": False}
    )
    assert patch_response.status_code == 401

    # Попытка обновления с неверным токеном -> 401
    patch_response = await client.patch(
        "/tasks/",
        json={"name": "task_name", "status": False},
        headers=headers_invlid
    )
    assert patch_response.status_code == 401

     # Попытка обновления с просроченным токеном -> 401
    patch_response = await client.patch(
        "/tasks/",
        json={"name": "task_name", "status": False},
        headers=headers_expired_token
    )
    assert patch_response.status_code == 401