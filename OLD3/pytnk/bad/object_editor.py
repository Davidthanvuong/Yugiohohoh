import pygame
import random
import pickle
import multiprocessing
import os
import importlib.util
import inspect
from typing import get_type_hints
import typing
import ast

registry = {}

def assetclass(cls):
    registry[cls.__name__] = cls
    return cls


def loadAssetsList(folder="pytnk"):
    # base_path = os.path.dirname(os.path.abspath(__file__))  # Get directory of main.py
    # folder = os.path.join(base_path, folder)

    if not os.path.exists(folder): # Tạo folder nếu không có
        os.makedirs(folder)

    for filename in os.listdir(folder):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3] # Loại .py
            module_path = os.path.join(folder, filename)

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if obj.__module__ == module_name: # Lấy từ file chứ không phải từ import chung
                        assetclass(obj)
                        print(f"Tìm thấy {module_name}")

            except Exception as e:
                print(f"Skipped {module_name}. {e}")

    print(f"Đã tìm thấy {len(registry)}")


def renameTypes(hint):
    '''Đổi tên các loại biến đã biết'''
    if hint is None:
        return "Unknown"
    
    # Đổi Optional[X] to "No X"
    if typing.get_origin(hint) is typing.Optional:
        inner_type = typing.get_args(hint)[0]
        return f"No {inner_type.__name__}"
    
    return hint.__name__ if hasattr(hint, "__name__") else str(hint)


def fetchParams():
    '''In tham số'''
    print("\n Đã tìm thấy: ")
    
    for class_name, cls in registry.items():
        print(f"\nClass: {class_name} (inherit: {cls.__bases__[0].__name__})")

        signature = inspect.signature(cls.__init__)
        type_hints = get_type_hints(cls.__init__)  # Get type hints

        for param_name, param in signature.parameters.items():
            if param_name == "self":
                continue
            
            # Get type hint (or infer from default value)
            param_type = type_hints.get(param_name, None)
            default_value = param.default if param.default is not inspect.Parameter.empty else "REQUIRED"

            # If no type hint, infer from default value
            if param_type is None and default_value != "REQUIRED":
                param_type = type(default_value)
            
            # Clean the type hint display
            readable_type = renameTypes(param_type)
            
            print(f"  {param_name}: {readable_type} = {default_value}")

def format_components(coms):
    """Formats the components dictionary for better readability and prints their values."""
    formatted = {f"{cls.__module__.split('.')[-1]}.{cls.__name__}": instance for cls, instance in coms.items()}
    for name, instance in formatted.items():
        print(f"{name}: {instance}")
    return formatted

def inspectObj(inst):
    '''Đổi tham số của một vật'''
    print("\nCurrent variables:")
    for key, value in inst.__dict__.items():
        print(f"  {key}: {value}")
    
    if hasattr(inst, "coms"):
        print("\nCurrent components:")
        format_components(inst.coms)
    
    params = input("Enter modifications or function calls (key=value, func(arg1, arg2)): ").strip()
    if params:
        try:
            if False and ("(" in params and ")" in params):  # Detect function call
                func_name, args = params.split("(")
                args = args.rstrip(")")
                args = ast.literal_eval(f"({args},)")  # Ensure it's a tuple
                if hasattr(inst, func_name):
                    getattr(inst, func_name)(*args)
                    print(f"Called {func_name}{args}")
                else:
                    print(f"Error: {func_name} is not a method of this object.")
            else:
                updates = ast.literal_eval(f"{{{params}}}")  # Convert input to dictionary
                if isinstance(updates, dict):
                    for key, value in updates.items():
                        if hasattr(inst, key):
                            setattr(inst, key, value)
                            print(f"Updated {key} to {value}")
                        else:
                            print(f"Warning: {key} is not a recognized attribute.")
        except (SyntaxError, ValueError):
            print("Invalid format. Use: key=value, func(arg1, arg2)")


def createObject():
    '''Tạo vật từ parameters'''
    fetchParams()
    class_name = input("\nTên class: ").strip()
    if class_name not in registry:
        print(f"Không tìm thấy '{class_name}'")
        return False
    
    params = input(f"Tham số:").strip()
    kwargs = {}
    if params:
        try:
            parsed_dict = ast.literal_eval(f"{{{params}}}")  # Safely parse into a dictionary
            if isinstance(parsed_dict, dict):
                kwargs.update(parsed_dict)
        except (SyntaxError, ValueError):
            print("Invalid parameter format.")

    new_object = registry[class_name](**kwargs)
    print(f"OK: {new_object}")
    return new_object