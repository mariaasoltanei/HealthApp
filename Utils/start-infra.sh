#!/bin/bash

# List all VMs
vms=$(VBoxManage list vms | awk -F\" '{print $2}')

# Start each VM
for vm in $vms; do
  echo "Starting VM: $vm"
  VBoxManage startvm "$vm" --type headless
  echo "VM $vm started"
done