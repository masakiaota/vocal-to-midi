# %%
from __future__ import annotations
import sys
import shutil
from threading import current_thread
from multiprocessing import cpu_count
import subprocess
from pathlib import Path
from IPython.display import Audio
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
