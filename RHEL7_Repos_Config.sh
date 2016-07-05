echo "Configuring CentOS repositories"
file=/etc/yum.repos.d/centos.repo

{
echo "[centos]
name=CentOS "\$releasever" - "\$basearch"
baseurl=http://ftp.heanet.ie/pub/centos/7/os/\$basearch/
enabled=1
gpgcheck=0"
} > $file

echo "CentOS repositories configured"

echo "Configuring Fedora EPEL"
file=/etc/yum.repos.d/fedoraepel.repo

{
echo "[fedoraepel]
name=FedoraEPEL "\$releasever" - "\$basearch"
baseurl=http://dl.fedoraproject.org/pub/epel/7/x86_64/
enabled=1
gpgcheck=0"
} > $file

echo "Fedora EPEL configured"
