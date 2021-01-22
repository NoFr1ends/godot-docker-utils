# Godot Server Docker Template
This project contains example and template scripts used to create docker images for dedicated server written in Godot.

It is optimized and intended to be called by a CI/CD pipeline to automatically build and push Docker images.

## Notes
This project is a short script which is only used by me right now so features you need might be still missing.
If you find a bug or have a feature idea please open an issue.

## Requirements
- Docker 
- Python 3

Install python dependencies using ``pip install -r requirements.txt``

## Usage
Execute ``python compile.py --help`` to view all available arguments.

```
usage: compile.py [-h] [--godot-version [GODOT_VERSION]] [--build-project [BUILD_PROJECT]] [--godot-editor [GODOT_EDITOR]] [--export-template [EXPORT_TEMPLATE]] [--image-tag [IMAGE_TAG]]

Build dedicated game server docker image

optional arguments:
  -h, --help            show this help message and exit
  --godot-version [GODOT_VERSION]
                        Godot version to use for the server in the following format: 3.2.3
  --build-project [BUILD_PROJECT]
                        Path to the project.godot file
  --godot-editor [GODOT_EDITOR]
                        Path to the godot editor, needed for compiling the godot project. If not specified we will look for a godot executable in the path
  --export-template [EXPORT_TEMPLATE]
                        Name of export template
  --image-tag [IMAGE_TAG]
                        Target docker image name
```

### Example
To compile a project and automatically create a docker image run the following command:
```
python3 compile.py --godot-version=3.2.3 --build-project=PATH_TO_PROJECT/project.godot --export-template=TEMPLATE_NAME --godot-editor=PATH_TO_GODOT_EDITOR_EXECUTABLE/godot --image-tag=gameserver
```

Please make sure to replace the placeholders before executing the command. The defined export template should be a Linux/X11 export template.

After that you can run your game server using docker:
```
docker run -d gameserver
```

For forwarding a local port to the container add the following parameter ``-p LOCALPORT:TARGETPORT``.
For more details about how to use Docker consult the Docker documentation.

## License
This project is licensed under the MIT license.