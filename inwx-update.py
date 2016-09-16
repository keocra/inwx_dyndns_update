from inwx_managed_python_lib.inwx import domrobot, prettyprint, getOTP
from getpass import getpass

import urllib2

import commentjson as json


configuration_file = "./inwx-update.json"
update_url = "update_url"
urls = "urls"


def read_config(config_file):
    with open(config_file) as fh:
        return json.load(fh)


def request_interactive_values(config):
    if config and isinstance(config, str) and config == "<ask>":
        return raw_input("Please enter a value for configuration parameter \"%s\": " % k)

    for k in config:
        if config[k] and config[k] == "<ask>":
            if k == "password":
                print "Please enter a value for configuration parameter \"%s\"" % k
                config[k] = getpass()
            else:
                config[k] = raw_input("Please enter a value for configuration parameter \"%s\": " % k)
        elif config[k] and isinstance(config[k], list):
            for li, obj in enumerate(config[k]):
                config[k][li] = request_interactive_values(obj)
        elif config[k] and isinstance(config[k], dict):
            config[k] = request_interactive_values(config[k])

    return config


def check_domain_existing(nameserver_check_result, domain):
    if not nameserver_check_result or not domain:
        return False, None

    if not isinstance(nameserver_check_result, dict):
        return False, None

    entry_list = nameserver_check_result["resData"]["record"]

    if not isinstance(entry_list, list):
        return False, None

    for obj in entry_list:
        if "name" in obj and obj["name"] == domain:
            return True, obj

    return False, None


def main():
    print "Starting inwx dyndns domain updater..."

    print "Loading config..."
    config = read_config(configuration_file)
    config = request_interactive_values(config)

    api_url = config[update_url]
    ip_page = config["ip_page"]

    # get current external ip address
    ip = urllib2.urlopen(ip_page).read()
    # print ip

    print "Iterating through updateable url descriptions..."
    for k in config[urls]:
        username = k["username"]
        password = k["password"]
        shared_secret = k["shared_secret"]
        tld = k["tld"]
        domain = k["domain"]
        overwrite_setting = k["overwrite"]

        print "Try to update %s.%s" % (domain, tld)

        inwx_conn = domrobot(api_url, False)
        loginRet = inwx_conn.account.login({'lang': 'en', 'user': username, 'pass': password})

        if 'tfa' in loginRet and loginRet['tfa'] == 'GOOGLE-AUTH':
            loginRet = inwx_conn.account.unlock({'tan': getOTP(shared_secret)})

        # get nameserver entry for top-level-domain
        nameserver_check_result = inwx_conn.nameserver.info({'domain': tld})
        # print json.dumps(nameserver_check_result, indent=1)

        # check if there is an object included in the response which has the stated domain nameserver_check_result
        domain_needs_creation, nameserver_obj = check_domain_existing(
            nameserver_check_result, 
            domain + "." + tld
        )
        domain_needs_creation = not domain_needs_creation
        
        # create record entry if not already existing
        if domain_needs_creation:
            create_result = inwx_conn.nameserver.createRecord({
                "type": "A",
                "content": ip,
                "name": domain,
                "domain": tld
            })

            print "Domain entry for %s.%s created." % (domain, tld)
            # print json.dumps(create_result, indent=1)
        elif overwrite_setting:
            if nameserver_obj["content"] == ip:
                print "Entry already up-to-date (%s.%s)." % (domain, tld)
            else:
                # delete entry and recreate it
                delete_result = inwx_conn.nameserver.deleteRecord({
                    "id": nameserver_obj["id"]
                })
                # print json.dumps(delete_result, indent=1)
                print "Domain entry for %s.%s deleted." % (domain, tld)

                create_result = inwx_conn.nameserver.createRecord({
                    "type": "A",
                    "content": ip,
                    "name": domain,
                    "domain": tld
                })
                # print json.dumps(create_result, indent=1)
                print "Domain entry for %s.%s re-created with updated informations." % (domain, tld)
        else:
            print "Domain already existing but should not get overwritten... (%s.%s)" % (domain, tld)

if __name__ == "__main__":
    main()
