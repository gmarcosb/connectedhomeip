import chip.clusters as Clusters
import logging
from chip.interaction_model import exceptions as IMExceptions

logger = logging.getLogger('PythonMatterControllerTEST')
logger.setLevel(logging.INFO)

NODE_ID = 1
LIGHTING_ENDPOINT_ID = 1


class ClusterObjectTests:
    @classmethod
    def TestAPI(cls):
        if Clusters.OnOff.id != 6:
            raise ValueError()
        if Clusters.OnOff.Commands.Off.command_id != 0:
            raise ValueError()
        if Clusters.OnOff.Commands.Off.cluster_id != 6:
            raise ValueError()
        if Clusters.OnOff.Commands.On.command_id != 1:
            raise ValueError()
        if Clusters.OnOff.Commands.On.cluster_id != 6:
            raise ValueError()

    @classmethod
    async def RoundTripTest(cls):
        req = Clusters.OnOff.Commands.On()
        res = await req.send(nodeId=NODE_ID, endpointId=LIGHTING_ENDPOINT_ID)
        if res is not None:
            logger.error(
                f"Got {res} Response from server, but None is expected.")
            raise ValueError()

    @classmethod
    async def RoundTripTestWithBadEndpoint(cls):
        req = Clusters.OnOff.Commands.On()
        try:
            await req.send(nodeId=NODE_ID, endpointId=233)
            raise ValueError(f"Failure expected")
        except IMExceptions.InteractionModelError as ex:
            logger.info(f"Recevied {ex} from server.")
            return

    @classmethod
    async def SendCommandWithResponse(cls):
        req = Clusters.TestCluster.Commands.TestAddArguments(Arg1=2, Arg2=3)
        res = await req.send(nodeId=NODE_ID, endpointId=LIGHTING_ENDPOINT_ID, responseType=Clusters.TestCluster.Commands.TestAddArgumentsResponse)
        if not isinstance(res, Clusters.TestCluster.Commands.TestAddArgumentsResponse):
            logger.error(f"Unexpected response of type {type(res)} received.")
            raise ValueError()
        logger.info(f"Received response: {res}")
        if res.ReturnValue != 5:
            raise ValueError()

    @classmethod
    async def RunTest(cls):
        try:
            cls.TestAPI()
            await cls.RoundTripTest()
            await cls.RoundTripTestWithBadEndpoint()
            await cls.SendCommandWithResponse()
        except Exception as ex:
            logger.error(
                f"Unexpected error occurred when running tests: {ex}")
            logger.exception(ex)
            return False
        return True
