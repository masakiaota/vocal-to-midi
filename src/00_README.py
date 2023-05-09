# %%
from __future__ import annotations

import shutil
import subprocess
import sys
from multiprocessing import cpu_count
from pathlib import Path
from threading import current_thread

import streamlit as st

# %%
# streamlit settings
st.set_page_config(
    page_title="README",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("README")
# multipageだとしても、実行はこのスクリプトを実行したディクレクトリ起点となる
# __file__で固定してしまってもいいかも

st.markdown("### このアプリについて")
st.markdown(
    """
- README
    - このページです。
- separation
    - uploadした音声をvocal, bass, drums, otherに分離します。
    - 裏では[demucs](https://github.com/facebookresearch/demucs)を使っています。
- audio to midi
    - uploadした音声をmidiに変換します。楽器が分離されていたほうがある程度うまくいきます。
    - 音声が長い(4分以上になる)とアプリごと落ちることがあります。
    - 裏では[basic-pitch](https://github.com/spotify/basic-pitch)を使っています。
"""
)

st.markdown("### 開発")
st.markdown(
    "この[リポジトリ](https://github.com/masakiaota/vocal-to-midi)で開発を行っています。 プルリク歓迎です。"
)
st.markdown("ホスティング費用が高額になってきたらしれっと消すかもしれません。")

st.markdown("### ライセンス")
st.markdown("Apache License 2.0")

# %%
