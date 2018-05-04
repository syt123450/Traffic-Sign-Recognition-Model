BASE_DIR=`pwd`"/.."
labels=$BASE_DIR"/models/output_labels.txt"
graph=$BASE_DIR"/models/output_graph.pb"

file_dir=$BASE_DIR"/data/images/improving_images_1"
to_dir=$BASE_DIR"/data/images/training_images"
eps=0.65

source activate tensorflow
python move_improved_images.py \
--graph=$graph \
--labels=$labels \
--input_layer=Mul \
--output_layer=final_result \
--input_mean=128 --input_std=128 \
--file_dir=$file_dir \
--to_dir=$to_dir \
--eps=$eps