# %%
from __future__ import annotations
import sys
import shutil
from contextlib import contextmanager, redirect_stdout
from io import StringIO
from time import sleep
from streamlit.scriptrunner.script_run_context import (
    SCRIPT_RUN_CONTEXT_ATTR_NAME,
)
from threading import current_thread
from multiprocessing import cpu_count
import subprocess
from pathlib import Path
from IPython.display import Audio
import streamlit as st
from basic_pitch.inference import predict_and_save


FREQUENCY_LIST = [int(440 * pow(2, i / 12)) for i in range(-36, 36)]


def save_uploadedfile(
    uploadedfile: st.runtime.uploaded_file_manager.UploadedFile,
    save_dir: Path | str,
) -> Path:
    save_dir = Path(save_dir)
    save_path = save_dir / uploadedfile.name
    with open(save_path, "wb") as f:
        f.write(uploadedfile.getbuffer())
    # st.success(f"Saved File: `{uploaded_file.name}` to `{save_dir.as_posix()}/`")
    return save_path


def make_dir(path: Path) -> None:
    """make directory if not exists. if exists, delete and remake."""
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


@contextmanager
def st_redirect(src, dst):
    placeholder = st.empty()
    output_func = getattr(placeholder, dst)

    with StringIO() as buffer:
        old_write = src.write

        def new_write(b):
            if getattr(current_thread(), SCRIPT_RUN_CONTEXT_ATTR_NAME, None):
                buffer.write(b + "\n")
                output_func(buffer.getvalue())
            else:
                old_write(b)

        try:
            src.write = new_write
            yield
        finally:
            src.write = old_write


@contextmanager
def st_stdout(dst):
    with st_redirect(sys.stdout, dst):
        yield


@contextmanager
def st_stderr(dst):
    with st_redirect(sys.stderr, dst):
        yield


# %%
# streamlit settings
st.set_page_config(
    page_title="Audio to MIDI",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("Audio to MIDI")
st.sidebar.title("Settings")

# default config
dir_of_this_file = Path(__file__).parent.resolve()
song_path = (dir_of_this_file / "../../data/shining_star_short_vocals.mp3").resolve()


class CFG:
    data_dir = (dir_of_this_file / "../../data/").resolve().as_posix() + "/"
    song_name = song_path.stem
    input_file = song_path.resolve().as_posix()  # path traversalされそうな気がするがどうしたら
    output_dir = (
        dir_of_this_file / "../../outputs/basic-pitch/" / song_path.stem
    ).resolve().as_posix() + "/"
    midi_wav_path = output_dir + song_path.stem + "_basic_pitch.wav"
    midi_mp3_path = output_dir + song_path.stem + "_basic_pitch.mp3"
    basic_pitch_settings = {
        "audio_path_list": [input_file],
        "output_directory": output_dir,
        "save_midi": True,
        "sonify_midi": True,
        "save_model_outputs": False,
        "save_notes": False,
        "onset_threshold": 0.5,
        "frame_threshold": 0.4,
        "minimum_note_length": 40,
        "minimum_frequency": 100,
        "maximum_frequency": 1000,
        "melodia_trick": True,
        "midi_tempo": 158,
    }


cfg = CFG()

# %%
# Settings
st.sidebar.warning("**Don't change these settings while running.**")
# reference
cfg.basic_pitch_settings["onset_threshold"] = st.sidebar.slider(
    "onset_threshold", 0.0, 1.0, 0.5
)
cfg.basic_pitch_settings["frame_threshold"] = st.sidebar.slider(
    "frame_threshold", 0.0, 1.0, 0.30
)
cfg.basic_pitch_settings["minimum_note_length"] = st.sidebar.slider(
    "minimum_note_length", 0, 100, 10
)
freq_min, freq_max = st.sidebar.select_slider(
    "frequency",
    options=FREQUENCY_LIST,
    value=(FREQUENCY_LIST[10], FREQUENCY_LIST[51]),
    format_func=lambda x: f"{x} Hz",
)
cfg.basic_pitch_settings["minimum_frequency"] = freq_min
cfg.basic_pitch_settings["maximum_frequency"] = freq_max
cfg.basic_pitch_settings["midi_tempo"] = st.sidebar.number_input(
    "midi_tempo", 0, 999, 158
)
cfg.basic_pitch_settings["melodia_trick"] = st.sidebar.checkbox(
    "use melodia trick", value=True
)


# %%
# upload audio file

st.markdown("### Upload Audio")
uploaded_file = st.file_uploader(
    "Choose an audio file",
    type=[
        "mp3",
    ],
)

if uploaded_file is not None:
    saved_path = save_uploadedfile(uploaded_file, cfg.data_dir)
    cfg.song_name = saved_path.stem
    cfg.input_file = saved_path.resolve().as_posix()
    cfg.output_dir = (
        dir_of_this_file / "../../outputs/basic-pitch/" / cfg.song_name
    ).resolve().as_posix() + "/"
    cfg.midi_wav_path = cfg.output_dir + saved_path.stem + "_basic_pitch.wav"
    cfg.midi_mp3_path = cfg.output_dir + saved_path.stem + "_basic_pitch.mp3"
    cfg.basic_pitch_settings["audio_path_list"] = [cfg.input_file]
    cfg.basic_pitch_settings["output_directory"] = cfg.output_dir
st.write(f"File Preview: {cfg.song_name}")
st.audio(cfg.input_file)

make_dir(Path(cfg.output_dir))

# %%
# run basic pitch
st.markdown("## ")
st.markdown("### Midi Generation")
with st.spinner("Midi generation in progress..."):
    predict_and_save(**cfg.basic_pitch_settings)
    subprocess.run(
        ["ffmpeg", "-i", cfg.midi_wav_path, cfg.midi_mp3_path],
    )
st.audio(cfg.midi_mp3_path)
