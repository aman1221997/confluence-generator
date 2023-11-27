# confluence-generator
It orchestrates the seamless synchronization of information within Confluence, ensuring real-time updates whenever changes occur in the servers.yml file of the confluence-generator repository's master branch. This dynamic process not only reflects a commitment to accuracy but also underscores the efficiency and precision of our system's information management, aligning seamlessly with the evolving needs of our organization.

## Prerequisites
*Required tools and services: Confluence, GitHub, Python.*

*Access and permissions needed on Confluence and GitHub.*

## Steps :-
1. To test purpose, create virtual environment first

    ```bash
    python -m venv aman_virtual_env
    source aman_virtual_env/Scripts/activate
   ```

2. To run Confluence generator

    ```bash
    # Install dependencies
    pip install -r requirements.txt

    # If getting issue in installing pyyaml
    pip install --upgrade PyYaml

    # Run confluence generator
    python confluence_generator.py --username <username> --password <password>
    ```


