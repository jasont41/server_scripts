import yaml

class profile: 
    current_user = None 
    config = {}
    def __init__(self, curr_user): 
        self.current_user = curr_user
        print("The current user is " + self.current_user)
        self.check_for_config()

    def check_for_config(self): 
        file_found = True
        yaml_loc = "../" + self.current_user + "profile.yaml"
        try:
            config = open(yaml_loc,'r')
            _config = yaml.safe_load(config)
        except: 
            file_found = False 
            print("File not found, creating one")
        if file_found != False:
            with open(fname, "w") as f:
                yaml_str = yaml.safe_dump({'user':'user'})
                f.write(yaml_str)
        return 



fname = 'test.yaml'
with open(fname, "w") as f:
    yaml_str = yaml.safe_dump({'user':'user'})
    f.write(yaml_str)