from .publicacion_tests import (
    CreateReadPublicacionTestCase,
    UpdateDeletePublicacionTestCase,
    ReadPublicacionByArrendadorTestCase
)

from .solicitud_tests import (
    CreateSolicitudTestCase,
    ReadUpdateDeleteSolicitudTestCase,
    ListSolicitudByEstudianteTestCase,
    ListSolicitudByArrendadorTestCase
)

from .resena_tests import (
    CreateReadResenaTestCase,
    NotificationSignalTestCase
)

_ = [
    CreateReadPublicacionTestCase,
    UpdateDeletePublicacionTestCase,
    ReadPublicacionByArrendadorTestCase
]

_ = [
    CreateSolicitudTestCase,
    ReadUpdateDeleteSolicitudTestCase,
    ListSolicitudByEstudianteTestCase,
    ListSolicitudByArrendadorTestCase
]

_ = [
    CreateReadResenaTestCase,
    NotificationSignalTestCase
]