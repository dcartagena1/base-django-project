def getBSTableParams(
        request,
        default_limit=20,
        default_offset=0,
        default_search="",
        default_sort="fecha",
        default_order="desc"):
    limit = int(request.GET.get("limit", default_limit))
    offset = int(request.GET.get("offset", default_offset))
    search = request.GET.get("search", default_search)
    sort   = request.GET.get("sort", default_sort)
    order  = request.GET.get("order", default_order)

    return (limit,offset,search,sort,order)
