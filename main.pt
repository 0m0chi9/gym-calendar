import flet as ft
import datetime
import calendar
import json
import os

DATA_FILE = "user_calendars.json"

# ================= データ読み込み・保存 ====================
def load_calendars():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_calendars(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ================ カレンダー追加・削除 =====================
def add_calendar(name, data):
    if name not in data:
        data[name] = []
        save_calendars(data)

def delete_calendar(name, data):
    if name in data:
        del data[name]
        save_calendars(data)

# =============== カレンダー表示ビュー ===================
def show_calendar_tab_view(page, selected_name, selected_year=None, selected_month=None):
    data = load_calendars()
    today = datetime.date.today()
    year = selected_year if selected_year else today.year
    month = selected_month if selected_month else today.month

    def save_checked(name, day):
        key = name
        date_str = f"{year}-{month:02}-{day:02}"
        days = set(data.get(key, []))
        if date_str in days:
            days.remove(date_str)
        else:
            days.add(date_str)
        data[key] = list(days)
        save_calendars(data)

    def calendar_component(name):
        _, last_day = calendar.monthrange(year, month)
        rows = []
        row = []
        first_weekday = datetime.date(year, month, 1).weekday()

        weekday_labels = ["月", "火", "水", "木", "金", "土", "日"]
        header = ft.Row([
            ft.Container(ft.Text(label), width=40, height=40, alignment=ft.alignment.center)
            for label in weekday_labels
        ])
        rows.append(header)

        for _ in range(first_weekday):
            row.append(ft.Container(width=40, height=40))

        for day in range(1, last_day + 1):
            date_str = f"{year}-{month:02}-{day:02}"
            label = "✅" if date_str in data.get(name, []) else str(day)

            def make_on_click(d):
                return lambda e: (save_checked(name, d), show_calendar_tab_view(page, name, year, month))

            btn = ft.Container(
                content=ft.Text(label, color="black"),
                width=40,
                height=40,
                alignment=ft.alignment.center,
                bgcolor="#E0E0E0",
                border=ft.border.all(1),
                data=day,
                on_click=make_on_click(day)
            )
            row.append(btn)
            if len(row) == 7:
                rows.append(ft.Row(row))
                row = []
        if row:
            rows.append(ft.Row(row))

        def on_year_change(e):
            new_year = int(e.control.value)
            show_calendar_tab_view(page, name, new_year, month)

        def on_month_change(e):
            new_month = int(e.control.value)
            show_calendar_tab_view(page, name, year, new_month)

        year_dropdown = ft.Dropdown(
            width=100,
            value=str(year),
            options=[ft.dropdown.Option(str(y)) for y in range(today.year - 5, today.year + 6)],
            on_change=on_year_change
        )

        month_dropdown = ft.Dropdown(
            width=100,
            value=str(month),
            options=[ft.dropdown.Option(str(m)) for m in range(1, 13)],
            on_change=on_month_change
        )

        delete_button = ft.ElevatedButton("削除", on_click=lambda e: (delete_calendar(name, data), show_calendar_tab_view(page, list(data.keys())[0] if data else None)))

        return ft.Column([
            ft.Row([year_dropdown, month_dropdown, delete_button], wrap=True, spacing=10),
            ft.Text(f"{year}年{month}月 {name} 記録", size=20),
            *rows
        ])

    def on_tab_change(e):
        name = e.control.tabs[e.control.selected_index].text
        show_calendar_tab_view(page, name, year, month)

    calendar_tabs = [
        ft.Tab(text=name) for name in data.keys()
    ]

    def on_add_calendar(name):
        if name.strip() and name not in data:
            add_calendar(name.strip(), data)
            show_calendar_tab_view(page, name.strip())

    name_input = ft.TextField(label="新しいカレンダー名を追加", width=200)

    page.views.clear()
    controls = [
        ft.Text("カテゴリ別 習慣記録カレンダー", size=20),
        ft.Row([
            name_input,
            ft.ElevatedButton("追加", on_click=lambda e: on_add_calendar(name_input.value))
        ], spacing=10),
    ]
    if selected_name:
        controls.append(ft.Tabs(tabs=calendar_tabs, selected_index=list(data.keys()).index(selected_name), on_change=on_tab_change))
        controls.append(calendar_component(selected_name))

    page.views.append(ft.View("/tabs", controls=controls))
    page.update()

# ==================== メイン ========================
def main(page: ft.Page):
    page.title = "ユーザー定義カレンダー"
    data = load_calendars()
    if data:
        first = list(data.keys())[0]
        show_calendar_tab_view(page, first)
    else:
        add_calendar("Training", {})
        show_calendar_tab_view(page, "Training")

ft.app(target=main, view=ft.WEB_BROWSER)
