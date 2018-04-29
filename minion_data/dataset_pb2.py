# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dataset.proto

import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor.FileDescriptor(
    name='dataset.proto',
    package='dataset',
    syntax='proto3',
    serialized_pb=_b(
        '\n\rdataset.proto\x12\x07\x64\x61taset\"\xff\x01\n\tDataPoint\x12\x0e\n\x06signal\x18\x01 \x03(\x02\x12%\n\nbasecalled\x18\x02 \x03(\x0e\x32\x11.dataset.BasePair\x12\x13\n\x0blower_bound\x18\x03 \x03(\r\x12\x1d\n\x05\x63igar\x18\x08 \x03(\x0e\x32\x0e.dataset.Cigar\x12&\n\x0b\x61ligned_ref\x18\t \x03(\x0e\x32\x11.dataset.BasePair\x12/\n\x14\x61ligned_ref_squiggle\x18\n \x03(\x0e\x32\x11.dataset.BasePair\x12.\n\x13\x62\x61secalled_squiggle\x18\x0b \x03(\x0e\x32\x11.dataset.BasePair*1\n\x08\x42\x61sePair\x12\x05\n\x01\x41\x10\x00\x12\x05\n\x01\x43\x10\x01\x12\x05\n\x01G\x10\x02\x12\x05\n\x01T\x10\x03\x12\t\n\x05\x42LANK\x10\x04*=\n\x05\x43igar\x12\t\n\x05MATCH\x10\x00\x12\x0c\n\x08MISMATCH\x10\x01\x12\r\n\tINSERTION\x10\x02\x12\x0c\n\x08\x44\x45LETION\x10\x03\x62\x06proto3'
    )
)

_BASEPAIR = _descriptor.EnumDescriptor(
    name='BasePair',
    full_name='dataset.BasePair',
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name='A', index=0, number=0, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name='C', index=1, number=1, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name='G', index=2, number=2, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name='T', index=3, number=3, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name='BLANK', index=4, number=4, options=None, type=None
        ),
    ],
    containing_type=None,
    options=None,
    serialized_start=284,
    serialized_end=333,
)
_sym_db.RegisterEnumDescriptor(_BASEPAIR)

BasePair = enum_type_wrapper.EnumTypeWrapper(_BASEPAIR)
_CIGAR = _descriptor.EnumDescriptor(
    name='Cigar',
    full_name='dataset.Cigar',
    filename=None,
    file=DESCRIPTOR,
    values=[
        _descriptor.EnumValueDescriptor(
            name='MATCH', index=0, number=0, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name='MISMATCH', index=1, number=1, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name='INSERTION', index=2, number=2, options=None, type=None
        ),
        _descriptor.EnumValueDescriptor(
            name='DELETION', index=3, number=3, options=None, type=None
        ),
    ],
    containing_type=None,
    options=None,
    serialized_start=335,
    serialized_end=396,
)
_sym_db.RegisterEnumDescriptor(_CIGAR)

Cigar = enum_type_wrapper.EnumTypeWrapper(_CIGAR)
A = 0
C = 1
G = 2
T = 3
BLANK = 4
MATCH = 0
MISMATCH = 1
INSERTION = 2
DELETION = 3

_DATAPOINT = _descriptor.Descriptor(
    name='DataPoint',
    full_name='dataset.DataPoint',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='signal',
            full_name='dataset.DataPoint.signal',
            index=0,
            number=1,
            type=2,
            cpp_type=6,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR
        ),
        _descriptor.FieldDescriptor(
            name='basecalled',
            full_name='dataset.DataPoint.basecalled',
            index=1,
            number=2,
            type=14,
            cpp_type=8,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR
        ),
        _descriptor.FieldDescriptor(
            name='lower_bound',
            full_name='dataset.DataPoint.lower_bound',
            index=2,
            number=3,
            type=13,
            cpp_type=3,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR
        ),
        _descriptor.FieldDescriptor(
            name='cigar',
            full_name='dataset.DataPoint.cigar',
            index=3,
            number=8,
            type=14,
            cpp_type=8,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR
        ),
        _descriptor.FieldDescriptor(
            name='aligned_ref',
            full_name='dataset.DataPoint.aligned_ref',
            index=4,
            number=9,
            type=14,
            cpp_type=8,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR
        ),
        _descriptor.FieldDescriptor(
            name='aligned_ref_squiggle',
            full_name='dataset.DataPoint.aligned_ref_squiggle',
            index=5,
            number=10,
            type=14,
            cpp_type=8,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR
        ),
        _descriptor.FieldDescriptor(
            name='basecalled_squiggle',
            full_name='dataset.DataPoint.basecalled_squiggle',
            index=6,
            number=11,
            type=14,
            cpp_type=8,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            options=None,
            file=DESCRIPTOR
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    options=None,
    is_extendable=False,
    syntax='proto3',
    extension_ranges=[],
    oneofs=[],
    serialized_start=27,
    serialized_end=282,
)

_DATAPOINT.fields_by_name['basecalled'].enum_type = _BASEPAIR
_DATAPOINT.fields_by_name['cigar'].enum_type = _CIGAR
_DATAPOINT.fields_by_name['aligned_ref'].enum_type = _BASEPAIR
_DATAPOINT.fields_by_name['aligned_ref_squiggle'].enum_type = _BASEPAIR
_DATAPOINT.fields_by_name['basecalled_squiggle'].enum_type = _BASEPAIR
DESCRIPTOR.message_types_by_name['DataPoint'] = _DATAPOINT
DESCRIPTOR.enum_types_by_name['BasePair'] = _BASEPAIR
DESCRIPTOR.enum_types_by_name['Cigar'] = _CIGAR
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DataPoint = _reflection.GeneratedProtocolMessageType(
    'DataPoint',
    (_message.Message,),
    dict(
        DESCRIPTOR=_DATAPOINT,
        __module__='dataset_pb2'
        # @@protoc_insertion_point(class_scope:dataset.DataPoint)
    )
)
_sym_db.RegisterMessage(DataPoint)

# @@protoc_insertion_point(module_scope)
