from utils.modals.modal_content_suplier.base import ModalContentSuplier, get_inputs_for_params
from utils.reinforced_learning.model.enviroment.builder import get_gym_make_params
from dash import html, dcc
import dash_bootstrap_components as dbc
import inspect
from utils.reinforced_learning.model.network.builder import get_options

class EnviromentModalContentSuplier(ModalContentSuplier):
    @property
    def get_modal_content(self)->html.Div:
        gym_make_inputs = get_inputs_for_params(get_gym_make_params(), 'make-param-input', True)
        return html.Div(
            className='env-container',
            children=[
                html.Div( children = [
                    dcc.Input(id='env-name-input', 
                              type='text',
                              n_submit=1,
                              required = True,
                              persistence = True,
                              placeholder='Input gymnasium enviroment name',
                              className='text-input',
                              autoComplete = 'on',
                              style={
                                  'width':'90%'
                              }),
                    html.Button(children=['Search'],
                                id = 'env-search-btn')
                    ],
                    style=dict(display='flex', width='80%', margin='0 auto')
                ),
                html.H2('Enviroment specific parameters:', style={'margin':'0 auto'}),
                html.Div(
                    id = 'env-params-container',
                    children = [html.H3('Input enviroment name to see more', style={'margin':'0 auto'})],
                    style={'background-color':'rgba(0,0,0,0)', 
                           'color':'lightgray',
                           'width':'80%', 
                           'display':'flex',
                           'margin':'2% auto',
                           'height':'max-content',
                           'align-items':'center',
                           'flex-direction':'column'}
                    ),
                html.H2('Additional gym.make parameters:', style={'margin':'0 auto'}),
                html.Div(
                    id = 'env-gym-make-params-container',
                    children= gym_make_inputs,
                    style={'background-color':'rgba(0,0,0,0)', 
                           'width':'80%', 
                           'display':'flex',
                           'margin':'2% auto',
                           'align-items':'center',
                           'flex-direction':'column',
                           'height':'max-content'}
                )
            ])
    

class NetworkModalContentSuplier(ModalContentSuplier):
    @property
    def get_modal_content(self) -> html.Div:
        return html.Div( 
            className='network-content',
            children= [
                html.Div(
                    children=[
                        html.Div(
                            className='network-dropdown-container',
                            id = 'network-dropdown-container',
                            style = {
                                "transition": "height 0.5s ease-out",
                                "width": "98%",
                                "height": "0",
                                "margin": "0 auto",
                                "overflow-y": "hidden",
                                "overflow-x": "auto",
                                "white-space": "nowrap"
                            },
                            children=[]
                        ),
                        html.Div(
                            className='network-btn-layers-container',
                            children=[
                                html.Div(className='hline'),
                                html.Button(id = 'network-layers-btn',
                                            children=[
                                                html.I(className='fa-solid fa-chevron-down', style={'font-size':'3em'})
                                            ],
                                            style={
                                                'background-color':'rgba(0,0,0,0)',
                                                'border':'none',
                                                'color':'white'
                                            }
                                        ), 
                                html.Div(className='hline')
                            ]
                        )
                    ],
                    id='network-header',
                    style = {
                        "transition": "height 0.5s ease-out",
                        'position': 'absolute',
                        'left': 0,
                        'top': 0,
                        'width': '100%',
                        'height': '10%',
                    }
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[],
                            id='network-playground-content'
                        )
                    ],
                    id='network-playground')
            ]
        )
    


class HyperparametersModalContentSuplier(ModalContentSuplier):
    @property
    def get_modal_content(self) -> html.Div:
        options,_ = get_options()

        return html.Div(
            children= get_inputs_for_params(options, 'memory_and_episode-param', all_required = True), 
            style = {
                'color':'pink',
                'width':'60%',
                'margin':"auto",
                'diplay':'flex'
                }
            )    


    
#class NetworkExperimentalModalContentSuplier(ModalContentSuplier):
#    @property
#    def get_modal_content(self) -> html.Div:
#        return html.Div(
#            children=[
#                dcc.Store(id="network-dragndrop-store"),
#                html.Div(id='network-layrs-params-placeholder'),
#
#                # Main network drop area
#                html.Div(
#                    children=[
#                        html.Div(
#                            className='network-drop-container',
#                            style={
#                                'background-color': 'rgba(0,0,0,0)',
#                                'display': 'flex',
#                                'flex-direction': 'column',
#                                'justify-content': 'center',
#                                'align-items': 'center',
#                                'width': '100%',
#                                'height': '100%',
#                                'margin': 'auto',
#                                'z-index': '10',
#                                'overflow-y': 'auto'
#                            },
#                            children=[
#                                html.I(
#                                    className='network-drop fa-regular fa-square-plus',
#                                    id={'type': 'network-drop', 'index': 0},
#                                    style={
#                                        'color': 'white',
#                                        'margin': '0',
#                                        'font-size': '3em'
#                                    }
#                                ),
#                                html.Div(
#                                    className='network-drop-output',
#                                    id="network-drop-output",
#                                    style={
#                                        'width': '60%',
#                                    }
#                                ),
#                                html.I(
#                                    className='network-drop fa-regular fa-square-plus',
#                                    id={'type': 'network-drop', 'index': 1},
#                                    style={
#                                        'color': 'white',
#                                        'margin': '0',
#                                        'font-size': '3em'
#                                    }
#                                ),
#                            ]
#                        )
#                    ],
#                    style={
#                        'background-color': 'rgba(0,0,0,0)',
#                        'display': 'flex',
#                        'justify-content': 'center',
#                        'align-items': 'center',
#                        'height': '96%',
#                        'width': '71%',
#                        'position': 'relative',
#                        'overflow-y': 'auto',  # Ensure the container itself can scroll
#                    }
#                ),
#
#                # Draggable items container
#                html.Div(
#                    children=[
#                        html.Div(
#                            className='network-draggable',
#                            draggable='true',
#                            id={'type': 'network-draggable', 'index': i},
#                            children=html.Div(
#                                name, 
#                                style={'margin': '2% 3%', 'color': 'black'}
#                            )
#                        ) for i, name in enumerate(get_available_layers())
#                    ],
#                    style={
#                        'overflow-y': 'auto',
#                        'background-color': 'rgba(0,0,0,0)',
#                        'margin': 'auto',
#                        'height': '96%',
#                        'width': '25%',
#                    }
#                )
#            ],
#            style={
#                'display': 'flex',
#                'background-color': 'rgba(0,0,0,0)',
#                'width': '100%',
#                'height': '100%',
#                'align-items': 'center',
#                'justify-content': 'space-between',
#            }
#        )
#
#
#