import appdaemon.plugins.hass.hassapi as hass
import urllib.request
import zipfile
import shutil
import os
import threading

DEPLOY_URL = "https://github.com/arunvishnu/akami-ha-automations/archive/refs/heads/deploy.zip"
APPS_DIR   = "/config/apps"


class Deployer(hass.Hass):
    """
    Listens for the 'appdaemon_deploy' HA event and pulls the latest
    apps from the GitHub deploy branch. AppDaemon hot-reloads changed files.

    Trigger from HA:
      service: homeassistant.fire_event
      data:
        event_type: appdaemon_deploy
    """

    def initialize(self):
        self.listen_state(self.on_deploy, "input_button.update_automations")
        self.log("Deployer ready — press input_button.update_automations to deploy")

    def on_deploy(self, event_name, data, kwargs):
        self.log("Deploy triggered — pulling from GitHub...")
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self):
        tmp_zip = "/tmp/ad_deploy.zip"
        tmp_dir = "/tmp/ad_deploy"

        try:
            self.log("Downloading...")
            urllib.request.urlretrieve(DEPLOY_URL, tmp_zip)

            if os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir)
            with zipfile.ZipFile(tmp_zip) as z:
                z.extractall(tmp_dir)

            src = os.path.join(tmp_dir, os.listdir(tmp_dir)[0], "apps")
            updated = []
            for f in os.listdir(src):
                if f == "deployer.py":   # never overwrite self mid-run
                    continue
                shutil.copy2(os.path.join(src, f), os.path.join(APPS_DIR, f))
                updated.append(f)

            shutil.rmtree(tmp_dir)
            os.remove(tmp_zip)

            self.log(f"Deploy complete — updated: {', '.join(updated)}")
            self.fire_event("appdaemon_deploy_complete", status="success")

        except Exception as e:
            self.log(f"Deploy failed: {e}", level="ERROR")
            self.fire_event("appdaemon_deploy_complete", status="failed", error=str(e))
