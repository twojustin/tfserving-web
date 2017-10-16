

# docker cp build_tf_serving.sh hopeful_saha:/build_tf_serving.sh
#

# Clone the source from Github
git clone --recurse-submodules https://github.com/tensorflow/serving

# Pin the version of Tensorflow Serving and its submodule
# v1.3.0
TENSOR_SERVING_COMMIT_HASH=267d682
# v1.3.0
TENSORFLOW_COMMIT_HASH=9e76bf3
cd /serving && git checkout $TENSOR_SERVING_COMMIT_HASH
cd /serving/tensorflow && git checkout $TENSORFLOW_COMMIT_HASH
cd /serving/tensorflow && ./configure

cd /serving && bazel test tensorflow_serving/...

#  Tensorflow Serving uses Bazel as the build tool. The Docker image already have Bazel installed in it.
# Run the following command to build the source with Bazel

# cd /serving && bazel build -c opt //tensorflow_serving/model_servers:tensorflow_model_server --jobs 10 --curses no --discard_analysis_cache
# The following bazel option flags was added:
# -c (compilation_mode): the compilation mode flag affects the the C++ generation. ‘opt’ compilation mode is selected to enable optimization and disable the assert calls.
# — discard_analysis_cache: will discard the analysis cache immediately after the analysis phase completes. This reduces memory usage by ~10%, but makes further incremental builds slower.
# — jobs: The default number of jobs spawned by bazel is 200. Depending on the system configuration of your host, you might like to update this parameter. We tune ours to 10.
