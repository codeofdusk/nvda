# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2020 NV Access Limited, Bill Dengler
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import sys
import os
import winUser

from typing import Union

winVersion=sys.getwindowsversion()
winVersionText="{v.major}.{v.minor}.{v.build}".format(v=winVersion)
if winVersion.service_pack_major!=0:
	winVersionText+=" service pack %d"%winVersion.service_pack_major
	if winVersion.service_pack_minor!=0:
		winVersionText+=".%d"%winVersion.service_pack_minor
winVersionText+=" %s" % ("workstation","domain controller","server")[winVersion.product_type-1]

def isSupportedOS():
	# NVDA can only run on Windows 7 Service pack 1 and above
	return (winVersion.major,winVersion.minor,winVersion.service_pack_major) >= (6,1,1)

def canRunVc2010Builds():
	return isSupportedOS()

UWP_OCR_DATA_PATH = os.path.expandvars(r"$windir\OCR")
def isUwpOcrAvailable():
	return os.path.isdir(UWP_OCR_DATA_PATH)


WIN10_VERSIONS_TO_BUILDS = {
	"15H1": 10240,
	"15H2": 10586,
	"16H2": 14393,
	"17H1": 15063,
	"17H2": 16299,
	"18H1": 17134,
	"18H2": 17763,
	"19H1": 18362,
	"19H2": 18363,
	"20H1": 19041,
	"20H2": 19042,
}


def isWin10(version: Union[int, str] = "15H1", atLeast: bool = True):
	"""
	Returns True if NVDA is running on the supplied release version of Windows 10. If no argument is supplied, returns True for all public Windows 10 releases.
	@param version: a release version of Windows 10 (such as 1903 or 19H1).
	@param atLeast: return True if NVDA is running on at least this Windows 10 build (i.e. this version or higher).
	"""
	if winVersion.major != 10:
		return False
	if isinstance(version, str):
		ver = version
	elif isinstance(version, int):
		year = version // 100
		month = version % 100
		half = 1 if month < 7 else 2
		ver = f"{year}H{half}"
	try:
		if atLeast:
			return winVersion.build >= WIN10_VERSIONS_TO_BUILDS[ver]
		else:
			return winVersion.build == WIN10_VERSIONS_TO_BUILDS[ver]
	except KeyError:
		from logHandler import log
		log.error(f"Unknown Windows 10 version {version}")
		return False


def isFullScreenMagnificationAvailable():
	return (winVersion.major, winVersion.minor) >= (6, 2)
