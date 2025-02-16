import zipfile
import os

def extractzip(zip_path):

    extract_folder = "./data"

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        
        zip_ref.extractall(extract_folder)
        print(f"{zip_path} has extracted.")

    h5ad_file = ""
    for file_name in os.listdir(extract_folder):
        if file_name.endswith('.h5ad'):  
            h5ad_file = os.path.join(extract_folder, file_name)
            break
        
    if h5ad_file == "":
        print("There is no h5ad file in this zip folder.")