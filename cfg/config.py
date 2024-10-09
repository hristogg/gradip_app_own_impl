import yaml
cname  = "config.yml" # This should be in main directory

def load_config(config_path:str = cname):
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f'error {e}')
            #logger.error(f"Failed to load the configuration file. Error: {e}")