import fnmatch
import os
import subprocess
import typing
import uuid
from pathlib import Path

PathLike = typing.Union[str, os.PathLike]


def print_command(
    *cmd_args: typing.Any, verbosity: int = 0, **cmd_kwargs: typing.Any
) -> None:
    try:
        output = subprocess.check_output(*cmd_args, **cmd_kwargs).decode("utf-8")
        if verbosity > 1:
            print(output)
    except subprocess.CalledProcessError as e:  # pragma: no cover
        print(e.returncode)
        print(e.output.decode("utf-8"))
        raise


def quote(s: str) -> str:
    return '"' + s + '"'


def download_executable(
    url: str,
    executable: PathLike,
    dest_dir: PathLike,
    unarchive_as: typing.Optional[str] = None,
    verbosity: int = 0,
) -> PathLike:
    # filename = Path(os.path.basename(url)
    # filename = Path(url).name
    is_zip = Path(url).suffix.lower() in [".zip", ".tar", ".tar.gz", ".gz"]
    # is_zip = os.path.splitext(filename)[1].lower() in [".zip", ".tar", ".tar.gz", ".gz"]
    archive = Path(dest_dir) / (str(uuid.uuid4()) if is_zip else executable)
    download_command = str(" ").join(
        [
            "wget",
            "-q",
            "-O",
            str(archive),
            # os.path.join(dest_dir, filename if is_zip else executable),
            quote(url),
        ]
    )
    if verbosity > 0:
        print(download_command)
    print_command(
        download_command,
        stderr=subprocess.STDOUT,
        shell=True,
        verbosity=verbosity,
    )
    executable_path = Path(dest_dir)
    if is_zip:
        unarchived_name = unarchive_as or Path(url).stem
        unzip_command = str(" ").join(
            [
                "unzip",
                # str((dest_dir / Path(url).name).absolute()),
                str(archive),
                "-d",
                # str((Path(dest_dir) / unarchived_name).absolute()),
                str(Path(dest_dir) / unarchived_name),
            ]
        )
        executable_path = executable_path / unarchived_name
        if verbosity > 0:
            print(unzip_command)
        print_command(
            unzip_command,
            stderr=subprocess.STDOUT,
            shell=True,
            verbosity=verbosity,
        )
    executable_path = executable_path / Path(executable)
    chmod_command = str(" ").join(["chmod", "+x", str(executable_path)])
    if verbosity > 0:
        print(chmod_command)
    print_command(
        chmod_command, stderr=subprocess.STDOUT, shell=True, verbosity=verbosity
    )
    return executable_path


def rglob(
    folder: PathLike, absolute: bool = False, match: str = "*"
) -> typing.List[PathLike]:
    matches: typing.List[PathLike] = []
    for root, dirnames, filenames in os.walk(str(folder)):
        for filename in fnmatch.filter(filenames, match):
            abs_match = os.path.join(root, filename)
            matches.append(
                abs_match if absolute else os.path.relpath(abs_match, folder)
            )
    return matches


def executable_in_path(
    name: str, path: typing.Optional[typing.List[PathLike]] = None
) -> typing.Optional[PathLike]:
    """Check if PATH contains an executable"""
    path_items = path or os.environ["PATH"].split(os.pathsep)
    for prefix in path_items:
        filename = os.path.abspath(os.path.join(str(prefix), name))
        executable = os.access(filename, os.X_OK)
        is_not_directory = os.path.isfile(filename)
        if executable and is_not_directory:
            return filename
    return None
