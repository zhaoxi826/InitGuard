import tomllib
def main():
    with open('pyproject.toml', 'r') as file:
        config = tomllib.load(file)
    print("kubeguard数据备份系统，版本号{{}}。".format(config["project"]["version"]))
    print("正在初始化中......请稍后")
    print("初始化完成，已经读取")
