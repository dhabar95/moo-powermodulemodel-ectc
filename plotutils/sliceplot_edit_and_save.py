"""
Slice Plot - Modified Ax
=============
Creates modified slice plot based from Ax

"""
import json
import plotly.graph_objects as go

def sliceplot_edit_and_save(json_sliceplot_files, parameter_name, objective_name, save_path):
    """
    
    
    Parameters
    ----------
    json_sliceplot_files : TYPE
        DESCRIPTION.
    parameter_name : TYPE
        DESCRIPTION.
    objective_name : TYPE
        DESCRIPTION.
    save_path : TYPE
        DESCRIPTION.
    
    Returns
    -------
    TYPE
        DESCRIPTION.
    
    """
    
    with open(json_sliceplot_files, 'r') as json_file:
        sliceplot_data = json.load(json_file)
        
    font_axis = 12
    
    x1 = parameter_name
    function_ni = objective_name
    function = f"{function_ni}"
    my_heading = f"<b>Slice Plot - {x1} vs. {function}</b>"
        
    sliceplot_data['layout']['title'] = dict(text=my_heading, font=dict(family="Times New Roman", size=18, color="#000000"))
    sliceplot_data['layout']['xaxis']['title']['text'] = x1
    sliceplot_data['layout']['xaxis']['title']['font'] = dict(family="Times New Roman", size=16, color="#000000")
    
    sliceplot_data['layout']['yaxis']['title']['text'] = function
    sliceplot_data['layout']['yaxis']['title']['font'] = dict(family="Times New Roman", size=16, color="#000000")
    
    
    sliceplot_data['layout']['xaxis']['tickfont']['size'] = font_axis
    sliceplot_data['layout']['yaxis']['tickfont']['size'] = font_axis
    sliceplot_data['layout']['xaxis']['tickfont']['family'] = "Times New Roman"
    sliceplot_data['layout']['xaxis']['tickfont']['color'] = "#000000"
    
    sliceplot_data['layout']['yaxis']['tickfont']['family'] = "Times New Roman"
    sliceplot_data['layout']['yaxis']['tickfont']['color'] = "#000000"
    
    
    #000000
    sliceplot_data['layout']['template']['layout']['font'] = dict(color = '#000000')
    
    sliceplot_data['data'][1]['line'] = dict(color = 'rgba(53,167,156,1)')
    sliceplot_data['data'][0]['line'] = dict(color = 'rgba(53,167,156,0)')
    sliceplot_data['data'][0]['fillcolor'] = "rgba(53,167,156,0.3)"
    
    data_plot = sliceplot_data['data']
    lay = sliceplot_data['layout']
    
    
    fig = {
        "data": data_plot,
        "layout": lay,
    }
    
    # Define the desired image resolution
    width_pixels = 600  # Adjust to your preferred width in pixels
    height_pixels = 400  # Adjust to your preferred height in pixels


# Save the figure as an image with the specified resolution

    return go.Figure(fig).write_image(save_path, width=width_pixels, height=height_pixels, scale = 4)
