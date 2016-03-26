from conf.settings import DEFAULT_SORT, DEFAULT_ORDER, DEFAULT_LIMIT

def getBSTableParams(
        request,
        default_limit=DEFAULT_LIMIT,
        default_sort=DEFAULT_SORT,
        default_order=DEFAULT_ORDER):
    limit = int(request.GET.get("limit", default_limit))
    offset = int(request.GET.get("offset", 0))
    search = request.GET.get("search")
    sort   = request.GET.get("sort", default_sort)
    order  = request.GET.get("order", default_order)

    return (limit,offset,search,sort,order)

def prepare_list(
        request,
        queryset,
        sort_dict={},
        default_sort=DEFAULT_SORT,
        default_order=DEFAULT_ORDER,
        default_limit=DEFAULT_LIMIT,
        search_filter=lambda search: Q(),
        ):

    limit,offset,search,sort,order = getBSTableParams(
        request,
        default_limit=DEFAULT_LIMIT,
        default_offset=DEFAULT_OFFSET,
        default_sort=DEFAULT_SORT,
        default_order=DEFAULT_ORDER,
    )

    if search:
        for filter_ in search_filters:
            queryset |= queryset.filter(filter_).distinct()
        queryset = queryset.filter(
            search_filter(search)).distinct()

    n = queryset.count()

    sort = posiblesSort.get(sort, default_sort)
    if sort:
        if order == 'desc':
            sort = '-' + sort
        queryset = queryset.order_by(sort)

    start = min(n_queryset, offset)
    end = min(n_queryset, offset+limit)

    return queryset[start:end], n
