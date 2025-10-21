# Quick Start Guide - Mobile UI JSON Editor

## Installation (One-time)

```bash
# Install PyQt5
pip install PyQt5==5.15.10
```

## Running the Editor

### Option 1: Using the launcher script (Recommended)
```bash
./run_editor.sh
```

### Option 2: Direct Python execution
```bash
python3 mobile_ui_editor.py
```

## First Steps

1. **Launch the application** using one of the methods above

2. **Open an example file**:
   - Click the "Open JSON" button
   - Navigate to `example_configs/` folder
   - Open `finance_main.json` or `dashboard_config.json`

3. **Try dragging widgets**:
   - You'll see colored rectangles representing widgets on the canvas
   - Click and drag them to new positions
   - Notice the position values update in the property editor

4. **Edit properties**:
   - Click on a widget to select it
   - See its properties appear in the right panel
   - Change any value (e.g., change a benefit text or an icon name)
   - Your changes are applied immediately

5. **Save your changes**:
   - Click the "Save" button in the toolbar
   - Or use "Save As..." to create a new file

## Understanding the Interface

```
┌─────────────────────────────────────────────────────────────────┐
│  [Open JSON]  [Save]  [Save As...]            File: example.json │
├──────────┬─────────────────────────┬─────────────────────────────┤
│          │                         │                             │
│  JSON    │    Visual Canvas        │   Property Editor           │
│  Tree    │                         │                             │
│          │   ┌───────────────┐     │   ┌──────────────────────┐  │
│  └─ id   │   │   Widget 1    │     │   │ id: Widget1          │  │
│  └─ tabs │   └───────────────┘     │   │ Component: [____]    │  │
│  └─ mod..│                         │   │ type: [____]         │  │
│          │   ┌───────────────┐     │   │ ── props ──          │  │
│  Widgets │   │   Widget 2    │     │   │ list: [....]         │  │
│  ┌ Wid1  │   └───────────────┘     │   │ position:            │  │
│  └ Wid2  │                         │   │   x: [50  ]          │  │
│          │                         │   │   y: [100 ]          │  │
│          │                         │   └──────────────────────┘  │
└──────────┴─────────────────────────┴─────────────────────────────┘
```

### Left Panel
- **JSON Structure Tree**: Navigate your entire JSON hierarchy
- **Module Elements**: Quick access to all widgets

### Center Panel
- **Visual Canvas**: Drag widgets to position them
- Shows a 375×812 pixel canvas (iPhone size)

### Right Panel
- **Properties Tab**: Edit widget properties with form controls
- **Raw JSON Tab**: Direct JSON editing for advanced users

## Common Tasks

### Task: Reposition a Widget
1. Click and drag the widget on the canvas
2. Release at the desired position
3. Click "Save" to persist changes

### Task: Edit Widget Text/Properties
1. Click the widget or select it from the left panel
2. In the Properties tab, edit the desired fields
3. Changes apply immediately
4. Click "Save"

### Task: Add Position to a Widget Without One
1. Open your JSON file
2. The editor will place it at a default position
3. Drag it where you want
4. Save - the position will be added to the JSON

### Task: Work with Your Own JSON Files
1. Place your JSON files anywhere on your system
2. Click "Open JSON" and navigate to them
3. Edit and save as normal
4. The editor works with any JSON following the expected structure

## JSON Structure Expected

Your JSON should have:
- `moduleElements` array: List of UI components
- `enhancedData` array: Additional data elements (optional)

Each element should have:
- `id`: Unique identifier
- `Component` or `type`: Widget type
- `props`: Properties object

The editor will add/update `props.position` with `x`, `y`, `width`, `height`.

## Tips

- **Multiple Files**: You can work with as many JSON files as you need - just open them one at a time
- **Precision**: Use the property editor to set exact pixel positions
- **Tree Navigation**: Click any item in the tree to view its properties
- **Unsaved Changes**: The filename shows an asterisk (*) when you have unsaved changes

## Next Steps

- Read the full **UI_EDITOR_README.md** for advanced features
- Explore the example files to understand the structure
- Start editing your own mobile UI configurations!

---

Happy editing!
