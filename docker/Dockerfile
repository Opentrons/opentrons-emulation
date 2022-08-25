#############################################################
#                       LOCAL TARGETS                       #
#############################################################

# Targets for all development builds of emulators
# All source code should be bind-mounted in, so do not copy it in.
# entrypoint.sh should also be bind-mounted in so do not copy it in either
# Make sure to include the OPENTRONS_HARDWARE env variable

FROM ghcr.io/opentrons/cpp-base:latest as cpp-base-with-rebuild-script
COPY rebuild.sh /rebuild.sh
ENTRYPOINT ["/rebuild.sh"]

FROM ghcr.io/opentrons/python-base:latest as python-base-with-rebuild-script
COPY rebuild.sh /rebuild.sh
ENTRYPOINT ["/rebuild.sh"]

############################
# Hardware Local Emulators #
############################

FROM cpp-base-with-rebuild-script as heater-shaker-hardware-local
ENV OPENTRONS_HARDWARE "heater-shaker-hardware"

FROM cpp-base-with-rebuild-script as thermocycler-hardware-local
ENV OPENTRONS_HARDWARE "thermocycler-hardware"

# Do not use common-ot3-firmware as value for OPENTRONS_HARDWARE
# What will happen is the first container to finish building will move all the executables to their new file location
# and the rest of the containers will not be able to find them

# Instead specify the individual piece of firware as the hardware. This will cause only the container to only build
# and move firmware for itself. Eliminating the issue of them clobbering each other

FROM cpp-base-with-rebuild-script as ot3-pipettes-hardware-local
ENV OPENTRONS_HARDWARE "ot3-pipettes-hardware"

FROM cpp-base-with-rebuild-script as ot3-head-hardware-local
ENV OPENTRONS_HARDWARE "ot3-head-hardware"

FROM cpp-base-with-rebuild-script as ot3-gantry-x-hardware-local
ENV OPENTRONS_HARDWARE "ot3-gantry-x-hardware"

FROM cpp-base-with-rebuild-script as ot3-gantry-y-hardware-local
ENV OPENTRONS_HARDWARE "ot3-gantry-y-hardware"

FROM cpp-base-with-rebuild-script as ot3-bootloader-hardware-local
ENV OPENTRONS_HARDWARE "ot3-bootloader-hardware"

FROM cpp-base-with-rebuild-script as ot3-gripper-hardware-local
ENV OPENTRONS_HARDWARE "ot3-gripper-hardware"

############################
# Firmware Local Emulators #
############################

FROM python-base-with-rebuild-script as thermocycler-firmware-local
ENV OPENTRONS_HARDWARE "thermocycler-firmware"

FROM python-base-with-rebuild-script as magdeck-firmware-local
ENV OPENTRONS_HARDWARE "magdeck-firmware"

FROM python-base-with-rebuild-script as tempdeck-firmware-local
ENV OPENTRONS_HARDWARE "tempdeck-firmware"

FROM python-base-with-rebuild-script as emulator-proxy-local
ENV OPENTRONS_HARDWARE "emulator-proxy"

FROM python-base-with-rebuild-script as robot-server-local
ENV OPENTRONS_HARDWARE "robot-server"

FROM python-base-with-rebuild-script as smoothie-local
ENV OPENTRONS_HARDWARE "smoothie"

FROM python-base-with-rebuild-script as can-server-local
ENV OPENTRONS_HARDWARE "can-server"





############################################### vvv PLEASE READ ME vvv #################################################
############################################### vvv PLEASE READ ME vvv #################################################
############################################### vvv PLEASE READ ME vvv #################################################

#                                                       Note:
# Configuration for local targets ends here. All following targets should either be remote targets or used to build
# remote targets. I am trying super hard to keep this file organized.

############################################### ^^^ PLEASE READ ME ^^^ #################################################
############################################### ^^^ PLEASE READ ME ^^^ #################################################
############################################### ^^^ PLEASE READ ME ^^^ #################################################





#############################################################
#                        REPO SOURCE                        #
#############################################################

# The following targets download source code, unpack it, and copy the entrypoint.sh file in.
# These should only be used for production targets.
# There should only be one repo builder target per source code repo being utlized.

# ot3-firmware-source:
#   * Based off of cpp-base
#   * Contains ot3-firmware source and entrypoint.sh

# opentrons-modules-source:
#   * Based off of cpp-base
#   * Contains modules source and entrypoint.sh

# opentrons-source:
#  * Based off of ghcr.io/opentrons/python-base:latest
#  * Contains opentrons source and entrypoint.sh

#######################
# ot3-firmware-source #
#######################

FROM ghcr.io/opentrons/cpp-base:latest as ot3-firmware-source
ARG FIRMWARE_SOURCE_DOWNLOAD_LOCATION
ADD $FIRMWARE_SOURCE_DOWNLOAD_LOCATION /ot3-firmware.zip
RUN (cd / &&  \
    unzip -q ot3-firmware.zip && \
    rm -f ot3-firmware.zip && \
    mv ot3-firmware* ot3-firmware)


##################
# modules-source #
##################

FROM ghcr.io/opentrons/cpp-base:latest as opentrons-modules-source
ARG MODULE_SOURCE_DOWNLOAD_LOCATION
ADD $MODULE_SOURCE_DOWNLOAD_LOCATION /opentrons-modules.zip
RUN (cd / &&  \
    unzip -q opentrons-modules.zip && \
    rm -f opentrons-modules.zip && \
    mv opentrons-modules* opentrons-modules)

####################
# opentrons-source #
####################

FROM ghcr.io/opentrons/python-base:latest as opentrons-source
ARG OPENTRONS_SOURCE_DOWNLOAD_LOCATION
ADD $OPENTRONS_SOURCE_DOWNLOAD_LOCATION /opentrons.zip
RUN (cd / &&  \
    unzip -q opentrons.zip && \
    rm -f opentrons.zip && \
    mv opentrons* opentrons)

#############################################################
#                    EXECUTABLE BUILDERS                    #
#############################################################

# The following targets should build executables.
# There should be a 1 to 1 mapping of Executable Builder to Production Target
# The Exectuable Builder should build the executable file and the Production Target should copy over the executable file
# from the executable builder target
# Building separately from the Production Target to reduce image size

FROM opentrons-modules-source as heater-shaker-builder
ENV OPENTRONS_HARDWARE "heater-shaker-hardware"
COPY entrypoint.sh /entrypoint.sh
RUN /entrypoint.sh build

FROM opentrons-modules-source as thermocycler-builder
ENV OPENTRONS_HARDWARE "thermocycler-hardware"
COPY entrypoint.sh /entrypoint.sh
RUN /entrypoint.sh build

FROM opentrons-source as python-emulator-builder
ENV OPENTRONS_HARDWARE "common-firmware"
COPY entrypoint.sh /entrypoint.sh
RUN /entrypoint.sh build

FROM ot3-firmware-source as ot3-firmware-builder
ENV OPENTRONS_HARDWARE "common-ot3-firmware"
COPY entrypoint.sh /entrypoint.sh
RUN /entrypoint.sh build

##################
# Firmware Common #
##################

# Added this firmware-common image because all firmware level emulator images are based off of
# the opentrons monorepo, it's just a different command that is ran for each.

FROM ghcr.io/opentrons/python-base:latest as firmware-common
RUN mkdir /dist
COPY --from=python-emulator-builder /dist/* /dist/
RUN pip install /dist/*

##############################################################
#                       REMOTE TARGETS                       #
##############################################################

# Targets for all remote builds of emulators
# Make sure to include the OPENTRONS_HARDWARE env variable
# Each Remote Target should copy in entrypoint.sh

#############################
# Hardware Remote Emulators #
#############################

# These emulators run C++ firmware code and emulate the hardware
# Each Hardware Production Target should copy the executable from the Executable Builder target
# Each Hardware Production Target should have a corresponding Executable Builder target

FROM ghcr.io/opentrons/ubuntu-base:latest as ot3-pipettes-hardware-remote
ENV OPENTRONS_HARDWARE "ot3-pipettes-hardware"
COPY --from=ot3-firmware-builder /pipettes-simulator /pipettes-simulator
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM ghcr.io/opentrons/ubuntu-base:latest as ot3-head-hardware-remote
ENV OPENTRONS_HARDWARE "ot3-head-hardware"
COPY --from=ot3-firmware-builder /head-simulator /head-simulator
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM ghcr.io/opentrons/ubuntu-base:latest as ot3-gantry-x-hardware-remote
ENV OPENTRONS_HARDWARE "ot3-gantry-x-hardware"
COPY --from=ot3-firmware-builder /gantry-x-simulator /gantry-x-simulator
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM ghcr.io/opentrons/ubuntu-base:latest as ot3-gantry-y-hardware-remote
ENV OPENTRONS_HARDWARE "ot3-gantry-y-hardware"
COPY --from=ot3-firmware-builder /gantry-y-simulator /gantry-y-simulator
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM ghcr.io/opentrons/ubuntu-base:latest as ot3-bootloader-hardware-remote
ENV OPENTRONS_HARDWARE "ot3-bootloader-hardware"
COPY --from=ot3-firmware-builder /bootloader-simulator /bootloader-simulator
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM ghcr.io/opentrons/ubuntu-base:latest as ot3-gripper-hardware-remote
ENV OPENTRONS_HARDWARE "ot3-gripper-hardware"
COPY --from=ot3-firmware-builder /gripper-simulator /gripper-simulator
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM ghcr.io/opentrons/ubuntu-base:latest as heater-shaker-hardware-remote
ENV OPENTRONS_HARDWARE "heater-shaker-hardware"
COPY --from=heater-shaker-builder /heater-shaker-simulator /heater-shaker-simulator
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM ghcr.io/opentrons/ubuntu-base:latest as thermocycler-hardware-remote
ENV OPENTRONS_HARDWARE "thermocycler-hardware"
COPY --from=thermocycler-builder /thermocycler-gen2-simulator /thermocycler-gen2-simulator
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

#################################
# Firmware Production Emulators #
#################################

# There emulators run python driver code and emulator the firmware
# All Firmware level emulators should be based off of firmware-common

FROM firmware-common as thermocycler-firmware-remote
ENV OPENTRONS_HARDWARE "thermocycler-firmware"
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM firmware-common as magdeck-firmware-remote
ENV OPENTRONS_HARDWARE "magdeck-firmware"
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM firmware-common as tempdeck-firmware-remote
ENV OPENTRONS_HARDWARE "tempdeck-firmware"
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM firmware-common as emulator-proxy-remote
ENV OPENTRONS_HARDWARE "emulator-proxy"
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM firmware-common as robot-server-remote
ENV OPENTRONS_HARDWARE "robot-server"
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM firmware-common as smoothie-remote
ENV OPENTRONS_HARDWARE "smoothie"
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM firmware-common as can-server-remote
ENV OPENTRONS_HARDWARE "can-server"
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]
