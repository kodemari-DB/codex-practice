#!/usr/bin/env python3
"""Simple task management CLI without external dependencies.

The data is stored next to this script in ``tasks.json``. Designed for
beginners and for cross-platform use (Windows/macOS/Linux).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Any, Dict, List


DATA_FILE = Path(__file__).resolve().with_name("tasks.json")


def load_tasks() -> List[Dict[str, Any]]:
    """Load tasks from the JSON file.

    - If the file does not exist, return an empty list.
    - If the file is broken or has unexpected contents, exit with a friendly
      message so the user can fix it manually.
    """

    if not DATA_FILE.exists():
        return []

    try:
        content = DATA_FILE.read_text(encoding="utf-8")
        if not content.strip():
            return []
        data = json.loads(content)
    except json.JSONDecodeError:
        print("tasks.json が壊れているようです。内容を確認してください。", file=sys.stderr)
        sys.exit(1)
    except OSError as exc:
        print(f"tasks.json を読み込めませんでした: {exc}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, list):
        print("tasks.json の形式が正しくありません（配列になっていません）。", file=sys.stderr)
        sys.exit(1)
    return data


def save_tasks(tasks: List[Dict[str, Any]]) -> None:
    try:
        DATA_FILE.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        print(f"tasks.json に保存できませんでした: {exc}", file=sys.stderr)
        sys.exit(1)


def next_id(tasks: List[Dict[str, Any]]) -> int:
    return max((task.get("id", 0) for task in tasks), default=0) + 1


def parse_date(value: str) -> str:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError("日付は YYYY-MM-DD 形式で指定してください。")
    return value


def is_overdue(task: Dict[str, Any]) -> bool:
    if task.get("done"):
        return False
    due = task.get("due")
    if not due:
        return False
    try:
        due_date = datetime.strptime(due, "%Y-%m-%d").date()
    except ValueError:
        return False
    return due_date < date.today()


def filter_tasks(
    tasks: List[Dict[str, Any]], *,
    include_done: bool = False,
    only_done: bool = False,
    tag: str | None = None,
    overdue_only: bool = False,
) -> List[Dict[str, Any]]:
    result = list(tasks)

    if tag:
        result = [t for t in result if t.get("tag") == tag]

    if only_done:
        result = [t for t in result if t.get("done")]
    elif not include_done:
        result = [t for t in result if not t.get("done")]

    if overdue_only:
        result = [t for t in result if is_overdue(t)]

    return sorted(result, key=lambda t: t.get("id", 0))


def format_task_row(task: Dict[str, Any]) -> List[str]:
    overdue_mark = "!" if is_overdue(task) else ""
    due_display = task.get("due") or "-"
    if overdue_mark:
        due_display = f"{due_display} {overdue_mark}"
    return [
        str(task.get("id", "")),
        "✔" if task.get("done") else "",
        due_display,
        task.get("tag") or "-",
        task.get("title") or "",
    ]


def print_table(tasks: List[Dict[str, Any]]) -> None:
    headers = ["id", "done", "due", "tag", "title"]
    rows = [headers] + [format_task_row(task) for task in tasks]

    col_widths = [max(len(row[i]) for row in rows) for i in range(len(headers))]

    for idx, row in enumerate(rows):
        line = "  ".join(cell.ljust(col_widths[i]) for i, cell in enumerate(row))
        print(line)
        if idx == 0:
            print("  ".join("-" * col_widths[i] for i in range(len(headers))))


def cmd_add(args: argparse.Namespace) -> None:
    tasks = load_tasks()
    task = {
        "id": next_id(tasks),
        "title": args.title,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "due": args.due,
        "tag": args.tag,
        "done": False,
        "done_at": None,
    }
    tasks.append(task)
    save_tasks(tasks)
    print(task["id"])


def cmd_list(args: argparse.Namespace) -> None:
    tasks = filter_tasks(
        load_tasks(),
        include_done=args.all,
        only_done=args.done,
        tag=args.tag,
        overdue_only=args.overdue,
    )
    if not tasks:
        print("対象のタスクはありません。")
        return
    print_table(tasks)


def cmd_today(_args: argparse.Namespace) -> None:
    today_str = date.today().strftime("%Y-%m-%d")
    tasks = [
        t for t in load_tasks()
        if not t.get("done") and t.get("due") == today_str
    ]
    if not tasks:
        print("今日が期限の未完了タスクはありません。")
        return
    print_table(sorted(tasks, key=lambda t: t.get("id", 0)))


def cmd_done(args: argparse.Namespace) -> None:
    tasks = load_tasks()
    for task in tasks:
        if task.get("id") == args.id:
            if task.get("done"):
                print("すでに完了しています。")
                return
            task["done"] = True
            task["done_at"] = datetime.now().isoformat(timespec="seconds")
            save_tasks(tasks)
            print(f"タスク {args.id} を完了にしました。")
            return
    print(f"id {args.id} のタスクが見つかりません。")


def cmd_search(args: argparse.Namespace) -> None:
    keyword = args.keyword.casefold()
    tasks = [t for t in load_tasks() if keyword in (t.get("title") or "").casefold()]
    if not tasks:
        print("該当するタスクはありません。")
        return
    print_table(sorted(tasks, key=lambda t: t.get("id", 0)))


def cmd_delete(args: argparse.Namespace) -> None:
    tasks = load_tasks()
    for task in tasks:
        if task.get("id") == args.id:
            title = task.get("title") or ""
            choice = input(f"タスク '{title}' を削除しますか？ (y/n): ").strip().lower()
            if choice not in {"y", "yes"}:
                print("キャンセルしました。")
                return
            tasks.remove(task)
            save_tasks(tasks)
            print(f"タスク {args.id} を削除しました。")
            return
    print(f"id {args.id} のタスクが見つかりません。")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="シンプルなタスク管理 CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="タスクを追加します")
    p_add.add_argument("title", help="タスクのタイトルを指定します")
    p_add.add_argument("--due", type=parse_date, help="期限 (YYYY-MM-DD)")
    p_add.add_argument("--tag", help="タグ")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="タスクを一覧表示します")
    p_list.add_argument("--all", action="store_true", help="完了・未完了すべてを表示")
    p_list.add_argument("--done", action="store_true", help="完了のみを表示")
    p_list.add_argument("--tag", help="タグで絞り込み")
    p_list.add_argument("--overdue", action="store_true", help="期限切れの未完了のみを表示")
    p_list.set_defaults(func=cmd_list)

    p_today = sub.add_parser("today", help="今日が期限の未完了タスクを表示")
    p_today.set_defaults(func=cmd_today)

    p_done = sub.add_parser("done", help="指定したタスクを完了にします")
    p_done.add_argument("id", type=int, help="完了にするタスクのID")
    p_done.set_defaults(func=cmd_done)

    p_search = sub.add_parser("search", help="タイトルで検索します")
    p_search.add_argument("keyword", help="検索キーワード（部分一致）")
    p_search.set_defaults(func=cmd_search)

    p_delete = sub.add_parser("delete", help="タスクを削除します")
    p_delete.add_argument("id", type=int, help="削除するタスクのID")
    p_delete.set_defaults(func=cmd_delete)

    return parser


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":  # pragma: no cover - entry point
    main()
