# Guardian
Getting started
1. clone the project:
    ```bash
    git clone git@github.com:efspoonler/fallstudie.git 
    ```
2. navigate into the projects root folder.
3. create virtual environment (in project root)
    ```bash
    pip install virtualenv
    python3 -m venv .venv
    source .venv/bin/activate
    ```
4. install requirements from requirements.txt
    ```bash
    pip install -r requirements.txt
    ```
5. put your personal api key into a new file at /crawler/key.txt
    ```bash
     echo "PUT_YOUR_PERSONAL_KEY_HERE" > ./crawler/key.txt

    ```
6. run main.py
