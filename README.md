# Informational Health Simulation: Social Desirability Bias & Signal Phase Transition

このリポジトリは、アンケートや大規模調査における「社会的望ましさバイアス（Social Desirability Bias / 忖度）」が、いかにしてマイノリティの警告シグナルを構造的かつ非線形に抹殺するかを数理的に証明するシミュレーション・コードです。

本プロジェクトは、「大数の法則」に過剰適応した現代のデータサイエンスにおいて、データ生成プロセスそのものに潜む「情報の不健康状態（Informational Ill-health）」を可視化し、「情報の健康診断」という新たなパラダイムを提唱します。

## 📌 背景と問題意識 (Background)

ビッグデータ時代において、「サンプルサイズが大きければ誤差は消える」という素朴な信仰が蔓延しています。しかし、回答者の意思決定プロセスに「社会的圧力（忖度）」という重力が作用している場合、巨大なデータは真実を映し出すのではなく、むしろ「歪んだ合意」を数学的な真理へとロンダリングする装置として機能します。

本シミュレーションは、以下の事実を数理的に証明します。
1. **シグナルの崖（Phase Transition）**: バイアスが一定の臨界点を超えた瞬間、マイノリティの「小さな声」はなだらかに減少するのではなく、非線形に「蒸発」する。
2. **確信度のパラドックス**: 回答者の確信度（$\beta$）が高いほど、社会的圧力に屈した際のシグナルの消失が徹底される。

## 🧮 数理モデル (Mathematical Model)

本シミュレーションでは、個人の最終的な効用 $U$ を、内発的な「本音の効用」と外発的な「忖度の効用」の線形結合として定義し、それをSoftmax関数に投入することで選択確率を算出します。

$$U_{total} = (1 - v_2)U_{true} + v_2U_{sontaku}$$

* $v_2$: 社会的望ましさ（忖度）の重み。0で完全な本音、1で完全な社会的同調。
* $\beta$: 逆温度係数（確信度）。Softmax関数の鋭敏さを制御。

## 📊 出力される結果 (Outputs)

スクリプトを実行すると、`simulation_results` フォルダが作成され、以下の分析結果が高画質な画像（PNG）および生データ（CSV）として出力・ZIP圧縮されます。

* **Fig 1: Survival Curve of 'Rating 1'** * バイアス $v_2$ の増大に伴い、警告シグナル（評価1）が臨界点（$v_2=0.5$）でいかに墜落するかを示す生存曲線。
* **Fig 2: Structural Alteration of Data**
  * 5つの異なるバイアス・シナリオにおける分布の変質。正常な分布が「偽の合意（False Consensus）」や「全体主義的収束（Totalitarian Convergence）」へと至る過程を可視化。

## 🚀 使い方 (Usage)

本コードは **Google Colaboratory** での実行に最適化されています。

1. `informational_health_sim.py`（または `.ipynb`）をGoogle Colabにアップロードして実行してください。
2. 実行が完了すると、結果をまとめた `simulation_results_archive.zip` がブラウザ経由で自動的にダウンロードされます。

**※ローカル環境での実行について:**
ローカルのPython環境で実行する場合は、Colab固有の処理である `from google.colab import files` および最後の `files.download()` の行をコメントアウトして実行してください。ZIPファイルは作業ディレクトリに生成されます。

```bash
# 必要なライブラリのインストール
pip install -r requirements.txt

# スクリプトの実行（ローカル用に修正後）
python informational_health_sim.py
