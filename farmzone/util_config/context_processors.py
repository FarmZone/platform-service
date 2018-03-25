from farmzone.util_config import current_environment
import logging
logger = logging.getLogger(__name__)


def from_settings(request):

    def get_env_message():
        env = current_environment()
        #logger.debug("Env {0}".format(env))
        if env in ["local", "dev"]:
            return {"color": "#D7DBDD",
                    "message": "This is Development environment, you can safely play around here."}
        elif env in ["stage"]:
            return {"color": "#F39C12", "message": "Go slow, this is Stage environment"}
        return {"color": "#C0392B", "message": "Caution!!! this is Prod Environment"}

    res = get_env_message()
    return {
        'ENVIRONMENT_NAME': res["message"],
        'ENVIRONMENT_COLOR': res["color"],
    }
