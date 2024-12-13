param allowed_special: Literal['all'] | Set[str] | None = None#
param check_embedding_ctx_length: bool = True#
Whether to check the token length of inputs and automatically split inputs longer than embedding_ctx_length.

param chunk_size: int = 1000#
Maximum number of texts to embed in each batch

param default_headers: Mapping[str, str] | None = None#
param default_query: Mapping[str, object] | None = None#
param deployment: str | None = 'text-embedding-ada-002'#
param dimensions: int | None = None#
The number of dimensions the resulting output embeddings should have.

Only supported in text-embedding-3 and later models.

param disallowed_special: Literal['all'] | Set[str] | Sequence[str] | None = None#
param embedding_ctx_length: int = 8191#
The maximum number of tokens to embed at once.

param headers: Any = None#
param http_async_client: Any | None = None#
Optional httpx.AsyncClient. Only used for async invocations. Must specify http_client as well if you’d like a custom client for sync invocations.

param http_client: Any | None = None#
Optional httpx.Client. Only used for sync invocations. Must specify http_async_client as well if you’d like a custom client for async invocations.

param max_retries: int = 2#
Maximum number of retries to make when generating.

param model: str = 'text-embedding-ada-002'#
param model_kwargs: Dict[str, Any] [Optional]#
Holds any model parameters valid for create call not explicitly specified.

param openai_api_base: str | None [Optional] (alias 'base_url')#
Base URL path for API requests, leave blank if not using a proxy or service emulator.

param openai_api_key: SecretStr | None [Optional] (alias 'api_key')#
Automatically inferred from env var OPENAI_API_KEY if not provided.

param openai_api_type: str | None [Optional]#
param openai_api_version: str | None [Optional] (alias 'api_version')#
Automatically inferred from env var OPENAI_API_VERSION if not provided.

param openai_organization: str | None [Optional] (alias 'organization')#
Automatically inferred from env var OPENAI_ORG_ID if not provided.

param openai_proxy: str | None [Optional]#
param request_timeout: float | Tuple[float, float] | Any | None = None (alias 'timeout')#
Timeout for requests to OpenAI completion API. Can be float, httpx.Timeout or None.

param retry_max_seconds: int = 20#
Max number of seconds to wait between retries

param retry_min_seconds: int = 4#
Min number of seconds to wait between retries

param show_progress_bar: bool = False#
Whether to show a progress bar when embedding.

param skip_empty: bool = False#
Whether to skip empty strings when embedding or raise an error. Defaults to not skipping.

param tiktoken_enabled: bool = True#
Set this to False for non-OpenAI implementations of the embeddings API, e.g. the –extensions openai extension for text-generation-webui

param tiktoken_model_name: str | None = None#
The model name to pass to tiktoken when using this class. Tiktoken is used to count the number of tokens in documents to constrain them to be under a certain limit. By default, when set to None, this will be the same as the embedding model name. However, there are some cases where you may want to use this Embedding class with a model name not supported by tiktoken. This can include when using Azure embeddings or when using one of the many model providers that expose an OpenAI-like API but with different models. In those cases, in order to avoid erroring when tiktoken is called, you can specify a model name to use here.

