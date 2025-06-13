import argparse
import re
import subprocess
import sys
from typing import Dict

def parse_java_version(version_output: str) -> Dict[str, str]:
    """
    Parse Java version output and extract relevant information.
    """
    result = {}
    
    jdk_match = re.search(r'openjdk version "(\d+)\.(\d+)\.(\d+)-beta"', version_output)
    if jdk_match:
        result['openjdk_version'] = f"{jdk_match.group(1)}.{jdk_match.group(2)}"
    
    openj9_match = re.search(r'OpenJ9\s*-\s*([0-9a-f]+)', version_output)
    if openj9_match:
        result['openj9_commit'] = openj9_match.group(1)
    
    omr_match = re.search(r'OMR\s*-\s*([0-9a-f]+)', version_output)
    if omr_match:
        result['omr_commit'] = omr_match.group(1)
    
    jcl_match = re.search(r'JCL\s*-\s*([0-9a-f]+)', version_output)
    if jcl_match:
        result['jcl_commit'] = jcl_match.group(1)
    
    required_fields = ['openjdk_version', 'openj9_commit', 'omr_commit', 'jcl_commit']
    missing_fields = [field for field in required_fields if field not in result]
    
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
    
    return result

def generate_compare_urls(good_info: Dict[str, str], bad_info: Dict[str, str]) -> Dict[str, str]:
    """
    Generate comparison URLs for each component.
    """
    urls = {}
    jdk_version = good_info['openjdk_version']
    
    urls['openj9'] = f"https://github.com/eclipse-openj9/openj9/compare/{good_info['openj9_commit']}...{bad_info['openj9_commit']}"
    urls['omr'] = f"https://github.com/eclipse-omr/omr/compare/{good_info['omr_commit']}...{bad_info['omr_commit']}"
    urls['jcl'] = f"https://github.com/ibmruntimes/openj9-openjdk-jdk{jdk_version}/compare/{good_info['jcl_commit']}...{bad_info['jcl_commit']}"
    
    return urls

def trigger_github_workflow(good_build: str, bad_build: str) -> None:
    """
    Trigger the GitHub workflow using gh CLI.
    """
    try:
        good_build_escaped = good_build.replace('"', '\\"')
        bad_build_escaped = bad_build.replace('"', '\\"')
        
        cmd = [
            'gh', 'workflow', 'run', 'gitcompare.yml',
            '-f', f'good_build="{good_build_escaped}"',
            '-f', f'bad_build="{bad_build_escaped}"'
        ]
        subprocess.run(cmd, check=True)
        print("Successfully triggered GitHub workflow")
    except subprocess.CalledProcessError as e:
        print(f"Failed to trigger workflow: {e}", file=sys.stderr)
        sys.exit(1)

def main():

    good_build = input("Enter good build version string: ")
    bad_build = input("Enter bad build version string: ")
    
    try:
        good_info = parse_java_version(good_build)
        bad_info = parse_java_version(bad_build)
        
        urls = generate_compare_urls(good_info, bad_info)
        
        print("OpenJ9: " + urls['openj9'])
        print("OMR: " + urls['omr'])
        print("JCL: " + urls['jcl'])
        
        trigger_github_workflow(good_build, bad_build)
        
    except ValueError as e:
        print(f"Error parsing version output: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 