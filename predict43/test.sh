basedir=`pwd`
labels="/Users/zchholmes/Desktop/255/Project/trained_models/output_labels_5.txt"
graph="/Users/zchholmes/Desktop/255/Project/trained_models/output_graph_5.pb"

file_dir="/Users/zchholmes/src_images/testing_images"

python model/test_images.py \
--graph=$graph \
--labels=$labels \
--input_layer=Mul \
--output_layer=final_result \
--input_mean=128 --input_std=128 \
--file_dir=$file_dir
