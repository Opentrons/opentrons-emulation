SUB = {SUB}
VAGRANT_CMD := ./opentrons-emulation vm && (cd vagrant && vagrant{SUB})

.PHONY: vm-create
vm-create:
	$(eval CMD := up)
	$(subst $(SUB), $(CMD), $(VAGRANT_CMD))

.PHONY: vm-remove
vm-remove:
	$(eval CMD := destroy --force)
	$(subst $(SUB), $(CMD), $(VAGRANT_CMD))

.PHONY: vm-ssh
vm-ssh:
	$(eval CMD := ssh default)
	$(subst $(SUB), $(CMD), $(VAGRANT_CMD))

.PHONY: vm-setup
vm-setup:
	$(eval CMD := ssh default -c '(cd opentrons-emulation/emulation_system && make setup)')
	$(subst $(SUB), $(CMD), $(VAGRANT_CMD))

