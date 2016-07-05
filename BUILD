# Description: Tensorflow Serving examples.

package(
    default_visibility = ["//tensorflow_serving:internal"],
    features = [
        "-parse_headers",
        "no_layering_check",
    ],
)

licenses(["notice"])  # Apache 2.0

exports_files(["LICENSE"])

load("//tensorflow_serving:serving.bzl", "serving_proto_library")

filegroup(
    name = "all_files",
    srcs = glob(
        ["**/*"],
        exclude = [
            "**/METADATA",
            "**/OWNERS",
        ],
    ),
)

serving_proto_library(
    name = "sc_plan_generator_proto",
    srcs = ["sc_plan_generator.proto"],
    has_services = 1,
    cc_api_version = 2,
    cc_grpc_version = 1,
)


py_binary(
    name = "sc_plan_generator_export",
    srcs = [
        "sc_plan_generator_export.py",
    ],
    deps = [
        "//tensorflow_serving/session_bundle:exporter",
        "@org_tensorflow//tensorflow:tensorflow_py",
    ],
)

#cc_binary(
#    name = "sc_plan_generator",
#    srcs = [
#        "sc_plan_generator.cc",
#    ],
#    linkopts = ["-lm"],
#    deps = [
#        ":sc_plan_generator_proto",
#        "//tensorflow_serving/servables/tensorflow:session_bundle_config_proto",
#        "//tensorflow_serving/servables/tensorflow:session_bundle_factory",
#        "//tensorflow_serving/session_bundle",
#        "//tensorflow_serving/session_bundle:manifest_proto",
#        "//tensorflow_serving/session_bundle:signature",
#        "@grpc//:grpc++",
#        "@org_tensorflow//tensorflow/core:core_cpu",
#        "@org_tensorflow//tensorflow/core:framework",
#        "@org_tensorflow//tensorflow/core:lib",
#        "@org_tensorflow//tensorflow/core:protos_all_cc",
#        "@org_tensorflow//tensorflow/core:tensorflow",
#    ],
#)
