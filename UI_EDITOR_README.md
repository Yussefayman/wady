# Mobile UI JSON Editor

A Python GUI application for visually controlling and editing mobile app UI configurations stored in JSON format.

## Features

- **Visual Canvas**: Drag-and-drop interface to position widgets on a mobile screen canvas (iPhone-sized: 375x812px)
- **Property Editor**: Edit JSON fields with type-appropriate controls (text fields, number spinners, combo boxes)
- **JSON Structure View**: Tree view of the entire JSON structure for easy navigation
- **Widget List**: Quick access to all module elements
- **Dual Editing Modes**:
  - Visual property editor with form fields
  - Raw JSON text editor for advanced users
- **Multi-file Support**: Load and edit multiple JSON configuration files
- **Auto-save Positions**: Widget positions are automatically saved to the JSON when you drag them
- **Undo Protection**: Warning before closing with unsaved changes

## Installation

### 1. Install Dependencies

```bash
pip install PyQt5==5.15.10
```

Or install all project dependencies:

```bash
pip install -r requirement.txt
```

### 2. Verify Python Version

This application requires Python 3.6 or higher.

```bash
python --version
```

## Usage

### Starting the Application

```bash
python mobile_ui_editor.py
```

Or make it executable:

```bash
chmod +x mobile_ui_editor.py
./mobile_ui_editor.py
```

### Quick Start Guide

1. **Open a JSON File**
   - Click "Open JSON" button
   - Navigate to your JSON configuration file
   - Example files are provided in `example_configs/` directory

2. **Visual Editing**
   - Widgets from `moduleElements` and `enhancedData` appear on the canvas
   - Drag widgets to reposition them
   - Click on a widget to select it and view its properties

3. **Property Editing**
   - Select a widget on the canvas or from the left panel
   - Edit properties in the "Properties" tab on the right
   - Changes are applied immediately

4. **Raw JSON Editing**
   - Switch to the "Raw JSON" tab for direct JSON editing
   - Useful for bulk changes or complex nested structures

5. **Save Changes**
   - Click "Save" to update the current file
   - Click "Save As..." to create a new file

## JSON Structure

The editor expects JSON files with the following structure:

```json
{
  "id": "UITransformationEngine",
  "themeId": "",
  "animationId": "",
  "tabs": [...],
  "moduleId": "FinanceMain",
  "moduleTitle": "",
  "moduleSubTitle": "",
  "moduleElements": [
    {
      "id": "WidgetId",
      "Component": "ComponentName",
      "type": "Component",
      "props": {
        "position": {
          "x": 50,
          "y": 100,
          "width": 280,
          "height": 120
        },
        // ... other properties
      }
    }
  ],
  "enhancedData": [
    {
      "id": "DataId",
      "props": {
        "position": {
          "x": 50,
          "y": 360,
          "width": 280,
          "height": 140
        },
        // ... other properties
      }
    }
  ]
}
```

### Position Properties

The editor automatically adds/updates position information in the `props.position` object:

- `x`: Horizontal position (pixels from left)
- `y`: Vertical position (pixels from top)
- `width`: Widget width (default: 150px)
- `height`: Widget height (default: 100px)

## Example Files

Two example JSON files are included in `example_configs/`:

1. **finance_main.json** - Finance module UI configuration
2. **dashboard_config.json** - Dashboard module UI configuration

## UI Layout

The application window is divided into three main panels:

### Left Panel - Structure
- **JSON Structure Tree**: Hierarchical view of the entire JSON
- **Module Elements List**: Quick access to widgets

### Center Panel - Canvas
- **Visual Canvas**: 375x812px mobile screen representation
- Widgets can be dragged to reposition
- Click to select and edit

### Right Panel - Editor
- **Properties Tab**: Form-based property editor
- **Raw JSON Tab**: Direct JSON text editing

## Keyboard Shortcuts

- **Ctrl+O**: Open file
- **Ctrl+S**: Save file
- **Ctrl+Shift+S**: Save as new file

## Tips

1. **Position Precision**: You can edit exact X/Y coordinates in the property editor
2. **Bulk Editing**: Use the Raw JSON tab for renaming fields across multiple widgets
3. **Navigation**: Use the tree view to navigate complex nested structures
4. **Auto-save Positions**: Positions are saved automatically when you drag widgets

## Troubleshooting

### Application Won't Start

**Problem**: `ModuleNotFoundError: No module named 'PyQt5'`

**Solution**: Install PyQt5:
```bash
pip install PyQt5==5.15.10
```

### JSON Won't Load

**Problem**: "Failed to load file" error

**Solution**:
- Verify the JSON is valid (use a JSON validator)
- Check file permissions
- Ensure the file uses UTF-8 encoding

### Widgets Not Appearing

**Problem**: Canvas is empty after loading

**Solution**:
- Ensure your JSON has `moduleElements` or `enhancedData` arrays
- Check that widgets have valid structure with `id` and `props` fields

### Changes Not Saving

**Problem**: Edits don't persist

**Solution**:
- Click the "Save" button after making changes
- Check you have write permissions to the file
- If using Raw JSON tab, ensure the JSON is valid before saving

## Development

### Project Structure

```
wady/
├── mobile_ui_editor.py      # Main application
├── example_configs/          # Example JSON files
│   ├── finance_main.json
│   └── dashboard_config.json
├── requirement.txt           # Python dependencies
└── UI_EDITOR_README.md      # This file
```

### Adding New Features

The application is built with PyQt5 and uses these main classes:

- `MobileUIEditor`: Main window and application logic
- `CanvasView`: QGraphicsView for the visual canvas
- `DraggableWidget`: QGraphicsRectItem for widgets on canvas
- `PropertyEditor`: Dynamic form generator for JSON properties

### Extending Widget Types

To add support for new widget rendering:

1. Modify `DraggableWidget.__init__()` to customize appearance based on widget type
2. Update `update_label()` to show relevant information
3. Optionally add icons or images to widgets

## License

This tool is provided as-is for UI configuration editing purposes.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Verify your JSON structure matches the expected format
3. Review example files in `example_configs/`

---

**Version**: 1.0.0
**Python**: 3.6+
**Dependencies**: PyQt5 5.15.10+
