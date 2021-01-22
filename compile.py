import argparse
import docker
import json
import requests
import subprocess
import os

# Parse arguments
parser = argparse.ArgumentParser(description='Build dedicated game server docker image')
# Required
parser.add_argument('--godot-version', nargs='?', help='Godot version to use for the server in the following format: 3.2.3', required=True)
# Arguments for building pck
parser.add_argument('--build-project', nargs='?', help='Path to the project.godot file')
parser.add_argument('--godot-editor', nargs='?', help='Path to the godot editor, needed for compiling the godot project. If not specified we will look for a godot executable in the path')
parser.add_argument('--export-template', nargs='?', help='Name of export template')
# Arguments for existing pck
# todo
# Image tag
parser.add_argument('--image-tag', nargs='?', default='gameserver', help='Target docker image name')

args = parser.parse_args()

godot_version = '3.2.3'
if args.godot_version != None:
    godot_version = args.godot_version

# Check if godot version is available
godot_download_url = 'https://downloads.tuxfamily.org/godotengine/' + godot_version + '/Godot_v' + godot_version + '-stable_linux_server.64.zip'
version_check_response = requests.head(godot_download_url)
if version_check_response.status_code != 200:
    print("Godot version " + godot_version + " is not available!")
    exit()

# Check if pck need to get compiled
if args.build_project != None:
    print("Building godot project...")

    # Verify export template is specified
    if args.export_template == None:
        print("No export template is specified!")
        parser.print_help()
        exit()

    godot_executable = "godot"
    if args.godot_editor != None:
        godot_executable = args.godot_editor

    # Build pck file into local directory
    build_process = subprocess.Popen([godot_executable, args.build_project, "--export-pack", args.export_template, os.path.join(os.getcwd(), "server.pck")], stdout=subprocess.PIPE)
    for line in iter(build_process.stdout.readline, b''):
        print(line)
    print("Building done!")

# Create docker client
client = docker.from_env().api

# Build docker image
print("Building docker image...")
streamer = client.build(path=".", decode=True, buildargs={
    'godot_url': godot_download_url
}, tag=args.image_tag)
while True:
    try:
        output = streamer.__next__()
        if 'stream' in output:
            for line in output['stream'].splitlines():
                print(line)
    except StopIteration:
        break

# Remove temporary pck
os.unlink("server.pck")