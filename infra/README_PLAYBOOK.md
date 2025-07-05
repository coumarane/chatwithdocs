# Ansible

## From the kubernetes-ansible/ directory, run:
```bash
ansible-playbook -i inventory.ini playbook.yml
```

If your SSH user requires a password for sudo (i.e., you don't have passwordless sudo configured), add --ask-become-pass:
```bash
ansible-playbook -i inventory.ini playbook.yml --ask-become-pass
```

## Deployement

1. Download the manifest and place it into kubernetes-ansible/roles/app_deployment/files/:
```bash
curl https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.1/deploy/static/provider/cloud/deploy.yaml -o roles/app_deployment/files/ingress-nginx-controller.yaml
```

2. To deploy the application:
```bash
ansible-playbook -i inventory.ini deploy_app_playbook.yml --tags metallb_deploy,app_deploy
```

3. To clean up the application:
```bash
ansible-playbook -i inventory.ini deploy_app_playbook.yml --tags cleanup
```
