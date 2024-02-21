import flet as ft
import requests


def main(page: ft.Page):
    page.title = 'Погода'
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    user_data = ft.TextField(label="Введите город", width=400)
    weather_data = ft.Text('')

    def get_info(event):
        if len(user_data.value) < 2:
            return

        API = 'f6af234f8ad6716fae9b66dcaeefdd36'
        URL = f'https://api.openweathermap.org/data/2.5/weather?q={user_data.value}&APPID={API}&units=metric'
        result = requests.get(URL).json()
        print(result)
        try:
            temp = result['main']['temp']
            weather_data.value = f'Погода: {temp}°'
        except:
            print('error')
        page.update()

    def change_theme(event):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.SUNNY, on_click=change_theme),
                ft.Text('Погодная программа')
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row([user_data], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([weather_data], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([ft.ElevatedButton(text='Получить', on_click=get_info)], alignment=ft.MainAxisAlignment.CENTER)
    )



ft.app(target=main)