# Vocal to midi

![python versions](https://img.shields.io/badge/python-3.8%20%7C%203.9-blue)
[![MIT License](https://img.shields.io/github/license/cvpaperchallenge/Ascender?color=green)](LICENSE)
[![Apache License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Code style: flake8](https://img.shields.io/badge/code%20style-flake8-black)](https://github.com/PyCQA/flake8)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Typing: mypy](https://img.shields.io/badge/typing-mypy-blue)](https://github.com/python/mypy)

## Usage

ここにアクセス
https://audio-to-midi-ezgaeqvxvq-an.a.run.app/

初回起動時遅いです。上記のURLでリロードするとアクセスできたりします。
`Please wait...`で止まったら一度タブを消して、改めて上記URLでアクセスしてみてください。

### 各ページの説明
- README
    - 読んでください。
- separation
    - uploadした音声をvocal, bass, drums, otherに分離します。裏では[demucs](https://github.com/facebookresearch/demucs)を使っています。
- audio to midi
    - uploadした音声をmidiに変換します。楽器が分離されていたほうがある程度うまくいきます。裏では[basic-pitch](https://github.com/spotify/basic-pitch)を使っています。


## How to Development
このリポジトリの構造は[Ascender](https://github.com/cvpaperchallenge/Ascender)をテンプレートにしています。
そのため、利用方法も基本的に同じです。

開発環境の起動方法は上記リポジトリ、または[日本語スライド](https://cvpaperchallenge.github.io/Britannica/ascender/ja/#/1)を参考にしてください。


## License
Apache License 2.0
