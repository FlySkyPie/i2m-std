import os
import zipfile
import re

if not os.path.exists("dist"):
    os.makedirs("dist")

print("Bundle addon...")

zip = zipfile.ZipFile("dist/ke_i2m.zip", "w", zipfile.ZIP_DEFLATED)
zip.write("LICENSE", "ke_i2m/LICENSE")


def zip_files_recursive(path="."):
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            zip_files_recursive(full_path)
        else:
            # print(full_path, re.sub("^src/", "ke_i2m/", full_path))
            zip.write(full_path, re.sub("^src/", "ke_i2m/", full_path))


zip_files_recursive("src")

zip.close()

print("Done")
