from .basic import router as basic_router
from .admin_handlers.add_employer import router as add_employer_router
from .admin_handlers.common_admin_handlers import router as common_admin_handlers_router
from .admin_handlers.rud_employers import router as rud_employers_router
from .client_handlers.client_handlers import router as client_handlers_router
from .client_handlers.registration_service import router as registration_service_router


def get_routers():
    return [
        basic_router,
        add_employer_router,
        client_handlers_router,
        common_admin_handlers_router,
        rud_employers_router,
        registration_service_router
    ]
