basedir=`pwd`
labels=$basedir"/model/output_labels.txt"
graph=$basedir"/model/output_graph.pb"

python model/label_image.py \
--graph=$graph \
--labels=$labels \
--input_layer=Mul \
--output_layer=final_result \
--input_mean=128 --input_std=128 \
--image=$1
