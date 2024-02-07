import flet as ft


def main(page: ft.Page):
    page.title = 'Flet App'
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    user_label = ft.Text('Info', color='#fafafa')
    user_text = ft.TextField(value='0', width=150, text_align=ft.TextAlign.CENTER)

    def get_info(event):
        user_label.value = user_text.value
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.HOME, on_click=get_info),
                ft.Icon(ft.icons.BACK_HAND),
                ft.ElevatedButton(text='Click me', on_click=get_info),
                ft.OutlinedButton(text='Click me', on_click=get_info),
                ft.Checkbox(label='Вы согласны?', value=True)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            [
                user_label,
                user_text
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
    )


ft.app(target=main)