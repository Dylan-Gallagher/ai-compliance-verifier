# Clone DREEAM repo
git clone https://github.com/Dylan-Gallagher/dreeam.git
cd dreeam

# Download pre-trained weights
gdown 1AezMu2bL7pz0sodk8dJMdy_iXCLBeIDh

mkdir dreeam_models
mv last.ckpt dreeam_models/best.ckpt

python run.py --data_dir dataset/docred \
--eval_mode infer_only \
--transformer_type roberta \
--model_name_or_path roberta-large \
--display_name inference_test \
--train_file test.json \
--dev_file test.json \
--test_file test.json \
--load_path dreeam_models \
--test_batch_size 1 \
--num_labels 14 \
--evi_thresh 0.2 \
--evi_lambda 1.0 \
--seed 22 \
--num_class 26