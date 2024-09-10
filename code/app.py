import os
from pathlib import Path
import shutil
from dash import Dash, html, dcc, Input, Output, State, Patch, ALL, ctx, MATCH
import dash_bootstrap_components as dbc
from flask import Flask, send_from_directory

from utils.exit_handler.exit_handler import ExitHandler, delete_files_in_directory
from utils.logger.log import Logger
from utils.modals.modal_content_suplier.base import get_inputs_for_params
from utils.modals.buttons_with_modals_suplier import SetupBtnWithModalSuplier
from utils.reinforced_learning.model.enviroment.builder import EnvBuilder, get_gym_make_params
from utils.reinforced_learning.model.network.builder import NetworkBuilder, get_params_for_layer_name, get_options
from utils.reinforced_learning.plotters import rewards
from utils.utils import InputParser
from utils.reinforced_learning.model.model import Model

import atexit

SETUP_OPTIONS = ["Enviroment", "Network","Hyperparameters", "Run"]
MOVIES_DIRECTORY = 'episodes_recaps'
PLAYER_DIRECTORY = 'static'
ENV_NAME_SET = False
ENV_SET = False
NET_SET = False

LAYERS_CTR = 0

rewards_plt = rewards.RewardPlotUpdater()
env_builder =  EnvBuilder()
network_builder = NetworkBuilder()

server = Flask(__name__)
app = Dash(__name__, external_stylesheets=[dbc.icons.FONT_AWESOME])

########################################
# main page layout
app.layout = [
    html.Div(className='app-header', 
             children=html.Div('RML Center', className='app-header--title')),
    html.Div(className='row', children= [
        html.Div(className='left-side',  
                 children=[
                     html.H2("Setup:", style={'margin-left':"5%", "margin-top": "4%", "margin-bottom": "0%"}),
                     html.Div(className='left-side--setup-options',
                              children=[
                                  SetupBtnWithModalSuplier().get_content_for_option(option)
                                  for option in SETUP_OPTIONS
                              ]),
                     html.H2("Log:", style={'margin-left':"5%", "margin-top": "0px", "margin-bottom": "5%"}),
                     html.Div(id = 'log')
                 ]),
        html.Div(className='right-side', 
                 children=[
                    html.Div(
                        children = [
                            html.Div(
                                id = "movie-title-and-dropdown-container",
                                children = [
                                    html.H2('Last episode review:',style={'margin-left':"2%", "margin-top":"1%", "margin-bottom": "0px"}),
                                    html.Div(
                                            dcc.Dropdown(
                                                id = "movie-dropwdown",
                                                options=[],
                                                placeholder = "Select episode to view",
                                                persistence=True,
                                                persistence_type= "session",
                                                persisted_props=['value']
                                            ),
                                            style={
                                                "width":"100%",
                                                "margin-left":"2%",
                                                #"align-content":'center'
                                            }
                                        ),
                                ]
                            ),
                            html.Div(id = 'rec-of-last-episode-container',
                                    children= [
                                        html.Video(src=None, controls=True, id='rec-of-last-episode')
                                    ]
                            )
                        ],
                        style={
                            'width':'100%',
                            'height':'40%',
                            'display':'flex',
                            'flex-direction':'row'
                        }
                    ),
                    html.H2('Rewards plot:',style={'margin-left':"2%", "margin-top":"0px", "margin-bottom": "10px"}),
                    dcc.Graph(id='graph', figure=rewards_plt.create())
                 ]),
        dcc.Interval(
            id = 'interval-component',
            interval=1000,
            n_intervals=0
        ),
        dcc.Interval(
            id = 'interval-component-2',
            interval=1000,
            n_intervals=0
        )
    ],
    style= {"display": "flex" , "width":'100%'})
]

#################################################
##interactive functions setup

@server.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.join(os.getcwd(), 'static'), path)

@app.callback(
        Output("network-dropdown-container", "children"),
        Input("setup-network", "n_clicks"),
        prevent_initial_call = True
)
def load_layers(n_clicks):
    if n_clicks < 2: 
        return [
            html.Div(
                    children= [html.H3(group_name, className='netwrok-layer-group-title')] + 
                    [html.Div(name, id = {'type':'layer-button','layer': i, 'index':j},className="network-layer") for j,name in enumerate(layers)],
                    style={
                        'color':'white',
                        'background-color':'none',
                        'border-left':'solid 2px white',
                        #'border-radius':'10px',
                        'margin':'0',
                        'margin-right':'2%',
                        'height':'100%',
                        'width':'max-content',
                        'min-width':'300px',
                        'max-width':'800px',
                        'display':'inline-block',   
                        'overflow-y':'scroll',
                        'overflow-x':'hidden',
                        'flex-direction':'column'
                        }
                ) for i,(group_name, layers) in enumerate(network_builder.get_layers())
            ]
    return Patch()

@app.callback(
        Output('network-playground-content','children'),
        Input({'type':'layer-button','layer':ALL, 'index':ALL}, 'n_clicks'),
        prevent_initial_call = True
)
def updade_network_schema(layers):
    global LAYERS_CTR, network_builder
    layer_group_id = ctx.triggered_id['layer']
    layer_id = ctx.triggered_id['index']
    layer_name = network_builder.get_layers()[layer_group_id][1][layer_id]
    
    i = 0
    layers_count = 0
    while i < layer_group_id:
        layers_count += len(network_builder.get_layers()[i][1])
        i+=1

    layer_div_id = layers_count + layer_id 
    if layers[layer_div_id] is None:
        return Patch()

    layer_popover =  html.Div(
            children=[
                html.Div(
                    children = [
                        html.I(className="fa-solid fa-chevron-up", id = {'type':'playground-layer-up', 'index': LAYERS_CTR}),
                        html.I(className="fa-solid fa-chevron-down", id = {'type':'playground-layer-down', 'index': LAYERS_CTR})
                    ],
                    style={
                        'display' : "flex", 
                        'flex-direction':'column',
                        'margin':'10%'
                        }
                ),
                html.Div(
                    html.I(className="fa-solid fa-xmark", 
                           style={'display':'flex', 'margin':'auto'},
                           id = {'type':'playground-layer-delete', 'index': LAYERS_CTR}),
                    style={
                        'display' : "flex", 
                        'flex-direction':'column',
                        'margin':'4px'
                        }
                )
            ],
            id = {'type':'playground-layer-popover', 'index': LAYERS_CTR},
            className='playground-layer-popover'
    )
    new_layer = html.Div(
        id = {'type':'playground-layer', 'index': LAYERS_CTR, 'group': layer_group_id, 'id': layer_id},
        className='network-playground-layer',
        children=[
            html.Div(layer_name, className='layer-name'),
            html.I(className="layer-show-params fa-solid fa-circle-chevron-down",
                   id = {'type':'playground-layer-more', 'index': LAYERS_CTR}
            ),
            html.Div(id = {'type':'playground-layer-params', 'index': LAYERS_CTR},
                     children=get_inputs_for_params(get_params_for_layer_name(layer_name), f'network-layer-param', black_color=True, group_counter = LAYERS_CTR),
                     className="layer-params-container",
                     hidden=True
            ),
            layer_popover
        ]
    )

    current_layers = Patch()
    current_layers.append(new_layer)

    LAYERS_CTR +=1
    return current_layers

@app.callback(
        Output('network-playground-content','children', allow_duplicate=True),
        Input({'type':'playground-layer-up', 'index': ALL}, 'n_clicks'),
        Input({'type':'playground-layer-down', 'index': ALL}, 'n_clicks'),
        Input({'type':'playground-layer-delete', 'index': ALL}, 'n_clicks'),
        State('network-playground-content','children'),
        prevent_initial_call = True
)
def move_layer(up, down, delete, layers):
    if type(layers) is not list:
        return Patch()
    
    layer_id = ctx.triggered_id['index']

    direction = ctx.triggered_id['type'][17:]
    layer_place = 0
    for i,layer in enumerate(layers):
        if layer['props']['id']['index'] == layer_id:
            layer_place = i
            break

    if direction == 'up' and layer_place>0:
        layer = layers[layer_place]
        layers[layer_place] = layers[layer_place-1]
        layers[layer_place-1] = layer
        return layers
    
    if direction == 'down' and layer_place<len(layers)-1:
        layer = layers[layer_place]
        layers[layer_place] = layers[layer_place+1]
        layers[layer_place+1] = layer
        return layers
    
    if direction == 'delete':
        del layers[layer_place]
        return layers
    
    return Patch()

@app.callback(
        [Output('network-dropdown-container','style'), 
         Output('network-layers-btn', 'children'), 
         Output('network-header', 'style')],
        Input('network-layers-btn', 'n_clicks'),
        [State('network-dropdown-container','style'),
         State('network-header', 'style')],
        prevent_initial_call = True
)
def toogle_layers(n_clicks, style1, style2):
    arrow = "fa-solid fa-chevron-down"
    if n_clicks:
        if style1 and style1.get('height') == '0':
            style1.update({'height': '90%'})
            style2.update({'height': '100%'})
            arrow = 'fa-solid fa-chevron-up'
        else:
            style1.update({'height': '0'})
            style2.update({'height': '5%'})
            arrow = 'fa-solid fa-chevron-down'
    return [style1, html.I(className=arrow, style={'font-size':'3em'}), style2]

@app.callback(
    [Output({'type':'playground-layer-more', 'index': MATCH}, 'className'),
     Output({'type':'playground-layer-params', 'index': MATCH}, 'hidden')],
    Input({'type':'playground-layer-more', 'index': MATCH}, 'n_clicks'),
    State({'type':'playground-layer-more', 'index': MATCH}, 'className'),
    prevent_initial_call = True
)
def toggle_rotation(n_clicks, class_name):
    if n_clicks and ctx.triggered_id is not None and ctx.triggered_id['type'] == "playground-layer-more":
        if 'rotated' in class_name:
            return [class_name.replace(' rotated', ''), True]
        else:
            return [class_name + ' rotated', False]
    return [class_name, True]


def toggle_modal(open_clicks, close_clicks, style):
    if open_clicks or close_clicks:
        if style and style.get('display') == 'block':
            return {'display': 'none'}
        else:
            return {'display': 'block'}
    return style

app.callback(
    Output("modal-enviroment", "style", allow_duplicate=True),
    [Input("setup-enviroment", "n_clicks"), Input('modal-enviroment-close-btn', 'n_clicks')],
    [State("modal-enviroment", "style")],
    prevent_initial_call = True
)(toggle_modal)

app.callback(
    Output("modal-network", "style", allow_duplicate=True),
    [Input("setup-network", "n_clicks"), Input('modal-network-close-btn', 'n_clicks')],
    [State("modal-network", "style")],
    prevent_initial_call = True
)(toggle_modal)

app.callback(
    Output("modal-enviroment", "style", allow_duplicate=True),
    [Input("setup-enviroment", "n_clicks"), Input("modal-enviroment-submit-btn", 'n_clicks')],
    [State("modal-enviroment", "style")],
    prevent_initial_call = True
)(toggle_modal)

app.callback(
    Output("modal-network", "style", allow_duplicate=True),
    [Input("setup-network", "n_clicks"), Input("modal-network-submit-btn", 'n_clicks')],
    [State("modal-network", "style")],
    prevent_initial_call = True
)(toggle_modal)

app.callback(
    Output("modal-hyperparameters", "style", allow_duplicate=True),
    [Input("setup-hyperparameters", "n_clicks"), Input("modal-hyperparameters-submit-btn", 'n_clicks')],
    [State("modal-hyperparameters", "style")],
    prevent_initial_call = True
)(toggle_modal)

app.callback(
    Output("modal-hyperparameters", "style", allow_duplicate=True),
    [Input("setup-hyperparameters", "n_clicks"), Input("modal-hyperparameters-close-btn", 'n_clicks')],
    [State("modal-hyperparameters", "style")],
    prevent_initial_call = True
)(toggle_modal)


@app.callback(
    Output('log', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_log(n_intervals):
    return Logger().read_from_log()

@app.callback(
    Output("graph", "figure"), 
    Input('interval-component', 'n_intervals'))
def update_figure(n_intervals):
    patched_fig = Patch()
    patched_fig["data"][0]["y"] = rewards_plt.reward
    patched_fig["data"][0]["x"] = rewards_plt.step
    return patched_fig

@app.callback(
    Output("movie-dropwdown", "options"), 
    Input('interval-component', 'n_intervals'),
    State("movie-dropwdown", "options")
)
def update_dropdown(n, options):
    global MOVIES_DIRECTORY
    if len(options) != os.listdir(MOVIES_DIRECTORY):
        return [f.name for f in sorted(Path(MOVIES_DIRECTORY).iterdir(), key=os.path.getmtime)]
    return Patch()

@app.callback(
        Output('rec-of-last-episode','src'),
        Input("movie-dropwdown", "value"),
        prevent_initial_call = True
)
def select_recap(value):
    global MOVIES_DIRECTORY, PLAYER_DIRECTORY
    filename = None
    try:
        assert((type(value) is str) and (value[-4:] == ".mp4")), "Incorrect recap filename"
        src_filename = os.path.join(MOVIES_DIRECTORY, value)
        dest_filename = os.path.join(PLAYER_DIRECTORY, value)
        delete_files_in_directory(PLAYER_DIRECTORY)
        shutil.copy(src_filename, dest_filename)
        filename = dest_filename
    except Exception as e:
        Logger().print_to_log(e)
    return filename

@app.callback(
        [Output('env-params-container','children'), 
         Output({'type':'make-param-input', 'index':ALL}, 'disabled'),
         Output({'type':'make-param-input', 'index':ALL}, 'style') ],
        [Input('env-search-btn','n_clicks'), Input('env-name-input', 'n_submit')],
        [State('env-name-input', 'value'), State({'type':'make-param-input', 'index':ALL}, 'value')],
        prevent_initial_call = True
)
def read_env_name_and_find_params(search_clicked, env_name_entered, env_name, make_params):
    global ENV_NAME_SET
    try:
        env_spec = env_builder.set_env_name(env_name)
        env_params_ids = env_builder.get_env_params()
        ENV_NAME_SET = True
    except Exception as e:
        ENV_NAME_SET = False
        return  html.H3("This env doesn't exist.", style={'color':'red'}), [True] * len(make_params), [{"background-color":"lightgray", 'width':'48%'}]  * len(make_params)

    params_input_divs = get_inputs_for_params(env_params_ids, 'env-param-input')

    return params_input_divs, [False] * len(make_params), [{"background-color":"white", 'width':'48%'}]  * len(make_params)

@app.callback( 
        output = dict(
            icon = Output('setup-enviroment-icon', 'className'), 
            icon_style = Output('setup-enviroment-icon', 'style')
            ),
        inputs = dict(
            submit_button = Input("modal-enviroment-submit-btn", "n_clicks")
        ),
        state = dict(
            env_params = State({'type':'env-param-input', 'index':ALL}, 'value'),
            gym_make_params = State({'type':'make-param-input', 'index':ALL}, 'value')
        ),
        prevent_initial_call = True
)
def run_env_setup(submit_button, env_params, gym_make_params):
    global ENV_NAME_SET, ENV_SET
    try:
        assert (ENV_NAME_SET == True), 'Set enviroment name before submit'
        env_params_dict = dict(env_builder.get_env_params())
        gym_params_dict = dict(get_gym_make_params())

        env_params_defs = [v.annotation for v in env_params_dict.values()]
        gym_params_defs = [type(eval(v.annotation)) for v in gym_params_dict.values()]

        env_params_parsed = InputParser().parse(env_params, env_params_defs)
        gym_make_params_parsed = InputParser().parse(gym_make_params, gym_params_defs)
        #Logger().print_to_log('Loaded following arguments into "{}" enviroment'.format(env_builder.env_name))
        #Logger().print_to_log(dict(zip(env_params_dict.keys(),env_params_parsed)))
        #Logger().print_to_log(dict(zip(gym_params_dict.keys(),gym_make_params_parsed)))

        env_builder.build(dict(zip(env_params_dict.keys(),env_params_parsed)),dict(zip(gym_params_dict.keys(),gym_make_params_parsed)))
        ENV_SET = True
        Logger().print_to_log('The environment was successfully loaded')
        Logger().print_to_log('Observation space:\n{}'.format(env_builder.env.observation_space))
        Logger().print_to_log('Action space:\n{}'.format(env_builder.env.action_space))
        return dict(icon = "fa-solid fa-circle-check", 
                icon_style = {"color":"green", 'font-size':'1.5em'})
    except Exception as e:
        Logger().print_to_log("An error occured when building enviroment. Check parameters and try again")
        ENV_SET = False
        Logger().print_to_log(str(e))
        return dict(icon = "fa-solid fa-circle-xmark", 
                icon_style = {"color":"red", 'font-size':'1.5em'})
    
    
@app.callback( 
        output = dict(
            icon = Output('setup-network-icon', 'className'), 
            icon_style = Output('setup-network-icon', 'style')
            ),
        inputs = dict(
            submit_button = Input("modal-network-submit-btn", "n_clicks")
        ),
        state = dict(
            net_params = State({'type': 'network-layer-param','group': ALL,'index':ALL}, 'value'),
            net_required = State({'type': 'network-layer-param','group': ALL,'index':ALL}, 'required'),
            net_ids = State({'type': 'network-layer-param','group': ALL,'index':ALL}, 'id'),
            net_layers = State('network-playground-content','children')
        ),
        prevent_initial_call = True
)
def run_network_setup(submit_button, net_params, net_required, net_ids, net_layers):
    global NET_SET, network_builder
    try:
        for param, is_required, id in zip(net_params, net_required, net_ids):
            if is_required and (param is None or param == ""):
                raise ValueError(f"Required value (layer: {id['group']}, param: {id['index']}) cannot be empty")
            
        available_layers = network_builder.get_layers()    
        layers = [available_layers[layer['props']['id']['group']][1][layer['props']['id']['id']] for layer in net_layers]

        layers_params_defs = [(layer_name,[v.annotation for v in get_params_for_layer_name(layer_name).values()]) for layer_name in layers]
        #Logger().print_to_log(layers_params_defs)

        layers_params_parsed = []
        parameter_index = 0
        for i,(layer_name, parameter_defs) in enumerate(layers_params_defs):
            parameter_count = len(parameter_defs)
            parsed_parameters = InputParser().parse(net_params[parameter_index:parameter_index+parameter_count], parameter_defs)
            parameter_index += parameter_count
            layers_params_parsed.append((layer_name, parsed_parameters))

        #Logger().print_to_log('Loading following layers: ')
        #Logger().print_to_log(layers_params_parsed)

        network_builder.build(layers_params_parsed)

        Logger().print_to_log(f'Loaded network:\n{network_builder.policy_network}')
        NET_SET = True
        Logger().print_to_log('The network was successfully loaded')
        return dict(icon = "fa-solid fa-circle-check", 
                icon_style = {"color":"green", 'font-size':'1.5em'})
    except Exception as e:
        Logger().print_to_log("An error occured when building network. Check parameters and try again")
        NET_SET = False
        Logger().print_to_log(str(e))
        return dict(icon = "fa-solid fa-circle-xmark", 
                icon_style = {"color":"red", 'font-size':'1.5em'})
    
@app.callback( 
        output = dict(
            icon = Output('setup-hyperparameters-icon', 'className'), 
            icon_style = Output('setup-hyperparameters-icon', 'style')
            ),
        inputs = dict(
            submit_button = Input("modal-hyperparameters-submit-btn", "n_clicks")
        ),
        state = dict(
            options = State({'type':'memory_and_episode-param', 'index':ALL}, 'value'),
            required =  State({'type':'memory_and_episode-param', 'index':ALL}, 'required')
        ),
        prevent_initial_call = True
)
def run_memory_and_episode_setup(submit_button, options, required):
    global NET_SET, network_builder
    try:
        assert (NET_SET == True), "Please set up network first"
        for param, is_required in zip(options, required):
            if is_required and (param is None or param == ""):
             raise ValueError(f"Inputs in 'Memory end episodes' cannot be leaved empty")
            
        options_defs = [val[1] for (opt,val) in get_options()[1].items()]
        parsed = InputParser().parse(options, options_defs)

        opions_values = dict(zip(get_options()[1].keys(), parsed))
        
        network_builder.set_optimizer(opions_values["LR"], True)
        network_builder.set_replay_memory(opions_values['REPLAY_MEMORY_CAPACITY'])
        network_builder.set_episode(opions_values["BATCH_SIZE"], 
                                    opions_values["GAMMA"],
                                    opions_values["EPS_START"],
                                    opions_values["EPS_END"],
                                    opions_values["EPS_DECAY"],
                                    opions_values["TAU"],
                                    opions_values["NUMBER_OF_EPISODES"])
            
        Logger().print_to_log('The memory end episodes were successfully set up')
        return dict(icon = "fa-solid fa-circle-check", 
                icon_style = {"color":"green", 'font-size':'1.5em'})
    except Exception as e:
        Logger().print_to_log("An error occured when setting up memory and episodes. Check parameters and try again")
        ENV_SET = False
        Logger().print_to_log(str(e))
        return dict(icon = "fa-solid fa-circle-xmark", 
                icon_style = {"color":"red", 'font-size':'1.5em'})



@app.callback(
    Input("setup-run", "n_clicks"),
    prevent_initial_call=True,
    #background=True,
    #manager=background_callback_manager,
    running=[
        (Output("setup-run", "disabled"), True, False),
    ])
def run_calculations(n_clicks):
    Logger().print_to_log(f'Calculations started successfully')

    model = Model(env_builder, network_builder, rewards_plt)
    model.train()

    Logger().print_to_log('Calculations ended')

    
if __name__ == '__main__':
    Logger().print_to_log(f'App started')
    app.run(debug=False)
    atexit.register(ExitHandler().handle)


###Network experimental modal callback
#app.clientside_callback(
#     ClientsideFunction(
#        namespace='clientside',
#        function_name='drag_and_drop_handler'
#    ),
#    Output("network-dragndrop-store", 'data'),
#    Input({'type':'network-draggable', 'index':ALL},'children'),
#)
#
#app.clientside_callback(
#    ClientsideFunction(
#        namespace='clientside',
#        function_name='layers_catcher'
#    ),
#    Output("network-dragndrop-store", 'data', allow_duplicate=True),
#    Input('interval-component-2', 'n_intervals'),
#    prevent_initial_call = True
#)
#
#app.clientside_callback(
#   ClientsideFunction(
#        namespace='clientside',
#        function_name='layers_rewriter'
#    ),
#    Input('network-layrs-params-placeholder','children'),
#    prevent_initial_call = True
#)
#
#def _get_div_for_layer(layer, idx):
#    params = get_params_for_layer_name(layer_name=layer['name'])
#    layer_inputs = get_inputs_for_params(params, idx, black_color= True)
#    return html.Div(id = {'type':'network-lyr-input-plchldr', 'index': idx}, 
#                                   children= layer_inputs + [html.Div(idx, style = {'color':'black'})],
#                                   style={'background-color':'rgba(0,0,0,0)', 'margin':'10px', 'display': 'none'})
#
#@app.callback(
#        Output('network-layrs-params-placeholder','children'),
#        Input("network-dragndrop-store", 'data'),
#        State('network-layrs-params-placeholder','children'),
#        prevent_initial_call = True
#)
#def insert_inputs_for_nn_layer(data, readable_children):
#    global LAYERS_CTR
#    current_inputs = Patch()
#
#    no_layers = readable_children is None and len(data['layers']) == 0
#    if no_layers:
#        LAYERS_CTR = 0 if LAYERS_CTR > 0 else LAYERS_CTR
#        return current_inputs
#
#    no_new_layers = len(data['layers']) == len(readable_children) if readable_children is not None else False
#    if no_new_layers:
#        return current_inputs
#    
#    only_one_layer = len(data['layers']) == 1
#    if only_one_layer:
#        first_layer = data['layers'][0]
#        first_layer_div= _get_div_for_layer(first_layer, LAYERS_CTR + 1)
#        LAYERS_CTR +=1
#        current_inputs = [first_layer_div] 
#        return current_inputs
#
#    #print(len(readable_children), len(data['layers']), LAYERS_CTR, data['layers_count'])
#
#    some_layers_deleted = len(data['layers']) < len(readable_children)
#    if some_layers_deleted:
#        if len(data['layers']) == 0:
#            return []
#        
#        was_deleted = False
#        for i, (layer, input) in enumerate(zip(data['layers'], readable_children)):
#            input_idx = input['props']['id']['index']
#            layer_idx = int(layer['id'][32:-1])
#            #print(i, layer_idx, input_idx)
#            if input_idx != layer_idx and not was_deleted:
#                #print('Deleting: ', i)
#                del current_inputs[i]
#                was_deleted = True
#                break
#        
#        if i + 1 == len(data['layers']) and not was_deleted:
#            #print('Deleting:', i+1)
#            del current_inputs[-1]
#            
#        return current_inputs
#
#    more_than_one_layers = type(data['layers']) is list and len(data['layers']) > 1
#    if more_than_one_layers:
#        first_layer = data['layers'][0]
#        #second_layer = data['layers'][1]
#        #print('FL: ', int(first_layer['id'][32:-1]))
#
#        added_layer_at_the_top = int(first_layer['id'][32:-1]) > LAYERS_CTR
#        if added_layer_at_the_top:
#            #print('added at the top')
#            first_layer_div = _get_div_for_layer(first_layer, LAYERS_CTR + 1)
#            LAYERS_CTR+=1
#            current_inputs.prepend(first_layer_div)
#            return current_inputs
#
#        last_layer = data['layers'][-1]
#        #print('LL: ', int(last_layer['id'][32:-1]))
#        added_layer_at_the_bottom = int(last_layer['id'][32:-1]) > LAYERS_CTR
#        if added_layer_at_the_bottom:
#            #print('added at the bottom')
#            last_layer_div = _get_div_for_layer(last_layer, LAYERS_CTR + 1)
#            LAYERS_CTR+=1
#            current_inputs.append(last_layer_div)
#            return current_inputs
#
#    return current_inputs
#
### End of network exprimental modal