import requests
import os
import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def fetch_github_repo(owner, repo, max_files=20, max_size=10000, token=None):
    """
    Fetch up to max_files text files from a GitHub repository and consolidate them
    into a single structured document for LLM processing.
    
    Args:
        owner: GitHub username/organization
        repo: Repository name
        max_files: Maximum number of files to fetch
        max_size: Maximum file size in bytes
        token: GitHub personal access token (optional for public repos)
    
    Returns:
        Tuple of (consolidated text, file count)
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
        # Stop if we've reached the file limit
        if len(repo_contents) >= max_files:
            return
            
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
            # Stop if we've reached the file limit
            if len(repo_contents) >= max_files:
                return
                
            if item["type"] == "dir":
                # Recursively fetch directory contents
                fetch_contents(item["path"])
            elif item["type"] == "file":
                # Skip binary files and files larger than max_size
                if (item["size"] > max_size or 
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
    
    # Create a consolidated document with all file contents
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    consolidated_text = f"""# GitHub Repository: {owner}/{repo}
# Retrieved: {current_date}
# Files Analyzed: {len(repo_contents)}

"""
    
    # Add each file with clear separation
    for file_path, content in repo_contents.items():
        consolidated_text += f"""
{'=' * 80}
FILE: {file_path}
{'=' * 80}

{content}

"""
    
    return consolidated_text, len(repo_contents)

def save_consolidated_text(text, owner, repo, output_file=None):
    """Save the consolidated text to a file"""
    if output_file is None:
        output_file = f"{owner}_{repo}_analysis.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    return output_file

if __name__ == "__main__":
    # Replace with repository details
    owner = "niklas-xgh-dev"
    repo = "ttx"
    token = os.environ.get("GITHUB_TOKEN")  # Set this as environment variable
    
    consolidated_text, file_count = fetch_github_repo(owner, repo, token=token)
    
    print(f"Fetched {file_count} files from {owner}/{repo}")
    
    # Save to file
    output_file = save_consolidated_text(consolidated_text, owner, repo)
    print(f"Saved consolidated repository content to: {output_file}")
    
    # Preview
    print("\nPreview of consolidated text:")
    print(consolidated_text[:500] + "...")