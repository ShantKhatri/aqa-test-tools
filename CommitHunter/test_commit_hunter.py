import subprocess
import sys
import os
from commit_hunter import parse_java_version, generate_compare_urls

def test_workflow():
    # Test data
    good_build = '''openjdk version "21.0.7-beta" 2025-04-15
IBM Semeru Runtime Open Edition 21.0.7+6-202504292333
Eclipse OpenJ9 VM 21.0.7+6-202504292333
OpenJ9   - ab9584ee40
OMR      - 38fbca611
JCL      - 39c20bca9'''

    bad_build = '''openjdk version "21.0.8-beta" 2025-07-15
IBM Semeru Runtime Open Edition 21.0.8+2-202505132342
Eclipse OpenJ9 VM 21.0.8+2-202505132342
OpenJ9   - 4d92969242
OMR      - b4802c56c
JCL      - 2119fbf3f'''

    try:
        good_info = parse_java_version(good_build)
        bad_info = parse_java_version(bad_build)
        print("Version parsing successful!")

        urls = generate_compare_urls(good_info, bad_info)
        
        with open('output.txt', 'w') as f:
            f.write(f"OpenJ9: {urls['openj9']}\n")
            f.write(f"OMR: {urls['omr']}\n")
            f.write(f"JCL: {urls['jcl']}\n")
        print("Output saved to output.txt")
        
        with open('output.txt', 'r') as f:
            for line in f:
                print(line.strip())

        try:
            subprocess.run(['gh', '--version'], check=True, capture_output=True)
            subprocess.run(['gh', 'auth', 'status'], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Error: GitHub CLI not found or not authenticated")

    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    test_workflow() 