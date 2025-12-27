# Codex Practice Repository

このリポジトリは、初心者の方が気軽にコードを試しながら「Codex」に慣れるための練習用プロジェクトです。難しい準備は必要ありません。手元の環境で Python を使って簡単なサンプルを動かしてみましょう。

## 使い方（Hello Codex）

1. Python がインストールされていることを確認してください（3.8 以上を推奨）。
2. リポジトリのルートで、以下のコマンドを実行します。
   ```bash
   python hello_codex.py
   ```
3. ターミナルの案内に従って自分の名前を入力してください。入力した名前がそのまま表示されれば成功です。

## 含まれているもの
- `hello_codex.py`: 入力した自分の名前を表示するシンプルな Python スクリプトです。コード内に初心者向けのコメントを入れています。

## 新しいタスク管理 CLI (taskcli.py)

### 概要
- 追加のライブラリは不要です（標準ライブラリのみ）。
- `taskcli.py` と同じフォルダに `tasks.json` を自動作成してデータを保存します。
- Windows / macOS / Linux で動作します。

### 使い方
1. Python 3.8 以上がインストールされていることを確認します。
2. リポジトリのルートで以下のように実行します。
   ```bash
   python taskcli.py <command> [options]
   ```

### 主なコマンド例
- タスク追加
  ```bash
  python taskcli.py add "買い物に行く" --due 2024-12-01 --tag errand
  ```

- 未完了の一覧（デフォルト表示）
  ```bash
  python taskcli.py list
  ```

- 完了を含めた一覧
  ```bash
  python taskcli.py list --all
  ```

- 今日が期限のタスクを表示
  ```bash
  python taskcli.py today
  ```

- タスクを完了にする（ID を指定）
  ```bash
  python taskcli.py done 3
  ```

- タイトルで検索（部分一致・大文字小文字を区別しません）
  ```bash
  python taskcli.py search "買い物"
  ```

- タスクを削除（削除前に y/n で確認）
  ```bash
  python taskcli.py delete 3
  ```

### 表示とフィルターのポイント
- 一覧表示は表形式で `id / done / due / tag / title` を見やすく整列します。
- 期限が過ぎている未完了タスクには `!` を付けて表示します。
- フィルターオプション（`list` コマンド）:
  - `--all`: 完了・未完了すべて
  - `--done`: 完了のみ
  - `--tag TAG`: 指定タグのみ
  - `--overdue`: 期限切れの未完了のみ

### 例外時の挙動
- `tasks.json` が存在しない場合は自動で作成されます。
- `tasks.json` が壊れている場合は、丁寧なメッセージを表示して終了します。

### 手動テスト手順（自動テストは不要です）
1. タスクを追加する
   ```bash
   python taskcli.py add "テストタスク" --due 2099-01-01 --tag demo
   ```
2. 未完了一覧に表示されることを確認する
   ```bash
   python taskcli.py list
   ```
3. 追加したタスクを完了にする（表示された ID を使用）
   ```bash
   python taskcli.py done <ID>
   ```
4. 完了済み一覧で確認する
   ```bash
   python taskcli.py list --done
   ```

## 何か試してみましょう
- コメントを読んで、出力メッセージを自分好みに変えてみましょう（例: あいさつを追加するなど）。
- さらに文字列を変えてみたり、`print` の行を増やしてみたりすると、コードの動きがよく分かります。
- エラーが出たときは、メッセージをよく読み、落ち着いて一つずつ修正してみてください。小さな変更を繰り返すことで、自信を持ってコードを書けるようになります。
