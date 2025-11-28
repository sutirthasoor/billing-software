import tkinter as tk
from tkinter import ttk
from config import Config

class DataTable(ttk.Frame):
    """Enhanced data table with sorting, filtering, and pagination"""
    
    def __init__(self, parent, columns, **kwargs):
        super().__init__(parent, style='Modern.TFrame')
        
        self.columns = columns
        self.data = []
        self.filtered_data = []
        self.sort_column = None
        self.sort_reverse = False
        self.current_page = 1
        self.page_size = kwargs.pop('page_size', 50)
        self.show_toolbar = kwargs.pop('show_toolbar', True)
        self.show_pagination = kwargs.pop('show_pagination', True)
        self.selectable = kwargs.pop('selectable', True)
        
        self.setup_table()
        
        if self.show_toolbar:
            self.setup_toolbar()
        
        if self.show_pagination:
            self.setup_pagination()
    
    def setup_table(self):
        """Setup the table with headers and scrollbars"""
        # Main frame for table
        table_frame = ttk.Frame(self, style='Modern.TFrame')
        table_frame.pack(fill='both', expand=True)
        
        # Create treeview
        self.tree = ttk.Treeview(table_frame, columns=self.columns, show='headings', 
                                style='Modern.Treeview', selectmode='browse' if self.selectable else 'none')
        
        # Setup columns
        for col in self.columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
            self.tree.column(col, width=100, minwidth=50)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack everything
        self.tree.pack(side='top', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind events
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.bind('<<TreeviewSelect>>', self.on_selection)
    
    def setup_toolbar(self):
        """Setup table toolbar with search and actions"""
        toolbar = ttk.Frame(self, style='Modern.TFrame')
        toolbar.pack(fill='x', pady=(10, 5))
        
        # Search box
        ttk.Label(toolbar, text="Search:", style='Normal.TLabel').pack(side='left', padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(toolbar, textvariable=self.search_var, 
                                style='Modern.TEntry', width=30)
        search_entry.pack(side='left', padx=(0, 10))
        search_entry.bind('<KeyRelease>', self.on_search)
        
        # Action buttons
        ttk.Button(toolbar, text="Refresh", style='Secondary.TButton',
                  command=self.refresh).pack(side='left', padx=(0, 5))
        ttk.Button(toolbar, text="Export", style='Secondary.TButton',
                  command=self.export_data).pack(side='left', padx=(0, 5))
        ttk.Button(toolbar, text="Clear Filters", style='Secondary.TButton',
                  command=self.clear_filters).pack(side='left')
    
    def setup_pagination(self):
        """Setup pagination controls"""
        pagination = ttk.Frame(self, style='Modern.TFrame')
        pagination.pack(fill='x', pady=(5, 0))
        
        # Page info
        self.page_info_var = tk.StringVar()
        page_label = ttk.Label(pagination, textvariable=self.page_info_var, style='Small.TLabel')
        page_label.pack(side='left')
        
        # Navigation buttons
        nav_frame = ttk.Frame(pagination, style='Modern.TFrame')
        nav_frame.pack(side='right')
        
        ttk.Button(nav_frame, text="⏪ First", style='Secondary.TButton',
                  command=lambda: self.go_to_page(1)).pack(side='left', padx=(0, 2))
        ttk.Button(nav_frame, text="◀ Prev", style='Secondary.TButton',
                  command=self.prev_page).pack(side='left', padx=(0, 2))
        ttk.Button(nav_frame, text="Next ▶", style='Secondary.TButton',
                  command=self.next_page).pack(side='left', padx=(0, 2))
        ttk.Button(nav_frame, text="Last ⏩", style='Secondary.TButton',
                  command=self.last_page).pack(side='left')
    
    def set_data(self, data):
        """Set table data"""
        self.data = data
        self.filtered_data = data.copy()
        self.current_page = 1
        self.refresh_display()
    
    def refresh_display(self):
        """Refresh table display"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Calculate pagination
        start_idx = (self.current_page - 1) * self.page_size
        end_idx = start_idx + self.page_size
        page_data = self.filtered_data[start_idx:end_idx]
        
        # Insert data
        for row in page_data:
            self.tree.insert('', 'end', values=row)
        
        # Update pagination info
        if self.show_pagination:
            total_pages = max(1, (len(self.filtered_data) + self.page_size - 1) // self.page_size)
            self.page_info_var.set(f"Page {self.current_page} of {total_pages} | Total: {len(self.filtered_data)} records")
    
    def sort_by_column(self, column):
        """Sort data by column"""
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
        
        try:
            col_index = self.columns.index(column)
            self.filtered_data.sort(key=lambda x: x[col_index], reverse=self.sort_reverse)
            self.refresh_display()
        except (ValueError, IndexError):
            pass
    
    def on_search(self, event=None):
        """Handle search filter"""
        search_text = self.search_var.get().lower()
        
        if not search_text:
            self.filtered_data = self.data.copy()
        else:
            self.filtered_data = [
                row for row in self.data
                if any(search_text in str(cell).lower() for cell in row)
            ]
        
        self.current_page = 1
        self.refresh_display()
    
    def clear_filters(self):
        """Clear all filters"""
        self.search_var.set('')
        self.filtered_data = self.data.copy()
        self.current_page = 1
        self.refresh_display()
    
    def go_to_page(self, page):
        """Go to specific page"""
        total_pages = max(1, (len(self.filtered_data) + self.page_size - 1) // self.page_size)
        if 1 <= page <= total_pages:
            self.current_page = page
            self.refresh_display()
    
    def prev_page(self):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_display()
    
    def next_page(self):
        """Go to next page"""
        total_pages = max(1, (len(self.filtered_data) + self.page_size - 1) // self.page_size)
        if self.current_page < total_pages:
            self.current_page += 1
            self.refresh_display()
    
    def last_page(self):
        """Go to last page"""
        total_pages = max(1, (len(self.filtered_data) + self.page_size - 1) // self.page_size)
        self.current_page = total_pages
        self.refresh_display()
    
    def refresh(self):
        """Refresh table data"""
        # This would typically reload data from source
        # For now, just refresh display
        self.refresh_display()
    
    def export_data(self):
        """Export table data"""
        # This would export to CSV or Excel
        print("Export functionality would be implemented here")
    
    def on_double_click(self, event):
        """Handle double click on row"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item)['values']
            self.on_row_double_click(values)
    
    def on_selection(self, event):
        """Handle row selection"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item)['values']
            self.on_row_select(values)
    
    def on_row_double_click(self, values):
        """Override this method for double-click behavior"""
        pass
    
    def on_row_select(self, values):
        """Override this method for selection behavior"""
        pass
    
    def get_selected_row(self):
        """Get currently selected row"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            return self.tree.item(item)['values']
        return None
    
    def get_selected_rows(self):
        """Get all selected rows (for multi-select mode)"""
        selections = self.tree.selection()
        return [self.tree.item(item)['values'] for item in selections]