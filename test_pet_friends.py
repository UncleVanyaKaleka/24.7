import os.path

from api import PetFriends
from settings import valid_email, valid_password, incorrect_password, incorrect_email

pf = PetFriends()

def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result["pets"]) > 0

def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                    age='4', pet_photo='images/cat1.jpg'):
   pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

def test_add_new_pet_with_valid_data(name='тыгыдык', animal_type='тыгыдыков',
                                     age='2', pet_photo='images/santa.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_successful_update_self_pet_info(name='тыгыдык', animal_type='тыгыдыков', age=2):
   _, auth_key = pf.get_api_key(valid_email, valid_password)
   _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

   if len(my_pets['pets']) > 0:
       status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'],
                                                name, animal_type, age)
       assert status == 200
       assert result['name'] == name
   else:
       raise Exception("There is no my pets")

def test_changing_pet_photo(pet_photo = 'images/nosferatu.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    pet_id = all_pets['pets'][0]['id']
    status, result = pf.add_photo_pet(auth_key, pet_id, pet_photo)
    assert status == 200

def test_successful_delete_self_pet():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "тыгыдык", "тыгыдыков", "2", "images/nosferatu.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_login_with_invalid_key():
    status, result = pf.get_api_key(incorrect_email, incorrect_password)
    assert status == 403

def test_login_with_invalid_password():
    status, result = pf.get_api_key(valid_email, incorrect_password)
    assert status == 403

def test_login_with_invalid_email():
    status, result = pf.get_api_key(incorrect_email, valid_password)
    assert status == 403

def test_delete_someone_else_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")
    pet_id = all_pets['pets'][0]['id']
    status, result = pf.delete_pet(auth_key, pet_id)
    _, all_pets = pf.get_list_of_pets(auth_key, "")

    assert status == 400
    assert pet_id not in all_pets.values()

def test_changing_someone_pet_photo(new_pet_photo = 'images/nosferatu.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")
    pet_photo = os.path.join(os.path.dirname(__file__), new_pet_photo)
    pet_id = all_pets['pets'][0]['id']
    status, result = pf.add_photo_pet(auth_key, pet_id, pet_photo)
    assert status == 400