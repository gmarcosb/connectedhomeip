#
#    Copyright (c) 2024 Project CHIP Authors
#    All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#

# === BEGIN CI TEST ARGUMENTS ===
# test-runner-runs:
#   run1:
#     app: ${ALL_CLUSTERS_APP}
#     app-args: --discriminator 1234 --KVS kvs1 --trace-to json:${TRACE_APP}.json
#     script-args: >
#       --storage-path admin_storage.json
#       --commissioning-method on-network
#       --discriminator 1234
#       --passcode 20202021
#       --trace-to json:${TRACE_TEST_JSON}.json
#       --trace-to perfetto:${TRACE_TEST_PERFETTO}.perfetto
#       --endpoint 1
#     factory-reset: true
#     quiet: true
# === END CI TEST ARGUMENTS ===

import logging

import chip.clusters as Clusters
from chip.clusters.Types import NullValue
from chip.interaction_model import InteractionModelError, Status
from chip.testing.matter_testing import MatterBaseTest, TestStep, async_test_body, default_matter_test_main
from mobly import asserts


class TC_VALCC_4_3(MatterBaseTest):
    async def read_valcc_attribute_expect_success(self, endpoint, attribute):
        cluster = Clusters.Objects.ValveConfigurationAndControl
        return await self.read_single_attribute_check_success(endpoint=endpoint, cluster=cluster, attribute=attribute)

    def desc_TC_VALCC_4_3(self) -> str:
        return "[TC-VALCC-4.3] AutoCloseTime functionality with (no synchronized time) DUT as Server"

    def steps_TC_VALCC_4_3(self) -> list[TestStep]:
        steps = [
            TestStep(1, "Commissioning, already done", is_commissioning=True),
            TestStep("2a", "Read FeatureMap attribute"),
            TestStep("2b", "Verify TimeSync feature is supported"),
            TestStep("3a", "Read UTCTime attribute from Time Synchronization cluster"),
            TestStep("3b", "Verify UTCTime is null"),
            TestStep(4, "Send Open command"),
            TestStep(5, "Read AutoCloseTime attribute"),
            TestStep(6, "Send Close command"),
            TestStep(7, "Read AutoCloseTime attribute"),
        ]
        return steps

    def pics_TC_VALCC_4_3(self) -> list[str]:
        pics = [
            "VALCC.S",
        ]
        return pics

    @async_test_body
    async def test_TC_VALCC_4_3(self):

        endpoint = self.get_endpoint(default=1)

        self.step(1)
        attributes = Clusters.ValveConfigurationAndControl.Attributes

        self.step("2a")
        feature_map = await self.read_valcc_attribute_expect_success(endpoint=endpoint, attribute=attributes.FeatureMap)

        is_ts_feature_supported = feature_map & Clusters.ValveConfigurationAndControl.Bitmaps.Feature.kTimeSync

        self.step("2b")
        if not is_ts_feature_supported:
            logging.info("TimeSync feature not supported skipping test case")

            # Skipping all remainig steps
            for step in self.get_test_steps(self.current_test_info.name)[self.current_step_index:]:
                self.step(step.test_plan_number)
                logging.info("Test step skipped")

            return

        else:
            logging.info("Test step skipped")

        self.step("3a")
        utcTime = await self.read_single_attribute_check_success(endpoint=0, cluster=Clusters.Objects.TimeSynchronization, attribute=Clusters.TimeSynchronization.Attributes.UTCTime)

        self.step("3b")
        if utcTime is not NullValue:
            logging.info("UTCTime is not null, skipping test case")

            # Skipping all remainig steps
            for step in self.get_test_steps(self.current_test_info.name)[self.current_step_index:]:
                self.step(step.test_plan_number)
                logging.info("Test step skipped")

            return

        else:
            logging.info("Test step skipped")

        self.step(4)
        try:
            await self.send_single_cmd(cmd=Clusters.Objects.ValveConfigurationAndControl.Commands.Open(), endpoint=endpoint)
        except InteractionModelError as e:
            asserts.assert_equal(e.status, Status.Success, "Unexpected error returned")
            pass

        self.step(5)
        auto_close_time_dut = await self.read_valcc_attribute_expect_success(endpoint=endpoint, attribute=attributes.AutoCloseTime)
        asserts.assert_true(auto_close_time_dut is NullValue, "AutoCloseTime is not null")

        self.step(6)
        try:
            await self.send_single_cmd(cmd=Clusters.Objects.ValveConfigurationAndControl.Commands.Close(), endpoint=endpoint)
        except InteractionModelError as e:
            asserts.assert_equal(e.status, Status.Success, "Unexpected error returned")
            pass

        self.step(7)
        auto_close_time_dut = await self.read_valcc_attribute_expect_success(endpoint=endpoint, attribute=attributes.AutoCloseTime)
        asserts.assert_true(auto_close_time_dut is NullValue, "AutoCloseTime is not null")


if __name__ == "__main__":
    default_matter_test_main()
