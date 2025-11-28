import tkinter as tk
from tkinter import ttk
from config import Config

class SearchBox(ttk.Frame):
    """Enhanced search box with suggestions and filters"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, style='Modern.TFrame')
        
        self.placeholder = kwargs.pop('placeholder', 'Search...')
        self.width = kwargs.pop('width', 30)
        self.on_search = kwargs.pop('on_search', None)
        self.on_select = kwargs.pop('on_select', None)
        self.suggestions = kwargs.pop('suggestions', [])
        self.filters = kwargs.pop('filters', {})
        self.show_filters = kwargs.pop('show_filters', False)
        
        self.setup_search_box()
        
        if self.show_filters:
            self.setup_filters()
    
    def setup_search_box(self):
        """Setup search input and suggestions"""
        # Main search frame
        search_frame = ttk.Frame(self, style='Modern.TFrame')
        search_frame.pack(fill='x')
        
        # Search icon and input
        icon_label = ttk.Label(search_frame, text="🔍", style='Normal.TLabel')
        icon_label.pack(side='left', padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var,
                                     style='Modern.TEntry', width=self.width)
        self.search_entry.pack(side='left', fill='x', expand=True)
        
        # Clear button
        self.clear_btn = ttk.Button(search_frame, text="✕", style='Secondary.TButton',
                                  width=3, command=self.clear_search)
        self.clear_btn.pack(side='left', padx=(5, 0))
        
        # Set placeholder
        self.set_placeholder()
        
        # Bind events
        self.search_entry.bind('<KeyRelease>', self.on_key_release)
        self.search_entry.bind('<FocusIn>', self.on_focus_in)
        self.search_entry.bind('<FocusOut>', self.on_focus_out)
        self.search_entry.bind('<Return>', self.on_enter)
        self.search_entry.bind('<Down>', self.show_suggestions)
        
        # Suggestions listbox
        self.suggestions_frame = ttk.Frame(self, style='Modern.TFrame')
        self.suggestions_listbox = tk.Listbox(self.suggestions_frame, 
                                            bg=Config.THEME['primary'],
                                            relief='solid', bd=1,
                                            font=Config.FONTS['small'])
        self.suggestions_listbox.pack(fill='x')
        self.suggestions_listbox.bind('<<ListboxSelect>>', self.on_suggestion_select)
        self.suggestions_listbox.bind('<Double-1>', self.on_suggestion_double_click)
        
        self.suggestions_visible = False
    
    def setup_filters(self):
        """Setup search filters"""
        self.filters_frame = ttk.Frame(self, style='Modern.TFrame')
        self.filters_frame.pack(fill='x', pady=(5, 0))
        
        # Filter buttons
        self.filter_buttons = {}
        for filter_name, filter_options in self.filters.items():
            filter_frame = ttk.Frame(self.filters_frame, style='Modern.TFrame')
            filter_frame.pack(side='left', padx=(0, 10))
            
            ttk.Label(filter_frame, text=f"{filter_name}:", style='Small.TLabel').pack(side='left')
            
            filter_var = tk.StringVar(value="All")
            filter_combo = ttk.Combobox(filter_frame, textvariable=filter_var,
                                      values=["All"] + filter_options,
                                      style='Modern.TCombobox', width=12)
            filter_combo.pack(side='left', padx=(5, 0))
            filter_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
            
            self.filter_buttons[filter_name] = filter_var
    
    def set_placeholder(self):
        """Set placeholder text"""
        if not self.search_var.get():
            self.search_entry.configure(foreground=Config.THEME['text_secondary'])
            self.search_var.set(self.placeholder)
    
    def clear_placeholder(self):
        """Clear placeholder text"""
        if self.search_var.get() == self.placeholder:
            self.search_entry.configure(foreground=Config.THEME['text_primary'])
            self.search_var.set('')
    
    def on_focus_in(self, event):
        """Handle focus in"""
        self.clear_placeholder()
        self.show_suggestions()
    
    def on_focus_out(self, event):
        """Handle focus out"""
        if not self.search_var.get():
            self.set_placeholder()
        self.hide_suggestions()
    
    def on_key_release(self, event):
        """Handle key release"""
        search_text = self.search_var.get()
        
        if search_text and search_text != self.placeholder:
            self.update_suggestions(search_text)
            self.show_suggestions()
            
            if self.on_search:
                self.on_search(search_text)
        else:
            self.hide_suggestions()
    
    def on_enter(self, event):
        """Handle enter key"""
        self.hide_suggestions()
        if self.on_search:
            self.on_search(self.search_var.get())
    
    def update_suggestions(self, search_text):
        """Update suggestions based on search text"""
        self.suggestions_listbox.delete(0, tk.END)
        
        if not search_text or search_text == self.placeholder:
            return
        
        filtered_suggestions = [
            s for s in self.suggestions 
            if search_text.lower() in s.lower()
        ][:10]  # Limit to 10 suggestions
        
        for suggestion in filtered_suggestions:
            self.suggestions_listbox.insert(tk.END, suggestion)
    
    def show_suggestions(self, event=None):
        """Show suggestions dropdown"""
        if self.suggestions_listbox.size() > 0 and not self.suggestions_visible:
            self.suggestions_frame.pack(fill='x', pady=(2, 0))
            self.suggestions_visible = True
    
    def hide_suggestions(self):
        """Hide suggestions dropdown"""
        if self.suggestions_visible:
            self.suggestions_frame.pack_forget()
            self.suggestions_visible = False
    
    def on_suggestion_select(self, event):
        """Handle suggestion selection"""
        selection = self.suggestions_listbox.curselection()
        if selection:
            selected_text = self.suggestions_listbox.get(selection[0])
            self.search_var.set(selected_text)
    
    def on_suggestion_double_click(self, event):
        """Handle suggestion double click"""
        self.on_suggestion_select(event)
        self.hide_suggestions()
        if self.on_select:
            self.on_select(self.search_var.get())
    
    def on_filter_change(self, event):
        """Handle filter change"""
        if self.on_search:
            self.on_search(self.search_var.get())
    
    def clear_search(self):
        """Clear search text"""
        self.search_var.set('')
        self.set_placeholder()
        self.hide_suggestions()
        
        if self.on_search:
            self.on_search('')
    
    def get_search_text(self):
        """Get current search text"""
        text = self.search_var.get()
        return '' if text == self.placeholder else text
    
    def set_suggestions(self, suggestions):
        """Update suggestions list"""
        self.suggestions = suggestions
    
    def get_filters(self):
        """Get current filter values"""
        filters = {}
        for filter_name, var in self.filter_buttons.items():
            value = var.get()
            if value != "All":
                filters[filter_name] = value
        return filters
    
    def set_focus(self):
        """Set focus to search box"""
        self.search_entry.focus()
        self.clear_placeholder()

class AdvancedSearchBox(SearchBox):
    """Advanced search with multiple criteria"""
    
    def __init__(self, parent, **kwargs):
        self.search_fields = kwargs.pop('search_fields', [])
        super().__init__(parent, **kwargs)
    
    def setup_search_box(self):
        """Setup advanced search interface"""
        # Search criteria frame
        criteria_frame = ttk.Frame(self, style='Modern.TFrame')
        criteria_frame.pack(fill='x')
        
        self.criteria_widgets = {}
        
        for i, field in enumerate(self.search_fields):
            field_frame = ttk.Frame(criteria_frame, style='Modern.TFrame')
            field_frame.pack(fill='x', pady=2)
            
            ttk.Label(field_frame, text=field['label'], style='Normal.TLabel', width=15).pack(side='left')
            
            if field['type'] == 'text':
                var = tk.StringVar()
                entry = ttk.Entry(field_frame, textvariable=var, style='Modern.TEntry')
                entry.pack