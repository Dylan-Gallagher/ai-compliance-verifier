#!/bin/bash

## Optional: Set up dreeam environment with Mamba
#mamba create -n dreeam python=3.8.13
#mamba activate dreeam
#mamba install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 cudatoolkit=11.3 -c pytorch
#mamba install transformers==4.14.1 numpy==1.22.4 opt-einsum==3.3.0 wandb ujson tqdm pandas


# Clone DREEAM repo
git clone https://github.com/Dylan-Gallagher/dreeam.git
cd dreeam

#mv ../extracted_entities/* .
mv ../dataset/* .

# Optional: Download pretrained weights using gdown. Alternatively, download directly from Google Drive https://drive.google.com/file/d/1Frs8PZiBAoN2l2elZUgYVcejbxbo2dJz/view?usp=sharing
#pip install gdown
#gdown --id 1Frs8PZiBAoN2l2elZUgYVcejbxbo2dJz -O weights.zip
#sudo apt-get install unzip
#unzip weights
#rm weights.zip
#mv dreeam_models/roberta_student_best.ckpt dreeam_models/best.ckpt

# Fine tune on our data.
python run.py --do_train \
--data_dir dataset/docred \
--transformer_type roberta \
--replace_output_layer \
--freeze_early_layers \
--model_name_or_path roberta-large \
--display_name test_training_run_1 \
--train_file train.json \
--dev_file dev.json \
--save_path checkpoints \
--load_path dreeam_models \
--train_batch_size 4 \
--test_batch_size 8 \
--gradient_accumulation_steps 1 \
--num_labels 14 \
--lr_transformer 1e-6 \
--lr_added 3e-6 \
--max_grad_norm 2.0 \
--evi_thresh 0.2 \
--evi_lambda 1.0 \
--warmup_ratio 0.1 \
--num_train_epochs 30.0 \
--seed 22 \
--num_class 26


