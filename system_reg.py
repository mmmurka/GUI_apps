import flet as ft
import sqlite3


def main(page: ft.Page):
    page.title = 'App'
    page.theme_mode = 'dark'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 380
    page.window_height = 600
    page.window_resizable = False

    def register(event):
        db = sqlite3.connect('database')

        cur = db.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, 
            login TEXT,
            pass TEXT
        )''')
        cur.execute(f"INSERT INTO users VALUES(NULL, '{user_login.value}', '{user_pass.value}')")

        db.commit()
        db.close()

        user_login.value = ''
        user_pass.value = ''
        btn_reg.text = 'Добавлено'
        page.update()

    def validate(event):
        if all([user_login.value, user_pass.value]):
            btn_reg.disabled = False
            btn_auth.disabled = False
        else:
            btn_reg.disabled = True
            btn_auth.disabled = True

        page.update()

    def auth_user(event):
        db = sqlite3.connect('database')

        cur = db.cursor()

        cur.execute(f'''
        SELECT * FROM users WHERE login = "{user_login.value}" AND pass = "{user_pass.value}"
        ''')

        result = cur.fetchone()
        if result is not None:
            user_login.value = ''
            user_pass.value = ''
            btn_reg.text = 'Авторизовано'

            if len(page.navigation_bar.destinations) == 2:
                page.navigation_bar.destinations.append(ft.NavigationDestination(
                    icon=ft.icons.BOOK,
                    label='Кабинет',
                    selected_icon=ft.icons.BOOKMARK
                ))

            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text('Data invalid'))
            page.snack_bar.open = True
            page.update()

        db.commit()
        db.close()



    user_login = ft.TextField(label='Логин', width=200, on_change=validate)
    user_pass = ft.TextField(label='Пароль', password=True, width=200, on_change=validate)
    btn_reg = ft.OutlinedButton(text='Добавить', width=200, on_click=register, disabled=True)
    btn_auth = ft.OutlinedButton(text='Авторизовать', width=200, on_click=auth_user, disabled=True)

    #User Cabinet

    users_list = ft.ListView(spacing=10, padding=20)

    # end

    panel_register = ft.Row(
        [
            ft.Column(
                [
                    ft.Text('Регистрация'),
                    user_login,
                    user_pass,
                    btn_reg
                ]
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )
    panel_auth = ft.Row(
        [
            ft.Column(
                [
                    ft.Text('Авторизация'),
                    user_login,
                    user_pass,
                    btn_auth
                ]
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    panel_cabinet = ft.Row(
        [
            ft.Column(
                [
                    ft.Text('Личный кабинет'),
                    users_list
                ]
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    def navigate(event):
        index = page.navigation_bar.selected_index
        page.clean()

        match index:
            case 0:
                page.add(panel_register)
            case 1:
                page.add(panel_auth)
            case 2:
                users_list.controls.clear()

                db = sqlite3.connect('database')

                cur = db.cursor()
                cur.execute('''SELECT * FROM users''')
                result = cur.fetchall()

                if result:
                    for user in result:
                        users_list.controls.append(ft.Row([
                            ft.Text(f'User: {user[1]}'),
                            ft.Icon(ft.icons.VERIFIED_USER_ROUNDED)
                        ]))

                db.commit()
                db.close()
                page.add(panel_cabinet)

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.VERIFIED_USER, label='Регистрация'),
            ft.NavigationDestination(icon=ft.icons.VERIFIED_USER_OUTLINED, label='Авторизация')
        ], on_change=navigate
    )

    page.add(panel_register)


ft.app(target=main)