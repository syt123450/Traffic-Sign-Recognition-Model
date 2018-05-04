BASE_DIR=`pwd`"/.."
IMAGE_DIR=$BASE_DIR"/data/images/training_images"
CURRENT_TIME=$(date "+%Y_%m_%d_%H_%M_%S")
OUTPUT_GRAPH=$BASE_DIR"/models/output_graph.pb"
INTERMEDIATE_OUTPUT_GRAPHS_DIR=$BASE_DIR"/data/inter_train/intermediate"
OUTPUT_LABELS=$BASE_DIR"/models/output_labels.txt"
MODEL_DIR=$BASE_DIR"/data/inter_train/imagenet"
SUMMARIES_DIR=$BASE_DIR"/data/inter_train/log"
BOTTLENECK_DIR=$BASE_DIR"/data/inter_train/bottleneck"
SAVED_MODEL_DIR=$BASE_DIR"/data/inter_train/saved_model/"$CURRENT_TIME

source activate tensorflow
python /Users/zchholmes/PycharmProjects/tensorflow/tensorflow/examples/image_retraining/retrain.py \
--image_dir $IMAGE_DIR \
--output_graph $OUTPUT_GRAPH \
--intermediate_output_graphs_dir $INTERMEDIATE_OUTPUT_GRAPHS_DIR \
--output_labels $OUTPUT_LABELS \
--model_dir $MODEL_DIR \
--summaries_dir $SUMMARIES_DIR \
--bottleneck_dir $BOTTLENECK_DIR \
--saved_model_dir $SAVED_MODEL_DIR

