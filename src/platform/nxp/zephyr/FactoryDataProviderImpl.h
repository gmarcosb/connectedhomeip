/*
 *
 *    Copyright (c) 2024 Project CHIP Authors
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
#pragma once

#include <platform/nxp/common/factory_data/legacy/FactoryDataProvider.h>

#include <zephyr/drivers/flash.h>
#include <zephyr/storage/flash_map.h>

namespace chip {
namespace DeviceLayer {

/**
 * @brief This class provides Commissionable data and Device Attestation Credentials.
 *
 * This implementation is using the SDK fwk_factory_data_provider module.
 *
 * For more information on this module, the interface description available in
 * FactoryDataProvider/fwk_factory_data_provider.h inside the SDK can be checked.
 */

class FactoryDataProviderImpl : public FactoryDataProvider
{
public:
    static FactoryDataProviderImpl sInstance;

    CHIP_ERROR Init(void);
    CHIP_ERROR SearchForId(uint8_t searchedType, uint8_t * pBuf, size_t bufLength, uint16_t & length,
                           uint32_t * contentAddr = NULL);
    CHIP_ERROR SignWithDacKey(const ByteSpan & digestToSign, MutableByteSpan & outSignBuffer);
    CHIP_ERROR SetEncryptionMode(EncryptionMode mode);

private:
    struct FactoryData
    {
        struct Header header;
        uint8_t factoryDataBuffer[FIXED_PARTITION_SIZE(factory_partition) - sizeof(struct Header)];
    };

    FactoryData mFactoryData;

    CHIP_ERROR ReadEncryptedData(uint8_t * dest, uint8_t * source);
    CHIP_ERROR LoadKeypairFromRaw(ByteSpan privateKey, ByteSpan publicKey, Crypto::P256Keypair & keypair);
};

FactoryDataProvider & FactoryDataPrvdImpl();

} // namespace DeviceLayer
} // namespace chip
