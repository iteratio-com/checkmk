@echo off
set CMK_VERSION="2.5.0b1"
echo ^<^<^<windows_intel_bonding^>^>^>


wmic /namespace:\\root\IntelNCS2 path IANET_TeamOfAdapters get Caption,Name,RedundancyStatus

echo ###

wmic /namespace:\\root\IntelNCS2 path IANET_TeamedMemberAdapter get AdapterFunction,AdapterStatus,GroupComponent,PartComponent

echo ###

wmic /namespace:\\root\IntelNCS2 path IANET_PhysicalEthernetAdapter get AdapterStatus,Caption,DeviceID

