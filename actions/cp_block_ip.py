import requests
import json
from st2actions.runners.pythonrunner import Action

class Checkpoint(Action):
    def run(self, username, password, ip, host_name, blacklist_group):
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
			"user": username,
			"password": password
		}
		r = requests.post('https://192.168.1.24:443/web_api/login', headers=headers, json=data, verify=False)
		print r.content
		sid = r.json()['sid']
		call_headers = {'Content-Type': 'application/json', 'X-chkp-sid': sid}
		host_payload = {
			"name": host_name,
			"ip-address": ip,
			"groups": blacklist_group
		}
		new_host = requests.post('https://192.168.1.24:443/web_api/add-host', json=host_payload, headers=call_headers,
								 verify=False)
		if 'meta-info' in new_host.json():
			validation = new_host.json()['meta-info']['validation-state']
			published = False
			publish = requests.post('https://192.168.1.24:443/web_api/publish', json={}, headers=call_headers,
									verify=False)
			while not published:
				task_id = publish.json()['task-id']
				published = True
			out_string = "{} was added to firewall group {}".format(bad_ip_list[i], blacklist_group)
			return (True, out_string)
		elif 'code' in new_host.json():
			out_string = "{} - {}".format(bad_ip_list[i], new_host.json()['message'])
			return (False, out_string)
