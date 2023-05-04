# %%
from __future__ import annotations
import sys
from contextlib import contextmanager, redirect_stdout
from io import StringIO
from time import sleep
from streamlit.runtime.scriptrunner.script_run_context import (
    SCRIPT_RUN_CONTEXT_ATTR_NAME,
)
from threading import current_thread
from multiprocessing import cpu_count
import subprocess
from pathlib import Path
from IPython.display import Audio
import streamlit as st
import redirect as rd
import demucs.separate


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


def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == "" and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc


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
    page_title="Audio Separation",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("Audio Separation")
st.sidebar.title("Settings")

# %%
# default config
song_path = Path("../data/shining_star_short.mp3")


class CFG:
    song_name = song_path.stem
    input_file = song_path.resolve().as_posix()  # path traversalされそうな気がするがどうしたら
    output_dir = "../outputs/"
    data_dir = "../data/"
    model = "htdemucs"
    cpu_count = cpu_count()


cfg = CFG()
# %%
# upload audio file

st.markdown("### Upload Audio")
uploaded_file = st.file_uploader(
    "Choose an audio file",
    type=["mp3", "wav"],
)

# with NamedTemporaryFile(dir="../data", type=)
if uploaded_file is not None:
    saved_path = save_uploadedfile(uploaded_file, cfg.data_dir)
    cfg.song_name = saved_path.stem
    cfg.input_file = saved_path.resolve().as_posix()
st.write(f"File Preview: {cfg.song_name}")
st.audio(cfg.input_file)

# %%
# demucsによる分離

cmd = [
    # "demucs",
    "-j",
    str(cfg.cpu_count // 2),
    "-n",
    cfg.model,
    "--overlap",
    "0.1",
    # "--two-stems","vocals",
    "--clip-mode",
    "clamp",
    "--mp3",
    "--mp3-bitrate",
    "192",
    "-o",
    cfg.output_dir,
    cfg.input_file,
]

st.markdown("## ")
st.markdown("### Separation")
st.write("command is", sep=" ")
st.code("demucs " + " ".join(cmd), language="shell")
button_placeholder = st.empty()
go_button = button_placeholder.button("Go Separation!")
if go_button:
    button_placeholder.empty()  # 紛らわしいのでボタンを消す
    with st.spinner("Separating..."):
        processing_placeholder = st.empty()
        with processing_placeholder:
            with st_stderr("info"):
                demucs.separate.main(opts=cmd)
        processing_placeholder.empty()

    # show separated audio
    separated_filename = ["vocals", "drums", "bass", "other"]
    separated_filepath = []
    for f in separated_filename:
        separated_filepath.append(
            Path(cfg.output_dir) / cfg.model / cfg.song_name / (f + ".mp3")
        )
    for f in separated_filepath:
        st.write(f"{f.stem}")
        st.audio(f.resolve().as_posix())

else:
    st.info("Click the button above to start separation.")
