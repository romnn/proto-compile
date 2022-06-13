import enum


class Target(enum.Enum):
    # maps Target T to identifier X, e.g. --X_out=...
    JAVASCRIPT = "js"
    TYPESCRIPT = "ts"
    JAVASCRIPT_GRPC = "grpc"
    CPP = "cpp"
    CSHARP = "csharp"
    DART = "dart"
    GO = "go"
    GO_GRPC = "go-grpc"
    JAVA = "java"
    KOTLIN = "kotlin"
    PYTHON = "python"
    PYTHON_GRPC = "grpc_python"
    MYPY = "mypy"
    GRPC_WEB = "grpc-web"
    IMPROBABLE_GRPC_WEB = "ts"


DEFAULT_PROTOC_VERSION = "3.20.1"

DEFAULT_PLUGIN_VERSIONS = {
    Target.GRPC_WEB: "1.3.1",
    Target.GO: "latest",  # protoc-gen-go
    Target.GO_GRPC: "latest",  # protoc-gen-go
    Target.IMPROBABLE_GRPC_WEB: "0.15.0",
}
