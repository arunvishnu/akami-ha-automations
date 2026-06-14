import urllib.request, zipfile, shutil, os

url = "https://github.com/arunvishnu/akami-ha-automations/archive/refs/heads/deploy.zip"
tmp_zip = "/tmp/automations_deploy.zip"
tmp_dir = "/tmp/automations_deploy"
dest = "/addon_configs/a0d7b954_appdaemon/apps"

print("Downloading...")
urllib.request.urlretrieve(url, tmp_zip)

print("Extracting...")
if os.path.exists(tmp_dir):
    shutil.rmtree(tmp_dir)
with zipfile.ZipFile(tmp_zip) as z:
    z.extractall(tmp_dir)

src = os.path.join(tmp_dir, os.listdir(tmp_dir)[0], "apps")
os.makedirs(dest, exist_ok=True)
for f in os.listdir(src):
    shutil.copy2(os.path.join(src, f), os.path.join(dest, f))

shutil.rmtree(tmp_dir)
os.remove(tmp_zip)
print("Done — AppDaemon will hot-reload changed files automatically")
