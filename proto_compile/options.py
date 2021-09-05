import typing

import proto_compile.versions as versions
from proto_compile.utils import PathLike
from proto_compile.versions import Target


class BaseCompilerOptions:
    def __init__(
        self,
        proto_source_dir: PathLike,
        output_dir: PathLike,
        minimal_include_dir: bool = False,
        clear_output_dirs: bool = False,
        verbosity: typing.Optional[int] = None,
        protoc_version: typing.Optional[str] = None,
    ) -> None:
        self.proto_source_dir = proto_source_dir
        self.output_dir = output_dir
        self.minimal_include_dir = minimal_include_dir
        self.clear_output_dirs = clear_output_dirs
        self.verbosity = verbosity or 0
        self.protoc_version = protoc_version or versions.DEFAULT_PROTOC_VERSION


class CompileTarget:
    def __init__(
        self,
        language: Target,
        out_options: typing.Optional[str] = None,
        output_dir: typing.Optional[PathLike] = None,
        plugin_version: typing.Optional[str] = None,
    ):
        self.language = language
        self.out_options = out_options
        self.output_dir = output_dir
        self.plugin_version = plugin_version


class CompilerOptions:
    def __init__(
        self,
        base_options: BaseCompilerOptions,
        targets: typing.List[CompileTarget],
        # js: bool = False,
        # js_out_options: typing.Optional[str] = None,
        # js_output_dir: typing.Optional[str] = None,
        # cpp: bool = False,
        # cpp_out_options: typing.Optional[str] = None,
        # cpp_output_dir: typing.Optional[str] = None,
        # cpp_output_dir: typing.Optional[str] = None,
        # csharp: bool = False,
        # csharp_out_options: typing.Optional[str] = None,
        # csharp_output_dir: typing.Optional[str] = None,
        # csharp_plugin_version: typing.Optional[str] = None,
        # dart: bool = False,
        # dart_out_options: typing.Optional[str] = None,
        # dart_output_dir: typing.Optional[str] = None,
        # dart_plugin_version: typing.Optional[str] = None,
        # go: bool = False,
        # go_out_options: typing.Optional[str] = None,
        # go_output_dir: typing.Optional[str] = None,
        # go_plugin_version: typing.Optional[str] = None,
        # java: bool = False,
        # java_out_options: typing.Optional[str] = None,
        # java_output_dir: typing.Optional[str] = None,
        # java_plugin_version: typing.Optional[str] = None,
        # kotlin: bool = False,
        # kotlin_out_options: typing.Optional[str] = None,
        # kotlin_output_dir: typing.Optional[str] = None,
        # kotlin_plugin_version: typing.Optional[str] = None,
        # py: bool = False,
        # py_out_options: typing.Optional[str] = None,
        # py_output_dir: typing.Optional[str] = None,
        # py_plugin_version: typing.Optional[str] = None,
        # grpc_web: bool = False,
        # grpc_web_out_options: typing.Optional[str] = None,
        # grpc_web_plugin_version: typing.Optional[str] = None,
    ) -> None:
        self.proto_source_dir = base_options.proto_source_dir
        self.minimal_include_dir = base_options.minimal_include_dir
        self.clear_output_dirs = base_options.clear_output_dirs
        self.output_dir = base_options.output_dir
        self.verbosity = base_options.verbosity
        self.protoc_version = (
            base_options.protoc_version or versions.DEFAULT_PROTOC_VERSION
        )
        self.targets = targets
        # self.js = js
        # self.js_out_options = js_out_options
        # self.js_output_dir = js_output_dir
        # self.js_plugin_version = js_plugin_version
        # self.cpp = cpp
        # self.cpp_out_options = cpp_out_options
        # self.cpp_output_dir = cpp_output_dir
        # self.csharp = csharp
        # self.csharp_out_options = csharp_out_options
        # self.csharp_output_dir = csharp_output_dir
        # self.dart = dart
        # self.dart_out_options = dart_out_options
        # self.dart_output_dir = dart_output_dir
        # self.go = go
        # self.go_out_options = go_out_options
        # self.go_output_dir = go_output_dir
        # self.java = java
        # self.java_out_options = java_out_options
        # self.java_output_dir = java_output_dir
        # self.kotlin = kotlin
        # self.kotlin_out_options = kotlin_out_options
        # self.kotlin_output_dir = kotlin_output_dir
        # self.py = py
        # self.py_out_options = py_out_options
        # self.py_output_dir = py_output_dir
        # self.grpc_web = grpc_web
        # self.grpc_web_out_options = grpc_web_out_options
        # self.grpc_web_output_dir = grpc_web_output_dir
        # self.grpc_web_plugin_version = grpc_web_plugin_version
