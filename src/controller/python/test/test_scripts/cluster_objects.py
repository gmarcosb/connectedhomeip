from chip.clusters import TestObjects
import logging
from chip.interaction_model import exceptions as IMExceptions

logger = logging.getLogger('PythonMatterControllerTEST')
logger.setLevel(logging.INFO)

NODE_ID = 1
LIGHTING_ENDPOINT_ID = 1


class ClusterObjectTests:
    @classmethod
    def TestAPI(cls):
        if TestObjects.OnOff.id != 6:
            raise ValueError()
        if TestObjects.OnOff.Commands.Off.command_id != 0:
            raise ValueError()
        if TestObjects.OnOff.Commands.Off.cluster_id != 6:
            raise ValueError()
        if TestObjects.OnOff.Commands.On.command_id != 1:
            raise ValueError()
        if TestObjects.OnOff.Commands.On.cluster_id != 6:
            raise ValueError()

    @classmethod
    async def RoundTripTest(cls):
        req = TestObjects.OnOff.Commands.On()
        res = await req.send(nodeId=NODE_ID, endpointId=LIGHTING_ENDPOINT_ID)
        if res is not None:
            logger.error(
                f"Got {res} Response from server, but None is expected.")
            raise ValueError()

    @classmethod
    async def RoundTripTestWithBadEndpoint(cls):
        req = TestObjects.OnOff.Commands.On()
        try:
            await req.send(nodeId=NODE_ID, endpointId=233)
            raise ValueError(f"Failure expected")
        except IMExceptions.InteractionModelError as ex:
            logger.info(f"Recevied {ex} from server.")
            return

    @classmethod
    async def RunTest(cls):
        try:
            cls.TestAPI()
            await cls.RoundTripTest()
            await cls.RoundTripTestWithBadEndpoint()
        except Exception as ex:
            logger.error(
                f"Unexpected error occurred when running tests: {ex}")
            logger.exception(ex)
            return False
        return True
