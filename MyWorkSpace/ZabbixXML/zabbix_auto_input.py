from xml.dom.minidom import *
import csv
import os.path
import glob
if glob.glob("*.csv"):
    p = glob.glob("*.csv")
    # info = xml.dom.minidom.parse('inform_43c2.xml')
    info = Document()
    group = info.documentElement
    zbb_ver = info.createElement("version")
    zbb_ver.appendChild(info.createTextNode("4.0"))
    zbb_exp = info.createElement("zabbix_export")
    info.appendChild(zbb_exp)
    zbb_exp.appendChild(zbb_ver)
    new_hosts = info.createElement("hosts")
    for file in p:
        num_str = 1
        with open(file, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")
            for row in reader:
                ip_addr = row['ip']
                server_name = row['server']
                hostname = row['hostname']
                template_name = row['template']
                GROUPS = row['group']
                num_str += 1
                if ip_addr != "" and server_name != "" and hostname != "" and template_name != "":
                    new_agent = info.createElement("host")
                    host_name = info.createElement("host")
                    host_name.appendChild(info.createTextNode(hostname))
                    name = info.createElement("name")
                    name.appendChild(info.createTextNode(server_name))
                    description = info.createElement("description")
                    proxy = info.createElement("proxy")
                    status = info.createElement("status")
                    status.appendChild(info.createTextNode("0"))
                    #
                    #
                    ipmi_authtype = info.createElement("ipmi_authtype")
                    ipmi_authtype.appendChild(info.createTextNode("-1"))
                    ipmi_privilege = info.createElement("ipmi_privilege")
                    ipmi_privilege.appendChild(info.createTextNode("2"))
                    ipmi_username = info.createElement("ipmi_username")
                    ipmi_password = info.createElement("ipmi_password")
                    #
                    #
                    tls_connect = info.createElement("tls_connect")
                    tls_connect.appendChild(info.createTextNode("1"))
                    tls_accept = info.createElement("tls_accept")
                    tls_accept.appendChild(info.createTextNode("1"))

                    tls_issuer = info.createElement("tls_issuer")
                    tls_subject = info.createElement("tls_subject")
                    tls_psk_identity = info.createElement("tls_psk_identity")
                    tls_psk = info.createElement("tls_psk")

                    templates = info.createElement("templates")
                    template = info.createElement("template")
                    name_temp = info.createElement("name")
                    name_temp.appendChild(info.createTextNode(template_name))

                    groups = info.createElement("groups")
                    group_new = info.createElement("group")
                    name_group = info.createElement("name")
                    name_group.appendChild(info.createTextNode(GROUPS))

                    interfaces = info.createElement("interfaces")
                    interface = info.createElement("interface")

                    default = info.createElement("default")
                    default.appendChild(info.createTextNode("1"))

                    type_el = info.createElement("type")
                    type_el.appendChild(info.createTextNode("1"))

                    useip = info.createElement("useip")
                    useip.appendChild(info.createTextNode("1"))
                    ip = info.createElement("ip")
                    ip.appendChild(info.createTextNode(ip_addr))

                    dns = info.createElement("dns")
                    port = info.createElement("port")
                    port.appendChild(info.createTextNode("10050"))

                    bulk = info.createElement("bulk")
                    bulk.appendChild(info.createTextNode("1"))

                    interface_ref = info.createElement("interface_ref")
                    interface_ref.appendChild(info.createTextNode("if1"))

                    applications = info.createElement("applications")
                    items = info.createElement("items")
                    discovery_rules = info.createElement("discovery_rules")
                    httptests = info.createElement("httptests")
                    macros = info.createElement("macros")
                    inventory = info.createElement("inventory")
                    #
                    template.appendChild(name_temp)
                    templates.appendChild(template)
                    #
                    group_new.appendChild(name_group)
                    groups.appendChild(group_new)
                    #
                    interfaces.appendChild(interface)
                    interface.appendChild(default)
                    interface.appendChild(type_el)
                    interface.appendChild(useip)
                    interface.appendChild(ip)
                    interface.appendChild(dns)
                    interface.appendChild(port)
                    interface.appendChild(bulk)
                    interface.appendChild(interface_ref)
                    #
                    new_agent.appendChild(host_name)
                    new_agent.appendChild(name)
                    new_agent.appendChild(description)
                    new_agent.appendChild(proxy)
                    new_agent.appendChild(status)
                    new_agent.appendChild(ipmi_authtype)
                    new_agent.appendChild(ipmi_privilege)
                    new_agent.appendChild(ipmi_username)
                    new_agent.appendChild(ipmi_password)
                    new_agent.appendChild(tls_connect)
                    new_agent.appendChild(tls_accept)
                    new_agent.appendChild(tls_issuer)
                    new_agent.appendChild(tls_subject)
                    new_agent.appendChild(tls_psk_identity)
                    new_agent.appendChild(tls_psk)
                    new_agent.appendChild(templates)
                    new_agent.appendChild(groups)
                    new_agent.appendChild(interfaces)
                    new_agent.appendChild(applications)
                    new_agent.appendChild(items)
                    new_agent.appendChild(discovery_rules)
                    new_agent.appendChild(httptests)
                    new_agent.appendChild(macros)
                    new_agent.appendChild(inventory)
                    new_hosts.appendChild(new_agent)
                    zbb_exp.appendChild(new_hosts)
                else:
                    print("Incorrect data was entered in the "+ file + " on the line " + str(num_str) )
    i = 1
    while True:
        if os.path.exists('zbx_agent_'+ str(i) +'.xml' ):
            i+=1
        else:
            info.writexml(open('zbx_agent_'+ str(i) + '.xml', 'w'))
            print('file zbx_agent_'+str(i)+'.xml is created')
            break
else:
    print(".csv file not found")