# TodoList

TodoList is a simple Todo plugin for Sublime Text 3. It is **window-based** and can have different active lists on separate windows. There are no connections to open files since the idea of the plugin is to be a general todo-list.

## Installation (no Package Control yet)

#### Way 1
1. Download [TodoList.sublime-package](https://github.com/2mas/TodoList/releases/latest)
2. Place it in your Installed Packages directory and restart Sublime Text.

#### Way 2

Clone this repository into your packages folder:
```
git clone https://github.com/2mas/TodoList.git 'TodoList'
```

## Usage/Functionality

Use the TodoList: Menu in Command Palette to begin.

- **Lists**
  - Create lists
  - Load/Switch active list
  - Delete lists

- **Todo items**
  - Add todo-items to active list
  - List todo items
  - Move items up/down
  - Remove items

## Configuration

TodoList will create a todo_list.json file in your user-path by default.

You can provide your own location and filename by going to `Preferences > Package Settings > TodoList > Settings - User` or `Settings - More > OS Specific`

For a example on Windows:
```
{
    "file_path": "C:\\folder\\todo.json"
}
```

## Commands

Available commands to bind if needed:

#### `todo_list_menu`
The main-menu of the plugin, also available in Command Palette

#### `todo_list_create_list`
Creates a new todo-list and set it as active list

####  `todo_list_load_list`
Load a list to your active Sublime window

#### `todo_list_delete_list`
Brings up a list of todo-lists, select one for deletion

#### `todo_list_delete_current_list`
Deletes the current active list

#### `todo_list_list_all`
Lists all todo-items in current list

#### `todo_list_add_todo`
Add a todo-item to current active list

## Keybindings
Default key-bindings:

    ctrl+t+m:   todo_list_menu
    ctrl+t+l:   todo_list_list_all

