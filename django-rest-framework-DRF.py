# https://i.redd.it/ve66iak6gxm11.png

# ========================================================================
#        DOs                                                             #
# ========================================================================

format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}


ViewSet = View + Automatic URLs + Automatic (overridable) CRUD

# ========================================================================
#        COOKBOOK                                                        #
# ========================================================================

request.data = request.POST | request.PATCH | request.UPDATE | request.FILES
request.query_params = request.GET

INSTALLED_APPS = ['rest_framework']  # install DRF
path('api-auth/', include('rest_framework.urls')),  # Path for auth
path('users/<int:pk>/', views.UserDetail.as_view()),

# Router
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)
urlpatterns = [path('', include(router.urls))]

# Associating objects
class UserSerializer(ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

class SnippetSerializer(ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

class SnippetDetail(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetViewSet(ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def custom_endpoint(self, request, *args, **kwargs):
        return Response(...)

# custom mapping
snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

# Object Level Permissions
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

# ========================================================================
#        SERIALIZERS                                                     #
# ========================================================================

class BaseSerializer:
    data: dict
    errors: dict
    validated_data: dict

    def __init__(instance, data, **kwargs): ...
    def update(instance, validated_data): ...
    def create(validated_data): ...
    def save(**kwargs): ...
    def is_valid(raise_exception): ...


class Serializer(BaseSerializer):
    fields: dict

    def get_fields(): ...
    def get_validators(): ...
    def get_initial(): ...
    def get_value(dictionary): ...
    def run_validation(data): ...
    def run_validators(value): ...
    def to_internal_value(data): ...
    def to_representation(instance): ...
    def validate(attrs): ...

class ListSerializer(BaseSerializer):
    f"""all of {Serialzer}"""


class ModelSerializer(Serialzer):
    f"""all of {ListSerializer}"""

    def get_fields(): ...

class HyperlinkedmodelSerializer(ModelSerializer): ...


class Meta:
    model = Snippet
    fields = [...]
    exclude = [...]
    readonly_fields = [...]

    depth # only for nested serializer



# ========================================================================
#        API VIEW                                                        #
# ========================================================================

class View:
    http_method_names = ['get', 'post', 'put', 'patch', 'delete',
                         'head', 'options', 'trace']
    def __any__http__method__name__ (request, *args, **kwargs): ...

    def setup(request, *args, **kwargs): ...
    def dispatch(request, *args, **kwargs): ...
    def http_method_not_allowed(request, *args, **kwargs): ...
    def options(request, *args, **kwargs): ...
    def as_view(): ...

class APIView(View):
    renderer_classes: list
    parser_classes: list
    authentication_classes: list
    throttle_classes: list
    permission_classes: list
    content_negotiation_classes: list
    metadata_classes: list
    versioning_classes: list
    settings: dict
    schema: Schema

    # properties
    allowed_methods: list
    default_response_headers: dict

    def permission_denies(request, message, code): ...
    def throttled(request, wait): ...
    def get_authenticate_header(request): ...
    def get_parser_context(http_request): ...
    def get_renderer_context(): ...
    def get_exception_handler_context(): ...
    def get_view_name(): ...
    def get_view_description(): ...
    def get_exception_handler(): ...
    def perform_content_negotiation(request, force): ...
    def perform_authentication(request): ...
    def check_permissions(request): ...
    def check_object_permissions(request): ...
    def check_throttles(request): ...
    def determine_version(request, *args, **kwargs): ...
    def initalize_request(request, *args, **lwargs): ...
    def inital(request, *args, **lwargs): ...
    def finalize_response(request, response, *args, **lwargs): ...
    def handle_exception(exc): ...
    def raise_uncaught_exception(exc): ...
    def dispatch(request, *args, **kwargs): ...
    def options(request, *args, **kwargs): ...

class GenericAPIView(APIView):
    queryset
    serializer_class
    lookup_field = 'pk'
    lookup_url_kwarg
    filter_backends
    pagination_class

    # properties
    paginator

    def get_queryset(): ...
    def get_object(): ...
    def get_serializer(): ...
    def get_serializer_class(): ...
    def get_serializer_context(): ...
    def filter_queryset(queryset): ...
    def paginate_queryset(queryset): ...
    def get_paginated_response(data): ...

# Other API views
[
    CreateAPIView, List, Retrieve, Destroy, Update,
    ListCreate, RetrieveUpdate, RetrieveDestory,
    RetrieveUpdateDestroy
]

# ========================================================================
#        VIEWSETS                                                        #
# ========================================================================

class ViewSetMmixin:
    @classmethod
    def get_extra_actions(): ...

    def initialize_request(request, *args, **kwargs): ...
    def reverse_action(url_name, *args, **kwargs): ...
    def get_extra_action_url_map(): ...

class ViewSet(ViewSetMmixin, APIView): ...
class GenericViewSet(ViewSetMmixin, GenericAPIView): ...
class ReadOnlyModelViewSet(Read + list): ...
class ModelViewSet(CRUD + list): ...



# ========================================================================
#        MIXINS                                                          #
# ========================================================================

class CreateModelMixin:
    def create(request, *args, **kwargs): ...
    def perform_create(serializer):
        serializer.save()
    def get_success_headers(data): ...

class ListModelMixin:
    def list(request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
class RetrieveModelMixin:
    def retrieve(request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UpdateModelMixin:
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class DestroyModelMixin:
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

# ========================================================================
#        REQUESTS & RESPONSES                                            #
# ========================================================================

class Request:
    content_type: str
    stream: object
    query_params: dict
    data: dict
    user: User
    auth: NonUserAuthInfo
    successful_authenticator(): Authenticator
    POST: dict
    META: dict
    session: dict

    def __init__(request, parsers, authenticators, negotiator, parser_context): ...
    force_plaintext_errors(value): ...

class Response(SimpleTemplateResponse):
    rendered_content: str
    status_text: str

    def __init__(data, status, template_name, headers, exception, content_type): ...



# ========================================================================
#        STATUS CODES                                                    #
# ========================================================================

{
    'Informational' : ['100 continue', '101 switching protocols'],
       'Successful' : ['200 ok', '201 created', '202 accepted', '203 non authoritative info'
                       '204 no content', '205 reset content', '206 partial content',
                       '207 multi status', '208 already reported', '226 Im used'],
      'Redirection' : ['300 multiple choices', '301 moved permanently', '302 found',
                       '303 see other', '304 not modified', '305 use proxy',
                       '306 reserved', '307 temp reditrect', '308 perm redirect'],
     'Client Error' : ['400 bad request', '401 unauthorized', '402 payment req',
                       '403 forbidden', '404 not found', '405 method not allowed',
                       '406 not acceptable', '407 proxy auth req', '408 request timeout',
                       '409 conflict', '410 gone', '411 length req',
                       '412 precondition failed', ...],
     'Server Error' : ['500 internal error', '501 not implemented', '502 bad gateway',
                       '503 service unavailable', '504 gateway timeout',
                       '505 http version not supported', '506 variant also negotiates',
                       '507 insufficient storage', '508 loop', '509 bandwidth exceeded',
                       '510 not extended', '511 network auth req'],
}


# ========================================================================
#        SIMPLE ROUTER                                                   #
# ========================================================================


"""
URL Style            | HTTP Method             Action                  | URL Name
=====================+=======================|=========================|========================
{prefix}/            | GET                   | list                    | {basename}-list
                     | POST                  | create                  |
---------------------+-----------------------|-------------------------|------------------------
{prefix}/{url_path}/ | GET, or as specified  | `@action(detail=False)` | {basename}-{url_name}
                     | by `methods` argument | decorated method        |
---------------------+-----------------------|-------------------------|------------------------
{prefix}/{lookup}/   | GET                   | retrieve                | {basename}-detail
                     | PUT                   | update                  |
                     | PATCH                 | partial_update          |
                     | DELETE                | destroy                 |
---------------------+-----------------------|-------------------------|------------------------
{prefix}/{lookup}/.. | GET, or as            | `@action(detail=True)`  |{basename}-{url_name}
      ..{url_path}/  | specified by `methods`| decorated method        |
                     | argument              |                         |
"""

router = SimpleRouter(trailing_slash=False)

DefaultRouter = SimpleRouter[.format]



additional_packages = [
    'https://github.com/alanjds/drf-nested-routers',
    'https://wq.io/wq.db',
    'https://chibisov.github.io/drf-extensions/docs/',
    'https://github.com/AltSchool/dynamic-rest',
    'https://github.com/MattBroach/DjangoRestMultipleModels',
    'https://github.com/MattBroach/DjangoRestMultipleModels',
]