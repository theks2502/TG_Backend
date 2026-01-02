from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # database_hostname:str
    # database_port:str
    # database_password:str
    # database_name:str
    # database_username:str
    database_url: str
    secret_key:str
    algorithm: str
    access_token_expire_minutes : int 


    mail_username: str
    mail_password :str
    mail_from : str 
    mail_port : str 
    mail_server : str 
    mail_starttls : bool 
    mail_ssl_tls : bool 
    use_credentials : bool 
    resend_api_key:str
    supabase_bucket: str
    supabase_url: str
    supabase_key: str
    base_url:str
    

    class Config:
        env_file = ".env"

settings = Settings()
