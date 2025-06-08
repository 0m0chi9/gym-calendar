import flet as ft
import calendar
import datetime
import json
import os

SAVE_FILE = "gym_days_by_route.json"

def load_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def build_calendar(category_key, title, page, data, year, month):
    calendar_column = ft.Column()

    def get_key():
        return f"{category_key}_{year}-{month}"

    key = get_key()
    checked_days = data.get(key, [])

    def toggle_day(e):
        day = e.control.data
        if day in checked_days:
            checked_days.remove(day)
            e.control.content = ft.Text(str(day))
        else:
            checked_days.append(day)
            e.control.content = ft.Text("✅")
        data[key] = checked_days
        save_data(data)
        page.update()

    _, last_day = calendar.monthrange(year, month)
    rows = []
    row = []

    first_weekday = datetime.date(year, month, 1).weekday()
    for _ in range(first_weekday):
        row.append(ft.Container(width=40, height=40))

    for day in range(1, last_day + 1):
        label = "✅" if day in checked_days else str(day)
        btn = ft.Container(
            content=ft.Text(label),
            width=40,
            height=40,
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.BLACK12,
            border=ft.border.all(1),
            data=day,
            on_click=toggle_day
        )
        row.append(btn)
        if len(row) == 7:
            rows.append(ft.Row(row))
            row = []
    if row:
        rows.append(ft.Row(row))

    calendar_column.controls.append(ft.Text(f"{year}年{month}月 {title} 記録", size=20))
    calendar_column.controls.extend(rows)
    return calendar_column

def calendar_view(page, category_key, title):
    today = datetime.date.today()
    current_year = today.year
    current_month = today.month
    data = load_data()

    year_dropdown = ft.Dropdown(
        width=100,
        value=str(current_year),
        options=[ft.dropdown.Option(str(y)) for y in range(current_year - 5, current_year + 6)]
    )
    month_dropdown = ft.Dropdown(
        width=100,
        value=str(current_month),
        options=[ft.dropdown.Option(str(m)) for m in range(1, 13)]
    )

    calendar_area = ft.Column()

    def refresh_calendar(e=None):
        selected_year = int(year_dropdown.value)
        selected_month = int(month_dropdown.value)
        calendar_area.controls.clear()
        calendar = build_calendar(category_key, title, page, data, selected_year, selected_month)
        calendar_area.controls.append(calendar)
        page.update()

    year_dropdown.on_change = refresh_calendar
    month_dropdown.on_change = refresh_calendar

    refresh_calendar()  # 初回描画

    selector = ft.Row([year_dropdown, month_dropdown], spacing=20)
    return ft.Column([selector, calendar_area])

def training_page(page: ft.Page):
    def on_tab_change(e):
        if e.control.selected_index == 1:
            page.go("/study")

    content = ft.Column([
        ft.Tabs(
            tabs=[
                ft.Tab(text="💪 Training"),
                ft.Tab(text="✏️ Study")
            ],
            selected_index=0,
            on_change=on_tab_change
        ),
        calendar_view(page, "training", "💪 Training")
    ])

    page.views.clear()
    page.views.append(ft.View("/training", [content]))
    page.update()

def study_page(page: ft.Page):
    def on_tab_change(e):
        if e.control.selected_index == 0:
            page.go("/training")

    content = ft.Column([
        ft.Tabs(
            tabs=[
                ft.Tab(text="💪 Training"),
                ft.Tab(text="✏️ Study")
            ],
            selected_index=1,
            on_change=on_tab_change
        ),
        calendar_view(page, "study", "✏️ Study")
    ])

    page.views.clear()
    page.views.append(ft.View("/study", [content]))
    page.update()

def main(page: ft.Page):
    page.title = "カテゴリ別 習慣記録カレンダー"

    def route_change(e):
        route = page.route
        if route == "/training":
            training_page(page)
        elif route == "/study":
            study_page(page)
        else:
            page.go("/training")

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main, view=ft.WEB_BROWSER)
