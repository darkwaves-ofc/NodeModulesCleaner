import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from pathlib import Path
import time


TEMPLATES = {
    "Next.js": {
        "folders": [".next", "node_modules", "dist", "build", ".cache"],
        "files": ["package-lock.json", "yarn.lock", ".env.local", ".env.development.local"]
    },
    "React": {
        "folders": ["build", "node_modules", "dist", ".cache"],
        "files": ["package-lock.json", "yarn.lock", ".env.local"]
    },
    "Vite": {
        "folders": ["dist", "node_modules", ".vite", "build"],
        "files": ["package-lock.json", "yarn.lock", ".env.local"]
    },
    "Python": {
        "folders": ["__pycache__", ".venv", "venv", "env", ".pytest_cache", "dist", "build"],
        "files": ["poetry.lock", "Pipfile.lock", ".coverage", "*.pyc", "*.pyo"]
    },
    "Node.js": {
        "folders": ["node_modules", "dist", "build", ".cache", ".npm"],
        "files": ["package-lock.json", "yarn.lock", "npm-debug.log", "*.log"]
    }
}

class ImprovedCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧹 Project Cleaner Pro")
        self.root.geometry("1000x700")
        self.root.configure(bg='#ffffff')
        
        # Variables
        self.base_path = tk.StringVar()
        self.template = tk.StringVar(value="Next.js")
        self.scan_results = []  # List of dictionaries with item info
        self.is_scanning = False
        
        # Configure styles
        self.setup_styles()
        self.build_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom styles
        style.configure('Card.TFrame', relief='solid', borderwidth=1, background='#f8f9fa')
        style.configure('Title.TLabel', font=('Segoe UI', 18, 'bold'), background='#ffffff', foreground='#2c3e50')
        style.configure('Subtitle.TLabel', font=('Segoe UI', 10), background='#ffffff', foreground='#7f8c8d')
        style.configure('Section.TLabel', font=('Segoe UI', 11, 'bold'), background='#f8f9fa', foreground='#34495e')
        style.configure('Primary.TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('Success.TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('Danger.TButton', font=('Segoe UI', 10, 'bold'))

    def build_ui(self):
        # Main container with padding
        main_container = tk.Frame(self.root, bg='#ffffff', padx=20, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header section
        self.create_header(main_container)
        
        # Configuration section
        self.create_config_section(main_container)
        
        # Action section
        self.create_action_section(main_container)
        
        # Results section
        self.create_results_section(main_container)

    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg='#ffffff')
        header_frame.pack(fill='x', pady=(0, 20))
        
        title = ttk.Label(header_frame, text="🧹 Project Cleaner Pro", style='Title.TLabel')
        title.pack()
        
        subtitle = ttk.Label(header_frame, text="Clean up build artifacts, dependencies, and temporary files from your projects", style='Subtitle.TLabel')
        subtitle.pack(pady=(5, 0))

    def create_config_section(self, parent):
        # Configuration card
        config_card = ttk.Frame(parent, style='Card.TFrame', padding=15)
        config_card.pack(fill='x', pady=(0, 15))
        
        ttk.Label(config_card, text="📁 Configuration", style='Section.TLabel').pack(anchor='w', pady=(0, 10))
        
        # Path selection
        path_frame = tk.Frame(config_card, bg='#f8f9fa')
        path_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(path_frame, text="Project Folder:", background='#f8f9fa').pack(anchor='w')
        
        path_input_frame = tk.Frame(path_frame, bg='#f8f9fa')
        path_input_frame.pack(fill='x', pady=(5, 0))
        
        self.path_entry = ttk.Entry(path_input_frame, textvariable=self.base_path, font=('Segoe UI', 10))
        self.path_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(path_input_frame, text="📂 Browse", command=self.browse_folder)
        browse_btn.pack(side='right')
        
        # Template selection
        template_frame = tk.Frame(config_card, bg='#f8f9fa')
        template_frame.pack(fill='x')
        
        ttk.Label(template_frame, text="Project Type:", background='#f8f9fa').pack(anchor='w')
        
        self.template_combo = ttk.Combobox(template_frame, textvariable=self.template, 
                                         values=list(TEMPLATES.keys()), state='readonly', 
                                         font=('Segoe UI', 10))
        self.template_combo.pack(fill='x', pady=(5, 0))

    def create_action_section(self, parent):
        action_frame = tk.Frame(parent, bg='#ffffff')
        action_frame.pack(fill='x', pady=(0, 15))
        
        # Left side - scan button and status
        left_frame = tk.Frame(action_frame, bg='#ffffff')
        left_frame.pack(side='left', fill='x', expand=True)
        
        self.scan_btn = ttk.Button(left_frame, text="🔍 Scan Project", command=self.start_scan, style='Primary.TButton')
        self.scan_btn.pack(side='left', padx=(0, 15))
        
        self.status_label = tk.Label(left_frame, text="Ready to scan", bg='#ffffff', fg='#7f8c8d', font=('Segoe UI', 9))
        self.status_label.pack(side='left', anchor='w')
        
        # Right side - selection controls
        right_frame = tk.Frame(action_frame, bg='#ffffff')
        right_frame.pack(side='right')
        
        self.select_all_btn = ttk.Button(right_frame, text="✅ Select All", command=self.select_all, state='disabled')
        self.select_all_btn.pack(side='left', padx=(0, 5))
        
        self.unselect_all_btn = ttk.Button(right_frame, text="❌ Clear All", command=self.unselect_all, state='disabled')
        self.unselect_all_btn.pack(side='left', padx=(0, 15))
        
        self.delete_btn = ttk.Button(right_frame, text="🗑️ Delete Selected", command=self.confirm_delete, 
                                   style='Danger.TButton', state='disabled')
        self.delete_btn.pack(side='left')

    def create_results_section(self, parent):
        # Results card
        results_card = ttk.Frame(parent, style='Card.TFrame', padding=15)
        results_card.pack(fill='both', expand=True)
        
        # Header with info
        results_header = tk.Frame(results_card, bg='#f8f9fa')
        results_header.pack(fill='x', pady=(0, 10))
        
        ttk.Label(results_header, text="📋 Scan Results", style='Section.TLabel').pack(side='left')
        
        self.info_label = tk.Label(results_header, text="", bg='#f8f9fa', fg='#7f8c8d', font=('Segoe UI', 9, 'bold'))
        self.info_label.pack(side='right')
        
        # Progress bar
        self.progress = ttk.Progressbar(results_card, mode='indeterminate')
        self.progress.pack(fill='x', pady=(0, 10))
        self.progress.pack_forget()  # Hide initially
        
        # Treeview with checkboxes
        tree_frame = tk.Frame(results_card, bg='#f8f9fa')
        tree_frame.pack(fill='both', expand=True)
        
        # Create treeview with columns
        columns = ('Selected', 'Size', 'Type', 'Path')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)
        
        # Configure columns
        self.tree.heading('Selected', text='✓', anchor='center')
        self.tree.heading('Size', text='Size', anchor='center')
        self.tree.heading('Type', text='Type', anchor='center')
        self.tree.heading('Path', text='Path', anchor='w')
        
        self.tree.column('Selected', width=50, minwidth=50, anchor='center')
        self.tree.column('Size', width=100, minwidth=80, anchor='center')
        self.tree.column('Type', width=80, minwidth=60, anchor='center')
        self.tree.column('Path', width=600, minwidth=300, anchor='w')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind click events for selection
        self.tree.bind('<Button-1>', self.on_tree_click)
        self.tree.bind('<space>', self.on_tree_space)

    def browse_folder(self):
        path = filedialog.askdirectory(title="Select Project Folder")
        if path:
            self.base_path.set(path)

    def start_scan(self):
        if self.is_scanning:
            return
            
        base_path = self.base_path.get().strip()
        if not base_path or not os.path.isdir(base_path):
            messagebox.showerror("Error", "Please select a valid project folder")
            return
        
        # Start scanning in a separate thread
        self.is_scanning = True
        self.scan_btn.config(state='disabled', text="🔄 Scanning...")
        self.progress.pack(fill='x', pady=(0, 10))
        self.progress.start(10)
        
        # Clear previous results
        self.clear_results()
        
        # Start scan thread
        scan_thread = threading.Thread(target=self.scan_project, daemon=True)
        scan_thread.start()

    def scan_project(self):
        try:
            base_path = self.base_path.get()
            template_config = TEMPLATES[self.template.get()]
            folders_to_find = template_config["folders"]
            files_to_find = template_config["files"]
            
            self.root.after(0, lambda: self.status_label.config(text="Scanning directories...", fg='#3498db'))
            
            found_items = []
            
            # Walk through directory tree
            for root_dir, dirs, files in os.walk(base_path):
                # Skip if we're inside a node_modules or similar large folder
                rel_path = os.path.relpath(root_dir, base_path)
                if any(skip_folder in rel_path.split(os.sep) for skip_folder in ['node_modules', '.git', '.venv']):
                    if os.path.basename(root_dir) not in folders_to_find:
                        continue
                
                # Check for folders to clean
                for folder_name in dirs[:]:  # Use slice to avoid modification issues
                    if folder_name in folders_to_find:
                        folder_path = os.path.join(root_dir, folder_name)
                        size = self.calculate_folder_size(folder_path)
                        
                        found_items.append({
                            'path': folder_path,
                            'relative_path': os.path.relpath(folder_path, base_path),
                            'type': 'Folder',
                            'size': size,
                            'selected': True
                        })
                        
                        # Don't recurse into found folders
                        dirs.remove(folder_name)
                
                # Check for files to clean
                for file_name in files:
                    if self.should_clean_file(file_name, files_to_find):
                        file_path = os.path.join(root_dir, file_name)
                        try:
                            size = os.path.getsize(file_path)
                        except (OSError, FileNotFoundError):
                            size = 0
                        
                        found_items.append({
                            'path': file_path,
                            'relative_path': os.path.relpath(file_path, base_path),
                            'type': 'File',
                            'size': size,
                            'selected': True
                        })
            
            # Update UI in main thread
            self.root.after(0, lambda: self.scan_completed(found_items))
            
        except Exception as e:
            self.root.after(0, lambda e=e: self.scan_error(str(e)))

    def should_clean_file(self, filename, patterns):
        """Check if file matches any of the cleanup patterns"""
        for pattern in patterns:
            if '*' in pattern:
                # Handle wildcard patterns
                if pattern.startswith('*'):
                    if filename.endswith(pattern[1:]):
                        return True
                elif pattern.endswith('*'):
                    if filename.startswith(pattern[:-1]):
                        return True
            else:
                # Exact match
                if filename == pattern:
                    return True
        return False

    def calculate_folder_size(self, folder_path):
        """Calculate total size of folder (optimized)"""
        total_size = 0
        try:
            # Use os.scandir for better performance
            with os.scandir(folder_path) as entries:
                for entry in entries:
                    if entry.is_file(follow_symlinks=False):
                        try:
                            total_size += entry.stat().st_size
                        except (OSError, FileNotFoundError):
                            pass
                    elif entry.is_dir(follow_symlinks=False):
                        total_size += self.calculate_folder_size(entry.path)
        except (OSError, FileNotFoundError, PermissionError):
            pass
        return total_size

    def scan_completed(self, found_items):
        self.is_scanning = False
        self.progress.stop()
        self.progress.pack_forget()
        self.scan_btn.config(state='normal', text="🔍 Scan Project")
        
        self.scan_results = found_items
        self.populate_results()
        
        if found_items:
            total_size = sum(item['size'] for item in found_items)
            self.status_label.config(text=f"Found {len(found_items)} items ({self.format_size(total_size)})", fg='#e67e22')
            self.enable_controls()
        else:
            self.status_label.config(text="✅ No cleanup items found - project is clean!", fg='#27ae60')

    def scan_error(self, error_msg):
        self.is_scanning = False
        self.progress.stop()
        self.progress.pack_forget()
        self.scan_btn.config(state='normal', text="🔍 Scan Project")
        self.status_label.config(text=f"❌ Scan failed: {error_msg}", fg='#e74c3c')

    def populate_results(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add items to tree
        for i, item in enumerate(self.scan_results):
            icon = "📁" if item['type'] == 'Folder' else "📄"
            selected_icon = "✅" if item['selected'] else "⬜"
            
            self.tree.insert('', 'end', iid=str(i), values=(
                selected_icon,
                self.format_size(item['size']),
                item['type'],
                f"{icon} {item['relative_path']}"
            ))
        
        self.update_info_label()

    def clear_results(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.scan_results = []
        self.disable_controls()
        self.info_label.config(text="")

    def enable_controls(self):
        self.select_all_btn.config(state='normal')
        self.unselect_all_btn.config(state='normal')
        self.delete_btn.config(state='normal')

    def disable_controls(self):
        self.select_all_btn.config(state='disabled')
        self.unselect_all_btn.config(state='disabled')
        self.delete_btn.config(state='disabled')

    def on_tree_click(self, event):
        """Handle tree item click for selection toggle"""
        item_id = self.tree.identify('item', event.x, event.y)
        column = self.tree.identify('column', event.x, event.y)
        
        if item_id and column == '#1':  # Clicked on Selected column
            self.toggle_selection(item_id)

    def on_tree_space(self, event):
        """Handle spacebar for selection toggle"""
        selection = self.tree.selection()
        if selection:
            self.toggle_selection(selection[0])

    def toggle_selection(self, item_id):
        """Toggle selection state of an item"""
        try:
            index = int(item_id)
            if 0 <= index < len(self.scan_results):
                self.scan_results[index]['selected'] = not self.scan_results[index]['selected']
                
                # Update tree display
                selected_icon = "✅" if self.scan_results[index]['selected'] else "⬜"
                current_values = list(self.tree.item(item_id, 'values'))
                current_values[0] = selected_icon
                self.tree.item(item_id, values=current_values)
                
                self.update_info_label()
        except (ValueError, IndexError):
            pass

    def select_all(self):
        """Select all items"""
        for item in self.scan_results:
            item['selected'] = True
        self.populate_results()

    def unselect_all(self):
        """Unselect all items"""
        for item in self.scan_results:
            item['selected'] = False
        self.populate_results()

    def update_info_label(self):
        """Update the info label with selection statistics"""
        selected_items = [item for item in self.scan_results if item['selected']]
        if selected_items:
            total_size = sum(item['size'] for item in selected_items)
            self.info_label.config(text=f"Selected: {len(selected_items)} items ({self.format_size(total_size)})")
        else:
            self.info_label.config(text="No items selected")

    def confirm_delete(self):
        """Confirm and delete selected items"""
        selected_items = [item for item in self.scan_results if item['selected']]
        
        if not selected_items:
            messagebox.showinfo("Info", "No items selected for deletion.")
            return
        
        total_size = sum(item['size'] for item in selected_items)
        
        result = messagebox.askyesno(
            "Confirm Deletion",
            f"Delete {len(selected_items)} items?\n\n"
            f"Total size: {self.format_size(total_size)}\n\n"
            f"⚠️ This action cannot be undone!",
            icon='warning'
        )
        
        if result:
            self.delete_items(selected_items)

    def delete_items(self, items_to_delete):
        """Delete the specified items"""
        self.delete_btn.config(state='disabled', text="🗑️ Deleting...")
        self.progress.pack(fill='x', pady=(0, 10))
        self.progress.start(10)
        
        # Start deletion in separate thread
        delete_thread = threading.Thread(target=self.perform_deletion, args=(items_to_delete,), daemon=True)
        delete_thread.start()

    def perform_deletion(self, items_to_delete):
        """Perform the actual deletion"""
        deleted_count = 0
        errors = []
        
        for item in items_to_delete:
            try:
                if item['type'] == 'Folder':
                    shutil.rmtree(item['path'])
                else:
                    os.remove(item['path'])
                deleted_count += 1
            except Exception as e:
                errors.append(f"{item['relative_path']}: {str(e)}")
        
        # Update UI in main thread
        self.root.after(0, lambda: self.deletion_completed(deleted_count, errors))

    def deletion_completed(self, deleted_count, errors):
        """Handle deletion completion"""
        self.progress.stop()
        self.progress.pack_forget()
        self.delete_btn.config(state='normal', text="🗑️ Delete Selected")
        
        if errors:
            error_msg = f"Deleted {deleted_count} items.\n\nErrors ({len(errors)}):\n"
            error_msg += "\n".join(errors[:5])
            if len(errors) > 5:
                error_msg += f"\n... and {len(errors) - 5} more errors"
            messagebox.showwarning("Deletion Complete with Errors", error_msg)
        else:
            messagebox.showinfo("Success", f"Successfully deleted {deleted_count} items!")
        
        # Refresh scan
        self.start_scan()

    def format_size(self, size_bytes):
        """Format bytes to human readable string"""
        if size_bytes == 0:
            return "0 B"
        
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"

if __name__ == "__main__":
    root = tk.Tk()
    app = ImprovedCleanerApp(root)
    root.mainloop()