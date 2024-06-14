import sciqlop.collab.crdt.manager as cdrt_man
import sciqlop.collab.model.speasy_model as sp_model
import sciqlop.collab.server.speasy_ws_api as sp_api


def list_catalogues(req: sp_api.ListCataloguesRequest) -> sp_api.ListCataloguesResponse:
    return sp_api.ListCataloguesResponse(
        catalogues=[
            sp_model.Catalogue(uuid=cinfo["uuid"], name=cinfo["name"])
            for cinfo in cdrt_man.list_catalogues()
        ]
    )


def create_catalogue(
    req: sp_api.CreateCatalogueRequest,
) -> sp_api.CreateCatalogueResponse:
    print("!create_catalogue!")
    assert isinstance(req, sp_api.CreateCatalogueRequest)
    return sp_api.CreateCatalogueResponse(
        catalogue_uuid=cdrt_man.create_catalogue(req.name).uuid
    )


def list_events(req: sp_api.ListEventsRequest) -> sp_api.CreateEventResponse:
    return sp_api.ListEventsResponse(events=cdrt_man.list_events(req.catalogue_uuid))


def create_event(req: sp_api.CreateEventRequest) -> sp_api.CreateEventResponse:
    event = cdrt_man.create_event(req.catalogue_uuid, req.event)
    return sp_api.CreateEventResponse(event_uuid=event.uuid)


def edit_event(req: sp_api.EditEventRequest) -> sp_api.EditEventResponse:
    cdrt_man.edit_event(req.catalogue_uuid, req.event_uuid, req.dic)
    return sp_api.EditEventResponse()


def resolve_actions():
    def req_to_fn(req):
        r = req.__name__[:-7]
        n = r[0].lower()
        for i in range(1, len(r)):
            if r[i].isupper():
                n += "_"
            n += r[i].lower()
        assert n in globals()
        return globals()[n]

    fns = {}
    for name, req in sp_api.available_requests.items():
        fns[req] = req_to_fn(req)
    return fns


available_actions = resolve_actions()
