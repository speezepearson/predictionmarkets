# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: predictionmarkets/server/api/protobuf/service.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='predictionmarkets/server/api/protobuf/service.proto',
  package='predictionmarkets.protobuf',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n3predictionmarkets/server/api/protobuf/service.proto\x12\x1apredictionmarkets.protobuf\"\x1e\n\x0bProbability\x12\x0f\n\x07ln_odds\x18\x01 \x01(\x01\"9\n\x06Stakes\x12\x17\n\x0fwinnings_if_yes\x18\x01 \x01(\x01\x12\x16\n\x0ewinnings_if_no\x18\x02 \x01(\x01\"\x83\x03\n\nCfarMarket\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0bproposition\x18\x02 \x01(\t\x12\x36\n\x05\x66loor\x18\x03 \x01(\x0b\x32\'.predictionmarkets.protobuf.Probability\x12\x38\n\x07\x63\x65iling\x18\x04 \x01(\x0b\x32\'.predictionmarkets.protobuf.Probability\x12\x36\n\x05state\x18\x05 \x01(\x0b\x32\'.predictionmarkets.protobuf.Probability\x12O\n\rentity_stakes\x18\x06 \x03(\x0b\x32\x38.predictionmarkets.protobuf.CfarMarket.EntityStakesEntry\x1aW\n\x11\x45ntityStakesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x31\n\x05value\x18\x02 \x01(\x0b\x32\".predictionmarkets.protobuf.Stakes:\x02\x38\x01\"\xea\x01\n\x13\x43reateMarketRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0bproposition\x18\x02 \x01(\t\x12\x36\n\x05\x66loor\x18\x03 \x01(\x0b\x32\'.predictionmarkets.protobuf.Probability\x12\x38\n\x07\x63\x65iling\x18\x04 \x01(\x0b\x32\'.predictionmarkets.protobuf.Probability\x12>\n\rinitial_state\x18\x05 \x01(\x0b\x32\'.predictionmarkets.protobuf.Probability\")\n\x14\x43reateMarketResponse\x12\x11\n\tmarket_id\x18\x01 \x01(\t\"\x1e\n\x10GetMarketRequest\x12\n\n\x02id\x18\x01 \x01(\t\"U\n\x11GetMarketResponse\x12\x36\n\x04\x63\x66\x61r\x18\x01 \x01(\x0b\x32&.predictionmarkets.protobuf.CfarMarketH\x00\x42\x08\n\x06market\"\x80\x01\n\x17UpdateCfarMarketRequest\x12\x11\n\tmarket_id\x18\x01 \x01(\t\x12\x16\n\x0eparticipant_id\x18\x02 \x01(\t\x12:\n\tnew_state\x18\x03 \x01(\x0b\x32\'.predictionmarkets.protobuf.Probability\"\x1a\n\x18UpdateCfarMarketResponse\"B\n\x1cUsernamePasswordLoginRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\".\n\x1dUsernamePasswordLoginResponse\x12\r\n\x05token\x18\x01 \x01(\t\")\n\x18GetEntityForTokenRequest\x12\r\n\x05token\x18\x01 \x01(\t\".\n\x19GetEntityForTokenResponse\x12\x11\n\tentity_id\x18\x01 \x01(\t\"#\n\x12\x44\x65leteTokenRequest\x12\r\n\x05token\x18\x01 \x01(\t\"\x15\n\x13\x44\x65leteTokenResponse2\xef\x02\n\x0bMarketplace\x12s\n\x0c\x43reateMarket\x12/.predictionmarkets.protobuf.CreateMarketRequest\x1a\x30.predictionmarkets.protobuf.CreateMarketResponse\"\x00\x12j\n\tGetMarket\x12,.predictionmarkets.protobuf.GetMarketRequest\x1a-.predictionmarkets.protobuf.GetMarketResponse\"\x00\x12\x7f\n\x10UpdateCfarMarket\x12\x33.predictionmarkets.protobuf.UpdateCfarMarketRequest\x1a\x34.predictionmarkets.protobuf.UpdateCfarMarketResponse\"\x00\x32\x90\x03\n\x06\x45ntity\x12\x8e\x01\n\x15UsernamePasswordLogin\x12\x38.predictionmarkets.protobuf.UsernamePasswordLoginRequest\x1a\x39.predictionmarkets.protobuf.UsernamePasswordLoginResponse\"\x00\x12\x82\x01\n\x11GetEntityForToken\x12\x34.predictionmarkets.protobuf.GetEntityForTokenRequest\x1a\x35.predictionmarkets.protobuf.GetEntityForTokenResponse\"\x00\x12p\n\x0b\x44\x65leteToken\x12..predictionmarkets.protobuf.DeleteTokenRequest\x1a/.predictionmarkets.protobuf.DeleteTokenResponse\"\x00\x62\x06proto3'
)




_PROBABILITY = _descriptor.Descriptor(
  name='Probability',
  full_name='predictionmarkets.protobuf.Probability',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ln_odds', full_name='predictionmarkets.protobuf.Probability.ln_odds', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=83,
  serialized_end=113,
)


_STAKES = _descriptor.Descriptor(
  name='Stakes',
  full_name='predictionmarkets.protobuf.Stakes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='winnings_if_yes', full_name='predictionmarkets.protobuf.Stakes.winnings_if_yes', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='winnings_if_no', full_name='predictionmarkets.protobuf.Stakes.winnings_if_no', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=115,
  serialized_end=172,
)


_CFARMARKET_ENTITYSTAKESENTRY = _descriptor.Descriptor(
  name='EntityStakesEntry',
  full_name='predictionmarkets.protobuf.CfarMarket.EntityStakesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='predictionmarkets.protobuf.CfarMarket.EntityStakesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='predictionmarkets.protobuf.CfarMarket.EntityStakesEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=475,
  serialized_end=562,
)

_CFARMARKET = _descriptor.Descriptor(
  name='CfarMarket',
  full_name='predictionmarkets.protobuf.CfarMarket',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='predictionmarkets.protobuf.CfarMarket.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='proposition', full_name='predictionmarkets.protobuf.CfarMarket.proposition', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='floor', full_name='predictionmarkets.protobuf.CfarMarket.floor', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ceiling', full_name='predictionmarkets.protobuf.CfarMarket.ceiling', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='state', full_name='predictionmarkets.protobuf.CfarMarket.state', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='entity_stakes', full_name='predictionmarkets.protobuf.CfarMarket.entity_stakes', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_CFARMARKET_ENTITYSTAKESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=175,
  serialized_end=562,
)


_CREATEMARKETREQUEST = _descriptor.Descriptor(
  name='CreateMarketRequest',
  full_name='predictionmarkets.protobuf.CreateMarketRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='predictionmarkets.protobuf.CreateMarketRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='proposition', full_name='predictionmarkets.protobuf.CreateMarketRequest.proposition', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='floor', full_name='predictionmarkets.protobuf.CreateMarketRequest.floor', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ceiling', full_name='predictionmarkets.protobuf.CreateMarketRequest.ceiling', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='initial_state', full_name='predictionmarkets.protobuf.CreateMarketRequest.initial_state', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=565,
  serialized_end=799,
)


_CREATEMARKETRESPONSE = _descriptor.Descriptor(
  name='CreateMarketResponse',
  full_name='predictionmarkets.protobuf.CreateMarketResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='market_id', full_name='predictionmarkets.protobuf.CreateMarketResponse.market_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=801,
  serialized_end=842,
)


_GETMARKETREQUEST = _descriptor.Descriptor(
  name='GetMarketRequest',
  full_name='predictionmarkets.protobuf.GetMarketRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='predictionmarkets.protobuf.GetMarketRequest.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=844,
  serialized_end=874,
)


_GETMARKETRESPONSE = _descriptor.Descriptor(
  name='GetMarketResponse',
  full_name='predictionmarkets.protobuf.GetMarketResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='cfar', full_name='predictionmarkets.protobuf.GetMarketResponse.cfar', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='market', full_name='predictionmarkets.protobuf.GetMarketResponse.market',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=876,
  serialized_end=961,
)


_UPDATECFARMARKETREQUEST = _descriptor.Descriptor(
  name='UpdateCfarMarketRequest',
  full_name='predictionmarkets.protobuf.UpdateCfarMarketRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='market_id', full_name='predictionmarkets.protobuf.UpdateCfarMarketRequest.market_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='participant_id', full_name='predictionmarkets.protobuf.UpdateCfarMarketRequest.participant_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='new_state', full_name='predictionmarkets.protobuf.UpdateCfarMarketRequest.new_state', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=964,
  serialized_end=1092,
)


_UPDATECFARMARKETRESPONSE = _descriptor.Descriptor(
  name='UpdateCfarMarketResponse',
  full_name='predictionmarkets.protobuf.UpdateCfarMarketResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1094,
  serialized_end=1120,
)


_USERNAMEPASSWORDLOGINREQUEST = _descriptor.Descriptor(
  name='UsernamePasswordLoginRequest',
  full_name='predictionmarkets.protobuf.UsernamePasswordLoginRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='username', full_name='predictionmarkets.protobuf.UsernamePasswordLoginRequest.username', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='password', full_name='predictionmarkets.protobuf.UsernamePasswordLoginRequest.password', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1122,
  serialized_end=1188,
)


_USERNAMEPASSWORDLOGINRESPONSE = _descriptor.Descriptor(
  name='UsernamePasswordLoginResponse',
  full_name='predictionmarkets.protobuf.UsernamePasswordLoginResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='token', full_name='predictionmarkets.protobuf.UsernamePasswordLoginResponse.token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1190,
  serialized_end=1236,
)


_GETENTITYFORTOKENREQUEST = _descriptor.Descriptor(
  name='GetEntityForTokenRequest',
  full_name='predictionmarkets.protobuf.GetEntityForTokenRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='token', full_name='predictionmarkets.protobuf.GetEntityForTokenRequest.token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1238,
  serialized_end=1279,
)


_GETENTITYFORTOKENRESPONSE = _descriptor.Descriptor(
  name='GetEntityForTokenResponse',
  full_name='predictionmarkets.protobuf.GetEntityForTokenResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='entity_id', full_name='predictionmarkets.protobuf.GetEntityForTokenResponse.entity_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1281,
  serialized_end=1327,
)


_DELETETOKENREQUEST = _descriptor.Descriptor(
  name='DeleteTokenRequest',
  full_name='predictionmarkets.protobuf.DeleteTokenRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='token', full_name='predictionmarkets.protobuf.DeleteTokenRequest.token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1329,
  serialized_end=1364,
)


_DELETETOKENRESPONSE = _descriptor.Descriptor(
  name='DeleteTokenResponse',
  full_name='predictionmarkets.protobuf.DeleteTokenResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1366,
  serialized_end=1387,
)

_CFARMARKET_ENTITYSTAKESENTRY.fields_by_name['value'].message_type = _STAKES
_CFARMARKET_ENTITYSTAKESENTRY.containing_type = _CFARMARKET
_CFARMARKET.fields_by_name['floor'].message_type = _PROBABILITY
_CFARMARKET.fields_by_name['ceiling'].message_type = _PROBABILITY
_CFARMARKET.fields_by_name['state'].message_type = _PROBABILITY
_CFARMARKET.fields_by_name['entity_stakes'].message_type = _CFARMARKET_ENTITYSTAKESENTRY
_CREATEMARKETREQUEST.fields_by_name['floor'].message_type = _PROBABILITY
_CREATEMARKETREQUEST.fields_by_name['ceiling'].message_type = _PROBABILITY
_CREATEMARKETREQUEST.fields_by_name['initial_state'].message_type = _PROBABILITY
_GETMARKETRESPONSE.fields_by_name['cfar'].message_type = _CFARMARKET
_GETMARKETRESPONSE.oneofs_by_name['market'].fields.append(
  _GETMARKETRESPONSE.fields_by_name['cfar'])
_GETMARKETRESPONSE.fields_by_name['cfar'].containing_oneof = _GETMARKETRESPONSE.oneofs_by_name['market']
_UPDATECFARMARKETREQUEST.fields_by_name['new_state'].message_type = _PROBABILITY
DESCRIPTOR.message_types_by_name['Probability'] = _PROBABILITY
DESCRIPTOR.message_types_by_name['Stakes'] = _STAKES
DESCRIPTOR.message_types_by_name['CfarMarket'] = _CFARMARKET
DESCRIPTOR.message_types_by_name['CreateMarketRequest'] = _CREATEMARKETREQUEST
DESCRIPTOR.message_types_by_name['CreateMarketResponse'] = _CREATEMARKETRESPONSE
DESCRIPTOR.message_types_by_name['GetMarketRequest'] = _GETMARKETREQUEST
DESCRIPTOR.message_types_by_name['GetMarketResponse'] = _GETMARKETRESPONSE
DESCRIPTOR.message_types_by_name['UpdateCfarMarketRequest'] = _UPDATECFARMARKETREQUEST
DESCRIPTOR.message_types_by_name['UpdateCfarMarketResponse'] = _UPDATECFARMARKETRESPONSE
DESCRIPTOR.message_types_by_name['UsernamePasswordLoginRequest'] = _USERNAMEPASSWORDLOGINREQUEST
DESCRIPTOR.message_types_by_name['UsernamePasswordLoginResponse'] = _USERNAMEPASSWORDLOGINRESPONSE
DESCRIPTOR.message_types_by_name['GetEntityForTokenRequest'] = _GETENTITYFORTOKENREQUEST
DESCRIPTOR.message_types_by_name['GetEntityForTokenResponse'] = _GETENTITYFORTOKENRESPONSE
DESCRIPTOR.message_types_by_name['DeleteTokenRequest'] = _DELETETOKENREQUEST
DESCRIPTOR.message_types_by_name['DeleteTokenResponse'] = _DELETETOKENRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Probability = _reflection.GeneratedProtocolMessageType('Probability', (_message.Message,), {
  'DESCRIPTOR' : _PROBABILITY,
  '__module__' : 'predictionmarkets.server.api.protobuf.service_pb2'
  # @@protoc_insertion_point(class_scope:predictionmarkets.protobuf.Probability)
  })
_sym_db.RegisterMessage(Probability)

Stakes = _reflection.GeneratedProtocolMessageType('Stakes', (_message.Message,), {
  'DESCRIPTOR' : _STAKES,
  '__module__' : 'predictionmarkets.server.api.protobuf.service_pb2'
  # @@protoc_insertion_point(class_scope:predictionmarkets.protobuf.Stakes)
  })
_sym_db.RegisterMessage(Stakes)

CfarMarket = _reflection.GeneratedProtocolMessageType('CfarMarket', (_message.Message,), {

  'EntityStakesEntry' : _reflection.GeneratedProtocolMessageType('EntityStakesEntry', (_message.Message,), {
    'DESCRIPTOR' : _CFARMARKET_ENTITYSTAKESENTRY,
    '__module__' : 'predictionmarkets.server.api.protobuf.service_pb2'
    # @@protoc_insertion_point(class_scope:predictionmarkets.protobuf.CfarMarket.EntityStakesEntry)
    })
  ,
  'DESCRIPTOR' : _CFARMARKET,
  '__module__' : 'predictionmarkets.server.api.protobuf.service_pb2'
  # @@protoc_insertion_point(class_scope:predictionmarkets.protobuf.CfarMarket)
  })
_sym_db.RegisterMessage(CfarMarket)
_sym_db.RegisterMessage(CfarMarket.EntityStakesEntry)

CreateMarketRequest = _reflection.GeneratedProtocolMessageType('CreateMarketRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEMARKETREQUEST,
  '__module__' : 'predictionmarkets.server.api.protobuf.service_pb2'
  # @@protoc_insertion_point(class_scope:predictionmarkets.protobuf.CreateMarketRequest)
  })
_sym_db.RegisterMessage(CreateMarketRequest)

CreateMarketResponse = _reflection.GeneratedProtocolMessageType('CreateMarketResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEMARKETRESPONSE,
  '__module__' : 'predictionmarkets.server.api.protobuf.service_pb2'
  # @@protoc_insertion_point(class_scope:predictionmarkets.protobuf.CreateMarketResponse)
  })
_sym_db.RegisterMessage(CreateMarketResponse)

GetMarketRequest = _reflection.GeneratedProtocolMessageType('GetMarketRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETMARKETREQUEST,
  '__module__' : 'predictionmarkets.server.api.protobuf.service_pb2'
  # @@protoc_insertion_point(class_scope:predictionmarkets.protobuf.GetMarketRequest)
  })
_sym_db.RegisterMessage(GetMarketRequest)

GetMarketResponse = _reflection.GeneratedProtocolMessageType('GetMarketResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETMARKETRESPONSE,
  '__module__' : 'predictionmarkets.server.api.protobuf.service_pb2'
  # @@protoc_insertion_point(class_scope:predictionmarkets.protobuf.GetMarketResponse)
  })
_sym_db.RegisterMessage(GetMarketResponse)

UpdateCfarMarketRequest = _reflection.GeneratedProtocolMessageType('UpdateCfarMarketRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATECFARMARKETREQUEST,
  '__module__' : 'predictionmarkets.server.api.protobuf.service_pb2'
  # @@protoc_insertion_point(class_scope:predictionmarkets.protobuf.UpdateCfarMarketRequest)
  })
_sym_db.RegisterMessage(UpdateCfarMarketRequest)

UpdateCfarMarketResponse = _reflection.GeneratedProtocolMessageType('UpdateCfarMarketResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPDATECFARMARKETRESPONSE,
  '__module__' : 'predictionmarkets.server.api.protobuf.service_pb2'
  # @@protoc_insertion_point(class_scope:predictionmarkets.protobuf.UpdateCfarMarketResponse)
  })
_sym_db.RegisterMessage(UpdateCfarMarketResponse)

UsernamePasswordLoginRequest = _reflection.GeneratedProtocolMessageType('UsernamePasswordLoginRequest', (_message.Message,), {
  'DESCRIPTOR' : _USERNAMEPASSWORDLOGINREQUEST,
  '__module__' : 'predictionmarkets.server.api.protobuf.service_pb2'
  # @@protoc_insertion_point(class_scope:predictionmarkets.protobuf.UsernamePasswordLoginRequest)
  })
_sym_db.RegisterMessage(UsernamePasswordLoginRequest)

UsernamePasswordLoginResponse = _reflection.GeneratedProtocolMessageType('UsernamePasswordLoginResponse', (_message.Message,), {
  'DESCRIPTOR' : _USERNAMEPASSWORDLOGINRESPONSE,
  '__module__' : 'predictionmarkets.server.api.protobuf.service_pb2'
  # @@protoc_insertion_point(class_scope:predictionmarkets.protobuf.UsernamePasswordLoginResponse)
  })
_sym_db.RegisterMessage(UsernamePasswordLoginResponse)

GetEntityForTokenRequest = _reflection.GeneratedProtocolMessageType('GetEntityForTokenRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETENTITYFORTOKENREQUEST,
  '__module__' : 'predictionmarkets.server.api.protobuf.service_pb2'
  # @@protoc_insertion_point(class_scope:predictionmarkets.protobuf.GetEntityForTokenRequest)
  })
_sym_db.RegisterMessage(GetEntityForTokenRequest)

GetEntityForTokenResponse = _reflection.GeneratedProtocolMessageType('GetEntityForTokenResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETENTITYFORTOKENRESPONSE,
  '__module__' : 'predictionmarkets.server.api.protobuf.service_pb2'
  # @@protoc_insertion_point(class_scope:predictionmarkets.protobuf.GetEntityForTokenResponse)
  })
_sym_db.RegisterMessage(GetEntityForTokenResponse)

DeleteTokenRequest = _reflection.GeneratedProtocolMessageType('DeleteTokenRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETETOKENREQUEST,
  '__module__' : 'predictionmarkets.server.api.protobuf.service_pb2'
  # @@protoc_insertion_point(class_scope:predictionmarkets.protobuf.DeleteTokenRequest)
  })
_sym_db.RegisterMessage(DeleteTokenRequest)

DeleteTokenResponse = _reflection.GeneratedProtocolMessageType('DeleteTokenResponse', (_message.Message,), {
  'DESCRIPTOR' : _DELETETOKENRESPONSE,
  '__module__' : 'predictionmarkets.server.api.protobuf.service_pb2'
  # @@protoc_insertion_point(class_scope:predictionmarkets.protobuf.DeleteTokenResponse)
  })
_sym_db.RegisterMessage(DeleteTokenResponse)


_CFARMARKET_ENTITYSTAKESENTRY._options = None

_MARKETPLACE = _descriptor.ServiceDescriptor(
  name='Marketplace',
  full_name='predictionmarkets.protobuf.Marketplace',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1390,
  serialized_end=1757,
  methods=[
  _descriptor.MethodDescriptor(
    name='CreateMarket',
    full_name='predictionmarkets.protobuf.Marketplace.CreateMarket',
    index=0,
    containing_service=None,
    input_type=_CREATEMARKETREQUEST,
    output_type=_CREATEMARKETRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetMarket',
    full_name='predictionmarkets.protobuf.Marketplace.GetMarket',
    index=1,
    containing_service=None,
    input_type=_GETMARKETREQUEST,
    output_type=_GETMARKETRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='UpdateCfarMarket',
    full_name='predictionmarkets.protobuf.Marketplace.UpdateCfarMarket',
    index=2,
    containing_service=None,
    input_type=_UPDATECFARMARKETREQUEST,
    output_type=_UPDATECFARMARKETRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_MARKETPLACE)

DESCRIPTOR.services_by_name['Marketplace'] = _MARKETPLACE


_ENTITY = _descriptor.ServiceDescriptor(
  name='Entity',
  full_name='predictionmarkets.protobuf.Entity',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  serialized_start=1760,
  serialized_end=2160,
  methods=[
  _descriptor.MethodDescriptor(
    name='UsernamePasswordLogin',
    full_name='predictionmarkets.protobuf.Entity.UsernamePasswordLogin',
    index=0,
    containing_service=None,
    input_type=_USERNAMEPASSWORDLOGINREQUEST,
    output_type=_USERNAMEPASSWORDLOGINRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetEntityForToken',
    full_name='predictionmarkets.protobuf.Entity.GetEntityForToken',
    index=1,
    containing_service=None,
    input_type=_GETENTITYFORTOKENREQUEST,
    output_type=_GETENTITYFORTOKENRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='DeleteToken',
    full_name='predictionmarkets.protobuf.Entity.DeleteToken',
    index=2,
    containing_service=None,
    input_type=_DELETETOKENREQUEST,
    output_type=_DELETETOKENRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_ENTITY)

DESCRIPTOR.services_by_name['Entity'] = _ENTITY

# @@protoc_insertion_point(module_scope)
