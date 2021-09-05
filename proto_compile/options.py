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
        self, base_options: BaseCompilerOptions, targets: typing.List[CompileTarget],
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
