import flet as ft
import calendar
import datetime
import json
import os

SAVE_FILE = "gym_days.json"

def load_check_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_check_data(data):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main(page: ft.Page):
    page.title = "ジム記録カレンダー"
    page.scroll = "auto"
    today = datetime.date.today()
    year = today.year
    month = today.month

    checked_days = load_check_data().get(f"{year}-{month}", [])

    def toggle_day(e):
        day = e.control.data
        if day in checked_days:
            checked_days.remove(day)
            e.control.bgcolor = ft.Colors.WHITE
        else:
            checked_days.append(day)
            e.control.bgcolor = ft.Colors.GREEN_200
        save_check_data({f"{year}-{month}": checked_days})
        page.update()

    _, last_day = calendar.monthrange(year, month)
    calendar_rows = []
    row = []

    first_weekday = datetime.date(year, month, 1).weekday()  # 0=Mon
    for _ in range(first_weekday):
        row.append(ft.Container(width=40, height=40))  # 空白マス

    for day in range(1, last_day + 1):
        bgcolor = ft.Colors.GREEN_200 if day in checked_days else ft.Colors.WHITE
        day_button = ft.Container(
            content=ft.Text(str(day)),
            width=40,
            height=40,
            alignment=ft.alignment.center,
            bgcolor=bgcolor,
            border=ft.border.all(1),
            data=day,
            on_click=toggle_day
        )
        row.append(day_button)
        if len(row) == 7:
            calendar_rows.append(ft.Row(row, alignment="start"))
            row = []

    if row:
        calendar_rows.append(ft.Row(row, alignment="start"))

    page.add(
        ft.Text(f"{year}年{month}月 ジム記録", size=20),
        *calendar_rows
    )

ft.app(target=main, view=ft.WEB_BROWSER)
