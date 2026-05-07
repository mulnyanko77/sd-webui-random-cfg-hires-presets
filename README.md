# sd-webui-random-cfg-hires-presets

A lightweight extension for **AUTOMATIC1111 Stable Diffusion WebUI** that randomizes CFG Scale, Hires steps, and Hires denoising strength with preset support.

**Generate forever** で連続生成するときに、毎回少しずつ違う設定を与えて変化を出すための拡張機能です。

---

# 日本語

## 概要

`sd-webui-random-cfg-hires-presets` は、**AUTOMATIC1111 Stable Diffusion WebUI** 用の軽量拡張機能です。

画像生成時に、以下の値を指定範囲内からランダムに選択して適用できます。

- CFG Scale
- Hires steps
- Hires denoising strength

特に **Generate forever** を使って連続生成するときに、完全に同じ設定で回し続けるのではなく、CFG や Hires fix 関連の値に controlled randomness を与えて、生成結果にほどよい変化を出すことを目的としています。

---

## 主な機能

### CFG Scale のランダム化

CFG Scale を、指定した最小値・最大値・刻み値の中からランダムに選択します。

例：

```text
Min: 4
Max: 5
Step: 0.1
```

この場合、以下の値からランダムに選ばれます。

```text
4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0
```

---

### Hires steps のランダム化

Hires fix 使用時の Hires steps を、指定範囲内からランダムに選択します。

例：

```text
Min: 5
Max: 10
Step: 1
```

この場合、以下の値からランダムに選ばれます。

```text
5, 6, 7, 8, 9, 10
```

---

### Hires denoising strength のランダム化

Hires fix 使用時の denoising strength を、指定範囲内からランダムに選択します。

例：

```text
Min: 0.3
Max: 0.4
Step: 0.01
```

この場合、以下の値からランダムに選ばれます。

```text
0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4
```

---

## プリセット機能

CFG / Hires steps / Hires denoise のランダム化設定を、プリセットとして保存・呼び出しできます。

保存される内容は以下です。

- Random CFG の有効 / 無効
- CFG Min / Max / Step
- Random Hires steps の有効 / 無効
- Hires steps Min / Max / Step
- Random Hires denoise の有効 / 無効
- Hires denoise Min / Max / Step

プリセットは、拡張フォルダ内の JSON ファイルに保存されます。

```text
random_param_presets.json
```


## インストール方法

### URLからインストール

AUTOMATIC1111 WebUI の拡張機能画面から、GitHub URLを指定してインストールできます。

1. AUTOMATIC1111 WebUI を開く
2. `Extensions` タブを開く
3. `Install from URL` を開く
4. `URL for extension's git repository` に以下のURLを貼り付ける

```text
https://github.com/mulnyanko77/sd-webui-random-cfg-hires-presets-v1
```

5. `Install` を押す
6. インストール完了後、AUTOMATIC1111 WebUI を再起動する

この方法でインストールすると、通常は以下の場所に拡張機能が配置されます。

```text
stable-diffusion-webui/extensions/sd-webui-random-cfg-hires-presets/
```

---

### 手動インストール

このリポジトリをダウンロードして、AUTOMATIC1111 WebUI の `extensions` フォルダに配置します。

```text
stable-diffusion-webui/extensions/
```

期待されるフォルダ構成：

```text
stable-diffusion-webui/
└─ extensions/
   └─ sd-webui-random-cfg-hires-presets/
      └─ scripts/
         └─ random_param_presets.py
```

配置後、AUTOMATIC1111 WebUI を再起動してください。

---

## 使い方

1. `txt2img` または `img2img` を開く
2. `Random CFG / Hires Params + Presets` を開く
3. ランダム化したい項目を有効化する
4. Min / Max / Step を設定する
5. 必要に応じてプリセットとして保存する
6. 通常通り画像生成する

Hires steps と Hires denoising strength は、Hires fix が有効な場合のみ反映されます。

---

## Generate forever での使い方

この拡張は、特に **Generate forever** との組み合わせを想定しています。

たとえば、以下のように設定します。

```text
CFG: 4.0 ～ 5.0 / Step 0.1
Hires steps: 5 ～ 10 / Step 1
Hires denoise: 0.30 ～ 0.40 / Step 0.01
```

この状態で Generate forever を使うと、各生成ジョブごとに CFG や Hires fix 関連の値がランダムに選ばれ、同じプロンプトでも少しずつ違う結果を得やすくなります。

---

## 注意点

- ランダム値は、基本的に1回の生成ジョブごとに1回選ばれます。
- Batch size を複数にしている場合、同じジョブ内の画像には同じランダム値が使われます。
- Hires steps と Hires denoising strength は、Hires fix が OFF の場合は反映されません。
- この拡張は小規模な個人利用向け拡張として作成されています。
- 環境や AUTOMATIC1111 WebUI のバージョンによっては、動作が変わる可能性があります。

---

# English

## Overview

`sd-webui-random-cfg-hires-presets` is a lightweight extension for **AUTOMATIC1111 Stable Diffusion WebUI**.

It allows you to randomize the following parameters during image generation:

- CFG Scale
- Hires steps
- Hires denoising strength

This extension is especially useful when using **Generate forever**, as it introduces controlled variation into long image-generation sessions without changing the prompt itself.

---

## Features

### Random CFG Scale

Randomly selects CFG Scale from a specified Min / Max / Step range.

Example:

```text
Min: 4
Max: 5
Step: 0.1
```

Possible values:

```text
4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0
```

---

### Random Hires steps

Randomly selects Hires steps when Hires fix is enabled.

Example:

```text
Min: 5
Max: 10
Step: 1
```

Possible values:

```text
5, 6, 7, 8, 9, 10
```

---

### Random Hires denoising strength

Randomly selects Hires denoising strength when Hires fix is enabled.

Example:

```text
Min: 0.3
Max: 0.4
Step: 0.01
```

Possible values:

```text
0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39, 0.4
```

---

## Preset Support

You can save and apply presets for all randomization settings.

Saved preset values include:

- Enable / disable Random CFG
- CFG Min / Max / Step
- Enable / disable Random Hires steps
- Hires steps Min / Max / Step
- Enable / disable Random Hires denoise
- Hires denoise Min / Max / Step

Presets are saved as a JSON file inside the extension folder.

```text
random_param_presets.json
```

## Installation

### Install from URL

You can install this extension directly from AUTOMATIC1111 WebUI by using the GitHub repository URL.

1. Open AUTOMATIC1111 WebUI
2. Go to the `Extensions` tab
3. Open `Install from URL`
4. Paste the following URL into `URL for extension's git repository`

```text
https://github.com/mulnyanko77/sd-webui-random-cfg-hires-presets-v1
```

5. Click `Install`
6. Restart AUTOMATIC1111 WebUI after installation

This usually installs the extension into the following folder:

```text
stable-diffusion-webui/extensions/sd-webui-random-cfg-hires-presets/
```

---

### Manual Installation

Download this repository and place it inside the `extensions` folder of AUTOMATIC1111 WebUI.

```text
stable-diffusion-webui/extensions/
```

Expected folder structure:

```text
stable-diffusion-webui/
└─ extensions/
   └─ sd-webui-random-cfg-hires-presets/
      └─ scripts/
         └─ random_param_presets.py
```

Restart AUTOMATIC1111 WebUI after installation.

---

## Usage

1. Open `txt2img` or `img2img`
2. Expand `Random CFG / Hires Params + Presets`
3. Enable the parameters you want to randomize
4. Set Min / Max / Step values
5. Save a preset if needed
6. Generate images as usual

Hires steps and Hires denoising strength only take effect when Hires fix is enabled.

---

## Usage with Generate forever

This extension is designed to be useful with **Generate forever**.

For example:

```text
CFG: 4.0 to 5.0 / Step 0.1
Hires steps: 5 to 10 / Step 1
Hires denoise: 0.30 to 0.40 / Step 0.01
```

When used with Generate forever, each generation job can receive slightly different CFG and Hires fix settings, making it easier to produce varied results from the same prompt.

---

## Notes

- Random values are selected once per generation job.
- Images generated in the same batch use the same selected random values.
- Hires steps and Hires denoising strength are ignored when Hires fix is disabled.
- This is a small personal-use extension.
- Behavior may vary depending on your AUTOMATIC1111 WebUI version and environment.

---

## License

MIT License