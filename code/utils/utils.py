from types import UnionType
from typing import Union, get_origin, get_args

class InputParser():
    def parse(self, values: list, expected_types: list):
        assert isinstance(values, list), "values should be a list"
        assert all(isinstance(v, str) for v in values), "all elements in values should be strings"
        assert isinstance(expected_types, list), "expected_types should be a list"
        assert all(isinstance(et, type) or (get_origin(et) is Union and any(isinstance(t, type) for t in get_args(et))) or isinstance(et, UnionType) for et in expected_types), "expected_types should contain types or Union/Optional types"
        assert len(values) == len(expected_types), "values and expected_types should have the same length"

        type_converters = {
            bool: lambda x: x in ('true', 'True', '1', 'T', 't'),
            int: int,
            float: float,
            str: str,
            None: lambda x: None
        }

        results = []
        for val, et in zip(values, expected_types):
            if val == 'None':
                results.append(None)
            else:
                convert = type_converters.get(et, str)
                results.append(convert(val))
        
        return results
    

