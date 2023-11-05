import requests

def upload(gh_token, repo, path, content):
    data = {
        "message": "Adding post",
        "content": content
    }

    headers = {"Authorization": f"Bearer {gh_token}"}
    requests.put(f"https://api.github.com/repos/{repo}/{path}", json=data)
