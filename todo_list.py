import os
import json
import sys
import sublime
import sublime_plugin


class TodoListMainObject(object):
    def __init__(self):
        self.selected_list = None
        try:
            if os.path.exists(TodoListMainObject.file_path):
                with open(TodoListMainObject.file_path) as json_file:
                    TodoListMainObject.loaded_lists = json.load(json_file)
            else:
                TodoListMainObject.save_file()
        except IOError:
            return None

    def move_todo(self, idx, new_idx):
        todo_item = TodoListMainObject.loaded_lists[
            self.selected_list
        ].pop(idx)

        TodoListMainObject.loaded_lists[
            self.selected_list
        ].insert(
            new_idx,
            todo_item
        )

        TodoListMainObject.save_file()

    @staticmethod
    def save_file():
        with open(TodoListMainObject.file_path, 'w') as outfile:
            json.dump(TodoListMainObject.loaded_lists, outfile)

    @staticmethod
    def get_setting(key, default=None):
        settings = sublime.load_settings('TodoList.sublime-settings')

        if os.name == 'nt':
            os_specific_settings = sublime.load_settings(
                'TodoList (Windows).sublime-settings'
            )
        elif sys.platform == 'darwin':
            os_specific_settings = sublime.load_settings(
                'TodoList (OSX).sublime-settings'
            )
        else:
            os_specific_settings = sublime.load_settings(
                'TodoList (Linux).sublime-settings'
            )

        return os_specific_settings.get(key, settings.get(key, default))

    """ Class variables """
    loaded_lists = {}
    custom_file_path = get_setting.__func__('file_path')

    """defaults to user-path of OS"""
    if custom_file_path:
        file_path = custom_file_path
    else:
        file_path = os.path.expanduser(
            os.path.join('~', 'todo_list.json')
        )


class TodoListMenuCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.menu = []

        if not getattr(self.window, 'todo_instance', None):
            self.window.todo_instance = TodoListMainObject()

        if self.window.todo_instance.selected_list:
            if len(TodoListMainObject.loaded_lists[
                self.window.todo_instance.selected_list
            ]) > 0:
                self.menu.append(
                    {
                        'text': 'Todos: List all',
                        'command': 'todo_list_list_all'
                    }
                )

            self.menu.append(
                {
                    'text': 'Todos: Add', 'command': 'todo_list_add_todo'
                }
            )

            if len(TodoListMainObject.loaded_lists) > 0:
                self.menu.append(
                    {
                        'text': 'List: Switch',
                        'command': 'todo_list_load_list'
                    }
                )

            self.menu.append(
                {
                    'text': 'List: Delete current',
                    'command': 'todo_list_delete_current_list'
                }
            )
        else:
            if len(TodoListMainObject.loaded_lists) > 0:
                self.menu.append(
                    {
                        'text': 'List: Load', 'command': 'todo_list_load_list'
                    }
                )
                self.menu.append(
                    {
                        'text': 'List: Delete',
                        'command': 'todo_list_delete_list'
                    }
                )

        self.menu.append(
            {
                'text': 'List: Create new', 'command': 'todo_list_create_list'
            }
        )

        self.window.show_quick_panel(
            [item['text'] for item in self.menu],
            self.on_done,
        )

    def on_done(self, idx: int):
        if idx >= 0 and idx < len(self.menu):
            self.window.run_command(self.menu[idx]['command'])


class TodoListCreateListCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel(
            'Enter list name:',
            '',
            self.on_done,
            None,
            None
        )

    def on_done(self, list_name: str):
        TodoListMainObject.loaded_lists[list_name] = []
        self.window.todo_instance.selected_list = list_name
        TodoListMainObject.save_file()

        self.window.run_command('todo_list_menu')


class TodoListLoadListCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_quick_panel(
            list(TodoListMainObject.loaded_lists.keys()),
            self.on_done,
        )

    def on_done(self, list_idx: int):
        self.window.todo_instance.selected_list = list(
            TodoListMainObject.loaded_lists.keys()
        )[list_idx]

        self.window.run_command('todo_list_menu')


class TodoListDeleteListCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_quick_panel(
            list(TodoListMainObject.loaded_lists.keys()),
            self.on_done,
        )

    def on_done(self, list_idx: int):
        list_name = list(
            TodoListMainObject.loaded_lists.keys()
        )[list_idx]
        del TodoListMainObject.loaded_lists[list_name]
        TodoListMainObject.save_file()

        if self.window.todo_instance.selected_list == list_name:
            self.window.todo_instance.selected_list = None

        self.window.run_command('todo_list_menu')


class TodoListDeleteCurrentListCommand(sublime_plugin.WindowCommand):
    def run(self):
        if self.window.todo_instance.selected_list:
            del TodoListMainObject.loaded_lists[
                self.window.todo_instance.selected_list
            ]
            TodoListMainObject.save_file()

            self.window.todo_instance.selected_list = None

        self.window.run_command('todo_list_menu')


class TodoListListAllCommand(sublime_plugin.WindowCommand):
    def run(self):
        if (not getattr(self.window, 'todo_instance', None) or
                not self.window.todo_instance.selected_list):
            self.window.run_command('todo_list_menu')

        self.window.show_quick_panel(
            TodoListMainObject.loaded_lists[
                self.window.todo_instance.selected_list
            ],
            self.on_done,
        )

    def on_done(self, idx: int):
        if idx >= 0:
            self.submenu = []

            if idx > 0:
                self.submenu.append({
                    'text': 'Move up',
                    'command': 'todo_list_move_up',
                    'todo_idx': idx
                })

            if idx < len(TodoListMainObject.loaded_lists[
                self.window.todo_instance.selected_list
            ]) - 1:
                self.submenu.append({
                    'text': 'Move down',
                    'command': 'todo_list_move_down',
                    'todo_idx': idx
                })

            self.submenu.append({
                'text': 'Remove item',
                'command': 'todo_list_remove_todo',
                'todo_idx': idx
            })

            self.window.show_quick_panel(
                [item['text'] for item in self.submenu],
                self.on_sub_select
            )

        elif idx == -1:
            self.window.run_command('todo_list_menu')

    def on_sub_select(self, idx: int):
        """on selected action on todo-item"""
        if idx >= 0 and idx < len(self.submenu):
            self.window.run_command(
                self.submenu[idx]['command'],
                {'todo_idx': self.submenu[idx]['todo_idx']}
            )
        else:
            self.window.run_command('todo_list_list_all')


class TodoListRemoveTodoCommand(sublime_plugin.WindowCommand):
    def run(self, **args):
        del TodoListMainObject.loaded_lists[
            self.window.todo_instance.selected_list
        ][args['todo_idx']]
        TodoListMainObject.save_file()
        self.window.run_command('todo_list_list_all')


class TodoListAddTodoCommand(sublime_plugin.WindowCommand):
    def on_done(self, text: str):
        TodoListMainObject.loaded_lists[
            self.window.todo_instance.selected_list
        ].append(text)

        TodoListMainObject.save_file()

        self.window.run_command('todo_list_list_all')

    def run(self):
        self.window.show_input_panel(
            'Add to-do:',
            '',
            self.on_done,
            None,
            None
        )


class TodoListMoveUpCommand(sublime_plugin.WindowCommand):
    def run(self, **args):
        self.window.todo_instance.move_todo(
            args['todo_idx'], args['todo_idx'] - 1
        )

        self.window.run_command('todo_list_list_all')


class TodoListMoveDownCommand(sublime_plugin.WindowCommand):
    def run(self, **args):
        self.window.todo_instance.move_todo(
            args['todo_idx'], args['todo_idx'] + 1
        )

        self.window.run_command('todo_list_list_all')
