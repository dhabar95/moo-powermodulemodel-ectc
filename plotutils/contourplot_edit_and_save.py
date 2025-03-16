"""
Contour Plot - Modified Ax
=============
Creates modified contour plot based from Ax

"""
import json
import plotly.graph_objects as go

def contourplot_edit_and_save(exampledata_filepath, x1, x2, title, save_location):
    """
    
    
    Parameters
    ----------
    exampledata_filepath : TYPE
        DESCRIPTION.
    x1 : TYPE
        DESCRIPTION.
    x2 : TYPE
        DESCRIPTION.
    title : TYPE
        DESCRIPTION.
    save_location : TYPE
        DESCRIPTION.
    
    Returns
    -------
    TYPE
        DESCRIPTION.
    
    """
    
    with open(exampledata_filepath, 'r') as file:
        data = json.load(file)
        
    font_axis = 12
    line = dict(width=2)
    
    marker_1 = {'color': 'black', 'opacity': 1, 'symbol': 34, 'line': line}
    marker_2 = {'color': 'black', 'opacity': 1, 'symbol': 34, 'line': line}
    
    color_plot_data_new = ['rgb(255,255,217)','rgb(237,248,177)','rgb(199,233,180)','rgb(127,205,187)','rgb(65,182,196)','rgb(29,145,192)','rgb(34,94,168)','rgb(37,52,148)','rgb(8,29,88)']
    color_plot_data_new_2 = ['rgb(255,247,243)','rgb(253,224,221)','rgb(252,197,192)','rgb(250,159,181)','rgb(247,104,161)','rgb(221,52,151)','rgb(174,1,126)','rgb(122,1,119)']
    
    margin_new = {'b': 80, 'l': 45, 'pad': 0, 'r': 45, 't': 45}
    
    data['layout']['title'] = dict(text=title, font=dict(family="Times New Roman", size=18, color="#000000"))
    
    data['layout']['xaxis']['title']['text'] = x1
    data['layout']['xaxis']['title']['font'] = dict(family="Times New Roman", size=16, color="#000000")
    
    
    data['layout']['yaxis']['title']['text'] = x2
    data['layout']['yaxis']['title']['font'] = dict(family="Times New Roman", size=16, color="#000000")
    
    
    data['layout']['xaxis2']['title']['text'] = x1
    data['layout']['xaxis2']['title']['font'] = dict(family="Times New Roman", size=16, color="#000000")
    
    data['layout']['xaxis']['tickfont']['size'] = font_axis
    data['layout']['xaxis']['tickfont']['family'] = "Times New Roman"
    data['layout']['xaxis']['tickfont']['color'] = "#000000"
    
    
    
    data['layout']['yaxis']['tickfont']['size'] = font_axis
    data['layout']['yaxis']['tickfont']['family'] = "Times New Roman"
    data['layout']['yaxis']['tickfont']['color'] = "#000000"
    
    
    data['layout']['xaxis2']['tickfont']['size'] = font_axis
    data['layout']['xaxis2']['tickfont']['family'] = "Times New Roman"
    data['layout']['xaxis2']['tickfont']['color'] = "#000000"
    
    
    data['data'][2]['marker'] = marker_1
    data['data'][3]['marker'] = marker_2
    data['layout']['margin'] = margin_new
    
    
    for i in range(9):
        data['data'][0]['colorscale'][i][1] = color_plot_data_new[i]
        
    for i in range(8):
        data['data'][1]['colorscale'][i][1] = color_plot_data_new_2[i]
    
    data_plot = data['data']
    lay = data['layout']
    
    
    fig = {
        "data": data_plot,
        "layout": lay,
    }
    
    # Define the desired image resolution
    width_pixels = 800  # Adjust to your preferred width in pixels
    height_pixels = 400  # Adjust to your preferred height in pixels

    return go.Figure(fig).write_image(save_location, width=width_pixels, height=height_pixels, scale = 4)

