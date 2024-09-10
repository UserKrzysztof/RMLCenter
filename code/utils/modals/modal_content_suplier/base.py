from abc import ABC, abstractmethod
from typing import Union, get_args, get_origin
from types import UnionType
from dash import html, dcc, Dash
from inspect import _empty

class ModalContentSuplier(ABC):
    @property
    @abstractmethod
    def get_modal_content(self) -> html.Div:
        pass

class DefaultModalContentSuplier(ModalContentSuplier):
    @property
    def get_modal_content(self)->html.Div:
        return html.Div(
            html.H2("Comming soon..."),
            style={'background-color':'red',
                    'width':'100px',
                    'height':'100px',
                    'display':'iniline-block'})
    
def get_inputs_for_params(env_params, id_type, disabled=False, black_color=False, group_counter = None, all_required = False):
    inputs = []
    i = 0
    for param, value in env_params.items():
        if get_origin(value.annotation) is Union:
            annotation_name = "Union" + str([arg.__name__ for arg in get_args(value.annotation)])
        elif hasattr(value.annotation, '__name__'):
            annotation_name = value.annotation.__name__
        else:
            annotation_name = str(value.annotation)

        if group_counter is None:
            input_id = {'type':id_type, 'index':i}
        else:
            input_id = {'type':id_type, 'group': group_counter,'index':i}

        input = dcc.Input(
            id=input_id,
            placeholder=f'please type value here',
            type='text',
            disabled=disabled,
            value= str(value.default) if value.default is not _empty else None,
            required= False if (value.default is not _empty) and (not all_required) else True,
            className='text-input',
            style={
                'background-color': 'lightgray' if disabled else 'white',
                'width':'48%',
                'display':'inline-block'
                }
        )  
        text = html.Div(children='{}: \n({})'.format(param,annotation_name), 
                       style={
                           'color':'lightgray' if not black_color else 'black',
                           'white-space': 'pre-wrap',
                           'margin':'0',
                           'width':'48%',
                       })

        inputs.append(html.Div(children=[text,input], style = {'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between', 'width':'96%'}))
        i+=1
    return inputs
