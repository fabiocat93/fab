import sys
import os

audio_representation_folder = '../../audio_representation/'
script_directory = os.path.dirname(os.path.abspath(__file__))
audio_representation_folder_absolute_path = os.path.join(script_directory, audio_representation_folder)
# adding freeVC_folder to the system path
sys.path.insert(0, audio_representation_folder_absolute_path)

from audio_representation import AudioRepresentation
from transformers import SpeechT5Processor, SpeechT5ForSpeechToSpeech, SpeechT5HifiGan
import soundfile as sf
import torchaudio
from tqdm import tqdm

processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_vc")
model = SpeechT5ForSpeechToSpeech.from_pretrained("microsoft/speecht5_vc")
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")
speakerEmbeddingExtractor = AudioRepresentation(model_name="SpkrecEcapaVoxceleb")


def anonymize(source_files, target_files, output_files):
    for line in tqdm(zip(source_files, target_files, output_files)):
        source_file, target_file, output_file = line
        source_waveform, source_sample_rate = torchaudio.load(source_file)
        source_audio_descriptor = processor(audio=source_waveform, sampling_rate=source_sample_rate,
                                            return_tensors="pt")
        target_waveform, target_sample_rate = torchaudio.load(target_file)
        target_speaker_embeddings = speakerEmbeddingExtractor.contextual_encoding(target_waveform)

        print('source_audio_descriptor["input_values"].shape')
        print(source_audio_descriptor["input_values"].shape)
        print('target_speaker_embeddings.shape')
        print(target_speaker_embeddings.shape)
        output_audio_descriptor = model.generate_speech(source_audio_descriptor["input_values"].squeeze(1),
                                                        target_speaker_embeddings.squeeze(1), vocoder=vocoder)
        sf.write(output_file, output_audio_descriptor.numpy(), samplerate=source_sample_rate)
