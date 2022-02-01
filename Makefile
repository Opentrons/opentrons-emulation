.PHONY: vm-create
vm-create:
	./opentrons-emulation vm && (cd vagrant && vagrant up)

.PHONY: vm-remove
vm-remove:
	./opentrons-emulation vm && (cd vagrant && vagrant destroy --force)

.PHONY: vm-ssh
vm-ssh:
	./opentrons-emulation vm && (cd vagrant && vagrant ssh default)
