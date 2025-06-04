import subprocess
import os

def run(cmd, shell=True, check=True):
    print(f"\n[+] Executando: {cmd}")
    subprocess.run(cmd, shell=shell, check=check)

def configure_timezone():
    run("timedatectl set-timezone America/Sao_Paulo")
    run("date")

def install_mysql():
    run("apt update && apt install -y mysql-server")
    run("systemctl enable mysql --now")
    run("systemctl status mysql")

def secure_mysql_and_create_db():
    print("\n[+] Configurando senha do MySQL e criando banco e usuário do Zabbix...")
    mysql_commands = """
    ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'senha_mysql_desejada';
    FLUSH PRIVILEGES;
    CREATE DATABASE zabbix CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
    CREATE USER 'zabbix'@'localhost' IDENTIFIED BY 'senha_zabbix_desejada';
    GRANT ALL PRIVILEGES ON zabbix.* TO 'zabbix'@'localhost';
    SET GLOBAL log_bin_trust_function_creators = 1;
    """
    run(f"mysql -uroot -psenha_mysql -e \"{mysql_commands}\"") 

def install_zabbix_repo_and_import_db():
    run("wget https://repo.zabbix.com/zabbix/7.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_7.0-2%2Bubuntu24.04_all.deb")
    run("dpkg -i zabbix-release_7.0-2+ubuntu24.04_all.deb")
    run("apt update")
    run("apt install -y zabbix-server-mysql zabbix-frontend-php zabbix-apache-conf zabbix-sql-scripts zabbix-agent")

    print("\n[+] Importando esquema do banco de dados...")
    run("zcat /usr/share/zabbix-sql-scripts/mysql/server.sql.gz | mysql -uzabbix -psenha_zabbix zabbix")

    print("\n[+] Desabilitando log_bin_trust_function_creators...")
    run("mysql -uroot -psenha_mysql -e \"SET GLOBAL log_bin_trust_function_creators = 0;\"")

def configure_zabbix_server():
    config_path = "/etc/zabbix/zabbix_server.conf"
    print(f"\n[+] Configurando senha do banco no {config_path}")
    run(f"sed -i 's/^# DBPassword=.*/DBPassword=senha_mysql/' {config_path}")

def enable_and_start_services():
    print("\n[+] Habilitando e iniciando serviços do Zabbix e Apache")
    run("systemctl enable zabbix-server apache2 php8.3-fpm zabbix-agent --now")
    run("systemctl restart apache2 php8.3-fpm")

def fix_locales():
    print("\n[+] Corrigindo problemas de locale")
    run("apt install -y locales")
    run("locale-gen pt_BR.UTF-8 en_US.UTF-8")
    run("update-locale")
    run("systemctl restart apache2")

def main():
    configure_timezone()
    install_mysql()
    secure_mysql_and_create_db()
    install_zabbix_repo_and_import_db()
    configure_zabbix_server()
    enable_and_start_services()
    fix_locales()
    print("\n✅ Zabbix Server 7 instalado com sucesso! Acesse via browser para concluir a configuração.")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Por favor, execute este script como root.")
        exit(1)
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao executar: {e.cmd}\nSaída: {e}")
