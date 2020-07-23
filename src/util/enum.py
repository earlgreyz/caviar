import enum
import functools
import operator


def withLimits(enumeration: enum.EnumMeta) -> enum.EnumMeta:
    none_flag = enumeration(0)
    # Only add ALL flag if enum is non empty to avoid exception.
    if len(enumeration) > 0:
        all_flag = enumeration(functools.reduce(operator.ior, enumeration))
        enumeration._member_map_['ALL'] = all_flag
    enumeration._member_map_['NONE'] = none_flag
    return enumeration
