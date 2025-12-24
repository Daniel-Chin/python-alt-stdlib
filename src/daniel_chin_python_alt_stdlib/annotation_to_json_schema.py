'''
Converts annotated Python functions into JSON Schema representations.  

Handles annotation `T` where `T` is one of:  
- Primitive: `int`, `float`, `str`, `bool`.  
- Typed list: `list[T]`, `tp.List[T]`.  
- "Metadata" dict: `dict[str, tp.Any]`, `tp.Dict[str, tp.Any]`.  
- Nullable: `tp.Optional[T]`, `T | None`, `tp.Union[T, None]`.  
- Literal enum: `tp.Literal[..., ...]`.  
- Annotated: `tp.Annotated[T, description: str]`.  

In particular, doesn't support: 
- NamedTuple, TypedDict. This is a todo.  
- Union beyond nullable.  
- `tp.Any`.  
- `list[tp.Any]`.  
- Dict beyond `str -> tp.Any`.  
- Tuple.  
- Enum.  

Recursive list types? Undefined behavior. Probably stack overflow, 
or Ctrl+C to see huge stack. So it's diagnosable downstream.  
'''

import typing as tp
import types
import builtins

LOOKUP = {
    builtins.int  : 'integer',
    builtins.float: 'number',
    builtins.str  : 'string',
    builtins.bool : 'boolean',
}

def non_null_to_json_schema(anno: tp.Any, /) -> dict[str, tp.Any]:
    match anno:
        case builtins.int | builtins.float | builtins.str | builtins.bool:
            return dict(
                type=LOOKUP[anno],
            )
        case types.GenericAlias() | tp._GenericAlias(): # type: ignore
            origin = tp.get_origin(anno)
            args   = tp.get_args(anno)
            match origin:
                case builtins.list:  # also matches tp.List
                    try:
                        member_anno, = args
                    except ValueError:
                        raise TypeError('List must have exactly one type argument.')
                    return dict(
                        type='array',
                        items=annotation_to_json_schema(member_anno),
                    )
                case builtins.dict:  # also matches tp.Dict
                    try:
                        key_anno, value_anno = args
                    except ValueError:
                        raise TypeError('Dict must have exactly two type arguments.')
                    if key_anno is not builtins.str:
                        raise TypeError('Only dicts with string keys are supported.')
                    if value_anno is not tp.Any:
                        raise TypeError('You should use TypedDict instead. Unfortunately we don\'t support TypedDict yet. So just use `dict[str, tp.Any]`.')
                    return dict(
                        type='object',
                    )
                case tp.Literal:
                    enums = tp.get_args(anno)
                    unique_types = {type(e) for e in enums}
                    if len(unique_types) != 1:
                        raise TypeError('All Literal enum values must have the same type.')
                    return dict(
                        type=LOOKUP[unique_types.pop()],
                        enum=list(enums),
                    )
                case _:
                    raise TypeError(f'Unsupported generic type: {origin}')
        case _:
            raise TypeError(f'Unsupported type annotation: {anno}')

def maybe_null_to_json_schema(anno: tp.Any, /) -> dict[str, tp.Any]:
    origin = tp.get_origin(anno)
    if origin is types.UnionType or origin is tp.Union:
        args = tp.get_args(anno)
        inner = extract_nullable(*args)
        return dict(
            type=[non_null_to_json_schema(inner)['type'], 'null'],
        )
    else:
        return non_null_to_json_schema(anno)

def annotation_to_json_schema(anno: tp.Any, /) -> dict[str, tp.Any]:
    if isinstance(anno, tp._AnnotatedAlias):    # type: ignore
        inner, description = tp.get_args(anno)
        return dict(
            **maybe_null_to_json_schema(inner),
            description=description,
        )
    return maybe_null_to_json_schema(anno)

def extract_nullable(*types_: tp.Any) -> tp.Any:
    non_null = [t for t in types_ if t is not types.NoneType]
    if len(non_null) == 1:
        return non_null[0]
    else:
        raise TypeError('We don\'t yet support unions beyond nullable.')

def test():
    import inspect
    from pprint import pprint

    def f(
        a: tp.Annotated[int, "Number of bananas"], 
        d: tp.Optional[float],
        e: tp.Union[float, None],
        f: float | None,
        g: int | str,
        b: tp.Annotated[list[tp.Annotated[
            float, "Angle between John and Mary", 
        ]], "Historic angles"] = [3.14],
        c: str = "Hello, World!",
        aa: tp.Literal['A', 'B', 'C'] = 'A',
    ) -> int:
        '''
        Goes to the Moon.  
        '''
        return 42
    
    for name, param in inspect.signature(f).parameters.items():
        print(f"Parameter: {name}")
        try:
            pprint(annotation_to_json_schema(param.annotation))
        except TypeError:
            print('invalid')
            assert name == 'g'
        else:
            assert name != 'g'
        print()

if __name__ == '__main__':
    test()
