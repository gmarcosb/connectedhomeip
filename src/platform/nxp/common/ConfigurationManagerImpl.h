/*
 *
 *    Copyright (c) 2020 Project CHIP Authors
 *    Copyright (c) 2020 Nest Labs, Inc.
 *    All rights reserved.
 *
 *    Licensed under the Apache License, Version 2.0 (the "License");
 *    you may not use this file except in compliance with the License.
 *    You may obtain a copy of the License at
 *
 *        http://www.apache.org/licenses/LICENSE-2.0
 *
 *    Unless required by applicable law or agreed to in writing, software
 *    distributed under the License is distributed on an "AS IS" BASIS,
 *    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *    See the License for the specific language governing permissions and
 *    limitations under the License.
 */

/**
 *    @file
 *          Provides an implementation of the ConfigurationManager object
 *          for NXP platforms using the NXP SDK.
 */

#pragma once

#include "NXPConfig.h"
#include <platform/internal/GenericConfigurationManagerImpl.h>

namespace chip {
namespace DeviceLayer {

/**
 * Concrete implementation of the ConfigurationManager singleton object for the NXP platform.
 */
class ConfigurationManagerImpl final : public Internal::GenericConfigurationManagerImpl<Internal::NXPConfig>
{
public:
    // This returns an instance of this class.
    static ConfigurationManagerImpl & GetDefaultInstance();
    CHIP_ERROR StoreSoftwareUpdateCompleted();

private:
    // ===== Members that implement the ConfigurationManager public interface.

    CHIP_ERROR Init(void) override;
    CHIP_ERROR GetPrimaryWiFiMACAddress(uint8_t * buf) override;
#if CONFIG_CHIP_ETHERNET
    CHIP_ERROR GetPrimaryMACAddress(MutableByteSpan & buf) override;
#endif
    bool CanFactoryReset(void) override;
    void InitiateFactoryReset(void) override;
    CHIP_ERROR ReadPersistedStorageValue(::chip::Platform::PersistedStorage::Key key, uint32_t & value) override;
    CHIP_ERROR WritePersistedStorageValue(::chip::Platform::PersistedStorage::Key key, uint32_t value) override;
    CHIP_ERROR GetUniqueId(char * buf, size_t bufSize) override;
    CHIP_ERROR StoreUniqueId(const char * uniqueId, size_t uniqueIdLen) override;
    CHIP_ERROR GenerateUniqueId(char * buf, size_t bufSize) override;
    CHIP_ERROR GetRebootCount(uint32_t & rebootCount) override;
    CHIP_ERROR StoreRebootCount(uint32_t rebootCount) override;
    CHIP_ERROR GetBootReason(uint32_t & bootReason) override;
    CHIP_ERROR StoreBootReason(uint32_t bootReason) override;
    CHIP_ERROR GetTotalOperationalHours(uint32_t & totalOperationalHours) override;
    CHIP_ERROR StoreTotalOperationalHours(uint32_t totalOperationalHours) override;

    // NOTE: Other public interface methods are implemented by GenericConfigurationManagerImpl<>.

    // ===== Members that implement the GenericConfigurationManagerImpl protected interface.
    CHIP_ERROR ReadConfigValue(Key key, bool & val) override;
    CHIP_ERROR ReadConfigValue(Key key, uint32_t & val) override;
    CHIP_ERROR ReadConfigValue(Key key, uint64_t & val) override;
    CHIP_ERROR ReadConfigValueStr(Key key, char * buf, size_t bufSize, size_t & outLen) override;
    CHIP_ERROR ReadConfigValueBin(Key key, uint8_t * buf, size_t bufSize, size_t & outLen) override;
    CHIP_ERROR WriteConfigValue(Key key, bool val) override;
    CHIP_ERROR WriteConfigValue(Key key, uint32_t val) override;
    CHIP_ERROR WriteConfigValue(Key key, uint64_t val) override;
    CHIP_ERROR WriteConfigValueStr(Key key, const char * str) override;
    CHIP_ERROR WriteConfigValueStr(Key key, const char * str, size_t strLen) override;
    CHIP_ERROR WriteConfigValueBin(Key key, const uint8_t * data, size_t dataLen) override;
    void RunConfigUnitTest(void) override;

    // ===== Private members reserved for use by this class only.

    static void DoFactoryReset(intptr_t arg);

    CHIP_ERROR DetermineBootReason(uint8_t rebootCause);
};

/**
 * Returns the platform-specific implementation of the ConfigurationManager object.
 *
 * Applications can use this to gain access to features of the ConfigurationManager
 * that are specific to the selected platform.
 */
ConfigurationManager & ConfigurationMgrImpl();

} // namespace DeviceLayer
} // namespace chip
