# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from predictionmarkets.server.api.protobuf import service_pb2 as predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2


class MarketplaceStub(object):
    """Missing associated documentation comment in .proto file"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetPublicMarkets = channel.unary_unary(
                '/predictionmarkets.protobuf.Marketplace/GetPublicMarkets',
                request_serializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.GetPublicMarketsRequest.SerializeToString,
                response_deserializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.GetPublicMarketsResponse.FromString,
                )
        self.CreateMarket = channel.unary_unary(
                '/predictionmarkets.protobuf.Marketplace/CreateMarket',
                request_serializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.CreateMarketRequest.SerializeToString,
                response_deserializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.CreateMarketResponse.FromString,
                )
        self.GetMarket = channel.unary_unary(
                '/predictionmarkets.protobuf.Marketplace/GetMarket',
                request_serializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.GetMarketRequest.SerializeToString,
                response_deserializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.GetMarketResponse.FromString,
                )
        self.UpdateCfarMarket = channel.unary_unary(
                '/predictionmarkets.protobuf.Marketplace/UpdateCfarMarket',
                request_serializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.UpdateCfarMarketRequest.SerializeToString,
                response_deserializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.UpdateCfarMarketResponse.FromString,
                )


class MarketplaceServicer(object):
    """Missing associated documentation comment in .proto file"""

    def GetPublicMarkets(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateMarket(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMarket(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateCfarMarket(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MarketplaceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetPublicMarkets': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPublicMarkets,
                    request_deserializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.GetPublicMarketsRequest.FromString,
                    response_serializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.GetPublicMarketsResponse.SerializeToString,
            ),
            'CreateMarket': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateMarket,
                    request_deserializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.CreateMarketRequest.FromString,
                    response_serializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.CreateMarketResponse.SerializeToString,
            ),
            'GetMarket': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMarket,
                    request_deserializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.GetMarketRequest.FromString,
                    response_serializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.GetMarketResponse.SerializeToString,
            ),
            'UpdateCfarMarket': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateCfarMarket,
                    request_deserializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.UpdateCfarMarketRequest.FromString,
                    response_serializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.UpdateCfarMarketResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'predictionmarkets.protobuf.Marketplace', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Marketplace(object):
    """Missing associated documentation comment in .proto file"""

    @staticmethod
    def GetPublicMarkets(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/predictionmarkets.protobuf.Marketplace/GetPublicMarkets',
            predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.GetPublicMarketsRequest.SerializeToString,
            predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.GetPublicMarketsResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateMarket(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/predictionmarkets.protobuf.Marketplace/CreateMarket',
            predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.CreateMarketRequest.SerializeToString,
            predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.CreateMarketResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMarket(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/predictionmarkets.protobuf.Marketplace/GetMarket',
            predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.GetMarketRequest.SerializeToString,
            predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.GetMarketResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateCfarMarket(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/predictionmarkets.protobuf.Marketplace/UpdateCfarMarket',
            predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.UpdateCfarMarketRequest.SerializeToString,
            predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.UpdateCfarMarketResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)


class EntityStub(object):
    """Missing associated documentation comment in .proto file"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.UsernamePasswordLogin = channel.unary_unary(
                '/predictionmarkets.protobuf.Entity/UsernamePasswordLogin',
                request_serializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.UsernamePasswordLoginRequest.SerializeToString,
                response_deserializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.UsernamePasswordLoginResponse.FromString,
                )
        self.GetEntityForToken = channel.unary_unary(
                '/predictionmarkets.protobuf.Entity/GetEntityForToken',
                request_serializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.GetEntityForTokenRequest.SerializeToString,
                response_deserializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.GetEntityForTokenResponse.FromString,
                )
        self.DeleteToken = channel.unary_unary(
                '/predictionmarkets.protobuf.Entity/DeleteToken',
                request_serializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.DeleteTokenRequest.SerializeToString,
                response_deserializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.DeleteTokenResponse.FromString,
                )


class EntityServicer(object):
    """Missing associated documentation comment in .proto file"""

    def UsernamePasswordLogin(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetEntityForToken(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteToken(self, request, context):
        """Missing associated documentation comment in .proto file"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_EntityServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'UsernamePasswordLogin': grpc.unary_unary_rpc_method_handler(
                    servicer.UsernamePasswordLogin,
                    request_deserializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.UsernamePasswordLoginRequest.FromString,
                    response_serializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.UsernamePasswordLoginResponse.SerializeToString,
            ),
            'GetEntityForToken': grpc.unary_unary_rpc_method_handler(
                    servicer.GetEntityForToken,
                    request_deserializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.GetEntityForTokenRequest.FromString,
                    response_serializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.GetEntityForTokenResponse.SerializeToString,
            ),
            'DeleteToken': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteToken,
                    request_deserializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.DeleteTokenRequest.FromString,
                    response_serializer=predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.DeleteTokenResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'predictionmarkets.protobuf.Entity', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Entity(object):
    """Missing associated documentation comment in .proto file"""

    @staticmethod
    def UsernamePasswordLogin(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/predictionmarkets.protobuf.Entity/UsernamePasswordLogin',
            predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.UsernamePasswordLoginRequest.SerializeToString,
            predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.UsernamePasswordLoginResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetEntityForToken(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/predictionmarkets.protobuf.Entity/GetEntityForToken',
            predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.GetEntityForTokenRequest.SerializeToString,
            predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.GetEntityForTokenResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteToken(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/predictionmarkets.protobuf.Entity/DeleteToken',
            predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.DeleteTokenRequest.SerializeToString,
            predictionmarkets_dot_server_dot_api_dot_protobuf_dot_service__pb2.DeleteTokenResponse.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
