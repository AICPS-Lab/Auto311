# ReadME
This repo contains essential information about the implementation of Auto311 and instructions for reproduction. All code files are carefully commented on and explained for better readability.
## Access to Our Demo Video
Find the video here: [link](https://www.youtube.com/watch?v=g2gvhK5nkUI).
Subscribe to our YouTube channel for the latest updates: [link](https://www.youtube.com/channel/UCAfUvVTJzvaLbd9GwQRvClg).
## Access to Trained Models
Due to the submission size limit, trained models that appeared in our paper are stored and uploaded to an anonymous Google Drive. Please access using this [link](https://drive.google.com/drive/folders/1h3QK4W-qc5QXwhdjBu0BidZDIBxd33VU?usp=sharing). 
This shared folder contains the following sub-folders: 
- [**incident_type_prediction**](https://drive.google.com/drive/folders/1zOtFTVDpeXOcbcgUECox0zBTsRzEWnKu?usp=drive_link), where contains all regarded models to predict the incident type(s) based on caller utterances.
  - **huggingface_bins**: contains all models in huggingface format.
  - **torch_bins**: contains all models in plain torch formats.
- [**information_itemization**](https://drive.google.com/drive/folders/1_YKmQO4MzodiIoorMeE1QEKuLYLW38bL?usp=drive_link), where contains all regarded models to itemize information based on caller utterances.
  - _auto311_info_itemization_narrative.pth_: refers to the itemization model on narrative fields.
  - **binary_questions**: contains all regarded models dealing with binary fields.

We provide model weights in both plain [PyTorch format](https://pytorch.org/docs/stable/generated/torch.nn.Module.html) or [Huggingface model](https://huggingface.co/docs/transformers/main/main_classes/model) format. Please load the weights using corresponding functions: `[corresponding_bert_types].from_pretrained(model_path)` and `torch.load(model_path)`.
**_Confidence measurement_** in textual outputs can be found in the `obtain_conf_scores()` in the _Info_Itemization_Train&Eval.ipynb_ under the **train_eval_scripts** folder. Please check the module codes carefully to ensure the downloaded models are placed at the desired path.

## System Dependencies

### Hardware Information
Experiments are mainly conducted on a local machine with a 2.50GHz CPU, 32GB memory, and Nvidia GeForce RTX 3080Ti GPU (also remote Google Colab notebooks with T4 GPUs).
### Environment Setups
We provide more detailed system environment files on required Python packages in `environemnt.yml`
Following are the major packages we applied in Auto311:
- [whisper](https://github.com/openai/whisper): for speech-to-text transcription. PS: full functionality also requires [ffmpeg](https://www.ffmpeg.org/) installed.
- [bark](https://github.com/suno-ai/bark)/[pyttsx3](https://pypi.org/project/pyttsx3/)/[gtts](https://github.com/pndurette/gTTS)/: for text-to-speech generation. Different methods can be configured in the `text_to_speech(.)` function at `modules/conversational_interface.py`.
- [transformers](https://github.com/huggingface/transformers): for the bert model and its variants.
- [sentence-transformer](https://www.sbert.net/): for semantic similarity in confidence measurement.
- [YAKE](https://liaad.github.io/yake/): for keyword overlapping in confidence measurement.

## Scripts and Commands

We include scripts and commands for both experiment-oriented reproduction and system-level demonstration. System codes can be found in both submission and this [link](https://drive.google.com/drive/folders/1Llw3SXZef8mp0Gpqx5705W9GMdkZpkxf?usp=drive_link).

### Experiment Reproduction
All relevant scripts can be found under the **train_eval_scripts** folder.
- `Incident_Type_Prediction_Train&Eval.ipynb`: includes all code files needed for incident type prediction, containing all mentioned NN models and BERT. You may need to fetch `bert-base-uncased` from Huggingface.
- `Info_Itemization_Train&Eval.ipynb` & `Info_Itemization_binary_Train&Eval.ipynb`: contains all code files needed for binary and narrative information itemization. You may need to fetch `distilbert-base-cased-distilled-squad` from Huggingface. Baseline models on other benchmark datasets can be loaded by switching [model_name] in both transformer models and tokenizers, e.g., `deepset/roberta-base-squad2`, `google/bigbird-base-trivia-itc`, `allenai/longformer-large-4096-finetuned-triviaqa`.

### System Demonstration
We highly recommend launching runtimes in a Windows OS. 
Considering full demonstration requires ALL mentioned packages and models installed and loaded PROPERLY, we also provide demo runtimes (under the`/demos` folder). To avoid overflowing RAM, we also recommend component-wise test runs -- `modules/incident_type_prediction.py` & `modules/information_itemization.py`.
The information we feed to these demo runtimes is testing results on our local machine. Thus running those files bypasss calling heavy models and only showcases our system logic. To run the demo runtimes:
`cp ./demos/demo_[cases].py ./demo_[cases].py && python3 demo_[cases].py`

## Restricted Data Sharing
We have signed a non-disclosure agreement (NDA) with the local government, restricting any forms of data sharing. However, we do introduce one data sample from our dataset with private and sensitive information masked in Appendix I.
Regarding any future dataset access, please contact the [local government](https://www.nashville.gov/departments/emergency-communications/quality-assurance-program) directly.
