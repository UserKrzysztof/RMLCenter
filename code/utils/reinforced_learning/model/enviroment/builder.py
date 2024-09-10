from collections import OrderedDict
from gymnasium.envs.registration import spec, load_env_creator, EnvSpec, EnvCreator
import gymnasium as gym
from utils.logger.log import Logger
from inspect import signature
from typing import Dict, Any

class EnvBuilder():
    def __init__(self) -> None:
        self.env_name = None
        self.env_spec = None

        self.env = None
    
    def set_env_name(self, env_name: str)->EnvSpec:
        try:
            self.env_spec = spec(env_id=env_name)
            self.env_name = env_name 
        except Exception as e:
            raise ValueError('Invalid enviroment name')
        
        return self.env_spec

    def get_env_params(self)-> OrderedDict:
        if self.env_name is None:
            raise ValueError('env_name must be set not None before calling EnvBuilder.get_env_name_params_list()')
        
        creator  = load_env_creator(self.env_spec.entry_point)
        creator_params = dict(signature(creator).parameters)
        creator_params.pop('render_mode', None)
        return creator_params
    
    def build(self, env_params_values: Dict[str,Any], make_params_values:Dict[str,Any]):
        assert(self.env_name is not None)
        assert(isinstance(self.env_spec, EnvSpec))

        env_params_values.update(make_params_values)
        env_params_values['id'] = self.env_name
        env_params_values['render_mode'] = "rgb_array"
        self.env = gym.make(**env_params_values)


def get_gym_make_params():
    params = dict(signature(gym.make).parameters)
    params.pop('id',None)
    params.pop('kwargs',None)
    return params