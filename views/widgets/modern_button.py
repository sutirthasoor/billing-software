import tkinter as tk
from tkinter import ttk
from config import Config

class ModernButton(ttk.Button):
    """Modern styled button with enhanced functionality"""
    
    def __init__(self, parent, **kwargs):
        # Extract custom parameters
        self.style_name = kwargs.pop('style_name', 'Modern.TButton')
        self.icon = kwargs.pop('icon', '')
        self.tooltip = kwargs.pop('tooltip', '')
        self.loading = kwargs.pop('loading', False)
        
        # Initialize parent
        super().__init__(parent, style=self.style_name, **kwargs)
        
        # Setup button
        self.setup_button()
        
        # Add tooltip if provided
        if self.tooltip:
            self.add_tooltip()
    
    def setup_button(self):
        """Setup button appearance and behavior"""
        # Bind hover effects
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<ButtonPress-1>', self.on_press)
        self.bind('<ButtonRelease-1>', self.on_release)
        
        # Set initial state
        self.is_pressed = False
        self.is_hovered = False
        
        # If loading state is requested
        if self.loading:
            self.show_loading()
    
    def on_enter(self, event):
        """Handle mouse enter"""
        self.is_hovered = True
        self.configure(style=f'{self.style_name}.Hover')
    
    def on_leave(self, event):
        """Handle mouse leave"""
        self.is_hovered = False
        if not self.is_pressed:
            self.configure(style=self.style_name)
    
    def on_press(self, event):
        """Handle mouse press"""
        self.is_pressed = True
        self.configure(style=f'{self.style_name}.Pressed')
    
    def on_release(self, event):
        """Handle mouse release"""
        self.is_pressed = False
        if self.is_hovered:
            self.configure(style=f'{self.style_name}.Hover')
        else:
            self.configure(style=self.style_name)
    
    def show_loading(self):
        """Show loading state"""
        original_text = self['text']
        self.loading_text = "⏳ Loading..."
        self.configure(text=self.loading_text, state='disabled')
        self.original_text = original_text
    
    def hide_loading(self):
        """Hide loading state"""
        if hasattr(self, 'original_text'):
            self.configure(text=self.original_text, state='normal')
    
    def disable(self):
        """Disable the button"""
        self.configure(state='disabled', style=f'{self.style_name}.Disabled')
    
    def enable(self):
        """Enable the button"""
        self.configure(state='normal', style=self.style_name)
    
    def set_success(self, message="✓ Done"):
        """Set success state"""
        original_text = self['text']
        self.configure(text=message, style='Success.TButton')
        self.after(2000, lambda: self.configure(text=original_text, style=self.style_name))
    
    def set_error(self, message="✗ Error"):
        """Set error state"""
        original_text = self['text']
        self.configure(text=message, style='Danger.TButton')
        self.after(2000, lambda: self.configure(text=original_text, style=self.style_name))
    
    def add_tooltip(self):
        """Add tooltip to button"""
        self.tooltip_window = None
        self.bind('<Enter>', self.show_tooltip)
        self.bind('<Leave>', self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        """Show tooltip"""
        if self.tooltip and not self.tooltip_window:
            x = self.winfo_rootx() + self.winfo_width() + 5
            y = self.winfo_rooty() + self.winfo_height() // 2
            
            self.tooltip_window = tk.Toplevel(self)
            self.tooltip_window.wm_overrideredirect(True)
            self.tooltip_window.wm_geometry(f"+{x}+{y}")
            
            label = ttk.Label(self.tooltip_window, text=self.tooltip, 
                            style='Tooltip.TLabel', background='yellow',
                            relief='solid', borderwidth=1, padding=(5, 2))
            label.pack()
    
    def hide_tooltip(self, event=None):
        """Hide tooltip"""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class IconButton(ModernButton):
    """Button with icon support"""
    
    def __init__(self, parent, **kwargs):
        self.icon = kwargs.pop('icon', '')
        self.icon_position = kwargs.pop('icon_position', 'left')  # 'left', 'right', 'top', 'bottom'
        self.icon_size = kwargs.pop('icon_size', 16)
        
        super().__init__(parent, **kwargs)
        
        if self.icon:
            self.setup_icon()
    
    def setup_icon(self):
        """Setup icon for button"""
        # In a real implementation, you would use PIL to create icons
        # For now, we'll use emoji or unicode characters as icons
        current_text = self['text']
        if self.icon_position == 'left':
            new_text = f"{self.icon} {current_text}"
        elif self.icon_position == 'right':
            new_text = f"{current_text} {self.icon}"
        else:
            new_text = f"{self.icon}\n{current_text}"
        
        self.configure(text=new_text)

class ToggleButton(ModernButton):
    """Toggle button with on/off states"""
    
    def __init__(self, parent, **kwargs):
        self.state = kwargs.pop('initial_state', False)
        self.on_text = kwargs.pop('on_text', 'ON')
        self.off_text = kwargs.pop('off_text', 'OFF')
        self.on_style = kwargs.pop('on_style', 'Success.TButton')
        self.off_style = kwargs.pop('off_style', 'Secondary.TButton')
        
        super().__init__(parent, **kwargs)
        
        self.update_appearance()
        
        # Override click behavior
        self.configure(command=self.toggle)
    
    def toggle(self):
        """Toggle button state"""
        self.state = not self.state
        self.update_appearance()
        
        # Call original command if exists
        if hasattr(self, 'original_command'):
            self.original_command()
    
    def update_appearance(self):
        """Update button appearance based on state"""
        if self.state:
            self.configure(text=self.on_text, style=self.on_style)
        else:
            self.configure(text=self.off_text, style=self.off_style)
    
    def set_state(self, state):
        """Set button state"""
        self.state = state
        self.update_appearance()
    
    def get_state(self):
        """Get button state"""
        return self.state