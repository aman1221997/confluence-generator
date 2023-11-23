from atlassian import Confluence
from collections.abc import Hashable
import yaml
import argparse



def generate_table_row(host_name, ip_address, location, atype, dc_type, ssh, ip_prefixes, geolocation):
    ip_prefixes_list = ""
    for ip_prefixes_item in ip_prefixes:
        ip_prefixes_list = ip_prefixes_list + f"<p>{ip_prefixes_item}</p>"

    geolocation_list = ""
    for geolocation_item in geolocation:
        if type(geolocation_item) == dict:
            latitude = geolocation_item.get('lat', False)
            longitude = geolocation_item.get('lon', False)
            geolocation_list = geolocation_list + f'<p><a href="https://www.google.com/maps/place/{latitude},{longitude}">{latitude,longitude}</a></p>'

    return f'''
    <tr>
        <td class="numberingColumn" />
        <td><p><a href="https://{host_name}">{host_name}</a></p></td>
        <td><p>{ip_address}</p></td>
        <td><p>{location}</p></td>
        <td><p>{atype}</p></td>
        <td><p>{dc_type}</p></td>
        <td><p>{ssh}</p></td>
        <td>{ip_prefixes_list}</td>
        <td>{geolocation_list}</td>
    </tr>'''


def get_body_content():

    body_table_start = '''<strong><table data-layout="full-width" ac:local-id="31c3c0b3-5577-4426-ac7c-e41cd49eae76">
               <colgroup>
                   <col /><col style="width: 310.0px;" /><col style="width: 175.0px;" /><col style="width: 110.0px;" />
                   <col style="width: 150.0px;" /><col style="width: 110.0px;" /><col style="width: 400.0px;" />
                   <col style="width: 250.0px;" /><col style="width: 400.0px;" />
               </colgroup>'''

    body_table_header = '''<tbody>
               <tr>
                   <th class="numberingColumn" />
                   <th><p>Hostname</p></th>
                   <th><p>IP Address</p></th>
                   <th><p>Location</p></th>
                   <th><p>Type</p></th>
                   <th><p>DC Type</p></th>
                   <th><p>SSH</p></th>
                   <th><p>IP Prefixes</p></th>
                   <th><p>Geolocation(latitude,longitude)</p></th>
               </tr>'''

    body_table_end = '''</tbody>
                </table>
                </strong>'''

    reformatted = {}
    
    with open('servers.yml', 'r') as f:
        try:
            host_info = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)
        # host_info = yaml.safe_load(f)
        for host, details in host_info.items():
            host_name = details.get('web', host)
            ip_address = details.get('ip_address', '-')
            environment = details.get('environment', '-')
            location = details.get('location', '-')
            atype = details.get('type', '-')
            status = details.get('status', '-')
            dc_type = details.get('dc_type', '-')
            ssh = details.get('ssh', '-')
            ip_prefixes = details.get('ip_prefixes', '-')
            geolocation = details.get('geolocation', '-')

            if not reformatted.get(environment, False):
                reformatted[environment] = {}
            if not reformatted[environment].get(status, False):
                reformatted[environment][status] = []
            reformatted[environment][status].append(
                generate_table_row(host_name, ip_address, location, atype, dc_type, ssh, ip_prefixes, geolocation))

    body_content2 = '''<h1>Overview</h1>
                        <p>A list of Servers owned by the Production team</p>'''

    for environment, details in reformatted.items():
        body_content2 = body_content2 + f"<h1>{environment}</h1>"
        for status, hosts in details.items():
            body_content2 = body_content2 + f"<h3>{status}</h3> " + body_table_start + body_table_header
            for host in hosts:
                body_content2 = body_content2 + f"{host}"
            body_content2 = body_content2 + body_table_end

    return body_content2


def get_links_at_bottom():
    resources = '''<h1>Resources and Links</h1>
                    <p><a href="https://jfrog.com/help/r/jfrog-artifactory-documentation">Artifactory Documentation</a></p> '''
    return resources


def main():
    # Create the parser
    parser = argparse.ArgumentParser()

    # Add an argument
    # parser.add_argument('--name', type=str, required=True)
    parser.add_argument('--username', nargs='?', help='passed username', required=True, type=str)
    parser.add_argument('--password', nargs='?', help='passed password', required=True, type=str)

    # Parse the argument
    args = parser.parse_args()

    # User Credentials
    username = args.username
    password = args.password


    confluence = Confluence(
        url='https://<organization>.atlassian.net',
        username=username,
        password=password,
        cloud=True)

    page_id = '<page Id>'
    title = '<title>'
    #page_id = '3272245321'
    #title = 'Production Servers'
    

    body = get_body_content()
    body = body + get_links_at_bottom()

    print(body)

    # Update page if already exist
    confluence.update_page(page_id, title, body, parent_id=None, type='page', representation='storage', minor_edit=False)

if __name__ == '__main__':
  main()
