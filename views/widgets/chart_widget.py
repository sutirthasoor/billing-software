import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from config import Config

class ChartWidget(ttk.Frame):
    """Modern chart widget using matplotlib"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, style='Modern.TFrame')
        
        self.chart_type = kwargs.pop('chart_type', 'bar')  # 'bar', 'line', 'pie', 'area'
        self.title = kwargs.pop('title', '')
        self.width = kwargs.pop('width', 8)
        self.height = kwargs.pop('height', 4)
        self.show_legend = kwargs.pop('show_legend', True)
        self.show_grid = kwargs.pop('show_grid', True)
        
        self.setup_chart()
    
    def setup_chart(self):
        """Setup the chart figure and canvas"""
        # Create matplotlib figure
        self.fig = Figure(figsize=(self.width, self.height), facecolor=Config.THEME['primary'])
        self.ax = self.fig.add_subplot(111)
        
        # Set style
        plt.style.use('seaborn-v0_8-whitegrid')
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Initial empty chart
        self.ax.text(0.5, 0.5, 'No data available', 
                    horizontalalignment='center', verticalalignment='center',
                    transform=self.ax.transAxes, fontsize=12, color=Config.THEME['text_secondary'])
        self.ax.set_xticks([])
        self.ax.set_yticks([])
    
    def set_data(self, data, labels=None, **kwargs):
        """Set chart data"""
        self.ax.clear()
        
        if not data:
            self.ax.text(0.5, 0.5, 'No data available', 
                        horizontalalignment='center', verticalalignment='center',
                        transform=self.ax.transAxes, fontsize=12, color=Config.THEME['text_secondary'])
            self.ax.set_xticks([])
            self.ax.set_yticks([])
        else:
            self.create_chart(data, labels, **kwargs)
        
        self.canvas.draw()
    
    def create_chart(self, data, labels=None, **kwargs):
        """Create chart based on type"""
        colors = ['#007ACC', '#28A745', '#DC3545', '#FFC107', '#6F42C1', '#20C997', '#FD7E14']
        
        if self.chart_type == 'bar':
            self.create_bar_chart(data, labels, colors, **kwargs)
        elif self.chart_type == 'line':
            self.create_line_chart(data, labels, colors, **kwargs)
        elif self.chart_type == 'pie':
            self.create_pie_chart(data, labels, colors, **kwargs)
        elif self.chart_type == 'area':
            self.create_area_chart(data, labels, colors, **kwargs)
        
        # Set title
        if self.title:
            self.ax.set_title(self.title, fontsize=14, fontweight='bold', pad=20)
        
        # Configure grid
        if self.show_grid:
            self.ax.grid(True, alpha=0.3)
        else:
            self.ax.grid(False)
        
        # Configure spines
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
    
    def create_bar_chart(self, data, labels, colors, **kwargs):
        """Create bar chart"""
        x = np.arange(len(data))
        
        if isinstance(data[0], (list, tuple)):  # Multiple series
            bar_width = 0.8 / len(data)
            for i, series in enumerate(data):
                self.ax.bar(x + i * bar_width, series, bar_width, 
                           label=kwargs.get('series_labels', [f'Series {i+1}'])[i],
                           color=colors[i % len(colors)], alpha=0.8)
        else:  # Single series
            self.ax.bar(x, data, color=colors[0], alpha=0.8)
        
        if labels:
            self.ax.set_xticks(x + 0.4 if isinstance(data[0], (list, tuple)) else x)
            self.ax.set_xticklabels(labels, rotation=45, ha='right')
        
        if self.show_legend and isinstance(data[0], (list, tuple)):
            self.ax.legend()
    
    def create_line_chart(self, data, labels, colors, **kwargs):
        """Create line chart"""
        x = np.arange(len(data[0] if isinstance(data[0], (list, tuple)) else data))
        
        if isinstance(data[0], (list, tuple)):  # Multiple series
            for i, series in enumerate(data):
                self.ax.plot(x, series, marker='o', linewidth=2,
                           label=kwargs.get('series_labels', [f'Series {i+1}'])[i],
                           color=colors[i % len(colors)])
        else:  # Single series
            self.ax.plot(x, data, marker='o', linewidth=2, color=colors[0])
        
        if labels:
            self.ax.set_xticks(x)
            self.ax.set_xticklabels(labels, rotation=45, ha='right')
        
        if self.show_legend and isinstance(data[0], (list, tuple)):
            self.ax.legend()
    
    def create_pie_chart(self, data, labels, colors, **kwargs):
        """Create pie chart"""
        if not labels:
            labels = [f'Item {i+1}' for i in range(len(data))]
        
        wedges, texts, autotexts = self.ax.pie(data, labels=labels, colors=colors[:len(data)],
                                              autopct='%1.1f%%', startangle=90)
        
        # Style the labels
        for text in texts:
            text.set_fontsize(10)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
    
    def create_area_chart(self, data, labels, colors, **kwargs):
        """Create area chart"""
        x = np.arange(len(data[0] if isinstance(data[0], (list, tuple)) else data))
        
        if isinstance(data[0], (list, tuple)):  # Multiple series
            self.ax.stackplot(x, data, labels=kwargs.get('series_labels', [f'Series {i+1}' for i in range(len(data))]),
                             colors=colors[:len(data)], alpha=0.8)
        else:  # Single series
            self.ax.fill_between(x, data, alpha=0.8, color=colors[0])
        
        if labels:
            self.ax.set_xticks(x)
            self.ax.set_xticklabels(labels, rotation=45, ha='right')
        
        if self.show_legend and isinstance(data[0], (list, tuple)):
            self.ax.legend()
    
    def set_chart_type(self, chart_type):
        """Change chart type"""
        self.chart_type = chart_type
    
    def set_title(self, title):
        """Set chart title"""
        self.title = title
        self.ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        self.canvas.draw()
    
    def save_chart(self, filename):
        """Save chart to file"""
        self.fig.savefig(filename, dpi=300, bbox_inches='tight', facecolor=Config.THEME['primary'])
    
    def clear(self):
        """Clear chart"""
        self.ax.clear()
        self.ax.text(0.5, 0.5, 'No data available', 
                    horizontalalignment='center', verticalalignment='center',
                    transform=self.ax.transAxes, fontsize=12, color=Config.THEME['text_secondary'])
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()

class MiniChart(ChartWidget):
    """Mini chart for dashboard widgets"""
    
    def __init__(self, parent, **kwargs):
        kwargs['width'] = kwargs.get('width', 4)
        kwargs['height'] = kwargs.get('height', 2)
        kwargs['show_legend'] = kwargs.get('show_legend', False)
        super().__init__(parent, **kwargs)
        
        # Remove padding for mini charts
        self.fig.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.2)

class SparklineChart(ttk.Frame):
    """Sparkline chart for showing trends"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, style='Modern.TFrame')
        
        self.data = []
        self.width = kwargs.get('width', 100)
        self.height = kwargs.get('height', 30)
        self.color = kwargs.get('color', Config.THEME['accent'])
        
        self.setup_sparkline()
    
    def setup_sparkline(self):
        """Setup sparkline canvas"""
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, 
                               bg=Config.THEME['primary'], highlightthickness=0)
        self.canvas.pack()
    
    def set_data(self, data):
        """Set sparkline data"""
        self.data = data
        self.draw_sparkline()
    
    def draw_sparkline(self):
        """Draw sparkline on canvas"""
        self.canvas.delete('all')
        
        if not self.data or len(self.data) < 2:
            return
        
        # Normalize data to fit canvas
        min_val = min(self.data)
        max_val = max(self.data)
        data_range = max_val - min_val if max_val != min_val else 1
        
        points = []
        for i, value in enumerate(self.data):
            x = (i / (len(self.data) - 1)) * (self.width - 10) + 5
            y = self.height - 5 - ((value - min_val) / data_range) * (self.height - 10)
            points.extend([x, y])
        
        # Draw line
        if len(points) >= 4:
            self.canvas.create_line(points, fill=self.color, width=2, smooth=True)
        
        # Draw last point
        if points:
            self.canvas.create_oval(points[-2]-2, points[-1]-2, 
                                  points[-2]+2, points[-1]+2, 
                                  fill=self.color, outline=self.color)