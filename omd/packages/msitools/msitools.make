MSITOOLS := msitools

MSITOOLS_BUILD := $(BUILD_HELPER_DIR)/$(MSITOOLS)-build
MSITOOLS_INSTALL := $(BUILD_HELPER_DIR)/$(MSITOOLS)-install

MSITOOLS_BUILD_DIR := $(BAZEL_BIN_EXT)/$(MSITOOLS)/$(MSITOOLS)

.PHONY: $(MSITOOLS_BUILD)
$(MSITOOLS_BUILD):
ifneq ($(filter $(DISTRO_CODE),sles15 sles15sp3 sles15sp4 sles15sp5 sles15sp6),)
	BAZEL_EXTRA_ARGS="--define omd-libgsf=true" $(BAZEL_BUILD) @$(MSITOOLS)//:$(MSITOOLS)
else
	$(BAZEL_BUILD) @$(MSITOOLS)//:$(MSITOOLS)
endif

.PHONY: $(MSITOOLS_INSTALL)
$(MSITOOLS_INSTALL): $(MSITOOLS_BUILD)
	$(RSYNC) --chmod=u+w $(MSITOOLS_BUILD_DIR)/ $(DESTDIR)$(OMD_ROOT)/
