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

# import redirect as rd
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
    page_title="README",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("README")

st.markdown("説明をここにダラダラと書くつもり")
# st.sidebar.title("Settings")

# # %%
# # default config
# song_path = Path("../data/shining_star_shortest.mp3")


# class CFG:
#     song_name = song_path.stem
#     input_file = song_path.resolve().as_posix()  # path traversalされそうな気がするがどうしたら
#     output_dir = "../outputs/"
#     data_dir = "../data/"
#     model = "htdemucs"
#     cpu_count = cpu_count()


# cfg = CFG()

# # Settings
# st.sidebar.warning("**Don't change these settings while running.**")
# # reference
# st.sidebar.markdown(
#     "Please refer to the following links for the meaning of each setting. [Code](https://github.com/facebookresearch/demucs/blob/8b48c27f82b0e119c91c613eee2ce87ba28575a0/demucs/separate.py#L53), [Readme](https://github.com/facebookresearch/demucs/#separating-tracks)"
# )

# cfg.model = st.sidebar.selectbox(
#     "Model",
#     ["htdemucs", "htdemucs_ft", "mdx_extra", "mdx_extra_q"],
# )
# cfg.overlap = st.sidebar.slider(
#     "--overlap (It can probably be reduced to 0.1 to improve a bit speed)",
#     0.1,
#     0.3,
#     0.1,
#     0.01,
# )
# cfg.clip_mode = st.sidebar.selectbox("--clip-mode", ["rescale", "clamp"])
# cfg.shifts = st.sidebar.slider(
#     "--shifts (This makes prediction `--shift` times slower. A little more accurate)",
#     1,
#     10,
#     1,
#     1,
# )

# # %%
# # upload audio file

# st.markdown("### Upload Audio")
# uploaded_file = st.file_uploader(
#     "Choose an audio file",
#     type=[
#         "mp3",
#     ],
# )

# if uploaded_file is not None:
#     saved_path = save_uploadedfile(uploaded_file, cfg.data_dir)
#     cfg.song_name = saved_path.stem
#     cfg.input_file = saved_path.resolve().as_posix()
# st.write(f"File Preview: {cfg.song_name}")
# st.audio(cfg.input_file)

# # %%
# # demucsによる分離

# cmd = [
#     # "demucs",
#     "-j",
#     str(cfg.cpu_count // 2),
#     "-n",
#     cfg.model,
#     "--overlap",
#     str(cfg.overlap),
#     # "--two-stems","vocals",
#     "--clip-mode",
#     cfg.clip_mode,
#     "--shifts",
#     str(cfg.shifts),
#     "--mp3",
#     "--mp3-bitrate",
#     "192",
#     "-o",
#     cfg.output_dir,
#     cfg.input_file,
# ]

# st.markdown("## ")
# st.markdown("### Separation")
# st.write("command is", sep=" ")
# st.code("demucs " + " ".join(cmd), language="shell")
# button_placeholder = st.empty()
# go_button = button_placeholder.button("Go Separation!")
# if go_button:
#     button_placeholder.empty()  # 紛らわしいのでボタンを消す
#     with st.spinner("Separating..."):
#         processing_placeholder = st.empty()
#         with processing_placeholder:
#             with st_stderr("info"):
#                 demucs.separate.main(opts=cmd)
#         processing_placeholder.empty()

#     # show separated audio
#     separated_filename = ["vocals", "drums", "bass", "other"]
#     separated_filepath = []
#     song_dir = Path(cfg.output_dir) / cfg.model / cfg.song_name
#     for f in separated_filename:
#         separated_filepath.append(song_dir / (f + ".mp3"))
#     for f in separated_filepath:
#         st.write(f"{f.stem}")
#         st.audio(f.resolve().as_posix())
#     # zip and download
#     shutil.make_archive(song_dir.parent / cfg.song_name, "zip", song_dir)
#     with open(song_dir.parent / (cfg.song_name + ".zip"), "rb") as f:
#         st.download_button(
#             label=f"Download Separated Audio as `{cfg.song_name}.zip`",
#             data=f,
#             file_name=f"{cfg.song_name}.zip",
#             mime="application/zip",
#         )

# else:
#     st.info("Click the button above to start separation.")


# # TODO 処理済みであれば初期化されないようにする
# # TODO 明示的な初期化ボタン作成
