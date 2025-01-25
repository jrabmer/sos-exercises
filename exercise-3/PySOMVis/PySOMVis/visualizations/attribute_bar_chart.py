import numpy as np
import holoviews as hv
import panel as pn
from bokeh.palettes import Viridis256
from controls.controllers import AttributeController
from visualizations.iVisualization import VisualizationInterface

BAR_CHART_SCALE = 0.05  # Scale for the bar chart height

class AttributeBarChart(VisualizationInterface):
    
    component_index = {"comp_0": 0}

    def __init__(self, main):
        self._main = main

        if self._main._component_names is None:
            component_names = list(range(1, self._main._dim + 1))
        else:
            component_names = self._main._component_names

        self.component_index = {name: idx for idx, name in enumerate(component_names)}

        self._controls = AttributeController(
            object_options=component_names,
            calculate=self._calculate,
            name='Attribute Bar Chart Visualization'
        )

    def _activate_controllers(self, ):
        self._main._controls.append(pn.Column(self._controls))
        self._calculate()
    
    def _deactivate_controllers(self, ):
        pass

    def _calculate(self, selected_attribute=None):
        if selected_attribute is None:
            return
        
        # Normalize weights vector
        normalized_weights = self._main._weights / np.linalg.norm(self._main._weights, axis=1, keepdims=True)

        # Get only currently selected attribute
        attribute_index = self.component_index.get(str(selected_attribute), 0)
        elements = normalized_weights[:, attribute_index]

        # Plot bar charts at unit positions
        pos_x, width, tops, pos_y = np.array([]), np.array([]), np.array([]), np.array([])
        
        for p in range(len(normalized_weights)):
            nx, ny = self._main._convert_to_xy(neuron=p)
            a, b, c, d = self._get_bar_chart(nx, ny, elements[p])
            pos_x       = np.append(pos_x,  a, axis=0)
            width       = np.append(width,  b, axis=0)
            tops        = np.append(tops,   c, axis=0)
            pos_y       = np.append(pos_y,  d, axis=0)

        figure = hv.render(self._main._Image, backend='bokeh')
        figure.vbar(x=pos_x, width=width, top=tops, bottom=pos_y)
        
        self._main._pdmap[0] = figure

    def _get_bar_chart(self, x, y, normalized_weight):
        return np.array([x]), np.array([0.05]), np.array([y + (normalized_weight * BAR_CHART_SCALE)]), np.array([y])