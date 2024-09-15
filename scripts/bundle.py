import os
import zipfile
from os.path import basename

if not os.path.exists("dist"):
    os.makedirs("dist")

print("Bundle addon...")

zip = zipfile.ZipFile("dist/ke_i2m.zip", "w", zipfile.ZIP_DEFLATED)
zip.write("LICENSE", "ke_i2m/LICENSE")

dir_list = os.listdir("src")
for file in dir_list:
    zip.write(f"src/{file}", f"ke_i2m/{file}")
zip.close()

print("Done")
