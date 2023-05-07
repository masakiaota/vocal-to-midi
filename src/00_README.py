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

st.markdown("説明をここにダラダラと書くつもり")
