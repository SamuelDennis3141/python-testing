import yaml


def main():
    services = read_config()
    initial_object = create_docker_compose()
    action_commands = define_action_commands()
    final_object = append_docker_compose(services, initial_object, action_commands)

    write_docker_compose(final_object)


def read_config():
    with open("../scripts.yml", "r") as f:
        return yaml.safe_load(f)


def create_docker_compose():
    return {"versions": 3, "services": {}}


def define_action_commands(directory):
    return {
        "format": '["python3","-m","autopep8","--in-place","--recursive","./src","./tests",]',
        "lint": '["python3", "-m", "pylint", "--recursive=y", "-j","2","./src","./tests"]',
        "test": f'["pip", "install", "-Ur", "requirements.txt", "requirements_dev.txt", "&& ", "python", "-m", "unittest", "discover", "-t", "/app/tests/{directory}"]',
    }


def append_docker_compose(services, current_object):
    for service, directory in services.items():
        action_commands = define_action_commands(directory)
        for action, command in action_commands.items():
            current_object["services"][f"{service}-{action}"] = {
                "build": {"context": ".", "dockerfile": f"Dockerfile.{action}"},
                "workingdir": "./app",
                "command": command,
                "volumes": [
                    f"../src/{directory}: /app/src",
                    f"../tests/{directory}: /app/tests",
                ],
            }
    return current_object


def write_docker_compose(object):
    with open("docker-compose-test.yml", "w") as f:
        yaml.dump(object, f)


if __name__ == "__main__":
    main()
