import platform
import subprocess
import typing

import pkg_resources
from grpc_tools.protoc import main as _compile_python_grpc

from proto_compile.utils import PathLike, download_executable, executable_in_path
from proto_compile.versions import DEFAULT_PLUGIN_VERSIONS, Target

PROTOC_RELEASE_BASE_URL = (
    "https://github.com/protocolbuffers/protobuf/releases/download"
)
GRPC_WEB_PLUGIN_RELEASE_BASE_URL = "https://github.com/grpc/grpc-web/releases/download"


class ProtoCompiler:
    def compile(self, arguments: typing.List[str], verbosity: int = 0) -> None:
        raise NotImplementedError()


class ProtocPlugin:
    def __init__(self,) -> None:
        self.executable = ""
        self.compiler: typing.Optional[ProtoCompiler] = None

    def installed(self) -> typing.Optional[PathLike]:
        return executable_in_path(self.executable)

    def install(
        self,
        dest_dir: PathLike,
        version: typing.Optional[str] = None,
        verbosity: int = 0,
    ) -> str:
        pass

    def install_hint(self) -> str:
        pass


class DartPlugin(ProtocPlugin):
    def __init__(self) -> None:
        super().__init__()
        self.executable = "protoc-gen-dart"

    def install_hint(self) -> str:
        return """
        The dart plugin has to be installed. Run:

            $ pub global activate protoc_plugin

        or consult the official documentation.
        """


class MyPyPlugin(ProtocPlugin):
    def __init__(self) -> None:
        super().__init__()
        self.executable = "protoc-gen-mypy"

    def install_hint(self) -> str:
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
    def __init__(self) -> None:
        super().__init__()
        self.executable = "grpc_node_plugin"
        self.compiler = PythonGrpcProtoCompiler()


class TypescriptPlugin(ProtocPlugin):
    def __init__(self) -> None:
        super().__init__()
        self.executable = "grpc_node_plugin"

    def install_hint(self) -> str:
        return """
        The {} plugin has to be installed. Run:

            $ npm install -g ts-protoc-gen

        or consult the official documentation.
        """.format(
            self.executable
        )


class GolangPlugin(ProtocPlugin):
    def __init__(self) -> None:
        super().__init__()
        self.executable = "protoc-gen-go"

    def install_hint(self) -> str:
        return """
        The {} plugin has to be installed. Run:

            $ go install google.golang.org/protobuf/cmd/protoc-gen-go
            $ export PATH="$PATH:$(go env GOPATH)/bin"

        or consult the official documentation.
        """.format(
            self.executable
        )


class GolangGrpcPlugin(ProtocPlugin):
    def __init__(self) -> None:
        super().__init__()
        self.executable = "protoc-gen-go-grpc"

    def install_hint(self) -> str:
        return """
        The {} plugin has to be installed. Run:

            $ go install google.golang.org/protobuf/cmd/protoc-gen-go
            $ go install google.golang.org/grpc/cmd/protoc-gen-go-grpc
            $ export PATH="$PATH:$(go env GOPATH)/bin"

        or consult the official documentation.
        """.format(
            self.executable
        )


class PHPGrpcPlugin(ProtocPlugin):
    def __init__(self) -> None:
        super().__init__()
        self.executable = "grpc_php_plugin"

    def install_hint(self) -> str:
        return """
        The {} plugin has to be installed. Run:

            $ pecl install grpc

        or consult the official documentation.
        """.format(
            self.executable
        )


class JavascriptGrpcPlugin(ProtocPlugin):
    def __init__(self) -> None:
        super().__init__()
        self.executable = "grpc_tools_node_protoc_plugin"

    def install_hint(self) -> str:
        return """
        The {} plugin has to be installed. Run:

            $ npm install -g grpc-tools

        or consult the official documentation.
        """.format(
            self.executable
        )


class GrpcWebPlugin(ProtocPlugin):
    def __init__(self) -> None:
        super().__init__()
        self.executable = "protoc-gen-grpc-web"

    def install_hint(self) -> str:
        raise NotImplementedError()

    def install(
        self,
        dest_dir: PathLike,
        version: typing.Optional[str] = None,
        verbosity: int = 0,
    ) -> str:
        system = platform.system().lower()  # darwin
        system_alias = "osx" if system == "darwin" else system  # osx for darwin
        system_alias = "win64" if system == "windows" else system_alias  # windows
        machine_arch = "x86_64" if system == "windows" else platform.machine()

        grpc_web_plugin_version = version or DEFAULT_PLUGIN_VERSIONS[Target.GRPC_WEB]
        grpc_web_plugin_release_url = GRPC_WEB_PLUGIN_RELEASE_BASE_URL
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
        plugin_executable = download_executable(
            self.executable,
            url=grpc_web_plugin_release_url,
            executable=self.executable,
            dest_dir=dest_dir,
            verbosity=verbosity,
        )
        return plugin_executable


PLUGINS = {
    Target.DART: DartPlugin(),
    Target.MYPY: MyPyPlugin(),
    Target.TYPESCRIPT: TypescriptPlugin(),
    Target.GO: GolangPlugin(),
    # GRPC
    Target.JAVASCRIPT_GRPC: JavascriptGrpcPlugin(),
    Target.PYTHON_GRPC: PythonGrpcPlugin(),
    Target.GO_GRPC: GolangGrpcPlugin(),
    Target.GRPC_WEB: GrpcWebPlugin(),
}
