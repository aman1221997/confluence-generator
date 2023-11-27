import requests
import argparse


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

    # Confluence details
    confluence_url = 'https://aman19s.atlassian.net'
    space_key = 'Servers'

    # Replace 'your_username' and 'your_password' with your Confluence username and password
    auth = (username, password)

    # Page details
    page_id = '3272245321'
    title = 'Production Servers'

    # Confluence REST API endpoint for creating a new page
    api_url = f'{confluence_url}/wiki/rest/api/content/{page_id}/child/page'

    # Page content (you can customize this)
    content = {
        'type': 'page',
        'title': title,
        'space': {'key': space_key},
        'body': {
            'storage': {
                'value': '<p>This is the list of production servers.</p>',
                'representation': 'storage'
            }
        }
    }

    # Headers for authentication
    headers = {
        'Content-Type': 'application/json',
    }

    # Make the REST API request to create the page
    response = requests.post(api_url, json=content, auth=auth)

    # Check the response status
    if response.status_code == 200:
        print(f'Successfully created the page with title: {title}')
    else:
        print(f'Failed to create the page. Status code: {response.status_code}, Error: {response.text}')


if __name__ == '__main__':
  main()
