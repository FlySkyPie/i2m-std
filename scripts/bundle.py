import os
import zipfile
from os.path import basename

if not os.path.exists("dist"):
    os.makedirs("dist")

print("Bundle addon...")

zip = zipfile.ZipFile("dist/ke_i2m.zip", "w", zipfile.ZIP_DEFLATED)
zip.write("LICENSE", "ke_i2m/LICENSE")
zip.write("src/__init__.py", "ke_i2m/__init__.py")
zip.write("src/clearslot.py", "ke_i2m/clearslot.py")
zip.close()

print("Done")
