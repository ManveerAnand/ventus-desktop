class Settings:
    def __init__(self):
        self.concurrent_connections = 2  
        self.max_file_size_mb = 500    
        self.bandwidth_limit = 0         
        self.sync_schedule = "daily"   


    def save_settings(self):
        return None