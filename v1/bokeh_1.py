tooltips = [('gender', '@gender'),
            ('pop', '@pop'),
            ('ID', '@index')]


hover = bokeh.models.HoverTool(tooltips=tooltips)

p = bokeh.plotting.figure(background_fill='#DFDFE5', plot_width=650, 
                          plot_height=450)
p.xgrid.grid_line_color = 'white'
p.ygrid.grid_line_color = 'white'
p.xaxis.axis_label ='PC 1'
p.yaxis.axis_label ='PC 2'

# Add the hover tool
p.add_tools(hover)

# Define colors in a dictionary to access them with
# the key from the pandas groupby funciton.
#keys = df_snp_pca.super_pop.dropna().unique()
#color_dict = {k: bebi103.rgb_frac_to_hex(sns.color_palette()[i]) 
#                      for i, k in enumerate(sorted(keys))}

p.legend.background_fill_alpha = 0.25
p.legend.background_fill_color = 'blanchedalmond'
p.legend.orientation = 'bottom_right'
bokeh.io.show(p)