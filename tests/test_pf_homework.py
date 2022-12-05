from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
from requests_toolbelt.multipart.encoder import MultipartEncoder

pf = PetFriends()


def test_set_photo_for_pet_in_all_pets(name='', animal_type='', age='', pet_photo='images/Tom991441.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, '')
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = all_pets['pets'][0]['id']
    pet_id_in_my_pets = my_pets['pets'][0]['id']
    status, result = pf.post_update_info_about_pet(auth_key, pet_id, pet_photo)

    if pet_id == pet_id_in_my_pets:
        assert status == 200
    else:
        assert status == 500


def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_with_empty_form(email='', password=''):
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_incorrect_age(name='bozu', animal_type='crocodile', age='99999'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result["age"] == age


def test_random_value_filter(filter='qwertyu'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    print(status, result)
    assert status == 500


def test_long_value_filter(
        filter='aasdfghjhktereaaasdhjhktereadnjfjsdfkkvdnjdjjjdjjdjaakakakkaaasdfghjhktereadnjfjsdfkkvdnjdjjjdjjdjaakakakkaaasdfghjhktereadnjfjsdfkkvdnjdjjjdjjdjaakakakkadnjfjsdfkkvdnjdjjjdjjdjaakakaasdfghjhktereadnjfjsdfkkvdnjdjjjdjjdjaakakakkaakkavkvkakavvkaavkakvavkav'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 500
    assert len(filter) == 255


def test_incorrect_filter(filter=123456789):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    print(result)
    assert status == 500


def test_invaid_age(name='bozu', animal_type='cat', age='ten'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result["age"] == age


def test_incorrect_name(name='Аркаша', animal_type='crocodile', age='9'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result["name"] == name


def test_delete_pet_from_all_pets():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")

    pet_id = all_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    assert status == 200


def test_set_photo_tif(name='', animal_type='', age='', pet_photo='images/Tom3.tif'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.post_update_info_about_pet(auth_key, pet_id, pet_photo)
    assert status == 500


def test_set_photo_gif(name='', animal_type='', age='', pet_photo='images/Tom2.gif'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.post_update_info_about_pet(auth_key, pet_id, pet_photo)

    assert status == 500
