import enum


class Target(enum.Enum):
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


DEFAULT_PROTOC_VERSION = "3.17.3"

DEFAULT_PLUGIN_VERSIONS = {
    Target.GRPC_WEB: "1.2.0",
}
