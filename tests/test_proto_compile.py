#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `proto_compile` package."""

import os
import tempfile
import typing

import pytest
from click.testing import CliRunner

from proto_compile import cli, proto_compile
from proto_compile.options import (
    BaseCompilerOptions,
    CompilerOptions,
    CompileTarget,
    Target,
)
from proto_compile.utils import PathLike, rglob

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
PROTO_DIR = os.path.join(TEST_DIR, "protos")


def sort(paths: typing.List[PathLike]) -> typing.List[str]:
    return sorted([str(p) for p in paths])


def base_options(
    out_dir: PathLike,
    proto_source_dir: PathLike = PROTO_DIR,
    clear_output_dirs: bool = True,
    verbosity: int = 3,
) -> BaseCompilerOptions:
    return BaseCompilerOptions(
        proto_source_dir=proto_source_dir,
        output_dir=out_dir,
        clear_output_dirs=clear_output_dirs,
        verbosity=verbosity,
    )


def test_command_line_interface() -> None:
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.proto_compile)
    assert result.exit_code == 0
    assert "Usage: proto-compile" in result.output
    help_result = runner.invoke(cli.proto_compile, ["--help"])
    assert help_result.exit_code == 0
    assert "Show this message and exit." in help_result.output


test_targets: typing.List[
    typing.Tuple[
        typing.List[CompileTarget],
        typing.List[PathLike],
    ]
] = [
    (
        [CompileTarget(Target.JAVASCRIPT)],
        [
            "routesummary.js",
            "point.js",
            "healthcheckrequest.js",
            "healthcheckresponse.js",
            "routenote.js",
            "feature.js",
            "rectangle.js",
        ],
    ),
    (
        [CompileTarget(Target.CPP)],
        [
            "example_service.pb.h",
            "example_service.pb.cc",
            "health.pb.cc",
            "health.pb.h",
        ],
    ),
    ([CompileTarget(Target.CSHARP)], ["ExampleService.cs", "Health.cs"]),
    (
        [CompileTarget(Target.GO)],
        [
            "google.golang.org/grpc/examples/route_guide/routeguide/example_service.pb.go",
            "google.golang.org/grpc/health/grpc_health_v1/health.pb.go",
        ],
    ),
    (
        [CompileTarget(Target.JAVA)],
        [
            "io/grpc/examples/routeguide/PointOrBuilder.java",
            "io/grpc/examples/routeguide/Point.java",
            "io/grpc/examples/routeguide/RouteNoteOrBuilder.java",
            "io/grpc/examples/routeguide/Feature.java",
            "io/grpc/examples/routeguide/RectangleOrBuilder.java",
            "io/grpc/examples/routeguide/RouteNote.java",
            "io/grpc/examples/routeguide/RouteSummary.java",
            "io/grpc/examples/routeguide/FeatureOrBuilder.java",
            "io/grpc/examples/routeguide/RouteSummaryOrBuilder.java",
            "io/grpc/examples/routeguide/Rectangle.java",
            "io/grpc/examples/routeguide/RouteGuideProto.java",
            "io/grpc/health/v1/HealthCheckRequest.java",
            "io/grpc/health/v1/HealthCheckRequestOrBuilder.java",
            "io/grpc/health/v1/HealthCheckResponse.java",
            "io/grpc/health/v1/HealthCheckResponseOrBuilder.java",
            "io/grpc/health/v1/HealthProto.java",
        ],
    ),
    (
        [CompileTarget(Target.JAVA), CompileTarget(Target.KOTLIN)],
        [
            "io/grpc/examples/routeguide/PointOrBuilder.java",
            "io/grpc/examples/routeguide/Point.java",
            "io/grpc/examples/routeguide/RouteNoteOrBuilder.java",
            "io/grpc/examples/routeguide/Feature.java",
            "io/grpc/examples/routeguide/RectangleOrBuilder.java",
            "io/grpc/examples/routeguide/RouteSummaryKt.kt",
            "io/grpc/examples/routeguide/RouteNote.java",
            "io/grpc/examples/routeguide/RouteSummary.java",
            "io/grpc/examples/routeguide/RectangleKt.kt",
            "io/grpc/examples/routeguide/RouteGuideProtoKt.kt",
            "io/grpc/examples/routeguide/FeatureOrBuilder.java",
            "io/grpc/examples/routeguide/RouteSummaryOrBuilder.java",
            "io/grpc/examples/routeguide/FeatureKt.kt",
            "io/grpc/examples/routeguide/Rectangle.java",
            "io/grpc/examples/routeguide/RouteNoteKt.kt",
            "io/grpc/examples/routeguide/PointKt.kt",
            "io/grpc/examples/routeguide/RouteGuideProto.java",
            "io/grpc/health/v1/HealthCheckRequest.java",
            "io/grpc/health/v1/HealthCheckRequestKt.kt",
            "io/grpc/health/v1/HealthCheckRequestOrBuilder.java",
            "io/grpc/health/v1/HealthCheckResponse.java",
            "io/grpc/health/v1/HealthCheckResponseKt.kt",
            "io/grpc/health/v1/HealthCheckResponseOrBuilder.java",
            "io/grpc/health/v1/HealthProto.java",
            "io/grpc/health/v1/HealthProtoKt.kt",
        ],
    ),
    ([CompileTarget(Target.PYTHON)], ["example_service_pb2.py", "health_pb2.py"]),
    (
        [
            CompileTarget(
                Target.JAVASCRIPT,
                out_options="import_style=commonjs,binary",
            ),
            CompileTarget(
                Target.GRPC_WEB,
                out_options="import_style=typescript,mode=grpcwebtext",
            ),
        ],
        [
            "example_service_pb.d.ts",
            "example_service_pb.js",
            "Example_serviceServiceClientPb.ts",
            "HealthServiceClientPb.ts",
            "health_pb.d.ts",
            "health_pb.js",
        ],
    ),
    (
        [
            CompileTarget(
                Target.JAVASCRIPT,
                out_options="import_style=commonjs,binary",
            ),
            CompileTarget(
                Target.IMPROBABLE_GRPC_WEB,
                # out_options="import_style=typescript,mode=grpcwebtext",
            ),
        ],
        [
            "example_service_pb.d.ts",
            "example_service_pb.js",
            "health_pb.d.ts",
            "health_pb.js",
        ],
    ),
    (
        [CompileTarget(Target.JAVASCRIPT), CompileTarget(Target.JAVASCRIPT_GRPC)],
        [
            "routesummary.js",
            "point.js",
            "routenote.js",
            "feature.js",
            "example_service_grpc_pb.js",
            "rectangle.js",
            "health_grpc_pb.js",
            "healthcheckrequest.js",
            "healthcheckresponse.js",
        ],
    ),
    (
        [
            CompileTarget(Target.TYPESCRIPT),
            CompileTarget(Target.JAVASCRIPT),
            CompileTarget(Target.JAVASCRIPT_GRPC),
        ],
        [
            "routesummary.js",
            "point.js",
            "routenote.js",
            "feature.js",
            "example_service_grpc_pb.js",
            "example_service_pb.d.ts",
            "rectangle.js",
            "health_grpc_pb.js",
            "healthcheckrequest.js",
            "healthcheckresponse.js",
            "health_pb.d.ts",
        ],
    ),
    (
        [CompileTarget(Target.GO), CompileTarget(Target.GO_GRPC)],
        [
            "google.golang.org/grpc/examples/route_guide/routeguide/example_service.pb.go",
            "google.golang.org/grpc/examples/route_guide/routeguide/example_service_grpc.pb.go",
            "google.golang.org/grpc/health/grpc_health_v1/health.pb.go",
            "google.golang.org/grpc/health/grpc_health_v1/health_grpc.pb.go",
        ],
    ),
    (
        [
            CompileTarget(Target.GO, out_options="paths=source_relative"),
            CompileTarget(Target.GO_GRPC, out_options="paths=source_relative"),
        ],
        [
            "health.pb.go",
            "health_grpc.pb.go",
            "example_service.pb.go",
            "example_service_grpc.pb.go",
        ],
    ),
    (
        [CompileTarget(Target.PYTHON), CompileTarget(Target.PYTHON_GRPC)],
        [
            "example_service_pb2.py",
            "example_service_pb2_grpc.py",
            "health_pb2.py",
            "health_pb2_grpc.py",
        ],
    ),
]

if os.environ.get("CI", False):
    test_targets += [
        # ([CompileTarget(Target.DART)], []),
        # ([CompileTarget(Target.MYPY)], []),
    ]


@pytest.mark.parametrize("targets, outputs", test_targets)
def test_compile(
    targets: typing.List[CompileTarget], outputs: typing.List[PathLike]
) -> None:
    """Test compiling protos for different languages"""

    with tempfile.TemporaryDirectory() as tmp:
        settings = CompilerOptions(
            base_options=base_options(tmp),
            targets=targets,
        )
        proto_compile.compile(settings)
        assert sort(rglob(tmp)) == sort(outputs)
