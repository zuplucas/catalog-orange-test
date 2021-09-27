#!/usr/bin/python3
import glob
import json
import os
import shutil
import zipfile
from pathlib import Path
from time import time

import requests
from templateframework.config import DEFAULT_SAMPLE_FOLDER_NAME
from templateframework.runner import apply_template


def download_release(repo_url, repo_tag):
    release_url = f'{repo_url}/archive/refs/tags/{repo_tag}.zip'

    new_path = Path(f'downloads/{"/".join(repo_url.split("/")[3:])}-{repo_tag}')
    if new_path.exists():
        return str(next(new_path.iterdir()))

    new_path.mkdir(parents=True, exist_ok=True)
    output_zip = new_path.joinpath(f'template-{time()}.zip')

    access_token = os.environ.get("RIT_CREDENTIAL_GITHUB_TOKEN")
    r = requests.get(
        release_url,
        headers={'Authorization': f'token {access_token}'}
    )

    with open(output_zip, 'wb') as f:
        f.write(r.content)

    with zipfile.ZipFile(output_zip, 'r') as zip_ref:
        zip_ref.extractall(str(new_path))

    os.remove(output_zip)

    output_path = str(next(new_path.iterdir()))
    return output_path


def main():
    input_json = os.environ.get("RIT_INPUT_JSON")
    input_obj = json.loads(input_json)

    template_input = input_obj['template_input']

    target = Path(input_obj['target'])

    for template in input_obj['templates']:
        repo_url = template["repo_url"]
        repo_tag = template["repo_tag"]
        output = download_release(repo_url, repo_tag)

        # Path onde está o template baixado do repo
        home = Path(output)

        # Nome do template que será executado (está no OrangeTemplate)
        template_name = template["template_name"]

        sample = DEFAULT_SAMPLE_FOLDER_NAME if template["sample"] is True else None

        apply_template(
            template=template_name,
            target=target,
            inputs=template_input,
            sample_folder=sample,
            home=home
        )

        print(f'\nTemplate with name "{template_name}" applied with success!\n')
    os.system(f'tree {target}')


def run():
    try:
        main()
    finally:
        files = glob.glob('downloads/*')
        for f in files:
            shutil.rmtree(f)
