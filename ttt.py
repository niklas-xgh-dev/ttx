import requests
import base64
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def fetch_github_repo(owner, repo, token=None):
    """
    Fetch all text files from a GitHub repository.
    
    Args:
        owner: GitHub username/organization
        repo: Repository name
        token: GitHub personal access token (optional for public repos)
    
    Returns:
        Dictionary mapping file paths to their content
    """
    # Base URL for GitHub API
    base_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    
    # Headers for API requests
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    # Dictionary to store file contents
    repo_contents = {}
    
    def fetch_contents(path=""):
        """Recursively fetch contents of the repository"""
        url = base_url
        if path:
            url = f"{base_url}/{path}"
            
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        contents = response.json()
        
        # Handle when contents is a single file (not a list)
        if not isinstance(contents, list):
            contents = [contents]
        
        for item in contents:
            if item["type"] == "dir":
                # Recursively fetch directory contents
                fetch_contents(item["path"])
            elif item["type"] == "file":
                # Skip binary files and very large files
                if (item["size"] > 1000000 or 
                    any(item["name"].endswith(ext) for ext in 
                        ['.png', '.jpg', '.jpeg', '.gif', '.exe', '.zip'])):
                    continue
                
                # Fetch file content
                file_response = requests.get(item["download_url"], headers=headers)
                try:
                    file_content = file_response.text
                    repo_contents[item["path"]] = file_content
                except:
                    # Skip if file can't be decoded as text
                    continue
    
    # Start fetching from root
    fetch_contents()
    return repo_contents

if __name__ == "__main__":
    # Replace with repository details
    owner = "username"
    repo = "repository-name"
    token = os.environ.get("GITHUB_TOKEN")  # Set this as environment variable
    
    repo_contents = fetch_github_repo(owner, repo, token)
    print(f"Fetched {len(repo_contents)} files from {owner}/{repo}")
    
    # Print first few files for verification
    for i, (path, content) in enumerate(list(repo_contents.items())[:3]):
        print(f"\nFile: {path}")
        print(f"Preview: {content[:100]}...")