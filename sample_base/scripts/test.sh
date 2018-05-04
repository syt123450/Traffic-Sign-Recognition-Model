BASE_DIR=`pwd`"/.."
labels=$BASE_DIR"/models/output_labels.txt"
graph=$BASE_DIR"/models/output_graph.pb"

test_out_path=$BASE_DIR"/models/test_results/test_results.txt"
file_dir=$BASE_DIR"/data/images/testing_images"

source activate tensorflow
python test_images.py \
--graph=$graph \
--labels=$labels \
--input_layer=Mul \
--output_layer=final_result \
--input_mean=128 --input_std=128 \
--test_out_path=$test_out_path \
--file_dir=$file_dir
