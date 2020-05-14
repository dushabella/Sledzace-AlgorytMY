"""
    Download data from google drive if not downloaded yet.
    Based on https://stackoverflow.com/a/39225039
"""
import requests
import os

def download_file_from_google_drive(id: str, filename: str):
    URL = "https://docs.google.com/uc?export=download"
    if os.path.isfile(filename):
        print("Database is up to date")
        return

    print("Downloading...")
    session = requests.Session()

    response = session.get(URL, params = { "id" : id }, stream = True)
    token = get_confirm_token(response)

    response = session.get(URL, params = { "id" : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { "id" : id, "confirm" : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, filename)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value

    return None

def save_response_content(response, filename):
    CHUNK_SIZE = 32768

    with open(filename, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    # clear()
    print(filename, "downloaded")


# def clear():
#     # for windows
#     if os.name == "nt":
#         _ = os.system("cls")
#
#     # for mac and linux(here, os.name is "posix")
#     else:
#         _ = os.system("clear")

if __name__ == "__main__":
    file_id = "114QEzVWm9FUiy-TAeW0rpAoxvATWuS8W"
    filename = "./data/nascar_02.mp4"
    download_file_from_google_drive(file_id, filename)