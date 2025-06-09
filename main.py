import flet as ft
import datetime
import calendar
import json
import os

# ================ カレンダー表示ビュー =====================
def show_calendar_tab_view(page, selected_name, load_calendars, save_calendars, username, selected_year=None, selected_month=None):
    data = load_calendars()
    today = datetime.date.today()
    year = selected_year if selected_year else today.year
    month = selected_month if selected_month else today.month

    def save_checked(name, day):
        date_str = f"{year}-{month:02}-{day:02}"
        days = set(data.get(name, []))
        if date_str in days:
            days.remove(date_str)
        else:
            days.add(date_str)
        data[name] = list(days)
        save_calendars(data)

    def calendar_component(name):
        _, last_day = calendar.monthrange(year, month)
        rows = []
        row = []
        first_weekday = datetime.date(year, month, 1).weekday()

        weekday_labels = ["月", "火", "水", "木", "金", "土", "日"]
        rows.append(ft.Row([
            ft.Container(ft.Text(day), width=40, height=40, alignment=ft.alignment.center)
            for day in weekday_labels
        ]))

        for _ in range(first_weekday):
            row.append(ft.Container(width=40, height=40))

        for day in range(1, last_day + 1):
            date_str = f"{year}-{month:02}-{day:02}"
            checked = date_str in data.get(name, [])
            label = ft.Column(
                controls=[
                    ft.Text(str(day), size=12, color="black"),
                    ft.Text("✅" if checked else "", size=12)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2
            )

            def make_on_click(d):
                return lambda e: (save_checked(name, d), show_calendar_tab_view(page, name, load_calendars, save_calendars, username, year, month))

            row.append(ft.Container(
                content=label,
                width=40,
                height=40,
                alignment=ft.alignment.center,
                bgcolor="#E0E0E0",
                border=ft.border.all(1),
                data=day,
                on_click=make_on_click(day)
            ))

            if len(row) == 7:
                rows.append(ft.Row(row))
                row = []
        if row:
            rows.append(ft.Row(row))

        def on_year_change(e):
            show_calendar_tab_view(page, name, load_calendars, save_calendars, username, int(e.control.value), month)

        def on_month_change(e):
            show_calendar_tab_view(page, name, load_calendars, save_calendars, username, year, int(e.control.value))

        year_dropdown = ft.Dropdown(
            width=150,
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

        delete_button = ft.ElevatedButton("削除", on_click=lambda e: show_delete_confirmation(page, name, load_calendars, save_calendars, username))
        
        return ft.Column([
            ft.Row([year_dropdown, month_dropdown, delete_button], spacing=10),
            ft.Text(f"{year}年{month}月 {name} 記録", size=20),
            *rows
        ])

    def on_tab_change(e):
        name = e.control.tabs[e.control.selected_index].text
        show_calendar_tab_view(page, name, load_calendars, save_calendars, username, year, month)

    def on_add_calendar(name):
        if name.strip() and name not in data:
            data[name.strip()] = []
            save_calendars(data)
            show_calendar_tab_view(page, name.strip(), load_calendars, save_calendars, username)

    name_input = ft.TextField(label="新しいカレンダー名を追加", width=200)

    controls = [
        ft.Text(f"{username} さんのカレンダー", size=24, weight=ft.FontWeight.BOLD),
        ft.Row([name_input, ft.ElevatedButton("追加", on_click=lambda e: on_add_calendar(name_input.value))], spacing=10),
    ]

    if selected_name:
        tabs = [ft.Tab(text=name) for name in data.keys()]
        controls.append(ft.Tabs(tabs=tabs, selected_index=list(data.keys()).index(selected_name), on_change=on_tab_change))
        controls.append(calendar_component(selected_name))

    page.views.clear()
    page.views.append(ft.View("/calendar", controls=controls))
    page.update()
    
    
# ================= 削除確認画面 =================
def show_delete_confirmation(page, name, load_calendars, save_calendars, username):
    def confirm_delete(e):
        data = load_calendars()
        data.pop(name, None)
        save_calendars(data)
        # カレンダー一覧が空でなければ最初のカレンダーを表示，なければ初期作成
        if data:
            first = list(data.keys())[0]
            show_calendar_tab_view(page, first, load_calendars, save_calendars, username)
        else:
            data["Training"] = []
            save_calendars(data)
            show_calendar_tab_view(page, "Training", load_calendars, save_calendars, username)

    def cancel_delete(e):
        show_calendar_tab_view(page, name, load_calendars, save_calendars, username)

    page.views.append(
        ft.View(
            "/confirm_delete",
            controls=[
                ft.Text(f"「{name}」カレンダーを本当に削除しますか？", size=20),
                ft.Row([
                    ft.ElevatedButton("はい（削除）", on_click=confirm_delete),
                    ft.ElevatedButton("いいえ（戻る）", on_click=cancel_delete),
                ], spacing=10)
            ]
        )
    )
    page.update()

# ================= メイン関数 =================
def main(page: ft.Page):
    page.title = "カレンダーアプリ（ユーザー名表示あり）"

    user_input = ft.TextField(label="ユーザー名を入力", width=200)
    status_text = ft.Text()

    def start_calendar(e):
        user = user_input.value.strip() or "default"
        data_file = f"user_calendars_{user}.json"

        def load_calendars():
            if os.path.exists(data_file):
                with open(data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {}

        def save_calendars(data):
            with open(data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        data = load_calendars()
        if data:
            first = list(data.keys())[0]
            show_calendar_tab_view(page, first, load_calendars, save_calendars, username=user)
        else:
            data["Training"] = []
            save_calendars(data)
            show_calendar_tab_view(page, "Training", load_calendars, save_calendars, username=user)

    page.add(
        ft.Text("カレンダーを使う前に，ユーザー名を入力してください", size=20),
        user_input,
        ft.ElevatedButton("開始", on_click=start_calendar),
        status_text
    )

ft.app(target=main, view=ft.WEB_BROWSER)
