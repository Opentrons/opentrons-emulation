em_vm := ./opentrons-emulation vm

.PHONY: vm-create
vm-create:
	$(em_vm) && (cd vagrant && vagrant up)

.PHONY: vm-remove
vm-remove:
	$(em_vm) && (cd vagrant && vagrant destroy --force)

.PHONY: vm-ssh
vm-ssh:
	$(em_vm) && (cd vagrant && vagrant ssh default)

.PHONY: vm-setup
vm-setup:
	$(em_vm) && (cd vagrant && vagrant ssh default -c "(cd opentrons-emulation/emulation_system && make setup)")
