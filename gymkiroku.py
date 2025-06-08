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
    state = {"year": today.year, "month": today.month}

    all_data = load_check_data()

    calendar_area = ft.Column()

    def rebuild_calendar():
        calendar_area.controls.clear()
        year = state["year"]
        month = state["month"]
        key = f"{year}-{month}"
        checked_days = all_data.get(key, [])

        def toggle_day(e):
            day = e.control.data
            if day in checked_days:
                checked_days.remove(day)
                e.control.bgcolor = ft.Colors.WHITE
            else:
                checked_days.append(day)
                e.control.bgcolor = ft.Colors.GREEN_200
            all_data[key] = checked_days
            save_check_data(all_data)
            page.update()

        _, last_day = calendar.monthrange(year, month)
        calendar_rows = []
        row = []

        first_weekday = datetime.date(year, month, 1).weekday()
        for _ in range(first_weekday):
            row.append(ft.Container(width=40, height=40))

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

        calendar_area.controls.append(
            ft.Text(f"{year}年{month}月 ジム記録", size=20)
        )
        calendar_area.controls.extend(calendar_rows)
        page.update()

    def prev_month(e):
        if state["month"] == 1:
            state["month"] = 12
            state["year"] -= 1
        else:
            state["month"] -= 1
        rebuild_calendar()

    def next_month(e):
        if state["month"] == 12:
            state["month"] = 1
            state["year"] += 1
        else:
            state["month"] += 1
        rebuild_calendar()

    nav = ft.Row([
        ft.ElevatedButton("← 前の月", on_click=prev_month),
        ft.ElevatedButton("次の月 →", on_click=next_month)
    ], alignment="center")

    page.add(nav, calendar_area)
    rebuild_calendar()

ft.app(target=main, view=ft.WEB_BROWSER)