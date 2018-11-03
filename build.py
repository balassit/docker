#!/usr/bin/env python3
"""This script handles building and optionally pushing docker images from this repo"""
from datetime import datetime
import argparse
import json
import os
import subprocess

try:
    from pip import main as pipmain
except:
    from pip._internal import main as pipmain

def install(package):
    """installs packages"""
    pipmain(['install', package, '-q'])


def read_dockerfile_for_args(target):
    """Reads a dockerfile to get all ARGs and pulls values from dockerfile or environment"""
    import colorama
    build_args = {}
    missing_args = {}
    empty_string = ""

    # read dockerfile for args that have no value
    try:
        with open(target + '/Dockerfile') as dockerfile:
            for line in dockerfile:
                if line.startswith("ARG "):
                    dockerfile_args = line.replace(
                        "ARG ", "").strip("\n").split("=")

                    arg_name = dockerfile_args[0]
                    arg_value = ""

                    if len(dockerfile_args) > 1:
                        arg_value = dockerfile_args[1].strip("\n")

                    env_value = os.environ.get(arg_name)

                    build_args[arg_name] = arg_value
                    if not env_value is None:
                        build_args[arg_name] = env_value

                    if build_args[arg_name] is empty_string:
                        missing_args[arg_name] = arg_name
    except FileNotFoundError:
        exit(f"Dockerfile not found: {target}/Dockerfile")

    if len(missing_args) > 1:
        message = "WARNING: Arguments found with no defined value " \
            "found in Dockerfile or environment [{}]"
        print(colorama.Fore.YELLOW + colorama.Style.BRIGHT +
              message.format(", ".join(missing_args)))

    return build_args


def tag(image_name, new_image_name):
    """tags images"""
    cmd_tag = f"docker tag {image_name} {new_image_name}"
    print(f"COMMAND: {cmd_tag}")
    print("", flush=True)
    return_code = subprocess.call(cmd_tag, shell=True)
    if return_code != 0:
        exit(f"Error with {cmd_tag}")
    return 0


def push(args, image_name_tag):
    """pushes images if the flag is set"""
    if args.push is True:
        cmd_push = f"docker push {image_name_tag}"
        print(f"COMMAND: {cmd_push}")
        print("", flush=True)
        return_code = subprocess.call(cmd_push, shell=True)
        if return_code != 0:
            exit(f"Error with {cmd_push}")
    return 0


def do_version_tag(args, image_name_tag, image_name):
    """do version tag and push"""
    if args.versiontag is True:
        date_stamp = "{:%Y%m%d%H%M%S}".format(datetime.now())
        version_tag = args.tag + '-' + date_stamp
        image_name_version_tag = f"{image_name}:{version_tag}"
        return_code = tag(image_name_tag, image_name_version_tag)
        if return_code == 0:
            push(args, image_name_version_tag)


def do_latest_tag(args, image_name_tag, image_name):
    """do latest tag and push"""
    if args.latest is True:
        if tag(image_name_tag, image_name+':latest'):
            push(args, image_name+':latest')

def createParser():
    parser = argparse.ArgumentParser(
        description='Builds one of the docker images within this dockerfiles repo'
    )

    parser.add_argument(
        'image', help='The image name for building (parent folder)')

    parser.add_argument(
        'tag', help='The image tag for building (subfolder)')

    parser.add_argument(
        '--latest', action='store_true', help='Tag as latest (default false)')

    parser.add_argument(
        '--versiontag', action='store_true', help='Also tag with datetime stamp (default false)')

    parser.add_argument(
        '--nocache', action='store_true', help='Disable cache (default false)')

    parser.add_argument(
        '--proxy', action='store_true', help='Pass proxy build args (default false)')

    parser.add_argument(
        '--push', action='store_true', help='Push after build (default false)')

    parser.add_argument(
        '--nopull', action='store_true', help='Turn off the force pulling of images to use local (default false)')

    return parser


def main():
    """main function"""
    parser = createParser()
    args = parser.parse_args()

    # do build
    target = args.image + '/' + args.tag

    namespace = 'balassit'

    image_name = namespace + '/' + args.image
    image_name_tag = image_name + ':' + args.tag

    build_args = read_dockerfile_for_args(target)

    if args.proxy:
        build_args["http_proxy"] = os.environ.get("http_proxy")
        build_args["https_proxy"] = os.environ.get("https_proxy")
        build_args["no_proxy"] = os.environ.get("no_proxy")
        build_args["HTTP_PROXY"] = os.environ.get("HTTP_PROXY")
        build_args["HTTPS_PROXY"] = os.environ.get("HTTPS_PROXY")
        build_args["NO_PROXY"] = os.environ.get("NO_PROXY")

    print(f"Building image {image_name_tag} with {len(build_args)} build_args:")

    build_arg_list = ""
    for key in build_args:
        print(f"  {key}={build_args[key]}")
        build_arg_list = build_arg_list + f" --build-arg {key}={build_args[key]}"

    build_cmd = f"docker build{'' if args.nopull else ' --pull'}{' --no-cache' if args.nocache else ''}{build_arg_list} --rm -t {image_name_tag} -f ./{target}/Dockerfile ./{target}"

    print(f"COMMAND: {build_cmd}")
    print("", flush=True)

    return_code = subprocess.call(build_cmd, shell=True)
    if return_code != 0:
        exit(f"Error building with {build_cmd}")

    # push with tag
    push(args, image_name_tag)

    # push with datetimestamp
    do_version_tag(args, image_name_tag, image_name)

    # push with latest
    do_latest_tag(args, image_name_tag, image_name)

if __name__ == '__main__':
    install('colorama')
    main()
