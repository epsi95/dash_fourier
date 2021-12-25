import json
import numpy as np
# import plotly.express as px
from scipy.fft import fft, ifft
from dash_canvas.utils import array_to_data_url, parse_jsonstring
import plotly.graph_objs as go


def get_line_cords(json_data, dimension=(500, 500)):
    lines = []
    for data in json_data['objects'][1:]:
        pts = np.where(parse_jsonstring(json.dumps({'objects': [data]}), dimension))
        complex_pts = pts[1] + 1j * pts[0]
        lines.append({'pts': complex_pts, 'color': data['stroke']})
    return lines


# def plot_complex_pts(complex_pts, dimension=(500, 500)):
#     color = complex_pts['color']
#     complex_pts = complex_pts['pts']
#     x = complex_pts.real
#     y = dimension[1] - complex_pts.imag
#     fig = px.scatter(x=x, y=y)
#     fig.update_traces(marker=dict(color=color))
#     fig.update_layout(
#         autosize=False,
#         width=dimension[0],
#         height=dimension[1]
#     )
#     fig.show()


def get_frames(ttl, dimension=(500, 500)):
    max_length = max(map(lambda x: len(x['pts']), ttl))
    step = max_length // 10
    for each_seq in ttl:
        each_seq['fft'] = fft(each_seq['pts'])

    frames = []
    for i in range(0, max_length + step, step):
        tmp = []
        for each_seq in ttl:
            color = each_seq['color']
            generated_sq = ifft(np.append(each_seq['fft'][:i], np.zeros(max(len(each_seq['fft']) - i, 0))))

            #         color = each_seq['color']
            #         x = generated_sq.real
            #         y = dimension[1]-(generated_sq.imag)

            # tmp.append(go.Scatter(x=x, y=y, mode='markers', marker=dict(color=color)))
            tmp.append(generated_sq)
        tmp2 = np.concatenate(tmp)
        # frames.append(go.Frame(data=tmp, layout=go.Layout(title_text=f"First {i} samples")))
        frames.append(go.Frame(data=[go.Scatter(x=tmp2.real,
                                                y=dimension[1] - tmp2.imag,
                                                mode='markers')], layout=go.Layout(title_text=f"{i} samples")))
    return frames


def get_figure(frames, dimension):
    print(frames)
    fig = go.Figure(
        data=[go.Scatter(x=[250], y=[250])],
        layout=go.Layout(
            title="Start Fourier Series Aggregation",
            autosize=False,
            width=dimension[0]+10,
            height=dimension[1]+10,
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                              method="animate",
                              args=[None])])]
        ),
        frames=frames
    )
    return fig
