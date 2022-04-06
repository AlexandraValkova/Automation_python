import os.path

from api import PetFriends
from settings import valid_email, valid_password

pf= PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """тест на получение api key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    print('status : ', status)


def test_get_all_pets_with_valid_key(filter=''):
    """тест на получение списка питомцев"""
    _, auth_key = pf.get_api_key(valid_email,valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets'])>0
    print('status : ', status)


def test_add_pets_with_valid_data(name='Новый', animal_type='собака',
                                  age=2, pet_photo='images\dog1.jpg'):
    """тест на добавление питомца"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet(auth_key, name, animal_type, age, pet_photo)
    print('status : ', status)
    assert status == 200
    assert result['name'] == name


def test_delete_pets():
    """удление питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key,"my_pets")
    if len(my_pets['pets']) == 0:
        pf.post_new_pet(auth_key, 'Новый', 'dog', 1, 'image\dog2.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    num = len(my_pets['pets']) - 1
    pet_id = my_pets['pets'][num]['id']
    status,result = pf.delete_pet(auth_key,pet_id)
    _,my_pets = pf.get_list_of_pets(auth_key,"my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()
    print('status : ', status)


def test_update_date_pets(name='Sasa', animal_type='собака', age=2):
    """обновление данных питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets= pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets'])>0:
        status, result= pf.put_update_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status==200
        assert result['name']==name
    else:
        raise Exception("список питомцев пуст")
    print('status : ', status)


"""тесты задания 19.7.2"""

def test_creat_pet_simple(name='Норд', animal_type='собака', age =5):
    """добавление питомца без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    print('status : ', status)


def test_add_photo_pets(pet_photo='images\dog1.jpg'):
    """добавление фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets'])>0:
        pet_id= my_pets['pets'][0]['id']
        status, result = pf.post_add_photo_pets(auth_key, pet_id, pet_photo)
        assert status == 200
        print (status)
    else:
        raise Exception("список питомцев пуст")
    print('status : ', status)


def test_api_key_no_valid(email='artktinka@dt.cg',password='g6j9k35d'):
    """тест на получение api key с неверным email и password"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    print('status : ', status)


def test_get_all_pets_no_valid_key(filter='my_pets'):
    """тест на получение списка питомцев c недействуещим auth_key"""
    auth_key={'key': 'ac1a1c7ec234ed'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
    print('status : ', status)


def test_add_pets_with_many_characters(name='йцукенгшщзхъфывапролджэячсмитьбюйцукенгшщзфывапролдячсмитьб', animal_type='собака',
                                  age='2', pet_photo='images\dog1.jpg'):
    """тест на добавление питомца с большим количеством символов"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet(auth_key, name, animal_type, age, pet_photo)
    print('status : ', status)
    assert status == 200
    assert result['name'] == name


def test_add_incorec_pets_no_photo(name="", animal_type="", age=""):
        """добавление питомца без фото c пустыми параметрами"""
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        status, result = pf.post_create_pet_simple(auth_key, name,animal_type,age)
        assert status == 200
        print('status : ', status)


def test_delete_pets_no_valid_id():
    """удление питомца с несуществуещим id"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key,"my_pets")

    pet_id = "no_valid_pet_id"
    status, result = pf.delete_pet(auth_key,pet_id)
    assert status == 200
    print('status : ', status)
    """тест выдает код 200 (кого удалил? ошибка!)"""


def test_add_pets_text_age(name='Фуня', animal_type='собака',
                           age='три', pet_photo='images\dog1.jpg'):
    """тест на добавление питомца c текстовым значением возраста"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['age'] == age
    print('status : ', status)


def test_name_pets_symbol(name='?56Q@#$$', animal_type='!#@$%/?',
                          age='5', pet_photo='images\dog1.jpg'):
    """тест на спец символы в имени и породе животного"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet(auth_key, name, animal_type, age, pet_photo)
    print('status : ', status)
    assert status == 200
    assert result['name'] == name


def test_udate_date_pets_no_corect_id(name="нет", animal_type="нет", age="5"):
    """обновление данных несуществуещего питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_pet(auth_key, my_pets['pets'][8]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("список питомцев пуст")
    print('status : ', status)



