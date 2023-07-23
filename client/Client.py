import json
import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/XMLRPC")


def print_files(files):
    for file in files:
        print("NUME: " + file["nume"] + " PATH: " + file["path"] + " HASH: " + file["hash"])
    print("\n")


def find_all_files():
    files = json.loads(proxy.findAllFiles())
    print_files(files)


def find_files_containing_substring():
    substring = input("Substring: ")
    files = json.loads(proxy.findFilesContainingSubstring(substring))
    print_files(files)


def content_type_menu():
    content_type_menu_items = {"1": ("Text: ", find_files_by_content_parts_text),
                               "2": ("Binary: ", find_files_by_content_parts_binary),
                               "3": ("Back", None)
                               }
    menuu(content_type_menu_items)


def find_files_by_content_parts_text():
    content = input("Content (text): ")
    files = json.loads(proxy.findFilesByContentPartsText(content))
    print_files(files)


def find_files_by_content_parts_binary():
    content = input("Content (binary): ")
    files = json.loads(proxy.findFilesByContentPartsBinary(content))
    print_files(files)


def find_files_with_duplicate_hash():
    files = json.loads(proxy.findFilesWithDuplicateHash())
    print_files(files)


def menuu(menu):
    for key in sorted(menu.keys()):
        print("\t" + key + ":  " + menu[key][0])

    try:
        choice = input("Option: ")
        _function = menu.get(str(choice))
        if isinstance(_function[1], dict):
            menu(_function[1])
        else:
            if _function[0] == "Back":
                return
            _function[1]()
    except SystemExit:
        raise SystemExit
    except (TypeError, NameError):
        print("Invalid option\n")

    menuu(menu)


def stop():
    raise SystemExit


def start():
    menu = {"1": ("Find all files", find_all_files),
            "2": ("Find files containing substring", find_files_containing_substring),
            "3": ("Find files by parts of content", content_type_menu),
            "4": ("Find files with duplicate content", find_files_with_duplicate_hash)
            }

    menuu(menu)
    start()


if __name__ == "__main__":
    start()
