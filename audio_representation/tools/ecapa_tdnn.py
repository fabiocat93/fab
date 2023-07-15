import os
import inspect
from speechbrain.pretrained import EncoderClassifier


class AudioEncoder:
    def __init__(self, model_name='ecapa_tdnn', model_checkpoint=None, models_save_dir=None, extra_params=None):
        """
        Initialize the AudioEncoder class.

        Args:
            model_checkpoint (str): The checkpoint name or path of the pretrained encoder model.
            models_save_dir (str): The directory where the pretrained models are saved.
        """
        # Check if temporal audio representation extraction method is available
        self.time_dependent_representation_available = self.check_temporal_audio_extraction()
        # Check if time independent audio representation extraction method is available
        self.time_independent_representation_available = self.check_time_independent_audio_extraction()

        if model_checkpoint is None:
            model_checkpoint = "speechbrain/spkrec-ecapa-voxceleb"

        if models_save_dir is None:
            models_save_dir = "../pretrained_models/"

        # Get the absolute path of the directory where the script is located
        script_directory = os.path.dirname(os.path.abspath(__file__))
        # Get the absolute path of the models save directory
        models_save_dir_absolute_path = os.path.join(script_directory, models_save_dir)

        # Load the pretrained encoder model
        self.encoder = EncoderClassifier.from_hparams(source=model_checkpoint,
                                                      savedir=os.path.join(models_save_dir_absolute_path,
                                                                           model_checkpoint.replace("/", "_")))
        self.extra_params = extra_params

    def check_temporal_audio_extraction(self):
        """
        Check if temporal audio representation extraction method is available.

        Returns:
            bool: True if the method is available, False otherwise.
        """
        # Check if the method 'temporal_audio_representation_extraction' exists and is a method
        return 'temporal_audio_representation_extraction' in dir(self) and \
            inspect.ismethod(getattr(self, 'temporal_audio_representation_extraction'))

    def check_time_independent_audio_extraction(self):
        """
        Check if time independent audio representation extraction method is available.

        Returns:
            bool: True if the method is available, False otherwise.
        """
        # Check if the method 'time_independent_audio_representation_extraction' exists and is a method
        return 'time_independent_audio_representation_extraction' in dir(self) and \
            inspect.ismethod(getattr(self, 'time_independent_audio_representation_extraction'))

    def temporal_audio_representation_extraction(self, input_waveforms):
        """
        Extract temporal audio representations from input waveforms.

        Args:
            input_waveforms (Tensor): Input waveforms for which representations need to be extracted.

        Returns:
            Tensor: Temporal audio representations (embeddings) of the input waveforms.
        Raises:
            NotImplementedError: If temporal audio representation extraction is not available.
        """
        # Check if temporal audio representation extraction is available
        if not self.time_dependent_representation_available:
            raise NotImplementedError("Temporal audio representation extraction is not available.")
        # Encode the input waveforms to obtain embeddings
        embeddings = self.encoder.encode_temp_batch(input_waveforms)
        return embeddings

    def time_independent_audio_representation_extraction(self, input_waveforms):
        """
        Extract time independent audio representations from input waveforms.

        Args:
            input_waveforms (Tensor): Input waveforms for which representations need to be extracted.

        Returns:
            Tensor: Time independent audio representations (embeddings) of the input waveforms.
        Raises:
            NotImplementedError: If time independent audio representation extraction is not available.
        """
        # Check if time independent audio representation extraction is available
        if not self.time_independent_representation_available:
            raise NotImplementedError("Time independent audio representation extraction is not available.")
        # Encode the input waveforms to obtain embeddings
        embeddings = self.encoder.encode_batch(input_waveforms).squeeze(1)
        return embeddings
