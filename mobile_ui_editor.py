#!/usr/bin/env python3
"""
Mobile UI JSON Editor
A GUI application to visually control and edit mobile app UI configurations
"""

import sys
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTreeWidget, QTreeWidgetItem, QSplitter,
    QFileDialog, QMessageBox, QLineEdit, QTextEdit, QComboBox,
    QScrollArea, QFrame, QGroupBox, QFormLayout, QSpinBox,
    QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem,
    QMenu, QAction, QInputDialog, QListWidget, QTabWidget
)
from PyQt5.QtCore import Qt, QRectF, QPointF, pyqtSignal
from PyQt5.QtGui import QColor, QBrush, QPen, QFont


class DraggableWidget(QGraphicsRectItem):
    """Represents a draggable widget on the canvas"""

    def __init__(self, widget_data: Dict, x: float, y: float, width: float, height: float):
        super().__init__(0, 0, width, height)
        self.widget_data = widget_data
        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.ItemIsSelectable)
        self.setFlag(QGraphicsRectItem.ItemSendsGeometryChanges)

        # Set appearance
        self.setBrush(QBrush(QColor(100, 150, 255, 100)))
        self.setPen(QPen(QColor(50, 100, 200), 2))

        # Add label
        self.label = QGraphicsTextItem(self)
        self.update_label()
        self.setPos(x, y)

    def update_label(self):
        """Update widget label based on data"""
        widget_id = self.widget_data.get('id', 'Unknown')
        widget_type = self.widget_data.get('Component', self.widget_data.get('type', 'Widget'))
        self.label.setPlainText(f"{widget_id}\n({widget_type})")
        self.label.setDefaultTextColor(QColor(255, 255, 255))
        font = QFont()
        font.setBold(True)
        font.setPointSize(10)
        self.label.setFont(font)

    def itemChange(self, change, value):
        """Handle position changes"""
        if change == QGraphicsRectItem.ItemPositionChange:
            # Store new position in widget data
            new_pos = value
            if 'position' not in self.widget_data.get('props', {}):
                if 'props' not in self.widget_data:
                    self.widget_data['props'] = {}
                self.widget_data['props']['position'] = {}
            self.widget_data['props']['position']['x'] = new_pos.x()
            self.widget_data['props']['position']['y'] = new_pos.y()
        return super().itemChange(change, value)


class CanvasView(QGraphicsView):
    """Canvas for visual widget positioning"""

    widget_selected = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # Set canvas properties
        self.setSceneRect(0, 0, 375, 812)  # iPhone-like dimensions
        self.scene.setBackgroundBrush(QBrush(QColor(240, 240, 240)))

        # Enable drag and drop
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRenderHint(self.renderHint(1))  # Antialiasing

        self.widgets_items = []

    def add_widget(self, widget_data: Dict):
        """Add a widget to the canvas"""
        # Get position from data or use defaults
        props = widget_data.get('props', {})
        position = props.get('position', {})
        x = position.get('x', 50 + len(self.widgets_items) * 20)
        y = position.get('y', 50 + len(self.widgets_items) * 20)
        width = position.get('width', 150)
        height = position.get('height', 100)

        widget_item = DraggableWidget(widget_data, x, y, width, height)
        self.scene.addItem(widget_item)
        self.widgets_items.append(widget_item)

    def clear_widgets(self):
        """Clear all widgets from canvas"""
        self.scene.clear()
        self.widgets_items = []

    def mousePressEvent(self, event):
        """Handle mouse press events"""
        super().mousePressEvent(event)
        item = self.itemAt(event.pos())
        if isinstance(item, DraggableWidget):
            self.widget_selected.emit(item.widget_data)
        elif isinstance(item, QGraphicsTextItem) and isinstance(item.parentItem(), DraggableWidget):
            self.widget_selected.emit(item.parentItem().widget_data)


class PropertyEditor(QWidget):
    """Editor for JSON properties"""

    property_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.current_data = None
        self.editors = {}
        self.init_ui()

    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()

        # Title
        title = QLabel("Property Editor")
        title.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        layout.addWidget(title)

        # Scroll area for properties
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.StyledPanel)

        self.properties_widget = QWidget()
        self.properties_layout = QFormLayout()
        self.properties_widget.setLayout(self.properties_layout)
        scroll.setWidget(self.properties_widget)

        layout.addWidget(scroll)
        self.setLayout(layout)

    def load_data(self, data: Dict):
        """Load data into property editor"""
        self.current_data = data
        self.clear_properties()

        if not data:
            return

        # Add editors for each field
        self.add_editors(data, "")

    def clear_properties(self):
        """Clear all property editors"""
        while self.properties_layout.count():
            item = self.properties_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.editors = {}

    def add_editors(self, data: Dict, prefix: str, depth: int = 0):
        """Recursively add editors for nested data"""
        if depth > 3:  # Prevent too deep nesting
            return

        for key, value in data.items():
            field_path = f"{prefix}.{key}" if prefix else key

            if isinstance(value, dict):
                # Add a label for nested objects
                label = QLabel(f"── {key} ──")
                label.setStyleSheet("font-weight: bold; color: #555; margin-top: 10px;")
                self.properties_layout.addRow(label)
                self.add_editors(value, field_path, depth + 1)
            elif isinstance(value, list):
                # Add list editor
                list_widget = QTextEdit()
                list_widget.setMaximumHeight(100)
                list_widget.setPlainText(json.dumps(value, indent=2))
                list_widget.textChanged.connect(lambda w=list_widget, p=field_path: self.update_list(p, w))
                self.properties_layout.addRow(f"{key}:", list_widget)
                self.editors[field_path] = list_widget
            elif isinstance(value, bool):
                # Add checkbox/combobox for boolean
                combo = QComboBox()
                combo.addItems(["true", "false"])
                combo.setCurrentText(str(value).lower())
                combo.currentTextChanged.connect(lambda v, p=field_path: self.update_field(p, v == "true"))
                self.properties_layout.addRow(f"{key}:", combo)
                self.editors[field_path] = combo
            elif isinstance(value, (int, float)):
                # Add number input
                spin = QSpinBox() if isinstance(value, int) else QSpinBox()
                spin.setMaximum(999999)
                spin.setMinimum(-999999)
                spin.setValue(int(value) if isinstance(value, int) else int(value))
                spin.valueChanged.connect(lambda v, p=field_path: self.update_field(p, v))
                self.properties_layout.addRow(f"{key}:", spin)
                self.editors[field_path] = spin
            else:
                # Add text input for strings
                line_edit = QLineEdit(str(value))
                line_edit.textChanged.connect(lambda v, p=field_path: self.update_field(p, v))
                self.properties_layout.addRow(f"{key}:", line_edit)
                self.editors[field_path] = line_edit

    def update_field(self, field_path: str, value):
        """Update a field in the data"""
        if not self.current_data:
            return

        keys = field_path.split('.')
        data = self.current_data

        # Navigate to the parent
        for key in keys[:-1]:
            data = data[key]

        # Update the value
        data[keys[-1]] = value
        self.property_changed.emit()

    def update_list(self, field_path: str, widget: QTextEdit):
        """Update a list field"""
        try:
            value = json.loads(widget.toPlainText())
            self.update_field(field_path, value)
        except json.JSONDecodeError:
            pass  # Invalid JSON, ignore


class MobileUIEditor(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.current_file = None
        self.json_data = None
        self.modified = False
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Mobile UI JSON Editor")
        self.setGeometry(100, 100, 1400, 900)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Toolbar
        toolbar = self.create_toolbar()
        main_layout.addLayout(toolbar)

        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)

        # Left panel - File tree and structure
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)

        # Center panel - Canvas
        center_panel = self.create_center_panel()
        splitter.addWidget(center_panel)

        # Right panel - Property editor
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)

        # Set initial sizes
        splitter.setSizes([300, 600, 400])

        main_layout.addWidget(splitter)

        # Status bar
        self.statusBar().showMessage("Ready")

    def create_toolbar(self):
        """Create toolbar with buttons"""
        layout = QHBoxLayout()

        # File operations
        btn_open = QPushButton("Open JSON")
        btn_open.clicked.connect(self.open_file)
        layout.addWidget(btn_open)

        btn_save = QPushButton("Save")
        btn_save.clicked.connect(self.save_file)
        layout.addWidget(btn_save)

        btn_save_as = QPushButton("Save As...")
        btn_save_as.clicked.connect(self.save_file_as)
        layout.addWidget(btn_save_as)

        layout.addStretch()

        # Current file label
        self.file_label = QLabel("No file loaded")
        self.file_label.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(self.file_label)

        return layout

    def create_left_panel(self):
        """Create left panel with JSON tree view"""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)

        # Title
        title = QLabel("JSON Structure")
        title.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        layout.addWidget(title)

        # Tree widget
        self.json_tree = QTreeWidget()
        self.json_tree.setHeaderLabel("Elements")
        self.json_tree.itemClicked.connect(self.tree_item_clicked)
        layout.addWidget(self.json_tree)

        # Widget list
        widgets_group = QGroupBox("Module Elements")
        widgets_layout = QVBoxLayout()
        widgets_group.setLayout(widgets_layout)

        self.widgets_list = QListWidget()
        self.widgets_list.itemClicked.connect(self.widget_list_item_clicked)
        widgets_layout.addWidget(self.widgets_list)

        layout.addWidget(widgets_group)

        return panel

    def create_center_panel(self):
        """Create center panel with canvas"""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)

        # Title
        title_layout = QHBoxLayout()
        title = QLabel("Visual Canvas")
        title.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        title_layout.addWidget(title)

        # Canvas size info
        size_label = QLabel("375 × 812 (iPhone)")
        size_label.setStyleSheet("color: #666; font-size: 11px;")
        title_layout.addWidget(size_label)
        title_layout.addStretch()

        layout.addLayout(title_layout)

        # Canvas
        self.canvas = CanvasView()
        self.canvas.widget_selected.connect(self.widget_selected)
        layout.addWidget(self.canvas)

        # Instructions
        instructions = QLabel("Drag widgets to reposition them. Click to select and edit properties.")
        instructions.setStyleSheet("color: #666; font-size: 11px; padding: 5px;")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        return panel

    def create_right_panel(self):
        """Create right panel with property editor"""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)

        # Tabs for different editors
        self.tabs = QTabWidget()

        # Property editor tab
        self.property_editor = PropertyEditor()
        self.property_editor.property_changed.connect(self.mark_modified)
        self.tabs.addTab(self.property_editor, "Properties")

        # Raw JSON editor tab
        self.raw_editor = QTextEdit()
        self.raw_editor.setFont(QFont("Courier"))
        self.raw_editor.textChanged.connect(self.mark_modified)
        self.tabs.addTab(self.raw_editor, "Raw JSON")

        layout.addWidget(self.tabs)

        return panel

    def open_file(self):
        """Open a JSON file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open JSON File",
            "",
            "JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            self.load_file(file_path)

    def load_file(self, file_path: str):
        """Load JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.json_data = json.load(f)

            self.current_file = file_path
            self.file_label.setText(f"File: {Path(file_path).name}")
            self.statusBar().showMessage(f"Loaded: {file_path}")
            self.modified = False

            # Update UI
            self.populate_tree()
            self.populate_widgets_list()
            self.load_canvas()
            self.update_raw_editor()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file:\n{str(e)}")

    def populate_tree(self):
        """Populate the tree view with JSON structure"""
        self.json_tree.clear()

        if not self.json_data:
            return

        root = QTreeWidgetItem(self.json_tree)
        root.setText(0, self.json_data.get('id', 'Root'))
        root.setExpanded(True)

        self.add_tree_items(root, self.json_data)

    def add_tree_items(self, parent: QTreeWidgetItem, data: Dict):
        """Recursively add items to tree"""
        for key, value in data.items():
            if isinstance(value, dict):
                item = QTreeWidgetItem(parent)
                item.setText(0, f"{key}")
                item.setData(0, Qt.UserRole, value)
                self.add_tree_items(item, value)
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                item = QTreeWidgetItem(parent)
                item.setText(0, f"{key} ({len(value)} items)")
                for i, elem in enumerate(value):
                    sub_item = QTreeWidgetItem(item)
                    sub_item.setText(0, f"[{i}] {elem.get('id', elem.get('Component', 'Item'))}")
                    sub_item.setData(0, Qt.UserRole, elem)
            else:
                item = QTreeWidgetItem(parent)
                item.setText(0, f"{key}: {value}")
                item.setData(0, Qt.UserRole, {key: value})

    def populate_widgets_list(self):
        """Populate the widgets list"""
        self.widgets_list.clear()

        if not self.json_data:
            return

        module_elements = self.json_data.get('moduleElements', [])
        for elem in module_elements:
            widget_id = elem.get('id', 'Unknown')
            self.widgets_list.addItem(widget_id)

    def load_canvas(self):
        """Load widgets onto the canvas"""
        self.canvas.clear_widgets()

        if not self.json_data:
            return

        # Load module elements
        module_elements = self.json_data.get('moduleElements', [])
        for elem in module_elements:
            self.canvas.add_widget(elem)

        # Load enhanced data
        enhanced_data = self.json_data.get('enhancedData', [])
        for elem in enhanced_data:
            self.canvas.add_widget(elem)

    def update_raw_editor(self):
        """Update raw JSON editor"""
        if self.json_data:
            self.raw_editor.blockSignals(True)
            self.raw_editor.setPlainText(json.dumps(self.json_data, indent=2))
            self.raw_editor.blockSignals(False)

    def tree_item_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle tree item click"""
        data = item.data(0, Qt.UserRole)
        if data:
            self.property_editor.load_data(data)

    def widget_list_item_clicked(self, item):
        """Handle widget list item click"""
        if not self.json_data:
            return

        widget_id = item.text()
        module_elements = self.json_data.get('moduleElements', [])

        for elem in module_elements:
            if elem.get('id') == widget_id:
                self.property_editor.load_data(elem)
                break

    def widget_selected(self, widget_data: Dict):
        """Handle widget selection on canvas"""
        self.property_editor.load_data(widget_data)
        self.statusBar().showMessage(f"Selected: {widget_data.get('id', 'Unknown')}")

    def mark_modified(self):
        """Mark the file as modified"""
        self.modified = True
        if self.current_file:
            self.file_label.setText(f"File: {Path(self.current_file).name} *")

    def save_file(self):
        """Save the current file"""
        if not self.current_file:
            self.save_file_as()
            return

        try:
            # Update JSON data from raw editor if that tab is active
            if self.tabs.currentWidget() == self.raw_editor:
                self.json_data = json.loads(self.raw_editor.toPlainText())

            with open(self.current_file, 'w', encoding='utf-8') as f:
                json.dump(self.json_data, f, indent=2, ensure_ascii=False)

            self.modified = False
            self.file_label.setText(f"File: {Path(self.current_file).name}")
            self.statusBar().showMessage(f"Saved: {self.current_file}")

            # Refresh UI
            self.populate_tree()
            self.load_canvas()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")

    def save_file_as(self):
        """Save file with a new name"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save JSON File",
            "",
            "JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            self.current_file = file_path
            self.save_file()

    def closeEvent(self, event):
        """Handle window close event"""
        if self.modified:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before closing?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )

            if reply == QMessageBox.Save:
                self.save_file()
                event.accept()
            elif reply == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()


def main():
    """Main entry point"""
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle('Fusion')

    # Create and show main window
    editor = MobileUIEditor()
    editor.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
