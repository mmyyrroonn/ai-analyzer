import argparse
import yaml

parser = argparse.ArgumentParser(description='Choose which Python service to start')
parser.add_argument('--config', type=str, required=True, help='Path to the configuration file')
args = parser.parse_args()

with open(args.config, 'r') as f:
    # 从配置文件中读取service_name参数
    config = yaml.safe_load(f)
    service_name = config.get('service_name', 'ai_analyzer')

# 根据配置文件中的参数启动不同的Python服务
if service_name == 'ai_analyzer':
    from ai_analyzer import main_logic
    main_logic()
elif service_name == 'tag_generator':
    from generate_ai_tag import main_logic
    main_logic()
else:
    print(f"Unknown service: {service_name}")