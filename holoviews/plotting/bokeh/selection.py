from ...selection import OverlaySelectionDisplay
from ...core.options import Store


class BokehOverlaySelectionDisplay(OverlaySelectionDisplay):
    """
    Overlay selection display subclass for use with bokeh backend
    """

    def _build_element_layer(self, element, layer_color, layer_alpha, **opts):
        backend_options = Store.options(backend='bokeh')
        style_options = backend_options[(type(element).name,)]['style']
        allowed = style_options.allowed_keywords

        merged_opts = {opt_name: layer_alpha for opt_name in allowed
                       if 'alpha' in opt_name}
        if layer_color is None:
            # Keep current color (including color from cycle)
            for color_prop in self.color_props:
                current_color = element.opts.get(group="style")[0].get(color_prop, None)
                if current_color:
                    merged_opts.update({color_prop: current_color})
        else:
            # set color
            merged_opts.update(self._get_color_kwarg(layer_color))

        for opt in ('cmap', 'colorbar'):
            if opt in opts and opt in allowed:
                merged_opts[opt] = opts[opt]

        return element.opts(backend='bokeh', clone=True, tools=['box_select'],
                            **merged_opts)

    def _style_region_element(self, region_element, unselected_color):
        from ..util import linear_gradient
        backend_options = Store.options(backend="bokeh")
        element_name = type(region_element).name
        style_options = backend_options[(element_name,)]['style']
        options = {}
        for opt_name in style_options.allowed_keywords:
            if 'alpha' in opt_name:
                options[opt_name] = 1.0

        if element_name != "Histogram":
            # Darken unselected color
            if unselected_color:
                region_color = linear_gradient(unselected_color, "#000000", 9)[3]
                options["color"] = region_color
            options["line_width"] = 1
            options["fill_alpha"] = 0
            options["selection_fill_alpha"] = 0
            options["nonselection_fill_alpha"] = 0
        else:
            # Darken unselected color slightly
            unselected_color = unselected_color or "#e6e9ec"
            region_color = linear_gradient(unselected_color, "#000000", 9)[1]
            options["fill_color"] = region_color
            options["color"] = region_color

        return region_element.opts(backend='bokeh', clone=True, **options)
