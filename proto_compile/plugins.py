import abc
import os
import platform
import subprocess
import typing
import uuid
from pathlib import Path

import pkg_resources
from grpc_tools.protoc import main as _compile_python_grpc

from proto_compile.utils import PathLike, download_executable, print_command
from proto_compile.versions import DEFAULT_PLUGIN_VERSIONS, Target

PROTOC_RELEASE_BASE_URL = (
    "https://github.com/protocolbuffers/protobuf/releases/download"
)


class ProtoCompiler:
    def compile(self, arguments: typing.List[str], verbosity: int = 0) -> None:
        raise NotImplementedError()


class ProtocPlugin(abc.ABC):
    def __init__(
        self,
        dest_dir: PathLike,
        version: typing.Optional[str] = None,
        verbosity: int = 0,
    ) -> None:
        self.dest_dir: Path = Path(dest_dir)
        self.version = version
        self.verbosity = verbosity

    def install(self) -> None:
        pass

    def install_hint(self) -> typing.Optional[str]:
        pass

    def executable(self) -> typing.Optional[PathLike]:
        return None

    def compiler(self) -> typing.Optional[ProtoCompiler]:
        return None


class DartPlugin(ProtocPlugin):
    def executable(self) -> typing.Optional[PathLike]:
        # todo
        return "protoc-gen-dart"

    def install_hint(self) -> typing.Optional[str]:
        return """
        The dart plugin has to be installed. Run:

            $ pub global activate protoc_plugin

        or consult the official documentation.
        """


class MyPyPlugin(ProtocPlugin):
    def executable(self) -> typing.Optional[PathLike]:
        # todo
        return "protoc-gen-mypy"

    def install_hint(self) -> typing.Optional[str]:
        return """
        The {} plugin has to be installed. Run:

            $ pip install mypy-protobuf

        This is only necessary to use the generated files:

            $ mypy>=0.910 types-protobuf>=0.1.14

        or consult the official documentation.
        """.format(
            self.executable
        )


class PythonGrpcProtoCompiler(ProtoCompiler):
    def compile(self, arguments: typing.List[str], verbosity: int = 0) -> None:
        proto_include = pkg_resources.resource_filename("grpc_tools", "_proto")
        arguments = [""] + arguments + ["-I{}".format(proto_include)]
        command = "python -m grpc_tools.protoc {}".format(
            " ".join([str(arg) for arg in arguments[1:]])
        )

        if verbosity > 0:
            print(command)
        return_code = int(_compile_python_grpc(arguments))
        if return_code != 0:
            raise subprocess.CalledProcessError(cmd=command, returncode=return_code)


class PythonGrpcPlugin(ProtocPlugin):
    def executable(self) -> typing.Optional[PathLike]:
        return "grpc_node_plugin"

    def compiler(self) -> typing.Optional[ProtoCompiler]:
        return PythonGrpcProtoCompiler()


class TypescriptPlugin(ProtocPlugin):
    def executable(self) -> typing.Optional[PathLike]:
        return "grpc_node_plugin"

    def install_hint(self) -> typing.Optional[str]:
        return """
        The {} plugin has to be installed. Run:

            $ npm install -g ts-protoc-gen

        or consult the official documentation.
        """.format(
            self.executable
        )


class GolangPlugin(ProtocPlugin):
    def executable(self) -> typing.Optional[PathLike]:
        return self.dest_dir / "bin" / "protoc-gen-go"

    def install_hint(self) -> typing.Optional[str]:
        return "install golang"

    def install(self) -> None:
        plugin_version = self.version or DEFAULT_PLUGIN_VERSIONS[Target.GO]
        install_command = str(" ").join(
            [
                "go",
                "install",
                "google.golang.org/protobuf/cmd/protoc-gen-go@%s" % plugin_version,
            ]
        )
        if self.verbosity > 0:
            print(install_command)
        print_command(
            install_command,
            stderr=subprocess.STDOUT,
            shell=True,
            env={
                **os.environ,
                **{
                    "GOPATH": str(self.dest_dir.absolute()),
                    "GOCACHE": str(
                        (self.dest_dir / ("cache-%s" % uuid.uuid4())).absolute()
                    ),
                },
            },
            cwd=self.dest_dir,
            verbosity=self.verbosity,
        )


class GolangGrpcPlugin(ProtocPlugin):
    def executable(self) -> typing.Optional[PathLike]:
        return self.dest_dir / "bin" / "protoc-gen-go-grpc"

    def install_hint(self) -> typing.Optional[str]:
        return "install golang"

    def install(self) -> None:
        plugin_version = self.version or DEFAULT_PLUGIN_VERSIONS[Target.GO_GRPC]
        for pkg in [
            "google.golang.org/protobuf/cmd/protoc-gen-go@%s"
            % DEFAULT_PLUGIN_VERSIONS[Target.GO_GRPC],
            "google.golang.org/grpc/cmd/protoc-gen-go-grpc@%s" % plugin_version,
        ]:
            install_command = str(" ").join(
                [
                    "go",
                    "install",
                    pkg,
                ]
            )
            if self.verbosity > 0:
                print(install_command)
            print_command(
                install_command,
                stderr=subprocess.STDOUT,
                shell=True,
                env={
                    **os.environ,
                    **{
                        "GOPATH": str(self.dest_dir.absolute()),
                        "GOCACHE": str(
                            (self.dest_dir / ("cache-%s" % uuid.uuid4())).absolute()
                        ),
                    },
                },
                cwd=self.dest_dir,
                verbosity=self.verbosity,
            )


class PHPGrpcPlugin(ProtocPlugin):
    def executable(self) -> typing.Optional[PathLike]:
        return "grpc_php_plugin"

    def install_hint(self) -> typing.Optional[str]:
        return """
        The {} plugin has to be installed. Run:

            $ pecl install grpc

        or consult the official documentation.
        """.format(
            self.executable
        )


class JavascriptGrpcPlugin(ProtocPlugin):
    def executable(self) -> typing.Optional[PathLike]:
        return (
            self.dest_dir / "node_modules" / "grpc-tools" / "bin" / "grpc_node_plugin"
        )

    def install_hint(self) -> typing.Optional[str]:
        return "install npm"

    def install(self) -> None:
        install_command = str(" ").join(
            [
                "npm",
                "install",
                "grpc-tools",
            ]
        )
        if self.verbosity > 0:
            print(install_command)
        print_command(
            install_command,
            stderr=subprocess.STDOUT,
            shell=True,
            cwd=self.dest_dir,
            verbosity=self.verbosity,
        )


class GrpcWebPlugin(ProtocPlugin):
    GRPC_WEB_PLUGIN_RELEASE_BASE_URL = (
        "https://github.com/grpc/grpc-web/releases/download"
    )

    def executable(self) -> PathLike:
        return self.dest_dir / "protoc-gen-grpc-web"

    def install(self) -> None:
        system = platform.system().lower()  # darwin
        system_alias = "osx" if system == "darwin" else system  # osx for darwin
        system_alias = "win64" if system == "windows" else system_alias  # windows
        machine_arch = "x86_64" if system == "windows" else platform.machine()

        grpc_web_plugin_version = (
            self.version or DEFAULT_PLUGIN_VERSIONS[Target.GRPC_WEB]
        )
        grpc_web_plugin_release_url = GrpcWebPlugin.GRPC_WEB_PLUGIN_RELEASE_BASE_URL
        grpc_web_plugin_release_url += "/" + grpc_web_plugin_version
        grpc_web_plugin_release_url += (
            "/protoc-gen-grpc-web-"
            + grpc_web_plugin_version
            + "-"
            + system
            + "-"
            + machine_arch
            + (".exe" if system == "windows" else "")
        )
        download_executable(
            # self.executable(),
            url=grpc_web_plugin_release_url,
            executable=self.executable(),
            dest_dir=self.dest_dir,
            verbosity=self.verbosity,
        )


class ImprobableGrpcWebPlugin(ProtocPlugin):
    def executable(self) -> typing.Optional[PathLike]:
        return (
            self.dest_dir / "node_modules" / "ts-protoc-gen" / "bin" / "protoc-gen-ts"
        )

    def install_hint(self) -> typing.Optional[str]:
        return "install npm"

    def install(self) -> None:
        install_command = str(" ").join(
            [
                "npm",
                "install",
                "ts-protoc-gen",
            ]
        )
        if self.verbosity > 0:
            print(install_command)
        print_command(
            install_command,
            stderr=subprocess.STDOUT,
            shell=True,
            cwd=self.dest_dir,
            verbosity=self.verbosity,
        )


PLUGINS = {
    Target.DART: DartPlugin,
    Target.MYPY: MyPyPlugin,
    Target.TYPESCRIPT: TypescriptPlugin,
    Target.GO: GolangPlugin,
    # GRPC
    Target.JAVASCRIPT_GRPC: JavascriptGrpcPlugin,
    Target.PYTHON_GRPC: PythonGrpcPlugin,
    Target.GO_GRPC: GolangGrpcPlugin,
    Target.GRPC_WEB: GrpcWebPlugin,
    Target.IMPROBABLE_GRPC_WEB: ImprobableGrpcWebPlugin,
}
