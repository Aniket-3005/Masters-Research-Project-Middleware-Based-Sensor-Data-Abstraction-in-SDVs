// Copyright 2016 Proyectos y Sistemas de Mantenimiento SL (eProsima).
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/*!
 * @file RawImageMsgTypeObjectSupport.hpp
 * Header file containing the API required to register the TypeObject representation of the described types in the IDL file
 *
 * This file was generated by the tool fastddsgen (version: 4.1.0).
 */

#ifndef FAST_DDS_GENERATED__SENSOR_RAWIMAGEMSG_TYPE_OBJECT_SUPPORT_HPP
#define FAST_DDS_GENERATED__SENSOR_RAWIMAGEMSG_TYPE_OBJECT_SUPPORT_HPP

#include <fastdds/dds/xtypes/type_representation/TypeObject.hpp>


#if defined(_WIN32)
#if defined(EPROSIMA_USER_DLL_EXPORT)
#define eProsima_user_DllExport __declspec( dllexport )
#else
#define eProsima_user_DllExport
#endif  // EPROSIMA_USER_DLL_EXPORT
#else
#define eProsima_user_DllExport
#endif  // _WIN32

#ifndef DOXYGEN_SHOULD_SKIP_THIS_PUBLIC

namespace sensor {
/**
 * @brief Register RawImageMsg related TypeIdentifier.
 *        Fully-descriptive TypeIdentifiers are directly registered.
 *        Hash TypeIdentifiers require to fill the TypeObject information and hash it, consequently, the TypeObject is
 *        indirectly registered as well.
 *
 * @param[out] TypeIdentifier of the registered type.
 *             The returned TypeIdentifier corresponds to the complete TypeIdentifier in case of hashed TypeIdentifiers.
 *             Invalid TypeIdentifier is returned in case of error.
 */
eProsima_user_DllExport void register_RawImageMsg_type_identifier(
        eprosima::fastdds::dds::xtypes::TypeIdentifierPair& type_ids);

} // namespace sensor


#endif // DOXYGEN_SHOULD_SKIP_THIS_PUBLIC

#endif // FAST_DDS_GENERATED__SENSOR_RAWIMAGEMSG_TYPE_OBJECT_SUPPORT_HPP
