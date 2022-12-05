from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
from requests_toolbelt.multipart.encoder import MultipartEncoder

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result["pets"]) > 0


def test_add_new_pet_with_valid_data(name='Tom', animal_type='cat', age='16', pet_photo='images/Tom991441.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.post_add_info_about_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_set_new_photo(name='Tom', animal_type='cat', age='16', pet_photo='images/Tom991441.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.post_update_info_about_pet(auth_key, pet_id, pet_photo)
    assert status == 200
    assert result['pet_photo'] != pet_photo


def test_delete_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.post_add_info_about_new_pet(auth_key, "Суперкот", "кот", "3", "images/unnamed.png")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_put_update_info_about_pet(name='Мурзик', animal_type='Котэ', age='5'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_info_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_post_create_pet_simple(name='Jerry', animal_type='mouse', age=3):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
