# akami-ha-automations

AppDaemon automations for Home Assistant. Python-based, git-deployed, self-updating.

## Local development

```bash
pip install appdaemon
cp appdaemon.yaml.example appdaemon.yaml
# fill in HA URL and token in appdaemon.yaml
appdaemon -c .
```

AppDaemon connects to the live HA instance at `https://home.arunvishnu.com` and hot-reloads any `.py` file in `apps/` on save. Test against real devices locally.

## Deploy pipeline

Push to `main` → GitHub Action copies `apps/` to `deploy` branch → press **Update Automations** button in HA → `deployer.py` downloads the deploy branch zip, copies files to `/config/apps/` (inside AppDaemon container), AppDaemon hot-reloads changed files automatically.

The **Update Automations** button is a Lovelace button card that presses `input_button.update_automations`. `deployer.py` listens for that state change.

## Critical paths

| Context | Path |
|---|---|
| AppDaemon container apps dir | `/config/apps/` |
| Host filesystem (from SSH) | `/addon_configs/a0d7b954_appdaemon/apps/` |
| AppDaemon config (host) | `/addon_configs/a0d7b954_appdaemon/appdaemon.yaml` |

The `update_automations.py` deploy script (on HA at `/tmp/update_automations.py`) writes to `/addon_configs/a0d7b954_appdaemon/apps/` — NOT `/config/apps/` from the SSH terminal's perspective (those are different paths).

## Apps

### deployer.py
Listens for `input_button.update_automations` state change. Downloads `deploy` branch zip from GitHub, copies all files except itself to `/config/apps/`. Never overwrites `deployer.py` mid-run to avoid reload loops. Fires `appdaemon_deploy_complete` event on finish.


## Adding a new automation

1. Add method to appropriate class in `lighting.py`, `fans.py`, or `system.py`
2. Register the callback in `initialize()` using `run_daily`, `run_at_sunset`, `listen_state`, etc.
3. If it's a new category, create a new `.py` file and add entry to `apps/apps.yaml`
4. Push and press Update Automations button in HA

## AppDaemon callback signatures

```python
# Time-based
def callback(self, kwargs): ...

# State change
def callback(self, entity, attribute, old, new, **kwargs): ...

# Event
def callback(self, event_name, data, kwargs): ...
```

## HA instance
- URL: `https://home.arunvishnu.com`
- HA Yellow, HA OS 17.3, HA 2026.6.3
- AppDaemon add-on ID: `a0d7b954_appdaemon`, version 4.5.13
