# -*- coding: utf-8 -*-

"""Main module."""

import os
import platform
import shutil
import subprocess
import tempfile
import typing

from proto_compile import versions as versions
from proto_compile.options import BaseCompilerOptions, CompilerOptions, CompileTarget
from proto_compile.plugins import PLUGINS, PROTOC_RELEASE_BASE_URL, ProtoCompiler
from proto_compile.utils import PathLike, download_executable, print_command, rglob
from proto_compile.versions import Target


class DefaultProtoCompiler(ProtoCompiler):
    def __init__(self, executable: PathLike) -> None:
        self.executable = executable

    def compile(self, arguments: typing.List[str], verbosity: int = 0) -> None:
        protoc_command_str = str(" ").join([str(self.executable)] + arguments)
        if verbosity > 0:
            print(protoc_command_str)
        print_command(
            protoc_command_str,
            stderr=subprocess.STDOUT,
            shell=True,
            verbosity=verbosity,
        )


def compile(options: CompilerOptions) -> None:
    abs_source = os.path.abspath(options.proto_source_dir)

    proto_files = rglob(abs_source, match="*.proto", absolute=True)
    if not len(proto_files) > 0:
        print("{} does not contain any .proto files. Skipping...".format(abs_source))
        return

    if options.minimal_include_dir:
        abs_source = os.path.abspath(os.path.dirname(os.path.commonpath(proto_files)))

    tmp_dir = tempfile.mkdtemp()
    try:
        system = platform.system().lower()  # darwin
        system_alias = "osx" if system == "darwin" else system  # osx for darwin
        system_alias = "win64" if system == "windows" else system_alias  # windows
        machine_arch = "" if system == "windows" else platform.machine()

        if options.verbosity > 0:
            print(system_alias)
        protoc_release_url = PROTOC_RELEASE_BASE_URL
        protoc_release_url += "/v" + options.protoc_version
        protoc_release_url += (
            "/protoc-"
            + options.protoc_version
            + "-"
            + system_alias
            + ("" if system == "windows" else "-")
            + machine_arch
            + ".zip"
        )

        protoc_executable = download_executable(
            "protoc",
            url=protoc_release_url,
            executable="protoc/bin/protoc",
            dest_dir=tmp_dir,
            verbosity=options.verbosity,
        )
        print_command(
            "ls -la " + tmp_dir,
            stderr=subprocess.STDOUT,
            shell=True,
            verbosity=options.verbosity,
        )

        # eventually clear the output dirs
        # also find the correct compiler
        proto_compiler: ProtoCompiler = DefaultProtoCompiler(protoc_executable)
        for target in options.targets:
            abs_output = os.path.abspath(target.output_dir or options.output_dir)
            if os.path.exists(abs_output) and options.clear_output_dirs:
                shutil.rmtree(abs_output, ignore_errors=True)

        # construct protoc compiler command
        proto_arguments: typing.List[str] = ["-I={}".format(abs_source)] + [
            str(f) for f in proto_files
        ]

        for target in options.targets:
            abs_output = os.path.abspath(target.output_dir or options.output_dir)
            language = str(target.language.value)

            # get the required plugin
            if target.language in PLUGINS:
                plugin = PLUGINS[target.language]
                if plugin.compiler is not None:
                    proto_compiler = plugin.compiler

                try:
                    # attempt to install the plugin
                    plugin_executable = plugin.installed()
                    if plugin_executable is None:
                        plugin_executable = plugin.install(
                            tmp_dir,
                            version=target.plugin_version,
                            verbosity=options.verbosity,
                        )
                    if plugin_executable is not None:
                        proto_arguments.append(
                            "--plugin=protoc-gen-{}={}".format(
                                language, plugin_executable,
                            )
                        )

                except NotImplementedError:
                    # show installation hints
                    try:
                        print(plugin.install_hint())
                    except NotImplementedError:
                        pass

            proto_arguments.append(
                "--{}_out={}{}".format(
                    str(target.language.value),
                    str((target.out_options + ":") if target.out_options else ""),
                    abs_output,
                )
            )

            # make sure the output path exists
            if not os.path.exists(abs_output):
                os.makedirs(abs_output)

        proto_compiler.compile(proto_arguments, verbosity=options.verbosity)
    finally:
        # Remove temporary directory
        shutil.rmtree(tmp_dir, ignore_errors=True)


def compile_grpc_web(
    options: BaseCompilerOptions,
    js_out_options: typing.Optional[str] = "import_style=commonjs,binary",
    js_output_dir: typing.Optional[PathLike] = None,
    grpc_web_out_options: typing.Optional[
        str
    ] = "import_style=typescript,mode=grpcwebtext",
    grpc_web_plugin_version: typing.Optional[str] = versions.DEFAULT_PLUGIN_VERSIONS[
        Target.GRPC_WEB
    ],
    grpc_web_output_dir: typing.Optional[PathLike] = None,
) -> None:
    return compile(
        CompilerOptions(
            base_options=options,
            targets=[
                CompileTarget(
                    Target.JAVASCRIPT,
                    output_dir=js_output_dir,
                    out_options=js_out_options,
                ),
                CompileTarget(
                    Target.GRPC_WEB,
                    out_options=grpc_web_out_options,
                    output_dir=grpc_web_output_dir,
                    plugin_version=grpc_web_plugin_version,
                ),
            ],
        )
    )


def compile_python_grpc(
    options: BaseCompilerOptions,
    py_out_options: typing.Optional[str] = None,
    py_output_dir: typing.Optional[PathLike] = None,
    py_grpc_out_options: typing.Optional[str] = None,
    py_grpc_output_dir: typing.Optional[PathLike] = None,
) -> None:
    return compile(
        CompilerOptions(
            base_options=options,
            targets=[
                CompileTarget(
                    Target.PYTHON, output_dir=py_output_dir, out_options=py_out_options,
                ),
                CompileTarget(
                    Target.PYTHON_GRPC,
                    out_options=py_grpc_out_options,
                    output_dir=py_grpc_output_dir,
                ),
            ],
        )
    )
