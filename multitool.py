from shutil import copy2
from sys import argv
import re
from pathlib import Path


PATH_HANDLER_STUB: Path = Path("stubs/object_handler.py")
PATH_HANDLER_TARGET_DIR: Path = Path("object_handlers")
PATH_OBJECT_STUB: Path = Path("stubs/object.py")
PATH_OBJECT_TARGET_DIR: Path = Path("objects")

OBJECT_HANDLER_CLASS: str = 'ObjectHandler'
OBJECT_CLASS: str = 'Object'
INIT_FILE: str = '__init__.py'
INIT_FILE_INSERTION_TAG: str = '# <The next generated class will be here>'

def camel_to_snake(text: str) -> str:
    return re.sub(r'(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', '_', text).lower()

def class_to_py_file(class_name: str) -> str:
    return f"{camel_to_snake(class_name)}.py"

def make_import_line(class_name: str) -> str:
    return f"from .{camel_to_snake(class_name)} import {class_name}"

def insert_into_init(dir: Path, class_name: str) -> None:
    old_content = None

    with open (dir / INIT_FILE, "r") as init_file:
        old_content = init_file.read()
        init_file.close()

    if INIT_FILE_INSERTION_TAG not in old_content:
        print(f"The \"{INIT_FILE_INSERTION_TAG}\" insertion tag not found in {dir}/{INIT_FILE}. Import line was not added.")
        return

    import_line = make_import_line(class_name)
    if import_line in old_content:
        return

    copy2(dir / INIT_FILE, dir / f"(backup){INIT_FILE}")

    new_content = old_content.replace(
        INIT_FILE_INSERTION_TAG,
        f"{import_line}\n{INIT_FILE_INSERTION_TAG}"
    )

    with open(dir / INIT_FILE, "w") as init_file:
        init_file.write(new_content)
        init_file.close()

def make_handler(args: list[str]) -> None:
    handled_class: str|None = None
    parent_classes: str|None = None
    parent_imports: str = ""

    # Validation
    if len(args) > 2:
        raise IndexError("Invalid number of arguments")

    for arg in args:
        if arg.startswith("--parent="):
            parent_classes = arg.split("=")[1]
        else:
            handled_class = arg

    if handled_class is None:
        raise ValueError(f"Invalid target class: {handled_class}")

    target_handler_class = f"{handled_class}Handler"
    target_filename = class_to_py_file(target_handler_class)
    target_filepath = (PATH_HANDLER_TARGET_DIR / target_filename)

    if Path.exists(target_filepath):
        raise FileExistsError(f"{target_filepath} already exists")

    if parent_classes is None:
        parent_classes = OBJECT_HANDLER_CLASS
    else:
        class_names: set[str] = {pc.strip() for pc in parent_classes.split(",")}
        class_names.discard(OBJECT_HANDLER_CLASS)

        if len(class_names) > 0:
            parent_classes = ' ,'.join(class_names)
            parent_imports = '\n'.join(
                make_import_line(pi) for pi in class_names
            )

    # Generating file from stub
    with open(target_filepath, "w") as target_file:
        final_code = None

        with open(PATH_HANDLER_STUB, "r") as stub_file:
            final_code = stub_file.read()
            stub_file.close()

        for old, new in {
            "_HandledObject_": handled_class,
            "_ParentImports_": parent_imports,
            "_NewHandlerClass_": target_handler_class,
            "_ParentClasses_": parent_classes,
        }.items():
            final_code = final_code.replace(old, new)

        target_file.write(final_code)
        target_file.close()

    insert_into_init(PATH_HANDLER_TARGET_DIR, target_handler_class)

def make_object(argv: list[str]) -> None:
    target_class: str|None = None
    parent_classes: str|None = None
    parent_imports: str = ""
    create_handler: bool = False
    handler_name: str = ""
    handler_parents: str|None = None

    # Parsing args
    for arg in argv:
        if arg.startswith("--parent="):
            parent_classes = arg.split("=")[1]
        elif arg.startswith("--handler"):
            handler_name = f"HANDLER_NAME: str = \"{arg.split("=")[1]}\""
        elif arg.startswith("--make-handler"):
            create_handler = True
            parts = arg.split("=")

            if len(parts) > 1:
                handler_parents = parts[1]
        else:
            target_class = arg

    if target_class is None:
        raise ValueError(f"Invalid target class: {target_class}")

    # Preparing file path and name
    target_filename = class_to_py_file(target_class)
    target_filepath = (PATH_OBJECT_TARGET_DIR / target_filename)

    if Path.exists(target_filepath):
        raise FileExistsError(f"{target_filepath} already exists")

    # Generating parent classes and import lines
    if parent_classes is None:
        parent_classes = OBJECT_CLASS
    else:
        class_names: set[str] = {pc.strip() for pc in parent_classes.split(",")}
        class_names.discard(OBJECT_CLASS)

        if len(class_names) > 0:
            parent_classes = ', '.join(class_names)
            parent_imports = '\n'.join(
                make_import_line(pi) for pi in class_names
            )

    # Generating slot declarations
    slots = "\n".join(f"\t\t*{pc.strip()}.__slots__," for pc in parent_classes.split(","))

    # Generating handler name if --make-handler is specified
    if create_handler:
        handler_name = f"HANDLER_NAME: str = \"{target_class}Handler\""

    # Generating file from stub
    with open(target_filepath, "w") as target_file:
        final_code = None

        with open(PATH_OBJECT_STUB, "r") as stub_file:
            final_code = stub_file.read()
            stub_file.close()

        for old, new in {
            "_ParentImports_": parent_imports,
            "_NewObjectClass_": target_class,
            "_ParentClasses_": parent_classes,
            "_ParentSlots": slots,
            "_HandlerName_": handler_name,
        }.items():
            final_code = final_code.replace(old, new)

        target_file.write(final_code)
        target_file.close()

    insert_into_init(PATH_OBJECT_TARGET_DIR, target_class)

    if create_handler:
        create_args = [target_class]

        if handler_parents is not None:
            create_args.append(f"--parent={handler_parents}")

        make_handler(create_args)

if __name__ == "__main__":
    if len(argv) < 2:
        raise IndexError("Invalid command")

    if argv[1] == "make:handler":
        make_handler(argv[2:])
    elif argv[1] == "make:object":
        make_object(argv[2:])
    else:
        raise ValueError(f"Invalid command: {argv[2]}")