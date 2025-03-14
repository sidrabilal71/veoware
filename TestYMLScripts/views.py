import ast
import os
from collections import OrderedDict
from collections.abc import MutableMapping

import yaml
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render



# Create your views here.
def update_tests(request):
    # Load the data from the config.yml file
    data = load_yaml('config.yml')
    # Extract only the 'Tests' section
    tests = data.get('Tests', {})

    testsflatten=get_dict_from_YML(tests)
    print(testsflatten)
    tests = data.get('Tests', {})

    return render(request, 'TestYMLScripts/update_tests.html', {'tests': tests})

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def get_dict_from_YML(data):
    if isinstance(data, dict):
        return {key: get_dict_from_YML(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [get_dict_from_YML(item) for item in data]
    else:
        return data

# def flattenDict(dictionary, parent_key='', separator=' '):
#     params = []
#     for key, value in dictionary.items():
#         new_key = parent_key + separator + key if parent_key else key
#         if isinstance(value, dict):
#             params.extend(flattenDict(value, new_key, separator=separator).items())
#         elif isinstance(value, list):
#             params.extend(flattenList(value, new_key,separator=separator))
#         else:
#             params.append((new_key, value))
#     return dict(params)
# def flattenList(listtest, parent_key='', separator=' '):
#     params = []
#     for index,item  in enumerate(listtest):
#         new_key = parent_key + separator + str(index) if parent_key else str(index)
#         if isinstance(item, dict):
#             params.extend(flattenDict(item, new_key, separator=separator).items())
#         elif isinstance(item, list):
#             params.extend(flattenList(item, new_key,separator=separator))
#         else:
#             params.append((new_key, item))
#     return list(params)

def save_tests(request):


    # if request.method == 'POST':
    #     updated_tests = {}
    #     for key, value in request.POST.items():
    #         if key != 'csrfmiddlewaretoken':  # Ignore CSRF token
    #             updated_tests[key] = value
    #     print(updated_tests)  # This will show the manipulated dictionary

    if request.method == 'POST':
        updated_tests = {}
        tests=(request.POST.dict())
        # Convert list structure back
        if isinstance(tests, list):
            original_structure = unflatten_list(tests)
        else:
            original_structure = unflatten_dict(tests)


        print(tests)
        print(original_structure)

        save_yaml({'Tests': original_structure}, 'scriptupdate.yml')
 # Redirect to a success page or the same page

        return render(request, 'TestYMLScripts/update_tests.html', {'tests': load_yaml('config1.yml')})


def save_yaml(data, file_path):
    with open(file_path, 'w') as file:
        yaml.safe_dump(data, file,sort_keys=False)

        return HttpResponseRedirect('/success/')

def unflatten_dict(flat_dict, separator='.'):
    unflattened_dict = {}
    for key, value in flat_dict.items():
        keys = key.split(separator)
        d = unflattened_dict
        for k in keys[:-1]:
            # if k.isdigit():
                # it means this is a list
                # but we also have to check for list of list
                # recursive call here???TODO
            d = d.setdefault(k, {})
        d[keys[-1]] = value
    return unflattened_dict

def unflatten_list(flat_list, separator='.'):
    unflattened_dict = {}
    for key, value in flat_list:
        keys = key.split(separator)
        d = unflattened_dict
        for k in keys[:-1]:
            if k.isdigit():
                k = int(k)
                while len(d) <= k:
                    d.append({})
                d = d[k]
            else:
                d = d.setdefault(k, {})
        if keys[-1].isdigit():
            key_index = int(keys[-1])
            while len(d) <= key_index:
                d.append(None)
            d[key_index] = value
        else:
            d[keys[-1]] = value
    return unflattened_dict
