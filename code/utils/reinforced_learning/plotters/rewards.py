import plotly.express as px
from  plotly.graph_objects import Figure
import numpy as np

class RewardPlotUpdater():
    def __init__(self) -> None:
        self.step = [0]
        self.reward = [0]

    def create(self):
        fig = px.scatter(x = self.step,  y = self.reward)
        fig.update_layout(
            xaxis=dict(
                autorange= True,
                range=[1,10000],
                rangeslider= dict(
                    autorange=True, 
                    visible=True,
                    range=[1,10000]), 
                type= "linear",
                title = dict(
                    text = "Step",
                    standoff = 20)),
            yaxis = dict(
                anchor="x",
                showline=True,
                side="left",
                autorange=True,
                mirror=True,
                type='linear',
                title = dict(
                    text = "Reward",
                    standoff = 20)
            )
        )
        fig.update_traces(
            hoverinfo="name+x+text",
            line={"width": 0.5},
            marker={"size": 8},
            mode="lines+markers",
            showlegend=False
        )
        fig.update_layout(
            dragmode="zoom",
            hovermode="x",
            legend=dict(traceorder="reversed"),
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(
                t=10,
                b=40
            )
        )
        return fig


    def update_values(self, step: int | list | np.ndarray, reward: float | int | list | np.ndarray) -> Figure:
        if type(step) is int and (type(reward) is float or type(reward) is int):
            self.step.append(step),
            self.reward.append(reward)
        else:
            self.step = step
            self.reward = reward
        


        