from dash import html
from utils.modals.modal_content_suplier import specific,base
from utils.logger.log import Logger

class SetupBtnWithModalSuplier():
    def __get_btn_content(self,option):
        return html.Div(children=[
                            html.Div(option,
                                    style={'font-size':'20px'}),  
                            html.I(className='fa-solid fa-circle-xmark',
                                id=f'setup-{option.lower()}-icon',
                                style={'font-size':'1.5em', 'color':'red'})
                            ], 
                        style={'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between'})


    def __get_btn(self,option):
        return html.Button(self.__get_btn_content(option), id= f'setup-{option.lower()}', className='setup-button', n_clicks=0)

    def __get_modal_content(self,option):
        try:
            return getattr(specific, f'{option.replace(" ", "_")}ModalContentSuplier')().get_modal_content
        except Exception as e:
            print(f'Default modal for {option}')
            #Logger().print_to_log(e)
            #Logger().print_to_log(f'Default modal for {option}')
        return base.DefaultModalContentSuplier().get_modal_content

    def __get_modal(self,option):
        return html.Div(
            className='modal',
            id=f'modal-{option.lower()}',
            children=[
                html.Div(
                    className='modal-content',
                    children=[
                        html.Div(
                            children=[
                                html.Div(f"{option} setup", className='modal-header--title'),
                                html.Div(
                                    children=[
                                        html.Button(
                                            html.I(className='fa-solid fa-xmark'),
                                            id=f'modal-{option.lower()}-close-btn',
                                            style={'border': 'none', 'background': 'none', 'color': 'white'},
                                            className='modal-close'
                                        )
                                        ],
                                        style={'position': 'relative'}
                                    ),
                                ],
                            className='modal-header'
                        ),
                        html.Div(className='row', children=[
                            html.Div(className='modal-option-content-placeholder', 
                                    style={'border-radius':'10px','height':'70vh','margin':'0','background-color':'rgba(0,0,0,1)'},
                                    children=[
                                        self.__get_modal_content(option)
                                    ]
                                    )
                        ]
                        ),
                        html.Div(className='modal-submit-button-container',
                                 children=[
                                     html.Button(className='modal-submit-button',
                                                 children = [
                                                     "Submit"
                                                 ],
                                                 id = f'modal-{option.lower()}-submit-btn')
                                 ],
                                style={'border-radius':'10px',
                                       'height':'6vh',
                                       'width':'100%',
                                       'background-color':'black',
                                       'margin-top':'0.5%',
                                       'display':'flex'}
                                )
                    ]
                )
            ]
        )

    def get_content_for_option(self,option):
        return  html.Div( children = [ 
                                      self.__get_btn(option),
                                      self.__get_modal(option)
                                  ])
